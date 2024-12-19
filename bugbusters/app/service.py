import os
import json
import sqlite3
from datetime import datetime, timezone
import requests
import schedule
import time
import logging
from flask import Flask, jsonify, request

# Asetetaan logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Flask-sovellus health checkille ja tietojen lisäysrajapinnalle
app = Flask(__name__)

# Asetetaan tietokanta
db_path = "/app/docker/config.db"

# Funktio tietojen hakemiseksi tietokannasta
def get_tokens_from_db():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT project_id, token FROM configurations")
    tokens = cursor.fetchall()
    conn.close()
    return tokens

# Testaa tietokantayhteyttä ja tulostaa tietokannan sisällön
def test_db_connection():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT project_id, token FROM configurations")
    data = cursor.fetchall()
    conn.close()
    logging.info(f"Tietokannan sisältö: {data}")

# Ajetaan testifunktio varmistaaksemme tietokantayhteyden
test_db_connection()

# Tallennetaan viimeisin commitin aika aikavyöhyketietoisena
last_checked = datetime.min.replace(tzinfo=timezone.utc)

# Funktio haara commitin hakemiseksi GitLabista
def get_branch_commits(project_id, token, branch_name):
    global last_checked
    url = f"https://gitlab.dclabra.fi/api/v4/projects/{project_id}/repository/commits"
    headers = {"PRIVATE-TOKEN": token}
    params = {"ref_name": branch_name}
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    commits = response.json()
    
    new_commits = []
    for commit in commits:
        commit_time = datetime.strptime(commit['created_at'], "%Y-%m-%dT%H:%M:%S.%f%z")
        if commit_time > last_checked:
            new_commits.append(commit)
    
    if new_commits:
        last_checked = max(datetime.strptime(c['created_at'], "%Y-%m-%dT%H:%M:%S.%f%z") for c in new_commits)
    return new_commits

# Funktio diff-tiivistelmän generointiin Ollaman avulla
def generate_summary(diff, model="gemma2"):
    prompt = f"Summaroi seuraavat koodimuutokset suomeksi: {diff}"
    response = requests.post(
        "http://host.docker.internal:11434/api/generate",
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

    return summary or "Yhteenvetoa ei saatu"

# Funktio tiedoston päivittämiseen GitLabissa
def update_file_in_gitlab(content, filename, project_id, token):
    if content.strip() == "":
        logging.error(f"{project_id} :Ei sisältöä päivitettäväksi tiedostoon {filename}.")
        return
    
    logging.info(f"Päivitetään {filename} projektissa {project_id} seuraavalla sisällöllä:\n{content[:200]}...")

    url = f"https://gitlab.dclabra.fi/api/v4/projects/{project_id}/repository/files/{filename}"
    headers = {"PRIVATE-TOKEN": token}
    data = {
        "branch": "documentation",
        "content": content,
        "commit_message": f"Päivitetty {filename} uusilla tiedoilla"
    }

    response = requests.put(url, headers=headers, json=data)
    
    if response.status_code == 200:
        logging.info(f"Tiedosto {filename} päivitettiin onnistuneesti GitLabissa.")
    elif response.status_code == 400 and "A file with this name doesn't exist" in response.text:
        logging.warning(f"Tiedostoa {filename} ei löydy. Yritetään luoda uusi tiedosto POST-pyynnöllä.")
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 201:
            logging.info(f"Tiedosto {filename} luotiin onnistuneesti GitLabiin.")
        else:
            logging.error(f"Virhe tiedoston {filename} luomisessa: {response.status_code} - {response.text}")
    else:
        logging.error(f"Virhe tiedoston {filename} päivittämisessä: {response.status_code} - {response.text}")

# Funktio committien päivittämiseksi
def post_to_commits_md(commit, summary, branch_name, project_id, token):
    filename = f"commits_{branch_name}.md"
    logging.info(f"Yritetään päivittää tiedostoa: {filename} projektissa: {project_id} commitille: {commit['id']}")
    
    url = f"https://gitlab.dclabra.fi/api/v4/projects/{project_id}/repository/files/{filename}/raw"
    headers = {"PRIVATE-TOKEN": token}
    params = {"ref": "documentation"}

    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        current_content = response.text
        commits = current_content.strip().split("\n" + "-" * 40 + "\n\n")
        logging.info(f"Tiedoston {filename} nykyinen sisältö haettu onnistuneesti.")
    else:
        commits = []
        logging.warning(f"Tiedostoa {filename} ei löydy GitLabista. Luodaan uusi tiedosto.")

    new_commit = f"## Commit ID: {commit['id']}\n" \
                 f"**Message**: {commit['message']}\n" \
                 f"**Author**: {commit['author_name']} - {commit['created_at']}\n" \
                 f"**Summary**:\n{summary}\n\n" + "-" * 40 + "\n\n"
    commits.append(new_commit)

    content = "\n".join(commits)
    update_file_in_gitlab(content, filename, project_id, token)

def check_for_new_commits():
    tokens = get_tokens_from_db()
    for project_id, token in tokens:
        token = token.strip()
        branches_url = f"https://gitlab.dclabra.fi/api/v4/projects/{project_id}/repository/branches"
        headers = {"PRIVATE-TOKEN": token}
        branches_response = requests.get(branches_url, headers=headers)

        if branches_response.status_code == 200:
            branches = branches_response.json()
            branch_names = [branch['name'] for branch in branches]
            checked_branches = {}
            errors = []

            if "documentation" not in branch_names:
                create_branch_url = f"https://gitlab.dclabra.fi/api/v4/projects/{project_id}/repository/branches"
                create_data = {"branch": "documentation", "ref": "main"}
                create_response = requests.post(create_branch_url, headers=headers, json=create_data)
                
                if create_response.status_code != 201:
                    logging.error(f"Virhe dokumentaatiohaaran luomisessa projektissa {project_id}: {create_response.status_code} - {create_response.text}")
                    errors.append(f"Dokumentaatiohaaran luominen epäonnistui projektissa {project_id}")
                    continue

            for branch_name in branch_names:
                if branch_name != "documentation":
                    try:
                        commits = get_branch_commits(project_id, token, branch_name)
                        checked_branches[branch_name] = len(commits)
                        for commit in commits:
                            diff_url = f"https://gitlab.dclabra.fi/api/v4/projects/{project_id}/repository/commits/{commit['id']}/diff"
                            diff_response = requests.get(diff_url, headers=headers)
                            diff_response.raise_for_status()
                            diff_list = diff_response.json()

                            diff = ""
                            for item in diff_list:
                                diff += f"File: {item.get('old_path', item.get('new_path'))}\n"
                                diff += f"Changes:\n{item.get('diff', '')}\n"
                                diff += "-" * 40 + "\n"

                            summary = generate_summary(diff)
                            post_to_commits_md(commit, summary, branch_name, project_id, token)

                        logging.info(f"Commit-tarkistus haaralle {branch_name} projektissa {project_id} onnistui")
                    except Exception as e:
                        error_msg = f"Virhe haarassa {branch_name} projektissa {project_id}: {str(e)}"
                        logging.error(error_msg)
                        errors.append(error_msg)

            log_summary_service_activity(project_id, token, checked_branches, errors)
        else:
            logging.error(f"Token epäonnistui autentikoinnissa project_id: {project_id}")

def log_summary_service_activity(project_id, token, checked_branches, errors=None):
    filename = "commit-summary-service-log.md"
    timestamp = datetime.now(timezone.utc).isoformat()
    
    log_entry = f"# Ajo: {timestamp}\n"
    log_entry += f"Tarkistetut haarat ja committien lukumäärät:\n"
    for branch_name, commit_count in checked_branches.items():
        log_entry += f"- {branch_name}: {commit_count} committia\n"
    if errors:
        log_entry += "\n**Virheet:**\n" + "\n".join(errors) + "\n"
    log_entry += "-" * 40 + "\n\n"

    url = f"https://gitlab.dclabra.fi/api/v4/projects/{project_id}/repository/files/{filename}/raw"
    headers = {"PRIVATE-TOKEN": token}
    params = {"ref": "documentation"}
    
    response = requests.get(url, headers=headers, params=params)
    current_content = response.text if response.status_code == 200 else ""

    updated_content = log_entry + current_content
    update_file_in_gitlab(updated_content, filename, project_id, token)
       
schedule.every(2).minutes.do(check_for_new_commits)

if __name__ == "__main__":
    from threading import Thread
    flask_thread = Thread(target=app.run, kwargs={"host": "0.0.0.0", "port": 5000})
    flask_thread.start()

    while True:
        schedule.run_pending()
        time.sleep(1)