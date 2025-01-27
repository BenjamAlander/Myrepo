import os
import json
import sqlite3
from datetime import datetime, timezone
import requests
import schedule
import time
import logging
from flask import Flask, jsonify, request, render_template
from threading import Thread
from urllib.parse import quote, unquote
from flasgger import Swagger

ollama_server_name = os.getenv("OLLAMASERVERNAME","host.docker.internal")

# Logging-asetukset
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Flask-sovellus
app = Flask(__name__, template_folder="templates")

# Flasgger Swagger-konfiguraatio
swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": "apispec",
            "route": "/apispec.json",
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/swagger/",
}
app.config["SWAGGER"] = {"title": "Flask API", "uiversion": 3}
swagger = Swagger(app, config=swagger_config)

# Tietokannan polku
db_path = "/app/docker/config.db"

# Tietokannan yhteyden testaaminen
def test_db_connection():
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT project_id, token, last_checked FROM configurations")
        data = cursor.fetchall()
        conn.close()
        logging.info(f"Tietokannan sisältö: {data}")
    except Exception as e:
        logging.error(f"Tietokantavirhe: {e}")

# Haetaan konfiguraatiot tietokannasta
def get_tokens_from_db():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT project_id, token, last_checked FROM configurations")
    tokens = cursor.fetchall()
    conn.close()
    return tokens

# Päivittää projektit tietokantaan koodatussa muodossa
def update_existing_project_ids():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT id, project_id FROM configurations")
    rows = cursor.fetchall()

    for row_id, project_id in rows:
        decoded_project_id = unquote(project_id)
        encoded_project_id = quote(decoded_project_id, safe='')
        if encoded_project_id != project_id:
            cursor.execute("UPDATE configurations SET project_id = ? WHERE id = ?", (encoded_project_id, row_id))

    conn.commit()
    conn.close()
    logging.info("Projektipolut koodattu tietokantaan vain tarvittaessa.")



# Flask-reitit
@app.route("/health", methods=["GET"])
def health_check():
    """
    Terveystarkistus
    ---
    responses:
      200:
        description: Sovellus toimii
    """
    return "OK", 200

@app.route("/", methods=["GET"])
def home():
    """
    Kotisivu
    ---
    responses:
      200:
        description: Näyttää kotisivun
    """
    return render_template("index.html")

@app.route('/api/add-config', methods=['POST'])
def add_config():
    """
    Lisää uusi konfiguraatio.
    ---
    parameters:
      - in: body
        name: body
        required: true
        description: Projektin tiedot
        schema:
          type: object
          properties:
            repo:
              type: string
              example: example/repo
            token:
              type: string
              example: example-token
    responses:
      201:
        description: Konfiguraatio lisätty
      400:
        description: Puuttuva repo tai token
      500:
        description: Palvelimen virhe
    """
    try:
        data = request.json
        repo = data.get("repo")
        token = data.get("token")

        if not repo or not token:
            return jsonify({"success": False, "error": "Puuttuu repo tai token"}), 400

        encoded_repo = quote(repo, safe='')
        current_time = datetime.now(timezone.utc).isoformat()  # Lisäämisen aikaleima

        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO configurations (project_id, token, last_checked) VALUES (?, ?, ?)",
            (encoded_repo, token, current_time)
        )
        conn.commit()
        conn.close()

        return jsonify({"success": True, "message": f"Konfiguraatio lisätty. Seuranta alkaa aikaleimasta {current_time}."}), 201
    except Exception as e:
        logging.error(f"Virhe konfiguraation tallennuksessa: {e}")
        return jsonify({"success": False, "error": "Palvelimen virhe"}), 500
@app.route('/api/delete-config', methods=['DELETE'])
def delete_config():
    """
    Poista konfiguraatio
    ---
    parameters:
      - in: body
        name: body
        required: true
        description: Poistettavan projektin tiedot
        schema:
          type: object
          properties:
            repo:
              type: string
              example: example/repo
    responses:
      200:
        description: Projekti poistettu
      400:
        description: Puuttuva repo
      500:
        description: Palvelimen virhe
    """
    try:
        data = request.json
        repo = data.get("repo")

        if not repo:
            return jsonify({"success": False, "error": "Puuttuu repo"}), 400

        encoded_repo = quote(repo, safe='')

        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM configurations WHERE project_id = ?", (encoded_repo,))
        conn.commit()
        conn.close()

        return jsonify({"success": True, "message": "Projekti poistettu onnistuneesti"}), 200

    except Exception as e:
        logging.error(f"Virhe projektin poistamisessa: {e}")
        return jsonify({"success": False, "error": "Palvelimen virhe"}), 500


def get_project_branches(project_id, token):
    """
    Hakee annetun projektin haarat GitLabista.
    """
    decoded_project_id = unquote(project_id)
    encoded_project_id = quote(decoded_project_id, safe='')
    url = f"https://gitlab.dclabra.fi/api/v4/projects/{encoded_project_id}/repository/branches"
    headers = {"PRIVATE-TOKEN": token}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    branches = [branch['name'] for branch in response.json()]
    return branches

def get_branch_commits(project_id, token, branch_name, last_checked):
    """
    Hakee annetun haaran commitit GitLabista ja suodattaa ne aikaleiman perusteella.
    """
    url = f"https://gitlab.dclabra.fi/api/v4/projects/{project_id}/repository/commits"
    headers = {"PRIVATE-TOKEN": token}
    params = {"ref_name": branch_name}
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    commits = response.json()

    new_commits = []
    for commit in commits:
        commit_time = datetime.strptime(commit['created_at'], "%Y-%m-%dT%H:%M:%S.%f%z")
        if not last_checked or commit_time > datetime.fromisoformat(last_checked):
            new_commits.append(commit)

    return new_commits


def update_last_checked(project_id, token):
    """
    Päivittää tietokantaan 'last_checked'-aikaleiman nykyhetkeen.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    current_time = datetime.now(timezone.utc).isoformat()  # ISO 8601 UTC-aikaleima
    cursor.execute(
        "UPDATE configurations SET last_checked = ? WHERE project_id = ?",
        (current_time, project_id),
    )
    conn.commit()
    conn.close()
    logging.info(f"Aikaleima päivitetty projektille {project_id}: {current_time}")


def log_to_file(branch_data, project_id, token):
    """
    Kirjoittaa lokitiedot commit-summary-service-log.md -tiedostoon GitLabin documentation-haaraan.
    """
    log_file = "commit-summary-service-log.md"
    log_entry = f"Ajo: {datetime.now(timezone.utc).isoformat()}\n\n"
    log_entry += "Tarkistetut haarat ja committien lukumäärät:\n"

    for branch_name, commit_count in branch_data.items():
        log_entry += f"- {branch_name}: {commit_count} committia\n"
    
    log_entry += "\n---\n"

    file_url = f"https://gitlab.dclabra.fi/api/v4/projects/{project_id}/repository/files/{log_file}"
    headers = {"PRIVATE-TOKEN": token}

    # Tarkista, onko tiedosto olemassa
    try:
        response = requests.get(f"{file_url}/raw", headers=headers, params={"ref": "documentation"})
        if response.status_code == 200:
            current_content = response.text
        else:
            current_content = ""
    except Exception as e:
        logging.warning(f"Virhe tiedoston {log_file} lukemisessa: {e}")
        current_content = ""

    # Päivitetään tai luodaan tiedoston sisältö
    updated_content = log_entry + current_content
    method = "POST" if response.status_code == 404 else "PUT"
    data = {
        "branch": "documentation",
        "content": updated_content,
        "commit_message": f"Päivitetty {log_file} uusilla tiedoilla",
    }

    try:
        if method == "POST":
            response = requests.post(file_url, headers=headers, json=data)
        else:
            response = requests.put(file_url, headers=headers, json=data)

        if response.status_code not in [200, 201]:
            logging.error(f"Tiedoston {log_file} päivitys epäonnistui: {response.text}")
        else:
            logging.info(f"Lokitiedot kirjoitettu tiedostoon {log_file} repositoryyn.")
    except Exception as e:
        logging.error(f"Tiedoston {log_file} käsittelyssä tapahtui virhe: {e}")

def check_for_new_commits():
    """
    Tarkistaa uudet commitit ja päivittää tiivistelmät.
    """
    logging.info("check_for_new_commits kutsuttu.")
    tokens = get_tokens_from_db()
    if not tokens:
        logging.warning("Ei projekteja konfiguraatiossa.")
        return

    for project_id, token, last_checked in tokens:
        branch_data = {}  # Dictionary haarojen commit-määrille

        try:
            branches = get_project_branches(project_id, token)
            branches = [branch for branch in branches if branch != "documentation"]

            for branch_name in branches:
                commits = get_branch_commits(project_id, token, branch_name, last_checked)
                branch_data[branch_name] = len(commits)  # Lisätään haaran commit-määrä
                if commits:
                    for commit in commits:
                        diff_url = f"https://gitlab.dclabra.fi/api/v4/projects/{project_id}/repository/commits/{commit['id']}/diff"
                        diff_response = requests.get(diff_url, headers={"PRIVATE-TOKEN": token})
                        diff_response.raise_for_status()
                        diff_list = diff_response.json()

                        diff = "\n".join(
                            f"Tiedosto: {item.get('old_path', item.get('new_path'))}\nMuutokset:\n{item.get('diff', '')}"
                            for item in diff_list
                        )
                        summary = generate_summary(diff)
                        update_documentation_file(project_id, branch_name, token, commit, summary)

                # Päivitä 'last_checked'-aikaleima, kun commitit on käsitelty
                update_last_checked(project_id, token)

            # Kirjoitetaan lokitiedot GitLabiin
            log_to_file(branch_data, project_id, token)

        except Exception as e:
            logging.error(f"Virhe projektin {project_id} käsittelyssä: {e}")

            
def generate_summary(diff, model="gemma2:27b"):
    """
    Generoi tiivistelmän koodimuutoksista käyttämällä Gemma-mallia.
    """
    prompt = f"Summaroi seuraavat koodimuutokset suomeksi:\n{diff}"
    try:
        response = requests.post(
            f"http://{ollama_server_name}:11434/api/generate",
            json={"model": model, "prompt": prompt},
            stream=True
        )
        response.raise_for_status()

        summary = ""
        for line in response.iter_lines():
            if line:
                try:
                    json_line = json.loads(line.decode("utf-8"))
                    summary += json_line.get("response", "")
                except json.JSONDecodeError as e:
                    logging.error(f"JSON-dekoodausvirhe: {e}")
                    continue
        return summary or "Tiivistelmää ei saatu."
    except Exception as e:
        logging.error(f"Virhe tiivistelmän generoinnissa: {e}")
        return "Tiivistelmää ei voitu luoda."

def update_documentation_file(project_id, branch_name, token, commit, summary):
    """
    Päivittää dokumentaation tiedoston tai luo uuden tarvittaessa.
    """
    # Varmista, että dokumentaatiohaara on olemassa
    ensure_branch_exists(project_id, token, branch_name="documentation")

    filename = f"commits_{branch_name}.md"
    file_url = f"https://gitlab.dclabra.fi/api/v4/projects/{project_id}/repository/files/{filename}"
    headers = {"PRIVATE-TOKEN": token}

    # Tarkista, onko tiedosto olemassa
    try:
        response = requests.get(f"{file_url}/raw", headers=headers, params={"ref": "documentation"})
        if response.status_code == 200:
            current_content = response.text
        else:
            current_content = ""
    except Exception as e:
        logging.warning(f"Virhe tiedoston {filename} lukemisessa: {e}")
        current_content = ""

    # Päivitetään tai luodaan tiedoston sisältö
    new_entry = f"## Commit ID: {commit['id']}\n**Viesti**: {commit['message']}\n**Luotu**: {commit['created_at']}\n\n**Tiivistelmä**:\n{summary}\n\n---\n"
    updated_content = new_entry + current_content

    # Päätetään HTTP-metodi: POST (luonti) tai PUT (päivitys)
    method = "POST" if response.status_code == 404 else "PUT"
    data = {
        "branch": "documentation",  # Käytetään oikeaa haaraa
        "content": updated_content,
        "commit_message": f"Päivitetty {filename} uusilla tiivistelmillä",
    }

    try:
        if method == "POST":
            response = requests.post(file_url, headers=headers, json=data)
        else:
            response = requests.put(file_url, headers=headers, json=data)

        if response.status_code not in [200, 201]:
            logging.error(f"Tiedoston {filename} päivitys epäonnistui: {response.text}")
    except Exception as e:
        logging.error(f"Tiedoston {filename} käsittelyssä tapahtui virhe: {e}")


def ensure_branch_exists(project_id, token, branch_name="documentation"):
    """
    Tarkistaa, onko haara olemassa. Jos ei, luo uuden haaran käyttäen tyhjää refiä.
    """
    url = f"https://gitlab.dclabra.fi/api/v4/projects/{project_id}/repository/branches/{branch_name}"
    headers = {"PRIVATE-TOKEN": token}

    logging.debug(f"Tarkistetaan, löytyykö haara '{branch_name}'.")

    # Tarkista, onko haara olemassa
    response = requests.get(url, headers=headers)
    if response.status_code == 404:
        logging.info(f"Haaran '{branch_name}' luominen.")
        create_branch_url = f"https://gitlab.dclabra.fi/api/v4/projects/{project_id}/repository/branches"
        data = {
            "branch": branch_name,
            "ref": "main"  # Voimme käyttää "main" vain pohjana luomiselle
        }

        create_response = requests.post(create_branch_url, headers=headers, json=data)
        if create_response.status_code in [200, 201]:
            logging.info(f"Haara '{branch_name}' luotu onnistuneesti.")
        else:
            logging.error(f"Haaran '{branch_name}' luominen epäonnistui: {create_response.text}")
            raise Exception(f"Haaran '{branch_name}' luominen epäonnistui: {create_response.text}")
    elif response.status_code == 200:
        logging.info(f"Haara '{branch_name}' löytyy jo.")
    else:
        logging.error(f"Virhe tarkistaessa haaraa '{branch_name}': {response.text}")
        raise Exception(f"Virhe tarkistaessa haaraa '{branch_name}': {response.text}")

        
# Flask-reitit ja kaikki muu pysyvät muuttumattomina
if __name__ == "__main__":
    update_existing_project_ids()
    test_db_connection()
    schedule.every(2).minutes.do(check_for_new_commits)
    flask_thread = Thread(target=app.run, kwargs={"host": "0.0.0.0", "port": 5000})
    flask_thread.start()

    while True:
        schedule.run_pending()
        time.sleep(1)