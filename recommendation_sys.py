

#import libraries
import json
import numpy as np
import pandas as pd

from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer


# store the data
df = pd.read_csv('product-recommendation-system/prods.csv')


def recommend(name):

    df['product_id'] = range(0, len(df))
    # show the first 2 rows in csv
    df.head(2)

    df.shape  # gets the count of rows and cols in the dateset

    # list of important items
    columns = ['name', 'desc', 'price', 'qty']

    # show the columns
    df[columns].head(3)

    # check for null values in the data provided
    df[columns].isnull().values.any()

    # function to combine values of important columns into a single string

    def get_important_features(data):
        important_features = []
        for i in range(0, data.shape[0]):
            important_features.append(
                data['name'][i]+' '+data['desc'][i]+' '+str(data['price'][i])+' '+str(data['qty'][i]))

        return important_features

    df['important_features'] = get_important_features(df)

    df.head(3)

    # convert the text to a matrixof token counts
    cm = CountVectorizer().fit_transform(df['important_features'])

    # get the consine similarity matrix from the count matrix
    cs = cosine_similarity(cm)
    # print(cs)

    # get the shape of the consine similarity matrix
    cs.shape

    pname = name

    # get the id of the product
    product_id = ""
    try:
        product_id = df[df.name == pname]['product_id'].values[0]
    except:
        product_id = None

    # print(product_id)

    # create a list of enumerations for the similarity score
    if product_id != None:
        score = list(enumerate(cs[product_id]))
        # scroe looks like: [(product_id, score), (1, 0.0625)
        # print(score)

        # sort the score list
        sorted_score = sorted(score, key=lambda x: x[1], reverse=True)
        sorted_score = sorted_score[1:]

        # print(sorted_score)

    # print the recommended products that are similar to what the user purchases
    j = 0
    print(f"The top 3 food recommended to {pname} are: \n")
    prods = []

    for item in sorted_score:
        product_title = df[df.product_id == item[0]]['name'].values[0]
        prods.append(product_title)
        print(j+1, product_title)
        j += 1
        if j > 3:
            break
    return prods
