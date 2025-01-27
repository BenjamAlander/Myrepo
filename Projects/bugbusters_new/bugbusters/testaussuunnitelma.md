# Bugbusters Testaussuunnitelma

## Johdanto

Tämä testaussuunnitelma keskittyy Bugbusters-projektin ydintoimintojen varmistamiseen. Projekti seuraa GitLab-repositorioiden commit-muutoksia, generoi diff-muutoksista tiivistelmiä ja päivittää dokumentaatiotiedostoja automaattisesti. Testauksen tavoitteena on todentaa, että sovelluksen ydinprosessit toimivat odotetusti ja virhetilanteet käsitellään asianmukaisesti.

## Sisällysluettelo
1. [Johdanto](#johdanto)
2. [Testauksen kohteet](#testauksen-kohteet)
3. [Testityypit](#testityypit)
   - [Yksikkötestit](#yksikkötestit)
   - [Integraatiotestit](#integraatiotestit)
   - [Virhetestit](#virhetestit)
4. [Testausvaiheet](#testausvaiheet)
   - [Vaihe 1: Testauksen valmistelu](#vaihe-1-testauksen-valmistelu)
   - [Vaihe 2: Yksikkötestaus](#vaihe-2-yksikkötestaus)
   - [Vaihe 3: Integraatiotestaus](#vaihe-3-integraatiotestaus)
   - [Vaihe 4: Virhetestaus](#vaihe-4-virhetestaus)
5. [Testaustyökalut ja raportointi](#testaustyökalut-ja-raportointi)
   - [Testaustyökalut](#testaustyökalut)
   - [Raportointi](#raportointi)
6. [Testauksen kriteerit](#testauksen-kriteerit)
   - [Hyväksymiskriteerit](#hyväksymiskriteerit)
   - [Hylkäyskriteerit](#hylkäyskriteerit)


## Testauksen kohteet

1. **Commitien haku ja analysointi:**
   - Commit-muutosten haku GitLabin API:sta.
   - Diff-tiivistelmien generointi Ollama API:n kautta.

2. **Dokumentaation päivitys:**
   - Tiivistelmien tallentaminen dokumentaatiohaaraan.
   - Dokumentaation päivitys GitLabissa.

3. **Virheenkäsittely:**
   - Puuttuvan tokenin käsittely.
   - Virheellinen commit-data.
   - Ollama API:n saavutettavuusongelmat.

## Testityypit

1. **Yksikkötestit**
   - Tavoite: Varmistaa yksittäisten funktioiden oikea toiminta.
   - Testattavat moduulit:
     - `db_setup.py`: Tietokannan alustaminen ja konfiguraatiotietojen tallennus.
     - `service.py`: Commit-muutosten haku ja diff-tiivistelmien luonti.

2. **Integraatiotestit**
   - Tavoite: Testata, että commit-haku, tiivistelmien generointi ja dokumentaation päivitys toimivat saumattomasti yhdessä.
   - Simuloi commit-muutoksia testi-GitLab-repositoriossa.

3. **Virhetestit**
   - Tavoite: Varmistaa, että sovellus reagoi oikein seuraaviin virheisiin:
     - Puuttuva tai virheellinen token.
     - API:n saavutettavuusongelmat.
     - Dokumentaatiohaaran puuttuminen.

## Testausvaiheet

### Vaihe 1: Testauksen valmistelu
- Asenna riippuvuudet:
  ```bash
  pip install -r requirements.txt
  ```
- Alusta tietokanta:
  ```bash
  python app/db_setup.py
  ```
- Varmista testiympäristö:
  - Dockerilla tai paikallisesti.
- Asenna pytest:
   ```pip install pytest
   ```


### Vaihe 2: Yksikkötestaus
- Testaa ydintoiminnot:
  ```bash
  pytest app/tests/test_db_setup.py
  pytest app/tests/test_service.py
  ```

### Vaihe 3: Integraatiotestaus
- Simuloi commit-muutokset testi-GitLab-repositoriossa.
- Tarkista, että tiivistelmät ja dokumentaatio päivittyvät odotetusti.

### Vaihe 4: Virhetestaus
- Simuloi virhetilanteet:
  - Puuttuva token.
  - Virheellinen commit-muoto.
  - Ollama API:n saavutettavuusongelmat.

## Testaustyökalut ja raportointi

### Testaustyökalut
- **Pytest**: Yksikkö- ja integraatiotestaukseen.
- **Docker**: Testiympäristön hallintaan.
- **Logitiedostot**: Tapahtumien ja virheiden tarkasteluun.

### Raportointi
- Kaikki testitulokset tarkastetaan lokitiedostoista.
- Tarvittaessa raportti tallennetaan tiedostoon `test-report.md`.

## Testauksen kriteerit

### Hyväksymiskriteerit
- Commit-muutokset haetaan ja tiivistelmät generoidaan onnistuneesti.
- Virheelliset syötteet tunnistetaan ja niistä raportoidaan.
- Dokumentaatio päivittyy ilman käyttäjän puuttumista.

### Hylkäyskriteerit
- Sovellus epäonnistuu commit-muutosten tiivistämisessä yli 10 % tapauksista.
- Sovellus ei käsittele virhetilanteita odotetusti.

