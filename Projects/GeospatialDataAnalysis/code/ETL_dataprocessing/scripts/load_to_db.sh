#!/usr/bin/env bash
# Muuttujat
SOURCE_CSV=C:/project-course-1/code/data/combined_data_cleaned5.csv
DOCKER_CONTAINER=iiwari-mariadb-server
DB_NAME=iiwari_org
DB_USER=root
DB_PASSWORD=d41k4Duu
TABLE_NAME=SensorData

# Tarkista, onko lähdekoodi olemassa
if [ -f "$SOURCE_CSV" ]; then
  echo "Lähdekoodi löytyi: $SOURCE_CSV"
else
  echo "Lähdekoodia ei löytynyt: $SOURCE_CSV"
  exit 1
fi

# Kopioi lähdetiedosto Docker-säiliöön
docker cp "$SOURCE_CSV" "$DOCKER_CONTAINER":/var/lib/mysql/"$TABLE_NAME".csv

# Luo taulu, jos sitä ei ole olemassa, ja poista ensimmäinen rivi (otsikot)
docker exec -i "$DOCKER_CONTAINER" mysql -u "$DB_USER" -p"$DB_PASSWORD" "$DB_NAME" -e "
CREATE TABLE IF NOT EXISTS $TABLE_NAME (
  sensor_id INT,
  timestamp DATETIME,
  x INT,
  y INT
);
LOAD DATA INFILE '/var/lib/mysql/$TABLE_NAME.csv'
IGNORE INTO TABLE $TABLE_NAME
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(sensor_id, timestamp, x, y);
"

# Poista kopioitu tiedosto Docker-säiliöstä
docker exec -i "$DOCKER_CONTAINER" rm /var/lib/mysql/"$TABLE_NAME".csv
