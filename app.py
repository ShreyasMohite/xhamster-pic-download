from flask import Flask,render_template,request,jsonify,send_file
from flask import after_this_request
import requests
import random
import os
import io
import img2pdf
from bs4 import BeautifulSoup
import time
import re
from os import listdir
import shutil
from pdfrw import PdfReader, PdfWriter, PageMerge
from PyPDF2 import PdfFileReader, PdfFileWriter



app=Flask(__name__)





@app.route("/")
def home():
    return render_template("index.html",title="home")


@app.route("/download",methods=['GET','POST'])
def download(): 
    if request.method=="POST":

        realurl=request.form['search']
        

        rannumber=random.randint(0,11)
        directory=f"mypdf{rannumber}"
        os.mkdir(directory)
        try:

            response=requests.get(realurl)
            Soup=BeautifulSoup(response.text,"html.parser")
            gather=Soup.findAll("div" ,class_="image-thumb")
            urls=[images["data-lazy"] for images in gather]
            for url in urls:
                filename = re.search(r'/([\w_-]+[.](jpg|gif|png))$', url)
                if not filename:
                    statusbar.config(text="Regex didn't match with the url: {0}".format(url))
                    continue
                with open(directory+"/"+filename.group(1), 'wb') as f:
                    if 'http' not in url:
                        url = '{}{}'.format(site, url)
                    response = requests.get(url)                                 
                    f.write(response.content)

        except Exception as e:
            print(e)




        ran=random.randint(1,11111)
        pdfname=f"hello{ran}.pdf"
        
        try:
            with open(pdfname,"wb") as f:
                try:
                    imgs = []
                    for fname in os.listdir(directory):
                        if not fname.endswith(".png"):
                            continue
                        path = os.path.join(directory, fname)
                        if os.path.isdir(path):
                            continue
                        imgs.append(path)
                    f.write(img2pdf.convert(imgs))
                except:
                    print("not jpg or jpeg")


                try:
                    imgs = []
                    for fname in os.listdir(directory):
                        if not fname.endswith(".jpg"):
                            continue
                        path = os.path.join(directory, fname)
                        if os.path.isdir(path):
                            continue
                        imgs.append(path)
                    f.write(img2pdf.convert(imgs))
                except:
                    print("not png or jpeg")


                try:
                    imgs = []
                    for fname in os.listdir(directory):
                        if not fname.endswith(".jpeg"):
                            continue
                        path = os.path.join(directory, fname)
                        if os.path.isdir(path):
                            continue
                        imgs.append(path)
                    f.write(img2pdf.convert(imgs))
                except:
                    print("not png or jpg")
        except Exception as e:
            print(e)


        with open(pdfname,'rb') as file:
            return_data = io.BytesIO(file.read())
        return_data.seek(0)
        shutil.rmtree(directory)
        os.remove(pdfname)
        ran=random.randint(0,111)
        return send_file(return_data,as_attachment=True,mimetype='application/pdf',attachment_filename=f"mypdf{ran}.pdf")





if __name__=="__main__":
    app.run(debug=True,host="192.168.1.204")