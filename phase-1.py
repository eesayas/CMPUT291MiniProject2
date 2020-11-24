import json, sys, re, time
from pymongo import MongoClient

def main():
    startTime = time.time()

    # TODO clarify error check on invalid port?

    try:
        port = sys.argv[1]
        client = MongoClient('mongodb://localhost:' + port)
    except IndexError:
        print("You have to provide a port number")
        sys.exit()

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
    # call setTerms() func on map to insert terms on post_data
    posts_data = map(setTerms, posts_data)

    # NOTE: comment out for testing only
    # for r in posts_data:
    #     print(r)
    #     print("\n")

    # insert to collection
    posts.insert_many(posts_data)

    # create index
    posts.create_index("terms")

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

    print("Successfully inserted Posts.json, Tags.json, Votes.json to '291db' Mongo database on port " + port)
    print ('The script took {0} minutes!'.format((time.time() - startTime) / 60 ))

'''
setTerms() - Helper function: Set Terms for a post
Purpose: This will extract terms (via other helper functions) and set it to post

Params: post - a dict
Return: post - updated or not dict
'''
def setTerms(post):
    terms = set([]) #define set

    # try "Title" field
    try:
       terms.update(extractTerms(post["Title"], False))
    except KeyError:
        pass

    # try "Body" field
    try:
       terms.update(extractTerms(post["Body"], False))
    except KeyError:
        pass

    # try "Tag" field
    try:
        terms.update(extractTerms(post["Tags"], True))
    except KeyError:
        pass

    # if len of terms is not 0, set a terms field
    if len(terms):
        post["terms"] = list(terms)
    
    return post

'''
extractTerms() - Helper function: Extract Terms from a string
Purpose: This will parse out html tags, whitespace and punctuations

Params: field - Title or Body or Tag (a string)
        isTag - if field is Tag (a boolean)

Return: list - a list of string terms
'''
def extractTerms(field, isTag):
    # set field string to lower case
    field = field.lower()

    if isTag:
        delimeters = '\<|\>'

        # extract terms by spliting on delimeters
        terms = re.split(delimeters, field)

    else:
        delimeters = ' |\n|\?|\"|\.|\,|\(|\)'

        # parse HTML tags
        field = re.sub('<[^<]*?/?>', ' ', field) 
        
        # extract terms by spliting on delimeters
        terms = re.split(delimeters, field) 

    # if/else end

    # make unique
    terms = list(set(terms))

    # filter out smaller terms
    terms = filter(filterSmallTerms, terms)

    # return terms
    return terms

'''
filterSmallTerms() - Helper function: Filter Out Small Terms
Purpose: Given a term, if its length is less than 3 return False, else True

Params: term - a String

Return: boolean - true or false
'''
def filterSmallTerms(term):
    if len(term) < 3:
        return False
    else:
        return True

# call main
main()




