hjelmiston vaatimusmäärittely: Bugbusters - Automaattinen Git Commit -muutosten seuranta ja dokumentointi

1. Johdanto

Bugbusters-sovelluksen tarkoituksena on automatisoida commit-muutosten seuranta ja dokumentointi GitLab-repositoriossa. Sovellus tarkistaa uudet commitit, luo yhteenvedot koodimuutoksista ja päivittää tarvittavat dokumentaatiotiedostot (commits.md, project_overview.md) suoraan GitLab-repositorioon. Sovellus on rakennettu Flask-kehystä hyödyntäen, ja se käyttää Ollama APIa tuottamaan tekstiyhteenvedot suomeksi.

2. Sovelluksen tarkoitus

Bugbusters-sovellus tarjoaa seuraavat toiminnot:

Commit-muutosten seuranta: Tunnistaa uudet commitit ja analysoi muutosten sisällön.

Yhteenvedon generointi: Tuottaa automaattisesti yhteenvedon commit-muutoksista.

Dokumentaation päivitys: Päivittää commits.md- ja project_overview.md-tiedostot.

API-tuki: Flask-sovellus tarjoaa rajapinnan manuaaliselle commit-analyysille ja dokumentoinnille.

3. Toiminnalliset vaatimukset

3.1 Käyttäjän toiminnallisuudet

Commit-muutosten seuranta: Sovellus tunnistaa automaattisesti uudet commitit GitLab-repositoriossa.

Yhteenvedon generointi commitista: Luo kuvailevan yhteenvedon commit-muutoksista ja tuottaa sen commits.md-tiedostoon.

Dokumentaation päivitys: Päivittää project_overview.md-tiedoston viimeisimpien commit-muutosten perusteella.

Käyttäjän hallinta: Mahdollistaa commit-analyysin ja dokumentaation päivityksen manuaalisesti sovelluksen API-rajapinnan kautta.

3.2 Järjestelmän toiminnallisuudet

Commit-muutosten analysointi: Tunnistaa commitin sisältämät koodimuutokset tiedostotasolla.

Ollama API -integraatio: Hyödyntää Ollama APIa tekstiyhteenvedon luomisessa suomeksi.

Tiedostojen päivitys: commits.md- ja project_overview.md-tiedostot päivittyvät automaattisesti commit-analyysin tuloksena.

4. Ei-toiminnalliset vaatimukset

4.1 Suorituskyky

Commit-analyysi ja tekstiyhteenvedon generointi tulee suorittaa muutamassa sekunnissa.

Sovelluksen toiminta ei saa vaikuttaa merkittävästi GitLab-repositorion käyttöön.

4.2 Skalautuvuus

Sovelluksen on toimittava tehokkaasti sekä pienissä että suurissa projekteissa, joissa voi olla satoja committeja.

4.3 Yläpidettävyys

Sovelluksen on oltava helposti päivitettävissä uusien API-versioiden ja kirjastojen tukemiseksi.

5. Rajapinnat ja tekniset vaatimukset

5.1 Rajapinnat

Ollama API: Tekstiyhteenvetojen tuottamiseen commit-muutoksista.

GitLab API: Commit-muutosten hakemiseen ja analysointiin.

5.2 Teknologiat

Ohjelmointikieli: Python

Web-kehys: Flask

Tietokanta: SQLite3 tai muu kevyt tietokanta audit-tietojen ja commit-muistioiden hallintaan.

API-käyttö: OpenAI- ja GitLab-API-integraatiot.

6. Suoritusympäristö

Palvelin: Toimii Docker-pohjaisessa ympäristössä, jossa on Python-ympäristö Flask-kehystä varten.

Yhteensopivuus: Tukee eri alustoja, kuten Windows, macOS ja Linux.

7. Rajoitukset

Kieli: Tukee aluksi vain suomenkielistä dokumentaatiota.

API-kustannukset: OpenAI API käyttö voi aiheuttaa kustannuksia.

Commit-yhteenvetojen tarkkuus: Sovellus voi luoda yleisen tason commit-yhteenvedon, joten erikoistapauksissa käyttäjän on tarpeen muokata yhteenvedon sisältöä.

8. Tulevaisuuden kehitysmahdollisuudet

Kielituen laajentaminen: Tuki useammille kielille.

Integraatio muiden versionhallintatyökalujen kanssa: Tuki GitHubille ja Bitbucketille.

Oppimiskykyinen AI: AI-mallin muokkaaminen siten, että se oppii aiempien commit-viestien perusteella tuottamaan tarkempia yhteenvedot.

