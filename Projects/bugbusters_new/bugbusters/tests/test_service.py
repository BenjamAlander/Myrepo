# app/tests/test_service.py

# Suorittaminen:
# Siirry oikeaan hakemistoon: cd ../Projekti4/bugbusters/tests
# Suorita testit komennolla: pytest -s test_service.py


# Lisätään projektin juurihakemisto moduulipolkuun
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from unittest.mock import patch
from app.service import generate_summary, get_branch_commits


@pytest.fixture
def mock_gitlab_response():
    # Luodaan mock-vastaus GitLab API:lle
    response = [
        {"id": "123abc", "created_at": "2023-11-23T10:00:00.000Z", "message": "Add feature", "author_name": "Tester"}
    ]
    print("\n[Fixture] Mock GitLab response created:", response)
    return response


@patch("app.service.requests.post")
def test_generate_summary_success(mock_post):
    # Mockataan Ollama API -vastaus
    mock_post.return_value.status_code = 200
    mock_post.return_value.iter_lines.return_value = [
        '{"response": "Lisätty uusi toiminnallisuus."}'.encode('utf-8')
    ]

    diff = "test_diff"
    print("\n[Test] Calling generate_summary with diff:", diff)
    # Kutsutaan generate_summary-funktiota mockatulla datalla
    summary = generate_summary(diff)
    print("[Test] Summary generated:", summary)

    # Tarkistetaan, että saatu yhteenveto on odotetun mukainen
    assert summary == "Lisätty uusi toiminnallisuus."
    print("[Test] test_generate_summary_success passed!")


@patch("app.service.requests.get")
def test_get_branch_commits(mock_get, mock_gitlab_response):
    # Mockataan GitLab API -vastaus
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = mock_gitlab_response

    project_id = "1"  # Testiprojektin ID
    token = "test_token"  # Testin käyttäjäkohtainen token
    branch_name = "main"  # Testattava haara
    last_checked = "2023-11-22T12:00:00.000Z"  # Testin viimeinen tarkistusajankohta

    print("\n[Test] Calling get_branch_commits with:")
    print("  Project ID:", project_id)
    print("  Token:", token)
    print("  Branch Name:", branch_name)
    print("  Last Checked:", last_checked)

    # Kutsutaan get_branch_commits-funktiota mockatulla datalla
    commits = get_branch_commits(project_id, token, branch_name, last_checked)
    print("[Test] Commits received:", commits)

    # Varmistetaan, että saatujen commitien määrä on oikea
    assert len(commits) == 1
    print("[Test] Number of commits is correct:", len(commits))

    # Varmistetaan, että ensimmäisen commitin ID on oikea
    assert commits[0]["id"] == "123abc"
    print("[Test] Commit ID is correct:", commits[0]["id"])
    print("[Test] test_get_branch_commits passed!")
