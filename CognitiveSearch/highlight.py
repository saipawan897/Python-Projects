import mysql.connector
#USE python_mysql;
from pprint import pprint
import os
import urllib.request
from app import app
from flask import Flask, flash, request, redirect, render_template,session
from werkzeug.utils import secure_filename
import pytesseract
from pytesseract import Output
import fitz
import cv2 
pytesseract.pytesseract.tesseract_cmd ="C:\\Users\\saipa\\AppData\\Local\\Tesseract-OCR\\tesseract.exe"
#session.clear()


mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="saipawan897",
  database = "mydatabase"
)

mycursor = mydb.cursor()


     
def highlight(keyword):
    #keyword = list(keyword.split(" "))

    directory = r'C:/Users/saipa/Desktop/project/static/'
    for filename in os.listdir(directory):
        if filename.endswith('.png'):
            print(filename)
            os.remove(os.path.join(directory,filename))  
    arun = "Not"
    keyword = str(keyword)
    keyword = (list(keyword.split(" ")))
    
    for k in keyword :
    #print(k)
        word = str(k)
        print(word)
    #word = str(keyword)
        for w in word:
            args = mycursor.callproc('find_word', (word, '@filename','@imagepath', '@coordinates') )
        
        for result in mycursor.stored_results():
            myresults = result.fetchall()
            lists = list(myresults)
            print(lists)
            num = 0
            fname1 = 'abdn'
            output_folder_img2 = 'abv'
            d = r'C:/Users/saipa/Desktop/project/Data/'
    
        for are in lists:
                    p_word = word
                    p_filename = are[0]   
                    p_imagepath = are[1]
                    path = p_imagepath 
                    head_tail = os.path.split(path) 
                    fname =  head_tail[1]
             
                    p_coordinates = are[2]
                    p_coordinates = p_coordinates[1:-1]
                    list2 = p_coordinates.split(",")
                    x = int(list2[0])
                    y = int(list2[1])
                    w = int(list2[2])
                    h = int(list2[3])        
                    s = (x, y, w, h)
                    alpha = 0.4
                    
                    
                    path3 = path 
                    head_tail = os.path.split(path3) 
                    fname3 =  head_tail[1]
                    print(fname1)
                    print(fname3)
                    if fname3 == fname1:
                       print("same")
                       img = cv2.imread(output_folder_img2)
                    else:
                       img = cv2.imread(path)                    
                    print(s)
                    (b1,b2,b3,b4) = s
                    cv2.rectangle(img, (b1, b2), (b1 + b3, b2 + b4), (255, 0, 0), 2)
                    output_name = str(fname)
                    output_folder = r'C:/Users/saipa/Desktop/project/static/'
                    output_folder_img2 = str(output_folder) + str(output_name)
                    path1 = output_folder_img2 
                    head_tail = os.path.split(path1) 
                    fname1 =  head_tail[1]
                    print(fname1)
                    cv2.imwrite(output_folder_img2, img)


                            
@app.route('/')
def upload_form():
    return render_template('upload.html')
@app.route('/upload.html', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        keyword = request.form['text']
        highlight(keyword)
       
        hists = os.listdir(r'C:/Users/saipa/Desktop/project/static/')
        hists = [file for file in hists]
        print (hists)
        return render_template('upload.html', hists = hists)
        
            
if __name__ == "__main__":
   app.run(port = 5050 )







