import time
from watchdog.events import FileSystemEventHandler
import os
from PyPDF2 import PdfFileReader
import mysql.connector
import pandas as pd
import re

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Dlp-747",
    database="mydatabase"
)

class Handler(FileSystemEventHandler):
    @staticmethod
    def on_any_event(event):
        # if event.is_directory:
        #     return None
        """print(
            "[{}] noticed: [{}] on: [{}] ".format(
                time.asctime(), event.event_type, event.src_path
            )
        )"""
        time.sleep(5)
        mycursor = mydb.cursor()
        mycursor.execute("DELETE FROM alerts")

        path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
        path2 = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Downloads')

        fileCheck(path)
        fileCheck(path2)


def fileCheck(path):
    mycursor = mydb.cursor()
    try:
        os.chdir(path)
        for file in os.listdir():

            if file.endswith(".xlsx"):
                file_path = f"{path}\{file}"

                df = pd.read_excel(file_path, dtype="string").to_string()
                if re.search(r'[\w\.-]+@[\w\.-]+', df):

                    sql = "INSERT INTO alerts (filePath, eventType) VALUES (%s, %s)"
                    val = (file_path, "E-Mail Credential Found")
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


                        sql = "INSERT INTO alerts (filePath, eventType) VALUES (%s, %s)"
                        val = (file_path, "Credit Card Credential Found")
                        mycursor.execute(sql, val)

                        mydb.commit()

                        print(mycursor.rowcount, "record inserted.")
                        print(file_path + " credential information founded ")

                    if re.search(r'[\w\.-]+@[\w\.-]+', txt):
                        print(file_path + " credential information founded ")


                        sql = "INSERT INTO alerts (filePath, eventType) VALUES (%s, %s)"
                        val = (file_path, "E-Mail Credential")
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


                        sql = "INSERT INTO alerts (filePath, eventType) VALUES (%s, %s)"
                        val = (file_path, "Credit Card Credential Found")
                        mycursor.execute(sql, val)

                        mydb.commit()

                        print(mycursor.rowcount, "record inserted.")
                        print(file_path + " credential information founded ")

                    if re.search(r'[\w\.-]+@[\w\.-]+', lines):


                        sql = "INSERT INTO alerts (filePath, eventType) VALUES (%s, %s)"
                        val = (file_path, "E-Mail Credential")
                        mycursor.execute(sql, val)

                        mydb.commit()

                        print(mycursor.rowcount, "record inserted.")
                        print(file_path + " credential information founded ")

                        print("mail found")

                    f.close()

            else:
                fileCheck2(path, file)
    except:
        print("---------------DOSYA Taşınma/Silinme HATASI-----------------")

def fileCheck2(path, file):

        dirPath = f"{path}\{file}"
        if os.path.isdir(dirPath):

            os.chdir(dirPath)

            for file in os.listdir():

                if file.endswith(".pdf"):
                    file_path = f"{dirPath}\{file}"
                    pdf = PdfFileReader(file_path)
                    for page_num in range(pdf.numPages):

                        pageObj = pdf.getPage(page_num)
                        txt = pageObj.extractText()
                        if re.search(r'((\d)-?(?!(-?\2){3})){16}', txt):
                            mycursor = mydb.cursor()

                            sql = "INSERT INTO alerts (filePath, eventType) VALUES (%s, %s)"
                            val = (file_path, "Credit Card Credential Found")
                            mycursor.execute(sql, val)

                            mydb.commit()

                            print(mycursor.rowcount, "record inserted.")
                            print(file_path + " credential information founded ")

                        if re.search(r'[\w\.-]+@[\w\.-]+', txt):
                            print(file_path + " credential information founded ")
                            mycursor = mydb.cursor()

                            sql = "INSERT INTO alerts (filePath, eventType) VALUES (%s, %s)"
                            val = (file_path, "E-Mail Credential Found")
                            mycursor.execute(sql, val)

                            mydb.commit()

                            print(mycursor.rowcount, "record inserted.")
                            print("mail found")

                if file.endswith(".txt"):
                    file_path = f"{dirPath}\{file}"
                    with open(file_path, 'r') as f:
                        lines = f.read()
                        if re.search(r'((\d)-?(?!(-?\2){3})){16}', lines):
                            mycursor = mydb.cursor()

                            sql = "INSERT INTO alerts (filePath, eventType) VALUES (%s, %s)"
                            val = (file_path, "Credit Card Credential Found")
                            mycursor.execute(sql, val)

                            mydb.commit()

                            print(mycursor.rowcount, "record inserted.")
                            print(file_path + " credential information founded ")

                        if re.search(r'[\w\.-]+@[\w\.-]+', lines):
                            mycursor = mydb.cursor()

                            sql = "INSERT INTO alerts (filePath, eventType) VALUES (%s, %s)"
                            val = (file_path, "E-Mail Credential Found")
                            mycursor.execute(sql, val)

                            mydb.commit()

                            print(mycursor.rowcount, "record inserted.")
                            print(file_path + " credential information founded ")
                        f.close()

                else:
                    return fileCheck2(dirPath, file)
