# Käytetään kevyttä Pythonin base imagea
FROM python:3.9-slim

# Asennetaan tarvittavat riippuvuudet
RUN apt-get update && apt-get install -y \
    curl \
    git \
    sqlite3 \
    && rm -rf /var/lib/apt/lists/*

# Asennetaan Ollama CLI (muokattu komento)
RUN curl -sSL "https://ollama.com/cli/download" | bash || echo "Ollama asennus epäonnistui. Varmista URL-osoite."

# Määritellään työkansio
WORKDIR /app

# Kopioidaan requirements.txt ja asennetaan Python-riippuvuudet
COPY requirements.txt .
RUN pip install -r requirements.txt

# Kopioidaan kaikki tiedostot app-hakemistosta kontin /app-hakemistoon
COPY app/ /app

# Luodaan tyhjät commits.md ja overview.md dokumentaatiohaaraa varten, mikäli niitä ei ole olemassa
RUN touch /app/commits.md /app/overview.md

# Määritellään käynnistyskomento
CMD ["bash", "/app/start.sh"]