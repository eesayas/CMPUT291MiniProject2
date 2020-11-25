"""-----------------------------------------------------------------
Asks the user to enter a user id if they wish to do so.

Input: None
Output: a numeric user id (if the user provides a user id), or '' to represent an anonymous user

-----------------------------------------------------------------"""
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


"""-----------------------------------------------------------------
Checks if the user_id already exists in the database

Input:  user id (numeric), 
        votes, posts (the collections)

Output: True if the user id already exists, otherwise False
-----------------------------------------------------------------"""
def checks_for_user_id(user_id, votes, posts):
	user_votes = votes.find({'UserId': user_id})
	user_posts = posts.find({'OwnerUserId': user_id})

    # the user_id exists (has appeared in the database before)
	if user_votes.count(True) > 0 or user_posts.count(True) > 0:
		return True 
	
	return False  


"""-----------------------------------------------------------------
showReport - Show report of user 
Purpose: Show report of user from post, votes collection

Input:  user id (numeric), 
        votes, posts (the collections)
-----------------------------------------------------------------"""
def showReport(user_id, votes, posts):

		user_votes = votes.find({'UserId': user_id})
		vote_count = user_votes.count(True) # counts the number of votes registered to a user
 
		overall  = posts.aggregate([
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

"""-----------------------------------------------------------------
nullReport - Show blank report
Purpose: user_id was provided but no match in db
-----------------------------------------------------------------"""
def nullReport(user_id):
    print("==========================================")
    print("USER REPORT FOR USER #", user_id, '\n')
    print('Question Count:', 0)
    print('Average Questions Score:', 0)
    print('Answer Count:', 0)
    print('Average Answers Score:', 0)
    print('Number of votes registered:', 0)
    print("==========================================")