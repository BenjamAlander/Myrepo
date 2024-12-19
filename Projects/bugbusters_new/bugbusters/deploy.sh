#!/bin/bash

# Asetetaan projekti-hakemiston polku
PROJECT_DIR=$(pwd)
DOCKER_CONTAINER_NAME="commit-summary-service"
DOCKER_IMAGE_NAME="commit-summary-image"
DOCKER_DB_DIR="$PROJECT_DIR/docker_temp"

# Luodaan mountattava hakemisto tietokannalle, jos sitä ei ole olemassa, ja annetaan sille käyttöoikeudet
mkdir -p "$DOCKER_DB_DIR"
chmod 777 "$DOCKER_DB_DIR"

# Poistetaan vanha kontti, jos se on olemassa
echo "Poistetaan vanha kontti, jos se on olemassa..."
docker rm -f $DOCKER_CONTAINER_NAME || true

# Rakennetaan uusi Docker-kuva
echo "Rakennetaan uusi Docker-kuva nimellä $DOCKER_IMAGE_NAME..."
# docker build --no-cache -t $DOCKER_IMAGE_NAME .
docker build -t $DOCKER_IMAGE_NAME .

# Käynnistetään uusi kontti mountattuna hakemistoon ja seurataan lokeja
echo "Käynnistetään kontti nimellä $DOCKER_CONTAINER_NAME..."
docker run --name $DOCKER_CONTAINER_NAME -v "$DOCKER_DB_DIR":/app/docker -p 8080:5000 $DOCKER_IMAGE_NAME &

# Odotetaan hetki kontin käynnistymistä
sleep 3

# Tarkistetaan, että kontti on käynnissä, ja näytetään lokit
if docker ps | grep -q $DOCKER_CONTAINER_NAME; then
    echo "Kontti $DOCKER_CONTAINER_NAME käynnissä. Näytetään lokit:"
    docker logs -f $DOCKER_CONTAINER_NAME
else
    echo "Virhe: Kontti $DOCKER_CONTAINER_NAME ei käynnistynyt oikein."
fi

#chmod +x deploy.sh  # Varmista, että skripti on suoritettavissa
#./deploy.sh