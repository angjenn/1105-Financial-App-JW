from flask import Flask, render_template, request

app = Flask(__name__)

#1st
@app.route("/",methods=["GET","POST"])
def index():
    return(render_template("index-1.html"))

#2nd
@app.route("/main",methods=["GET","POST"])
def main():
    r= request.form.get("q")
    return(render_template("main.html", r=r))#get the r value same to the template

#3rd
@app.route("/prediction",methods=["GET","POST"])
def prediction():
    return(render_template("prediction.html"))


#4th
@app.route("/dbs_price",methods=["GET","POST"])
def dbs_price():
    q= float(request.form.get("q"))
    return(render_template("dbs_price.html", r=(q*-50.6)+90.2)) #-50.6 is model_coef,90.2 is the model_intercept.Data in google colab



#if __name__ == "__main__": is a common idiom used in Python scripts to check if the script is being run directly by the Python interpreter or if it's being imported as a module into another script. If the script is being run directly, the code block under this condition will be executed.
#in the case of a Flask application, this check ensures that the Flask development server (app.run()) is only started when the script is executed directly, rather than when it's imported as a module into another script. This is because when the Flask application is imported, you typically don't want the development server to start automatically; you might want to use it in a larger application structure or in production with a different server configuration.
if __name__ =="__main__":
    app.run()
