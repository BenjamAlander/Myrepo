import sys
import os

# Lisää projektin juurihakemisto hakupolkuun
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def test_example():
    """
    Yksinkertainen testi varmistaaksesi, että pytest toimii.
    """
    assert 1 + 1 == 2

def test_health_endpoint(client):
    """
    Testaa, että /health-reitti palauttaa "OK".
    """
    response = client.get("/health")
    assert response.status_code == 200
    assert response.data.decode("utf-8") == "OK"

def test_add_configuration_to_db(test_db):
    """
    Testaa, että konfiguraatio lisätään tietokantaan oikein.
    """
    conn = test_db
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO configurations (project_id, token, last_checked) VALUES (?, ?, ?)",
        ("example/repo", "example-token", None),
    )
    conn.commit()

    cursor.execute("SELECT project_id, token, last_checked FROM configurations")
    result = cursor.fetchone()
    assert result == ("example/repo", "example-token", None)

def test_mocked_gitlab_api(mock_gitlab_api):
    """
    Testaa, että GitLab API -mock toimii oikein.
    """
    mock_get, mock_put, mock_post = mock_gitlab_api

    # Mockataan GET-pyyntö
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = [{"name": "main"}, {"name": "dev"}]

    # Simuloidaan API-kutsu
    import requests
    response = requests.get("https://gitlab.example.com/api/v4/projects/123/repository/branches")
    assert response.status_code == 200
    assert response.json() == [{"name": "main"}, {"name": "dev"}]

    # Varmistetaan, että mockia käytettiin
    mock_get.assert_called_once()