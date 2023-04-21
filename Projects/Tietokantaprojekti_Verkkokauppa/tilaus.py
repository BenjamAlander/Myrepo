from SQLPYconnector import databaseConnector as connect
import pymysql
import mysql.connector as database
import pandas as pd
import numpy as np
from datetime import date
from tuote import tuote
from asiakas import asiakas
import matplotlib.pyplot as plt


class tilaus:
    
    def __init__(self, asiakasID, tilausPVM):
        self.tilausPVM = tilausPVM
        self.asiakasID = asiakasID
                
    def readTilaus():
        conn = connect.connectDB("tietokantaprojekti","localhost","root","")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tilaus")
    
        rows = cursor.fetchall()
        column_names = [desc[0] for desc in cursor.description]
        df = pd.DataFrame(rows, columns=column_names)
        conn.commit()
        conn.close()
        return df
    
    
    def ostosKori():
        print(asiakas.readAsiakas())
        print("--------------------------------------------------------")
        ostoskori = []
        indeksi = 0
        asiakasID = int(input("Syötä asiakasID jatkaaksesi: "))
        print("--------------------------------------------------------")
    
        while True:
            print("Ostoskorisi sisältö (tuoteID): ", ostoskori)
            print(tuote.readTuote())
            print("Voit poistua vastaamalla 'exit'")
            print("Lisää tuotteen tuoteID tai vastaa 'tilaa' vahvistaaksesi tilauksen: ")
            print("")
            ans = input("Valitse tuotteen tuoteID tai vahvista tilaus (tilaa/exit): ")
        
            if ans == "exit":
                return "Pyyntö peruttu"
                  
            elif ans == "tilaa":
                conn = connect.connectDB("tietokantaprojekti","localhost","root","")
                try:
                    # Open database connection
                    tilausPVM = date.today()
                    cursor = conn.cursor()
                
                    # Luo listan ostoskorin tuotteiden id-numeroista
                    tuotteet = [tuoteID for tuoteID in ostoskori]
                    mrkjono = ""
                    for i in tuotteet:
                        mrkjono += i
                        mrkjono += ","
                    mrkjono = mrkjono[0:-1]
            
            
                    cursor.execute("INSERT INTO tilaus (tuotteet, tilausPVM, asiakasID) VALUES (%s, %s, %s)", (mrkjono,tilausPVM, asiakasID))
                    conn.commit()
                    conn.close()
                    return "Tilaus luotu"
                
                except database.Error as e:
                    print(f"Error adding entry to database: {e}")
                
            else:
                ostoskori.append(ans)
                print(tuote.readTuote())
                print("Tuote", ans, "on nyt lisätty ostoskoriin")
                print("--------------------------------------------------------")
                
    def delTilaus():
        conn = connect.connectDB("tietokantaprojekti","localhost","root","")
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM tilaus")
            rows = cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            df = pd.DataFrame(rows, columns=column_names)
            print(df)
        
            tilaus_id = input("Anna tilauksen tilausID minkä haluat poistaa: ")
            cursor.execute(f"DELETE FROM tilaus WHERE tilausID = {tilaus_id}")
            conn.commit()
            conn.close()
    
        except database.Error as e:
            print(f"Error reading the database: {e}")
            
    def poistaTilaus():
        ans = input("Haluatko poistaa tuotteen? (K/E) (Kyllä/Ei)")
        kyl = ["Kyllä", "K", "Joo", "Yes", "Jep", "KYLLÄ", "joo", "k"]
        if ans in kyl:
            tilaus.delTilaus()
            print("Tilaus poistettu onnistuneesti.")
        else:
            print("Pyyntö peruttu")
            
            
            
    def tilauksenSisalto():
        print(tilaus.readTilaus())
        conn = connect.connectDB("tietokantaprojekti","localhost","root","")
        try:
            cursor = conn.cursor()
            tilaus_id = input("Anna tilauksen tilausID: ")
    
            # Get customer details
            cursor.execute(f"SELECT asiakas.etunimi, asiakas.sukunimi, asiakas.postinumero, asiakas.osoite, asiakas.email FROM tilaus JOIN asiakas ON tilaus.asiakasID = asiakas.asiakasID WHERE tilaus.tilausID = {tilaus_id}")
            customer_row = cursor.fetchone()
            customer_details = f"\n{customer_row[0]}\n{customer_row[1]}\n{customer_row[2]}\n{customer_row[3]}\n"
            print(customer_details)
    
            # Print ASCII separators
            separator = "-"*50
            print(separator)
    
            cursor.execute(f"SELECT tuote.tuotenimi, tuote.tuotehinta FROM tilaus JOIN tuote ON tilaus.tuotteet LIKE CONCAT('%', tuote.tuoteID, '%') WHERE tilaus.tilausID = {tilaus_id}")
            rows = cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            df = pd.DataFrame(rows, columns=column_names)
            print(df)
        
            # Print total price
            total = sum([row[1] for row in rows])
            print(f"Tilauksen kokonaissumma: {total}")
    
            # Print ASCII separators
            print(separator)
    
            conn.close()
        except database.Error as e:
            print(f"Error retrieving data from database: {e}")


            
            
    def tilaustenTuotto():
        conn = connect.connectDB("tietokantaprojekti","localhost","root","")
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT SUM(tuote.tuotehinta) AS total_sales FROM tilaus JOIN tuote ON tilaus.tuotteet LIKE CONCAT('%', tuote.tuoteID, '%')")
            rows = cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            df = pd.DataFrame(rows, columns=column_names)
            print(df)

            conn.close()
        except database.Error as e:
            print(f"Error retrieving data from database: {e}")
            
    


  

  

    




        

        

                    
                
        
    
               
                
                    
                
                
        
            
        
        
        
        
            
       