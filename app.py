from flask import Flask, render_template, redirect, url_for

from flask_pymongo import PyMongo

import scraping

#set up flask
app =Flask(__name__)

#tell python how to connect to mongo db

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

@app.route("/")

def index():
    
    mars = mongo.db.mars.find_one()
    
    return render_template("index.html", mars=mars)


@app.route("/scrape")
def scrape():

    #assign a new variable that points to our Mongo database
   mars = mongo.db.mars

   #created a new variable to hold the newly scraped data
   mars_data = scraping.scrape_all()

  #Here, we're inserting data, but not if an identical record already exists.
  # # In the query_parameter, we can specify a field (e.g. {"news_title": "Mars Landing Successful"}), in which case MongoDB will update a document with a matching news_title
   mars.update_one({}, {"$set":mars_data}, upsert=True)
   return redirect('/', code=302)

if __name__ == "__main__":
    app.run()

