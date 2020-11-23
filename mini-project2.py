from pymongo import MongoClient
from datetime import datetime
import random
import sys

"""
The user will be asked to enter a title, a body, and tags (which can be zero tags or more), which will then be
recorded in te database with a unique id

Input: (optional) user ID. If the user is anonymous (has no user ID), then the default argument will be an empty string.

Output: returns a dictionary (known as q_info_dict) with the title, body, and tags as its keys,
where title and body are returned as strings, and the tags are returned as a list of strings
eg. {'title': _____, 'body': ______, 'tag': [__,___,__]}


"""
def q_input(user_id = ''):
	tag_list = [] # will be used to store the tag(s) that the user has typed in

	# will be used to store the title, body, and tags 
	q_info_dict = {'Title': '', 'Body': '', 'Tags':'', 'OwnerUserId': str(user_id)} 

	title = input("Enter a title: ")
	while title.strip() == '': # the user did not enter a title
		title = input("Please enter a title: ")
	q_info_dict['Title'] = title

	body = input("Enter a body: ")
	while body.strip() == '': # the user did not enter a body
		body = input("Please enter a body: ")
	q_info_dict['Body'] = body

	
	ask_tag = input("Would you like to enter a tag? (Enter 'y' for yes or 'n' for no): ").lower()

	while ask_tag not in ('y','n'):
		ask_tag = input("Please enter a valid input (y/n): ")

	while ask_tag == 'y': # while the user would like to enter a tag
		user_tag = input("Enter a tag (one tag at a time): ")

		while user_tag.strip() == '': # if the user enters an empty string
			user_tag = input("Invalid Input. Enter a tag (one tag at a time): ")

		tag_list.append(user_tag)

		ask_tag = input("Would you like to enter another tag? (Enter 'y' for yes or 'n' for no): ").lower()

		if ask_tag == 'n':
			break

	q_info_dict['Tags'] = tag_list # adds the list of tags as a value to the key 'tag'


	# Add tag count if tag already exists, otherwise insert tag and its count as 1
	tag_collection = database['tags_col'] # in actual project, should be called Tags

	for tag in tag_list: # for each tag entered by the user
		tag_results = tag_collection.find_one({"TagName": tag.lower()}) # only one result is expected
		
		if tag_results != None: # the tag name exists
			tag_collection.update_one({"TagName": tag.lower()}, ({"$set": {"Count": tag_results['Count'] + 1}}))
			# increases the tag count by 1
		else:
			pid = check_unique_pid() # generates a unique id for the tag
			tag_collection.insert_one({'Id': pid, 'TagName': tag, 'Count': 1}) # new tag with an initial count of 1


	return q_info_dict

"""
Generates a unique pid. If the pid already exists, then it will generate another one. 

Input: none
Output: unique pid as a string (will be an integer from 1 to 9998 inclusive)

"""
def check_unique_pid():
	is_unique = False # the pid is currently assumed to not be unique
	q_pid = str(random.randint(1,9999))

	# only displays the _id 
	# Example output:
	# {'_id': '469'} \n {'_id': '3663'}
	results = p_collection.find({}, {'Id': q_pid}) 

	while not is_unique:
		for post in results:
			if post['Id'] == q_pid:
				q_pid = str(random.randint(1,9999)) # generates another q_pid 
				break
		is_unique = True

	return q_pid




def post_question():

	q_id = '1' # post type ID is set 1 to show that it is a question

	# returns a dictionary with the title, body, and tag(s) as its keys
	# eg. {'title': 't', 'body': 'b', 'tag': ['123']}
	q_dict = q_input()
	

	# Used to modify the date and time format so that it matches the format shown in the Posts.json file 
	# eg. "CreationDate": "2011-02-22T21:47:22.987"
	date_time = str(datetime.today())[:-3] # takes away the last three digits
	date_time = date_time.replace(' ', 'T') # replaces the space in the middle with 'T'

	question = {'Id': check_unique_pid(), 'PostTypeID': '1', 'CreationDate': date_time, 'Score': 0, 'ViewCount': 0, 
			'AnswerCount': 0, 'CommentCount': 0, 'FavoriteCount': 0, 'ContentLicense': "CC BY-SA 2.5"}

	# modified_tags - used to modify the tag format so that it matches the format shown in the Posts.json file
	# eg. Tags: "<hardware><mac><powerpc><macos>"
	modified_tags = ''
	if len(q_dict['Tags']) > 0: # if the user has entered tag(s)
		for tag in q_dict['Tags']:
			modified_tags += '<' + tag + '>'
		question['Tags'] = modified_tags # a tag field will only exist if one or more tags have been entered 


	# if the OwnerUserId is not an empty string, then it can be inserted. Otherwise,
	# it should not be inserted
	for key,value in q_dict.items():
		if key == 'OwnerUserId' and len(value) > 0: 
			question[key] = value # the OwnerUserId field will only exist if the user is not anonymous

	p_collection.insert_one(question) # inserts the question into the database
	print('Your question has been posted!')

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

"""
The user is asked to enter one or more keywords. 

Input: none
Output: a list containing all the keywords that the user has entered (where each keyword is a string)

"""
def user_keywords():

	keyword_list = [] # stores the keywords that user has typed in

	finished = False # the user has not finished searching keywords

	while not finished:

		user_input = input('Enter a keyword: ')

		while user_input.strip() == '': # If the user enters an empty string as their keyword
			user_input = input('Enter a keyword: ')

		keyword_list.append(user_input.strip()) # assuming if the user adds any random spaces (eg. '   no')

		ask_again = input('Would you like to enter another keyword (y/n): ').lower()

		while ask_again not in ('y','n'): # user has not entered a valid input
			ask_again = input('Invalid input. Please enter a valid input (y/n): ').lower()

		if ask_again == 'n': # the user is done searching for keywords
			finished = True

	return keyword_list

"""
The user selects a question action.

Input: None
Output: None

"""

def question_action():
	action_dict = {'1': 'Question action-Answer', '2':'Question action-List answers'}

	for key,value in action_dict:
		print(key + ': ' + value)

	action_input = input('Which of the following question actions would you like to perform? Type in its number: ')

	while action_input not in list(action_dict.keys()):
		action_input = input('Please enter a valid number input: ')

	if action_input == '1':
		pass
		# Question action-Answer
	else:
		pass
		# Question action-List answers

def search():
	keyword_list = user_keywords()

	q_options = {} # stores the possible options for the user to select from 
	q_num = 1 # will be used to display the results (eg. Question 1, Question 2, etc)
	posts_list = []  # keeps track of the posts and prevents the same posts from being displayed more than once

	for keyword.lower() in keyword_list: # for each keyword entered by the user

		# checks if the keyword exists in either the body, title, or tag (if the length is less than 3)
		if len(keyword) < 3:
			k_posts = posts_col.find({'PostTypeId': '1', '$or': [
								{'Body': {'$regex': keyword, '$options': 'i'}}, # 'i' is an option for case-insensitive
								{'Title': {'$regex': keyword, '$options': 'i'}}, 
								{'Tags':{'$regex': keyword, '$options': 'i'}}
								]})
		else:
			k_posts = posts_col.find({'PostTypeId': '1', 'Terms': {'$in': keyword.split()}}) # used to search the terms array
			# checks if the Terms field contains the keyword 
		

		# for each post, some information about the post is displayed
		for post in k_posts:
			
			if q_num == 201: # displays a maximum of 200 results
				break

			if post['Id'] not in posts_list:
				posts_list.append(post['Id'])
				print('------------------------------')
				print('Question ' + str(q_num) + ': ')
				print('Title: ', post['Title'])
				print('Creation Date: ', post['CreationDate'])
				print('Score: ', post['Score'])
				print('AnswerCount: ', post['AnswerCount'])
				print('------------------------------')

				# added to the possible options for the user to select from 
				# eg. {'1': '123'} means that if the user enters '1', they have selected the question post with a pid of '123'
				q_options[str(q_num)] = post['Id'] 
				q_num +=1

	if len(posts_list) == 0: # no posts have been found
		print('The keyword(s) you have provided did not return any results. Please try using other keywords.')
		return # will return None if no posts were displayed to the user

	# the user chooses from the results displayed above
	user_select = input('Select the question by typing in the number associated with that question: ')

	while user_select not in q_options.keys():	
		user_select = input('Invalid input. Select a question number above: ')	
	
	# the following displays all the fields of the question post selected by the user
	print('\n==================================================================')
	print('POST INFO: \n')
	selected_post = posts_col.find_one({'Id': q_options[user_select]}, {'_id': 0}) # Does not display the '_id' or ObjectId

	# increases the view count of the question post by 1 (before displaying all the fields)
	posts_col.update_one({'Id': q_options[user_select]}, {'$set': {'ViewCount': selected_post['ViewCount'] + 1}})

	for key,value in selected_post.items(): # prints out all the fields of a question post
		print(key + ':', value) 
	print('==================================================================')

	print('\nYou have selected question ' + user_select + '!')
	return q_options[user_select] # returns the question id

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
            post_question()
            mainMenu()
        elif action == '3':
            returnedQuestionId = str(search())
            print("Question Anctions:")
            print("Enter 1 to post an answer to this question")
            print("Enter 2 to list the answers of the question (from there you can place a vote on an answer")
            print("Enter 3 to go back to main menu")
            print("Enter 4 to exit")
            action = input("What action would you like to take?: ") 
            while (True):
                #user chose to post ananswer to this post
                if action == '1':
                    body = input("What would you like the answer to say?: ")
                    create_answer(returnedQuestionId, body)
                    mainMenu()
                elif action == '2':
                    list_answers(returnedQuestionId)
                    mainMenu()
                elif action == '3':
                    mainMenu()
                elif action == '4':
                    #user chose to exit
                    exit()
                else:
                    #users did not make a valid choice, get a new choice
                    action = input("Invalid action please choose a valid action from either '1','2','3','4': ")
        elif action == '4':
            #user chose to exit
            exit()
        else:
            #users did not make a valid choice, get a new choice
            action = input("Invalid action please choose a valid action from either '1','2','3','4': ")

def main():
    #PHASE ONE WE NEED TO DELETE ANY PREVIOUSLY EXISTING COLLECTIONS AND THEN TO CREATE THE COLLECTIONS AND FILL THEM
    #THIS IS DONE BY ESSAYAS, ALSO CONNECTING TO THE CORRECT DP
    mainMenu()

