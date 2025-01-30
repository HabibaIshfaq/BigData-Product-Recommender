from flask import Flask, jsonify  # Import Flask and jsonify
import json  # Use Python's standard JSON module
from bson import json_util
from bson.objectid import ObjectId
from flask_cors import CORS, cross_origin
import db
import pymongo
import pandas as pd

app = Flask(__name__)  # Initialize the Flask app
app.json_encoder = db.MongoJSONEncoder
app.url_map.converters['ObjectId'] = db.ObjectIdConverter
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# Updated connection string for MongoDB Atlas
client = pymongo.MongoClient("mongodb+srv://habiba9:bigdata@recommendation-cluster.qiw8e.mongodb.net/foodon?retryWrites=true&w=majority")
db = client["foodon"]  # Database name: foodon

port = 6050

def fetch(id):
    col = db["orders"]  # Collection name: orders

    objInstance = ObjectId(id)

    docs = col.find_one({"user": objInstance})

    data = []
    data.append(json.dumps(docs, indent=4, default=json_util.default))

    return data

def main():
    @app.route('/')
    def home():
        return "Welcome to the Product Recommendation System API"

    @app.route('/recommend/<string:id>', methods=['POST'])
    def post(id):
        obj = fetch(id)
        docs = json.loads(obj[0])
        prods = []
        for item in docs['orderedItems']:
            for products in item['product']:
                prods.append(products)

        _json = open("names.json", 'w')
        _json.write(json.dumps(prods))
        _json.close()

        with open('names.json', encoding='utf-8') as inputfile:
            df = pd.read_json(inputfile)

        df.to_csv('prods.csv', encoding='utf-8', index=False)

        fileObject = open("./names.json", "r")
        jsonContent = fileObject.read()
        prods_list = json.loads(jsonContent)

        names = [item['name'] for item in prods_list]

        from random import randrange as random

        import recommendation_sys as recommender
        recom = recommender.recommend(names[random(len(names))])
        final_recom = []
        for item in recom:
            for lobj in prods_list:
                if item == lobj['name']:
                    final_recom.append(lobj)

        return jsonify(final_recom)

    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(port=port)

if __name__ == "__main__":
    main()
