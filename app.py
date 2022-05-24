from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# use flask pymongo to set up the connection to the database
app.config ["MONGO_URI"] = "mongodb://localhost:27017/mars_data_db"
mongo = PyMongo(app)

@app.route("/")
def index():
    mars_data = mongo.db.MarsData.find_one()
    return "You reached the index"

@app.route("/scrape")
def scrape():
    # reference to a database collection (table)
    marsTable = mongo.db.marsData

    # drop table if it already exists
    mongo.db.marsData.drop()

    mars_data = scrape_mars.scrape_all()
    
    # load the dictionary and load into MongoDB
    marsTable.insert_one(mars_data)

    # go back to the index route
    return redirect("/")

if __name__ == "__main__":
    app.run()
