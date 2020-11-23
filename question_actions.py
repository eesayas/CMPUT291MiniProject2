from post_question import generateRandomId
from datetime import datetime

"""-----------------------------------------------------------------
The user will be asked to enter a title, a body, and tags (which can be zero tags or more), which will then be
recorded in te database with a unique id
Input: (optional) user ID. If the user is anonymous (has no user ID), then the default argument will be an empty string.
Output: returns a dictionary (known as q_info_dict) with the title, body, and tags as its keys,
where title and body are returned as strings, and the tags are returned as a list of strings
eg. {'title': _____, 'body': ______, 'tag': [__,___,__]}
-----------------------------------------------------------------"""
def create_answer(questionId, body, user, posts):
    # Used to modify the date and time format so that it matches the format shown in the Posts.json file 
    # eg. "CreationDate": "2011-02-22T21:47:22.987"
    date_time = str(datetime.today())[:-3] # takes away the last three digits
    date_time = date_time.replace(' ', 'T') # replaces the space in the middle with 'T'
    theId = generateRandomId(posts)
    answer = {
        "Id": theId,
        "PostTypeId": "2",
        "ParentId": questionId,
        "CreationDate": date_time,
        "Score": 0,"Body": body,
        "LastEditDate": date_time,
        "LastActivityDate": date_time,
        "CommentCount": 0,
        "ContentLicense":"CC BY-SA 2.5"
    }

    # insert following fields iff user is provided
    if user:
        answer["OwnerUserId"] = user
        answer["LastEditorUserId"] = user


    posts.insert_one(answer)
    # Print list of the _id values of the inserted documents
    #movie_ids = ret.inserted_ids
    #print(movie_ids)

    # results = posts.find({"Body": body})
    # for mem in results:
    #     if mem["Body"] == body:
    #         print(mem["Id"])

    print('Your answer has been posted!')


"""-----------------------------------------------------------------
Purpose: Lists answers
-----------------------------------------------------------------"""
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