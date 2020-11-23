"""The user should be able to answer the question by providing a text. 
An answer record should be inserted into the database, with body field set to the provided text. 
A unique id should be assigned to the post by your system, the post type id should be set to 2 
(to indicate that the post is an answer), the post creation date should be set to the current date 
and the owner user id should be set to the user posting it (if a user id is provided). 
The parent id should be set to the id of the question. The quantities Score and CommentCount are all 
set to zero and the content license is set to "CC BY-SA 2.5".
"""

from pymongo import MongoClient
from datetime import datetime
import random
import sys

global user
user = "302097"


global client
client = MongoClient('mongodb://localhost:'+ sys.argv[1]) # will take port number as input (will be changed later)

global database
database = client['291dbbb'] 


# List collection names.
collist = database.list_collection_names()
if "posts" in collist:
    print("The collection exists.")

# Create or open the collection in the db
global posts
posts = database['posts']

global votes
votes = database['votes']

# delete all previous entries in the movies_collection
# specify no condition.
posts.delete_many({})
votes.delete_many({})






"""
The user will be asked to enter a title, a body, and tags (which can be zero tags or more), which will then be
recorded in te database with a unique id
Input: (optional) user ID. If the user is anonymous (has no user ID), then the default argument will be an empty string.
Output: returns a dictionary (known as q_info_dict) with the title, body, and tags as its keys,
where title and body are returned as strings, and the tags are returned as a list of strings
eg. {'title': _____, 'body': ______, 'tag': [__,___,__]}
"""
def create_answer(questionId, body):
    # Used to modify the date and time format so that it matches the format shown in the Posts.json file 
    # eg. "CreationDate": "2011-02-22T21:47:22.987"
    date_time = str(datetime.today())[:-3] # takes away the last three digits
    date_time = date_time.replace(' ', 'T') # replaces the space in the middle with 'T'
    theId = generateRandomId()
    answer = [
        {"Id": theId,
        "PostTypeId": "2",
        "ParentId": questionId,
        "CreationDate": date_time,
        "Score": 0,"Body": body,
        "OwnerUserId": user,
        "LastEditorUserId": user,
        "LastEditDate": date_time,
        "LastActivityDate": date_time,
        "CommentCount": 0,
        "ContentLicense":"CC BY-SA 2.5"}]
    ret = posts.insert_many(answer)
    # Print list of the _id values of the inserted documents
    #movie_ids = ret.inserted_ids
    #print(movie_ids)

    results = posts.find({"Body": body})
    for mem in results:
        if mem["Body"] == body:
            print(mem["Id"])
    return theId


def generateRandomId():
    length = 100
    counter = 0
    while (True):
        unique = True
        randomId = str(random.randint(length/10,length))
        #print(randomId)
        results = posts.find({"Id": randomId})
        for result in results:
            if result["Id"] == randomId:
                unique = False
        if (unique == False):
            counter = counter + 1
            if counter >= (length / 10):
                counter = 0
                length = length *10
        else:
            break
    return randomId

def list_answers(questionId):
    acceptedAnswerBool = False
    results = posts.find({"Id": questionId})
    acceptedAnswerID = ""
    for result in results:
        try:
            acceptedAnswerID = result["AcceptedAnswerId"]
            acceptedAnswerBool = True
        except:
            acceptedAnswerID = ""
            acceptedAnswerBool = False
    index = 0
    answers=[0]*10000
    if (acceptedAnswerBool == True):
        answers[index] = acceptedAnswerID
        results = posts.find({"Id": acceptedAnswerID})
        for result in results:
            score = result["Score"]
            creationDate = result["CreationDate"]
            body = result["Body"]
        first80Chars = body[0:79]
        #https://thispointer.com/python-how-to-get-first-n-characters-in-a-string/
        print("* Index "+ str(index) + ":\nBody: "+first80Chars + "\nCreation Date: "+str(creationDate)+"\nScore: "+str(score))
        index = index + 1
    results = posts.find({"ParentId": questionId})
    for result in results:
        if result["Id"] != acceptedAnswerID:
            answers[index] = result["Id"]
            try: 
                score = result["Score"]
            except:
                score = "No Score"
            try: 
                creationDate = result["CreationDate"]
            except:
                creationDate = "No creation date"
            try: 
                body = result["Body"]
            except:
                body = "No body"
            first80Chars = body[0:79]
            print("Index "+ str(index) + ":\nBody: "+first80Chars + "\nCreation Date: "+str(creationDate)+"\nScore: "+str(score))
            index = index +1
    
    #choice = input("Select the index number of the answer you would like to select or enter 'exit' to exit or 'menu' to go back to main menu: ")
    while (True):
        choice = input("Select the index number of the answer you would like to select or enter 'exit' to exit or 'menu' to go back to main menu: ")
        if (choice.lower() == "exit"):
            exit()
        elif (choice.lower() == "menu"):
            mainMenu()
        else:
            try:
                if (int(choice)>=index):
                    print("Not a valid choice")
                else:
                    break
            except:
                print("Not a valid choice")
    chosenId = answers[int(choice)]
    results = posts.find({"Id": str(chosenId)})
    for result in results:
        try: 
            postTypeId = result["PostTypeId"]
        except:
            postTypeId = "No postTypeId"
        try: 
            parentId = result["ParentId"]
        except:
            parentId = "No parentId"
        try: 
            creationDate = result["CreationDate"]
        except:
            creationDate = "No CreationDate"
        try: 
            score = result["Score"]
        except:
            score = "No Score"
        try: 
            body = result["Body"]
        except:
            body = "No Body"
        try: 
            ownerUserId = result["OwnerUserId"]
        except:
            ownerUserId = "No OwnerUserId"
        try: 
            lastActivityDate = result["LastActivityDate"]
        except:
            lastActivityDate = "No LastActivityDate"
        try: 
            commentCount = result["CommentCount"]
        except:
            commentCount = "No CommentCount"
        try: 
           contentLicense = result["ContentLicense"]
        except:
            contentLicense = "No ContentLicense"
        print("Id: " +str(result["Id"]) +"\nPostTypeId: "+str(postTypeId) + "\nParent Id: "+str(parentId)+"\nCreationDate: "+str(creationDate)+"\nScore: "+str(score)+"\nBody: "+str(body)+"\nOwnerUserId: "+str(ownerUserId)+"\nLastActivityDate: "+str(lastActivityDate)+"\nCommentCount: "+str(commentCount)+"\nContentLicense: "+str(contentLicense)+"\nScore: "+str(score))
        while(True):
            voteChoice = input("Would you like to vote on this post? Enter either 'yes', 'no', 'exit' or 'menu': ")
            if (voteChoice.lower() == "yes"):
                vote(str(chosenId))
                mainMenu()
            elif (voteChoice.lower() == "no"):
                mainMenu()
            elif (voteChoice.lower() == "menu"):
                mainMenu()
            elif (voteChoice.lower() == "exit"):
                exit()
            else:
                print("Not a valid choice") 
            
    #results = posts.find({$and: [{"Id": questionId},{"AcceptedAnswerId": questionId}, ])
    #({ $and: [ {<key1>:<value1>}, { <key2>:<value2>} ] })

    return

def vote(postId):
    postScore = 0
    postExists = False
    results = posts.find({"Id": postId})
    for result in results:
        postExists = True
        postScore = result["Score"]
    if (postExists==False):
        print("Post does not exist")
        return
    anonymous = False
    if (user == ""):
        anonymous = True
    #using the $ in python from https://www.w3schools.com/python/python_mongodb_update.asp
    results = votes.find({ "$and": [ {"PostId":postId}, { "UserId":user} ] })
    for result in results:
        print("You have already voted on this post. Vote rejected")
        return
    results = results = posts.find({"Id": postId})
    postType = ""
    for result in results:
        if result["PostTypeId"] == "2":
            postType = "answer"
        else:
            postType = "question"
    voteId = generateRandomId()
    # eg. "CreationDate": "2011-02-22T21:47:22.987"
    date_time = str(datetime.today())[:-3] # takes away the last three digits
    date_time = date_time.replace(' ', 'T') # replaces the space in the middle with 'T'
    if anonymous == False:
        vote = [
            {"Id": str(voteId),
            "PostId": str(postId),
            "VoteTypeId": "2",
            "UserId": str(user),
            "CreationDate":date_time}]
        votes.insert_many(vote)
    else:
        vote = [
            {"Id": str(voteId),
            "PostId": str(postId),
            "VoteTypeId": "2",
            "CreationDate":date_time}]
        votes.insert_many(vote)
    newPostScore = int(postScore)+1
    posts.update({"Id":postId},{"$set":{"Score": str(newPostScore)}})
    print("Vote added! Post "+ postId + " has also had its Score increased")
    return

def exit():
    global user
    user = ""
    # this will print when exit() is called
    print("\nGoodbye!\n")

    # standard python exit
    sys.exit()

def mainMenu():
    print("Main menu:")
    print("Enter 1 to provide a user id to use")
    print("Enter 2 to post a question")
    print("Enter 3 to search for a question")
    print("Enter 4 to exit")
    action = input("What action would you like to take?: ") 
    #loops untill a valid choice is made
    while (True):
        #user chose to post ananswer to this post
        if action == '1':
            return
            #ELENA TO DO
        elif action == '2':
            return
            #ELENA TO DO
        elif action == '3':
            return
            #ELENA TO DO
        elif action == '4':
            #user chose to exit
            exit()
        else:
            #users did not make a valid choice, get a new choice
            action = input("Invalid action please choose a valid action from either '1','2','3','4': ")







    
    

mainMenu()
answr = create_answer("352055", "NICEEEEEEe")
answer = [
    {"Id": "352055",
    "PostTypeId": "1",
    "AcceptedAnswerId": str(answr)},
    {"Id": "352057",
    "PostTypeId": "2",
    "ParentId": "352055"}]
ret = posts.insert_many(answer)
list_answers("352055")
vote(str(answr))
