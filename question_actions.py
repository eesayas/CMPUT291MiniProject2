from post_question import generateRandomId
from datetime import datetime

"""-----------------------------------------------------------------
create_answer - Creates an answer
Purpose: Based upon the body provided it creates an answer in the 
posts collection
Input: questionId : The id of the question on which we are posting the answer
body : the body we would like to use for the answer
user : current user or "" to denote anonymous user
posts : our collection of posts
Output: None
-----------------------------------------------------------------"""
def create_answer(questionId, body, user, posts):
    # Used to modify the date and time format so that it matches the format shown in the Posts.json file 
    # eg. "CreationDate": "2011-02-22T21:47:22.987"
    date_time = str(datetime.today())[:-3] # takes away the last three digits
    date_time = date_time.replace(' ', 'T') # replaces the space in the middle with 'T'
    theId = generateRandomId(posts) #get a unique Id for our answer
    #fill in all the fields as per the assignment specifications
    answer = {
        "Id": theId,
        "PostTypeId": "2",
        "ParentId": questionId,
        "CreationDate": date_time,
        "Score": 0,
        "Body": body,
        "CommentCount": 0,
        "ContentLicense":"CC BY-SA 2.5"
    }

    # insert following fields iff user is provided
    if user != "":
        answer["OwnerUserId"] = user

    #insert our answer to the posts collection
    posts.insert_one(answer)

    print('Your answer has been posted!')


"""-----------------------------------------------------------------
list_answers - List the answers for a question
Purpose: Based upon the question provided by the user list the answers
to this question, if the question has an accepted answer this will be
listed first
posts collection
Input: questionId : The id of the question on which we are listing the answers
posts: the posts collection
Output: an array with two elements
1. the array of all the id's of the answers for our question(in the same
order and with the same indexes as these answers were presented to the user)
2. The length of said list
-----------------------------------------------------------------"""
def list_answers(questionId,posts):
    #used to track if the question has an accepted answer
    acceptedAnswerBool = False
    #get the question from our posts collection
    results = posts.find({"Id": questionId})
    #Id of accepted answer "" to represent no accepted answer
    acceptedAnswerID = ""
    for result in results:
        #try to access assepted answer (will only work if with post has an accepted answer field)
        try:
            acceptedAnswerID = result["AcceptedAnswerId"]
            acceptedAnswerBool = True
        except:
            #post does not have an accepted answer
            acceptedAnswerID = ""
            acceptedAnswerBool = False
    #index if very important, used to maintain some connection between the answers we show to the user
    #and the answers in our answers array
    index = 0
    answers=[0]*10000
    if (acceptedAnswerBool == True):
        #make sure if there is an accepted answer that it appears first
        answers[index] = acceptedAnswerID
        results = posts.find({"Id": acceptedAnswerID})
        for result in results:
            score = result["Score"]
            creationDate = result["CreationDate"]
            body = result["Body"]
        first80Chars = body[0:79]
        #https://thispointer.com/python-how-to-get-first-n-characters-in-a-string/
        #display the fields of our answer as per the assignment specs
        print("* Index "+ str(index) + ":\nBody: "+first80Chars + "\nCreation Date: "+str(creationDate)+"\nScore: "+str(score))
        index = index + 1
    #now that accepted answer is dealt with present the rest of this question's answers to the user and fill the answers array with the same ordering
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
    return [answers,index]