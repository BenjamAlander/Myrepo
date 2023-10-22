import csv

# Muokkaa näitä tiedostonimiä tarpeen mukaan
input_file = "code/data/combined_data_cleaned2.csv"
output_file = "code/data/combined_data_cleaned3.csv"

# Z- ja Q-sarakkeiden otsikot
z_otsikko = "z"
q_otsikko = "q"

# Alusta muuttujat indekseille
z_sarake = None
q_sarake = None

with open(input_file, "r", encoding="utf-8") as input_csv, open(output_file, "w", encoding="utf-8", newline='') as output_csv:
    csv_reader = csv.reader(input_csv)
    csv_writer = csv.writer(output_csv)

    for i, row in enumerate(csv_reader):
        if i == 0:
            # Etsi Z- ja Q-sarakkeiden indeksit ensimmäiseltä riviltä
            z_sarake = row.index(z_otsikko)
            q_sarake = row.index(q_otsikko)

        # Tallenna poistettavien sarakkeiden indeksit listaan ja poista ne käänteisessä järjestyksessä
        poistettavat_sarakkeet = [z_sarake, q_sarake]
        for sarake in sorted(poistettavat_sarakkeet, reverse=True):
            del row[sarake]

        # Kirjoita muokattu rivi uuteen tiedostoon
        csv_writer.writerow(row)

print("Tiedosto on käsitelty ja uusi tiedosto on luotu: ", output_file)
