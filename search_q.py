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

"""
def main():
	keyword_list = user_keywords()

	q_options = {} # stores the possible options for the user to select from 
	q_num = 1 # will be used to display the results (eg. Question 1, Question 2, etc)

	for keyword in keyword_list: # for each keyword entered by the user

		# checks if the keyword exists in either the body, title, or tag
		k_posts = posts_col.find({'$or': [
								{'Terms': {'$in': list(keyword)}}, # used to search the terms array
								{'Body': {'$regex': keyword, '$options': 'i'}}, # 'i' is an option for case-insensitive
								{'Title': {'$regex': keyword, '$options': 'i'}}, 
								{'Tags':{'$regex': keyword, '$options': 'i'}}
								]})
		

		# for each post, some information about the post is displayed
		for post in k_posts:
			print('------------------------------')
			print('Question ' + str(q_num) + ': ')
			print('Title: ', post['Title'])
			print('Creation Date: ', post['CreationDate'])
			print('Score: ', post['Score'])
			print('AnswerCount: ', post['AnswerCount'])
			print('------------------------------')

			# added to the possible options for the user to select from 
			# eg. {'1': 123} means that if the user enters '1', they have selected the question post with a pid of 123
			q_options[str(q_num)] = post['Id'] 

			q_num +=1

	# the user chooses from the results displayed above
	user_select = input('Select the question by typing in the number associated with that question: ')		
	
	# the following displays all the fields of the question post selected by the user
	print('\n==================================================================')
	print('\nPOST INFO: \n')
	selected_post = posts_col.find_one({'Id': q_options[user_select]}, {'_id': 0}) # Does not display the '_id' or ObjectId
	for key,value in selected_post.items():
		print(key + ':', value)
	print('==================================================================')

	return q_options[user_select]


main()

# Sources used:
# https://kb.objectrocket.com/mongo-db/how-to-query-mongodb-documents-with-regex-in-python-362
# https://docs.mongodb.com/manual/reference/operator/query/in/