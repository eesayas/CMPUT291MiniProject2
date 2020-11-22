"""The user should be able to post a question by providing a title text, a body text, and zero or more tags. 
The post should be properly recorded in the database. 
A unique id should be assigned to the post by your system, 
the post type id should be set to 1 (to indicate that the post is a question),
 the post creation date should be set to the current date and the owner user id should be set to the user posting it (if a user id is provided). 
The quantities Score, ViewCount, AnswerCount, CommentCount, and FavoriteCount are all set to zero 
and the content license is set to "CC BY-SA 2.5".

THINGS TO WORK ON:


"""

from pymongo import MongoClient
from datetime import datetime
import random
import sys

global conn
conn = MongoClient() # will take port number as input (will be changed later)

global database
database = conn['mp2'] # mp2 is the name of the database for testing (in actual project, will be '291db')

global p_collection
p_collection = database['posts_col'] # posts_col is the name of the collection (in actual project, should be Posts)


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




def main():

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


main()

# Sources:
# https://stackoverflow.com/questions/11040177/datetime-round-trim-number-of-digits-in-microseconds
# https://www.tutorialspoint.com/python/string_replace.htm

