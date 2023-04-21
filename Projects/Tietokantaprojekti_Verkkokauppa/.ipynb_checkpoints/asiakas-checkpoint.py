from SQLPYconnector import databaseConnector as connect
import pymysql
import mysql.connector as database
import pandas as pd
import numpy as np


class asiakas:
    
    def __init__(self, etunimi, sukunimi, postinumero, osoite, email):
        self.etunimi = etunimi
        self.sukunimi = sukunimi
        self.osoite = osoite
        self.email = email
        self.postinumero = postinumero

    def addAsiakas():
        ans = input("Haluatko lisätä uuden asiakkaan tietokantaan? (K/E) (Kyllä/Ei)")
        kyl = ["Kyllä", "K", "Joo", "Yes", "Jep", "KYLLÄ", "joo", "k","kyllä","k'","K'"]
        if ans in kyl:
            etunimi = input(str('etunimi: '))
            sukunimi = input(str('sukunimi: '))
            postinumero = input(str("postinumero: "))
            osoite = input(str('osoite: '))
            email = input(str('email: ')) 
            conn = connect.connectDB("tietokantaprojekti","localhost","root","")
        
            try:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO asiakas (etunimi, sukunimi, postinumero, osoite, email) VALUES (%s, %s, %s, %s, %s)", (etunimi,sukunimi,postinumero,osoite,email))
                   
                # Commit your changes in the database
                conn.commit()
                conn.close()
            
            finally:
                print("Tiedot syötetty onnistuneesti")
        else:
            print("Pyyntö peruttu")
        
            
    
            
    def readAsiakas():
        conn = connect.connectDB("tietokantaprojekti","localhost","root","")
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM asiakas")
    
            rows = cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            df = pd.DataFrame(rows, columns=column_names)
            conn.commit()
            conn.close()
            return df
    
        except database.Error as e:
            print(f"Error reading the database: {e}")
            
    def updateAsiakas():
        
        conn = connect.connectDB("tietokantaprojekti","localhost","root","")
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM asiakas")
            rows = cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            df = pd.DataFrame(rows, columns=column_names)
            print(df)
        
            customer_id = input("Anna päivitettävän asiakkaan asiakasID: ")
            valinta = input("Minkä tiedon haluat päivittää? (etunimi,sukunimi,osoite,email,postinumero)")
        
            if valinta == "etunimi":
                try:
                    v1 = input("Syötä korvaava etunimi: ")
                    cursor.execute(f"UPDATE asiakas SET etunimi = %s WHERE asiakasID = {customer_id}", v1)
                    conn.commit()
                    conn.close()
                except:
                    print("Syöttämäsi asiakasID on virheellinen")
                print("Tieto päivitetty tietokantaan")
                
            elif valinta == "sukunimi":
                try:
                    v2 = input("Syötä korvaava sukunimi: ")
                    cursor.execute(f"UPDATE asiakas SET sukunimi = %s WHERE asiakasID = {customer_id}", v2)
                    conn.commit()
                    conn.close()
                except:
                    print("Syöttämäsi asiakasID on virheellinen")
                print("Tieto päivitetty tietokantaan")
                
            elif valinta == "osoite":
                try:
                    v3 = input("Syötä korvaava osoite: ")
                    cursor.execute(f"UPDATE asiakas SET osoite = %s WHERE asiakasID = {customer_id}", v3)
                    conn.commit()
                    conn.close()
                except:
                    print("Syöttämäsi asiakasID on virheellinen")
                print("Tieto päivitetty tietokantaan")
                
            elif valinta == "email":
                try:
                    v4 = input("Syötä korvaava email")
                    cursor.execute(f"UPDATE asiakas SET email = %s WHERE asiakasID = {customer_id}", v4)
                    conn.commit()
                    conn.close()
                except:
                    print("Syöttämäsi asiakasID on virheellinen")
                print("Tieto päivitetty tietokantaan")
            elif valinta == "postinumero":
                try:
                    v5 = input("Syötä korvaava postinumero")
                    cursor.execute(f"UPDATE asiakas SET postinumero = %s WHERE asiakasID = {customer_id}", v5)
                    conn.commit()
                    conn.close()
                except:
                    print("Syöttämäsi asiakasID on virheellinen")
                print("Tieto päivitetty tietokantaan")
            else:
                print("Ei mennyt ihan putkeen, kokeile uudelleen")
                print("")
                print("Sinun tulee syöttää joku näistä valinnoista:")
                print("(etunimi,sukunimi,osoite,email)")
            
            
        
    
        except database.Error as e:
            print(f"Error reading the database: {e}")
            
    def muokkaa():
        ans = input("Haluatko muokata asiakastietoja? (K/E) (Kyllä/Ei)")
        kyl = ["Kyllä", "K", "Joo", "Yes", "Jep", "KYLLÄ", "joo", "k","kyllä","k'","K'"]
        if ans in kyl:
            asiakas.updateAsiakas()
        else:
            print("Pyyntö peruttu")
            
    
    
    def delAsiakas():
        conn = connect.connectDB("tietokantaprojekti","localhost","root","")
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM asiakas")
            rows = cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            df = pd.DataFrame(rows, columns=column_names)
            print(df)
        
            customer_id = input("Anna poistettavan asiakkaan asiakasID tai poistu (exit)")
            if customer_id == "exit":
                return "Exited succesfully"
            else:
                try:
                    cursor.execute(f"DELETE FROM asiakas WHERE asiakasID = {customer_id}")
                    print("Asiakas poistettu onnistuneesti.")
                    conn.commit()
                    conn.close()
                except:
                    print("Asiakkaalla on tilaus käsittelyssä, et voi poistaa asiakasta vielä")
    
        except database.Error as e:
            print(f"Error reading the database: {e}")

        
            
    def poistaAsiakas():
        ans = input("haluatko poistaa asiakkaan tietokannasta? (K/E) (Kyllä/Ei)")
        kyl = ["Kyllä", "K", "Joo", "Yes", "Jep", "KYLLÄ", "joo", "k"]
        if ans in kyl:
            asiakas.delAsiakas()
            
        else:
            print("Pyyntö peruttu")
        
        


            
        

    