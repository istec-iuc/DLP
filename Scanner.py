import time
from watchdog.events import FileSystemEventHandler
import os
import mysql.connector
import pandas as pd
import re
from datetime import datetime

mydb = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="",
    database="dlp"
)

path = os.path.join(os.path.join(os.environ['USERPROFILE']))


os.chdir(path)

class Handler(FileSystemEventHandler):
    @staticmethod
    def on_any_event(event):
        # if event.is_directory:
        #     return None
        print(
            "[{}] noticed: [{}] on: [{}] ".format(
                time.asctime(), event.event_type, event.src_path
            )
        )
    
    def on_modified(self, event):

        for file in os.listdir():

            if file.endswith(".xlsx"):
                file_path = f"{path}\{file}"

                df = pd.read_excel(file_path, dtype="string").to_string()
                if re.search(r'[\w\.-]+@[\w\.-]+', df):
                    mycursor = mydb.cursor()
                    sql = "INSERT INTO dlp_logs (file_path, event_type, created_date) VALUES (%s, %s, %s)"
                    val = (file_path, "E-Mail Credential Found", now)
                    mycursor.execute(sql, val)

                    mydb.commit()

                    print(mycursor.rowcount, "record inserted.")
                    print(file_path + " credential information founded ")
                if re.search(r'((\d)-?(?!(-?\2){3})){16}', df):
                    pass

            if file.endswith(".pdf"):
                file_path = f"{path}\{file}"
                pdf = PdfFileReader(file_path)
                print(file_path)
                for page_num in range(pdf.numPages):

                    pageObj = pdf.getPage(page_num)
                    txt = pageObj.extractText()
                    if re.search(r'((\d)-?(?!(-?\2){3})){16}', txt):
                        mycursor = mydb.cursor()

                        now = datetime.now()
                        sql = "INSERT INTO dlp_logs (file_path, event_type, created_date) VALUES (%s, %s, %s)"
                        val = (file_path, "Credit Card Credential Found", now)
                        mycursor.execute(sql, val)

                        mydb.commit()

                        print(mycursor.rowcount, "record inserted.")
                        print(file_path + " credential information founded ")

                    if re.search(r'[\w\.-]+@[\w\.-]+', txt):
                        print(file_path + " credential information founded ")
                        mycursor = mydb.cursor()
                        now = datetime.now()
                        sql = "INSERT INTO dlp_logs (file_path, event_type, created_date) VALUES (%s, %s, %s)"
                        val = (file_path, "E-Mail Credential", now)
                        mycursor.execute(sql, val)

                        print(mycursor.rowcount, "record inserted.")
                        mydb.commit()

                        print(mycursor.rowcount, "record inserted.")
                        print("mail found")

            if file.endswith(".txt"):

                file_path = f"{path}\{file}"
                print(file_path)
                
                with open(file_path, 'r') as f:
                    lines = f.read()
                    if re.search(r'((\d)-?(?!(-?\2){3})){16}', lines):
                        print("creditcard")
                        mycursor = mydb.cursor()
                        now = datetime.now()
                        sql = "INSERT INTO dlp_logs (file_path, event_type, created_date) VALUES (%s, %s, %s)"
                        val = (file_path, "Credit Card Credential Found", now)
                        mycursor.execute(sql, val)

                        mydb.commit()

                        print(mycursor.rowcount, "record inserted.")
                        print(file_path + " credential information founded ")

                    if re.search(r'[\w\.-]+@[\w\.-]+', lines):
                        mycursor = mydb.cursor()
                        now = datetime.now()
                        sql = "INSERT INTO dlp_logs (file_path, event_type, created_date) VALUES (%s, %s, %s)"
                        val = (file_path, "E-Mail Credential", now)
                        mycursor.execute(sql, val)

                        mydb.commit()

                        print(mycursor.rowcount, "record inserted.")
                        print(file_path + " credential information founded ")

                        print("mail found")
