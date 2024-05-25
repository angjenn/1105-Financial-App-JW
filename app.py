from flask import Flask, render_template, request
import google.generativeai as palm
import replicate
import os
import sqlite3
import datetime
import pytz #to add timezone
from flask import Markup #so that can pull the log

flag = 1  #flag variable - Most frequently, a flag is employed as a while loop condition. 
name = ""
makersuite_api=os.getenv("MAKERSUITE_API_TOKEN")
palm.configure(api_key=makersuite_api)
#"AIzaSyDwj5p73l7diKdHC2cLTbv5Haz5KYo4skc"(MAKERSUITE API)
#os.environ["REPLICATE_API_TOKEN"]= "r8_SfyswKHfVsBlq22fXaAiNDatDYiAWTk2l4JaN"

model =  {"model" : "models/chat-bison-001"}
app = Flask(__name__)

#1st
@app.route("/",methods=["GET","POST"])
def index():
    return(render_template("index-1.html"))

#2nd
@app.route("/main",methods=["GET","POST"])
def main():
    global flag , name #need global
    if flag ==1: #flag variable is to let the the main pull the name once. The loop would continue while the flag’s value was True and end if it became False.
        name = request.form.get("q")
        time_zone= pytz.timezone("Singapore")
        current_time = datetime.datetime.now(time_zone)
        conn = sqlite3.connect("log.db")
        c = conn.cursor()
        c.execute("insert into user (name,time) values (?,?)", (name,current_time))
        conn.commit()
        c.close()
        conn.close()
        flag = 0
    return(render_template("main.html", r=name))#get the r value same to the template

#3rd
@app.route("/prediction",methods=["GET","POST"])
def prediction():
    return(render_template("prediction.html"))


#4th
@app.route("/dbs_price",methods=["GET","POST"])
def dbs_price():
    q= float(request.form.get("q"))
    return(render_template("dbs_price.html", r=(q*-50.6)+90.2)) #-50.6 is model_coef,90.2 is the model_intercept.Data in google colab

#adding chatbot(18 may)
@app.route("/generate_text",methods=["GET","POST"])#question
def generate_text():
    return(render_template("generate_text.html"))


@app.route("/text_result_makersuite",methods=["GET","POST"])#reply
def text_result_makersuite():
    q= request.form.get("q")
    r = palm.chat(**model, messages=q)
    return(render_template("text_result_makersuite.html", r=r.last))

#adding image chatbot(18 may)
@app.route("/generate_image",methods=["GET","POST"])#question
def generate_image():
    return(render_template("generate_image.html"))


@app.route("/image_result",methods=["GET","POST"])#reply
def image_result():
    q= request.form.get("q")
    r = replicate.run("stability-ai/stable-diffusion:db21e45d3f7023abc2a46ee38a23973f6dce16bb082a930b0c49861f96d1e5bf",
                  input = {"prompt":q})
    return(render_template("image_result.html", r=r[0]))


@app.route("/log",methods=["GET","POST"])#log.db
def log():
    conn = sqlite3.connect("log.db")
    c = conn.cursor()
    c.execute("select * from user")
    r = ""
    for row in c:
      r += str(row) + "<br>" #need change from "/n" to <br>
    print(r)
    r = Markup(r)
    c.close()
    conn.close()
    return(render_template("log.html", r=r))

@app.route("/delete",methods=["GET","POST"])#delete log records
def delete():
    conn = sqlite3.connect("log.db")
    c = conn.cursor()
    c.execute("delete from user")
    conn.commit()
    c.close()
    conn.close()
    return(render_template("delete.html"))



#need to end to terminate the loop
@app.route("/end",methods=["GET","POST"]) 
def end():
    global flag
    flag = 1
    return(render_template("index-1.html"))


#if __name__ == "__main__": is a common idiom used in Python scripts to check if the script is being run directly by the Python interpreter or if it's being imported as a module into another script. If the script is being run directly, the code block under this condition will be executed.
#in the case of a Flask application, this check ensures that the Flask development server (app.run()) is only started when the script is executed directly, rather than when it's imported as a module into another script. This is because when the Flask application is imported, you typically don't want the development server to start automatically; you might want to use it in a larger application structure or in production with a different server configuration.

if __name__ =="__main__":
    app.run()
