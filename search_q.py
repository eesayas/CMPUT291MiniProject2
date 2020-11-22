"""Search for questions. 
The user should be able to provide one or more keywords, and the system should retrieve all posts that 
contain at least one keyword either in title, body, or tag fields (the match should be case-insensitive). 
Questions have a post type id of 1 in Posts. 
For each matching question, display the title, the creation date, the score, and the answer count. 
The user should be able to select a question to see all fields of the question from Posts. 
After a question is selected, the view count of the question should increase by one (in Posts) 
and the user should be able to perform a question action (as discussed next).

THINGS TO WORK ON:
- Maybe have different conditions for searching? (eg. If the term has a length greater than 3, than search terms array, etc)

- Understand what needs to be returned (whether it's the keyword itself or if the keyword is part of a word)
[UPDATE: partial searches are allowed but not required]

"""



from pymongo import MongoClient
import sys

global db_name
client = MongoClient() # will take port number as input (will be changed later)
db_name = client['mp2'] # mp2 is the name of the database for testing (in actual project, will be '291db')

global posts_col
posts_col = db_name['posts_col']  # posts_col is the name of the collection for testing (in actual project, should be Posts)


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
		keyword_list.append(user_input)

		ask_again = input('Would you like to enter another keyword (y/n): ').lower()

		while ask_again not in ('y','n'): # user has not entered a valid input
			ask_again = input('Invalid input. Please enter a valid input (y/n): ').lower()

		if ask_again == 'n': # the user is done searching for keywords
			finished = True

	return keyword_list


"""
Returns the pid of the question post (the unique pid) selected by the user

Input: None
Output: returns the unique question id of the post that the user has selected

"""
def main():
	keyword_list = user_keywords()

	q_options = {} # stores the possible options for the user to select from 
	q_num = 1 # will be used to display the results (eg. Question 1, Question 2, etc)
	posts_list = []  # keeps track of the posts and prevents the same posts from being displayed more than once

	for keyword in keyword_list: # for each keyword entered by the user

		# checks if the keyword exists in either the body, title, or tag (if the length is less than 3)
		if len(keyword) < 3:
			k_posts = posts_col.find({'$or': [
								{'Body': {'$regex': keyword, '$options': 'i'}}, # 'i' is an option for case-insensitive
								{'Title': {'$regex': keyword, '$options': 'i'}}, 
								{'Tags':{'$regex': keyword, '$options': 'i'}}
								]})
		else:
			k_posts = posts_col.find({'Terms': {'$in': keyword.split()}}) # used to search the terms array
			# checks if the Terms field contains the keyword 
		

		# for each post, some information about the post is displayed
		for post in k_posts:
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
	
	# the following displays all the fields of the question post selected by the user
	print('\n==================================================================')
	print('POST INFO: \n')
	selected_post = posts_col.find_one({'Id': q_options[user_select]}, {'_id': 0}) # Does not display the '_id' or ObjectId

	# increases the view count of the question post by 1
	posts_col.update_one({'Id': q_options[user_select]}, {'$set': {'ViewCount': selected_post['ViewCount'] + 1}})

	for key,value in selected_post.items(): # prints out all the fields of a question post
		print(key + ':', value) 
	print('==================================================================')

	print('\nYou have selected question ' + user_select + '!')
	return q_options[user_select] # returns the question id
	

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



question_id = main()



# Sources used:
# https://kb.objectrocket.com/mongo-db/how-to-query-mongodb-documents-with-regex-in-python-362
# https://docs.mongodb.com/manual/reference/operator/query/in/