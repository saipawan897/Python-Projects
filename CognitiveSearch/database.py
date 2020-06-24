import mysql.connector
import os
import overlay
#import magic
import urllib.request
import fitz
from app import app
from flask import Flask, flash, request, redirect, render_template
from werkzeug.utils import secure_filename
import pytesseract
import numpy as np
from pytesseract import Output

import cv2

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="saipawan897",
  database = "mydatabase"
)
  
mycursor = mydb.cursor()
pytesseract.pytesseract.tesseract_cmd ="C:\\Users\\saipa\\AppData\\Local\\Tesseract-OCR\\tesseract.exe"
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
directory = r'C:/Users/saipa/Desktop/project/Data'
total_count = 0
for filename in os.listdir(directory):
    if filename.endswith(".pdf"):
        #new = os.path.join(directory, filename)
        #print(new)
        pdffile = os.path.join(directory, filename)
        doc = fitz.open(pdffile)
        count = doc.pageCount
        print(filename)
        print(count)
        no = 0
        new = {}
        for i in range(count):
            page = doc.loadPage(i)
            pix = page.getPixmap()
            image_matrix = fitz.Matrix(fitz.Identity)
            image_matrix.preScale(2, 2)
            #gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            pix = page.getPixmap(alpha = False, matrix=image_matrix)
            output_folder = r'C:/Users/saipa/Desktop/project/input/'
            output = str(output_folder)+str(filename)+"-"+str(no)+".png"
            print(output)
    #print(output)
            pix.writePNG(output)
            no += 1
            alpha = 0.3 
            img = cv2.imread(output) # Read in the image and convert to grayscale
            d = pytesseract.image_to_data(img, output_type=Output.DICT, lang='eng')
            n_boxes = len(d['level'])
            overlay = img.copy()
            #word = list(keyword.split(" "))
            for i in range(n_boxes):
                text = d['text'][i]
                (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
                if(str(text) != "" and str(text).isspace() == False):
                    result = [str(filename),str(output),str(text), str((x, y, w, h))]
                    new.setdefault('result', [])
                    new['result'].append(result)
        print(new)
        sample = []
        sample = list(new.values())
        filecontent  = sample[0]
        result = (filecontent)
#print(result[5])
#new = []
#for i in result:
  #new = new.append(i)
        for x in result:
            files = x
    #print(files)
            for y in files:
                if y.endswith(".pdf"):
                    filename = y
            #print("filename:"+y)
                elif y.endswith('.png'):
                     imagepath = y   
                elif y.startswith("(") and y.endswith(")") :
                    coordinates = y
            #print("co-ordinates:"+y)
                else :
                    word = y.replace(",", "").replace("=","").replace('"',"")
            #print("word:"+y)
#sql_Delete_query = """truncate table testword """
#mycursor.execute(sql_Delete_query)
#mydb.commit()
    #for n in files:           
            sql_format ='INSERT INTO testword (filename,imagepath, word, coordinates) VALUES ("'+filename+'","'+imagepath+'","'+word+'","'+coordinates+'")'
            #real_sql = sql_format.format(*result)
            print (word)
            mycursor.execute(sql_format)
            mydb.commit()
#row_count = mycursor.rowcount
#print ("number of affected rows: {}".format(row_count))
#if row_count == 0:
   # print ("It Does Not Exist")
#mycursor.execute("SELECT word FROM testword ")
#myresult = mycursor.fetchall()
#print(myresult)
#x += 1
    
#mycursor.execute(real_sql)
#mydb.commit()
      
  