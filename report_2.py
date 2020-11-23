"""
Write a program that supports the following operations on the MongoDB database created in Phase 1. 
Your program will take as input a port number under which the MongoDB server is running, and will connect to a database named 291db on the server. 
Your program should allow the users of the system to provide a user id (if they wish), which is a numeric field, formatted as shown in the sample json files. 
If a user id is provided, the user will be shown a report that includes 
(1) the number of questions owned and the average score for those questions, 
(2) the number of answers owned and the average score for those answers, 
and (3) the number of votes registered for the user. 
Users may also use the system without providing a user id, in which case no report is displayed.
"""

from pymongo import MongoClient


# # Used to get rid of DeprecationWarning: count is deprecated. Use Collection.count_documents instead.
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) 

global conn
conn = MongoClient()

global database
database = conn['mp2'] # mp2 is the name of the database (in actual project, will be '291db')

global p_collection
p_collection = database['Posts'] # posts_col is the name of the collection (in actual project, should be Posts)

global v_collection
v_collection = database['Votes']

"""
Asks the user to enter a user id if they wish to do so.

Input: None
Output: a numeric user id (if the user provides a user id), or '' to represent an anonymous user

"""
def ask_for_user_id():
	ask_id = input("Would you like to provide a user id? (Enter 'y' for yes or 'n' for no): ").lower()

	while ask_id not in ('y','n'):
		ask_id = input('Please enter a valid input (y/n): ')

	if ask_id == 'y':
		user_id = input('Please provide a numeric user id: ')

		while not user_id.isnumeric(): # while the user id is not fully numeric (eg. 'u001' is not acceptable)
			user_id = input('Please provide a numeric user id (all numbers): ')

		print('You have provided a user id!')
		return user_id
	else:
		print('You have decided not to provide a user id.')
		return ''


"""
Checks if the user_id already exists in the database

Input: user id (numeric)
Output: True if the user id already exists, otherwise False

"""
def checks_for_user_id(user_id):
	votes = v_collection.find({'UserId': user_id})
	posts = p_collection.find({'OwnerUserId': user_id})

	if votes.count(True) > 0 or posts.count(True) > 0:
		return True # the user_id exists (has appeared in the database before)
	
	return False  

def main():
	user_id = ask_for_user_id()
	confirm_user = checks_for_user_id(user_id)

	if confirm_user: # if a user id has been provided and the user id already exists 
		user_votes = v_collection.find({'UserId': user_id})
		vote_count = user_votes.count(True) # counts the number of votes registered to a user
 
		overall  = p_collection.aggregate([
		{'$match': {'OwnerUserId': user_id}},
		{'$group': {'_id': {'PostTypeId': '$PostTypeId'}, 
				'Count': {'$sum': 1},
				'AverageScore': {'$avg': '$Score'}}}
				]
			)

		# example format that is displayed in overall:
		# {'_id': {'PostTypeId': '1'}, 'Count': 2, 'AverageScore': 3.0}
		# some dictionaries may not be present (eg. if a user owns zero questions)

		print("==========================================")
		print("USER REPORT FOR USER #", user_id, '\n')

		question_answer = ['Question Count', 'Average Questions Score', 'Answer Count', 'Average Answers Score']
		keep_track = [] # keeps track of the information that has already been displayed
		for line in overall:
			# If there is at least one question present
			if line['_id'] == {'PostTypeId': '1'}:
				print('Question Count:',line['Count'])
				keep_track.append('Question Count')
				print('Average Questions Score:', line['AverageScore'])
				keep_track.append('Average Questions Score')

			# If there is at least one answer present
			if line['_id'] == {'PostTypeId': '2'}:
				print('Answer Count:',(line['Count']))
				keep_track.append('Answer Count')
				print('Average Answers Score:', line['AverageScore'])
				keep_track.append('Average Answers Score')

		# Compares the two lists: question_answer and keep_track
		# If there is an element in question_answer that has not been displayed yet, then it will be printed as zero
		for info in question_answer:
			if info not in keep_track:
				print(info + ':', 0)
		

		print('Number of votes registered:', vote_count)
		print("==========================================")

	# if a user id has been provided but the user did not exist before
	elif user_id != '' and not confirm_user: 
		print("==========================================")
		print("USER REPORT FOR USER #", user_id, '\n')
		print('Question Count:', 0)
		print('Average Questions Score:', 0)
		print('Answer Count:', 0)
		print('Average Answers Score:', 0)
		print('Number of votes registered:', 0)
		print("==========================================")

	else: # If the user chooses not to provide a user id
		return


main()


# Sources used:
# https://docs.mongodb.com/manual/aggregation/#aggregation-pipeline
# https://stackoverflow.com/questions/879173/how-to-ignore-deprecation-warnings-in-python