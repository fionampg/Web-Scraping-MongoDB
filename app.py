# Flask, creating local server to run website

# Import modules
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo 
import scrape_mars
import os

# Create an instance of flask app
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
#app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

# Set route to render index.html template and finds documents from mongo
@app.route("/")
def home():
    mars_info = mongo.db.collection.find_one()

    return render_template("index.html", mars_info = mars_info)

# Route to initialize scrape function
@app.route("/scrape")
def scrape():

    mars_data = scrape_mars.scrape_mars_news()
    mars_data = scrape_mars.scrape_mars_feat_image()
    mars_data = scrape_mars.scrape_mars_facts()
    mars_data = scrape_mars.scrape_mars_weather()
    mars_data = scrape_mars.scrape_mars_hemisphere()

    #update mongdoDB
    mongo.db.collection.update({},mars_data,upsert=True)

    return redirect("/", code= 302)



# End Flask
if __name__ == "__main__":
    app.run(debug=True)



