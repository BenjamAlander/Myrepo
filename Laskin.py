### Pohja laskimelle
###
def yhteenlasku(x, y):
    return (x + y)
    #tämä funktio laskee kahden luvun yhteenlaskun
def vähennys(x, y):
    return (x - y)
    #tämä funktio laskee kahden luvun erotuksen
def kerto(x, y):
    return x * y
    #tämä funktio laskee kahden luvun tulon
def jako(x, y):
    return int(x/y) #tällä hetkellä palauttaa kokonaisluvun 0 laskutoimituksella 3/4
    #tämä funktio laskee kahden luvun jakolaskun
    #Halutaanko tässä määrittää kuinka monta desimaalia näkyy? Näyttäisi paremmalle jos ei
    #tulisi mahdottoman pitkää rimpsua desimaaleja. T
print("Valitse toiminne")
print("1. Yhteenlasku")
print("2. Erotus")
print("3. Kerro")
print("4. Jaa")

while True:
    #ota syöte käyttäjältä
    valinta = input("Valitse (1)(2)(3)(4): ")
    if valinta in ("1","2","3","4"):
        luku1 = int(input("Syötä ensimmäinen luku: "))
        luku2 = int(input("Syötä toinen luku: "))

        if valinta == "1":
            print(luku1, "+", luku2, "=", yhteenlasku(luku1, luku2))
        elif valinta == "2":
            print(luku1, "-", luku2, "=", vähennys(luku1, luku2))
        elif valinta == "3":
            print(luku1, "*", luku2, "=", kerto(luku1, luku2))
        elif valinta == "4":
            print(luku1, "/", luku2, "=", jako(luku1, luku2))
        #Varmista haluaako käyttäjä laskea uudelleen
        seuraava_lasku = input("Haluatko laskea uudelleen? (haluan/en): ")
        seuraava_lasku = seuraava_lasku.lower()
        if seuraava_lasku == "en":
            break       

 

