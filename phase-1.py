import json
from os import execlp
import re
from pymongo import MongoClient

def main():
    # TODO change later for dynamic port argument
    client = MongoClient('mongodb://localhost:27017')

    # Create or open database
    db = client["291db"]

    # List of collections in database
    colsInDB = db.list_collection_names()

    # List of collections in the project
    colsInProj = [ "posts", "tags", "votes" ]

    # for each collection in project
    #   if in colsInDB, then drop collection
    for col in colsInProj:
        if col in colsInDB:
            db[col].drop()

    # create collections, then store access to global variables?
    posts, tags, votes = db["posts"], db["tags"], db["votes"]

    # insert data from Posts.json
    with open("Posts.json") as p:
        posts_data = json.load(p)
        posts_data = posts_data["posts"]["row"] # extract proper data from JSON

    # FOR GROUPS OF 3: Create new field "terms"
    posts_data = map(extractTerms, posts_data)

    # insert to collection
    posts.insert_many(posts_data)

    # from Tags.json
    with open("Tags.json") as t:
        tags_data = json.load(t)
        tags_data = tags_data["tags"]["row"] # extract proper data from JSON

    # insert to colleciton
    tags.insert_many(tags_data)

    # from Votes.json
    with open("Votes.json") as v:
        votes_data = json.load(v)
        votes_data = votes_data["votes"]["row"] # extract proper data from JSON

    # insert to collection
    votes.insert_many(votes_data)

# helper function
def extractTerms(post):
    terms = []
    delimeters = ' |\n|\?|\"|\.|\,|\(|\)'
    clean = re.compile('<.*?>')

    try:
        
        titleTerms = re.sub(clean, ' ', post["Title"])
        titleTerms = re.split(delimeters, titleTerms)
        titleTerms = list(set(filter(filterSmallTerms, titleTerms)))

        terms += titleTerms

    except KeyError:
        pass

    try:
        bodyTerms = re.sub(clean, ' ', post["Body"])
        bodyTerms = re.split(delimeters, bodyTerms)
        bodyTerms = list(set(filter(filterSmallTerms, bodyTerms)))

        terms += bodyTerms

    except KeyError:
        pass

    if len(terms):
        post["terms"] = terms
    
    return post


# helper function: filter length < 3
def filterSmallTerms(term):
    if len(term) < 3:
        return False
    else:
        return True

main()




