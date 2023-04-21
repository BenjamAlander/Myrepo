from SQLPYconnector import databaseConnector as connect
import pymysql
import mysql.connector as database
import pandas as pd
import numpy as np


class tuote:
    
    def __init__(self, tuotenimi, tuotehinta):
        self.tuotenimi = tuotenimi
        self.tuotehinta = tuotehinta
        
    def addProduct(tuotenimi, tuotehinta):
        conn = connect.connectDB("tietokantaprojekti","localhost","root","")
        try:
            # Open database connection
            cursor = conn.cursor()
            cursor.execute("INSERT INTO tuote (tuotenimi, tuotehinta) VALUES (%s, %s)", (tuotenimi, tuotehinta))
                   
            # Commit your changes in the database
            conn.commit()
            conn.close()
            print("Tuote lisätty onnistuneesti tietokantaan")
        except database.Error as e:
            print(f"Error adding entry to database: {e}")
            
    def addTuote():
        ans = input("Haluatko lisätä tuotteen tietokantaan? (K/E) (Kyllä/Ei)")
        kyl = ["Kyllä", "K", "Joo", "Yes", "Jep", "KYLLÄ", "joo", "k","kyllä","k'","K'"]
        if ans in kyl:
            tuotenimi = input(str('aseta tuotteen nimi'))
            tuotehinta = input(str('aseta tuotteen hinta (€)'))
            tuote.addProduct(tuotenimi, tuotehinta) 
        else:
            print("Pyyntö peruttu")
            
    def readTuote():
        conn = connect.connectDB("tietokantaprojekti","localhost","root","")
        try:
          # Open database connection
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM tuote")
        
            rows = cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
        
            df = pd.DataFrame(rows, columns=column_names)
        
                   
            # Commit your changes in the database
            conn.commit()
            conn.close()
            return df
    
        except database.Error as e:
            print(f"Error reading the database: {e}")
            
            
    def delTuote():
        conn = connect.connectDB("tietokantaprojekti","localhost","root","")
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM tuote")
            rows = cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            df = pd.DataFrame(rows, columns=column_names)
            print(df)
        
            tuote_id = input("Anna tuotteen tuoteID minkä haluat poistaa: ")
            cursor.execute(f"DELETE FROM tuote WHERE tuoteID = {tuote_id}")
            
            conn.commit()
            conn.close()
    
        except database.Error as e:
            print(f"Error reading the database: {e}")
            
    def poistaTuote():
        ans = input("Haluatko poistaa tuotteen? (K/E) (Kyllä/Ei)")
        kyl = ["Kyllä", "K", "Joo", "Yes", "Jep", "KYLLÄ", "joo", "k"]
        if ans in kyl:
            tuote.delTuote()
            print("Tuote poistettu onnistuneesti.")
        else:
            print("Pyyntö peruttu")
       