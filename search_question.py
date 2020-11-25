"""-----------------------------------------------------------------
The user is asked to enter one or more keywords. 

Input: none
Output: a list containing all the keywords that the user has entered (where each keyword is a string)

-----------------------------------------------------------------"""
def user_keywords():

    keyword_list = [] # stores the keywords that user has typed in (keywords will all be lowercase)

    finished = False # the user has not finished searching keywords

    while not finished:

        user_input = input('Enter a keyword: ').lower()

        while user_input.strip() == '': # If the user enters an empty string as their keyword
            user_input = input('Enter a keyword: ').lower()
        
        if user_input in keyword_list: 
            print("You have already entered that keyword.")
        else: # if the user has not entered the keyword yet
            keyword_list.append(user_input.strip()) # assuming if the user adds any random spaces (eg. '   no')

        ask_again = input('Would you like to enter another keyword (y/n): ').lower()

        while ask_again not in ('y','n'): # user has not entered a valid input
            ask_again = input('Invalid input. Please enter a valid input (y/n): ').lower()

        if ask_again == 'n': # the user is done searching for keywords
            finished = True

    return keyword_list

"""-----------------------------------------------------------------
Returns the pid of the question post (the unique pid) selected by the user

Input: None
Output: returns the unique question id of the post that the user has selected

-----------------------------------------------------------------"""
def searchQuestions(posts):
    keyword_list = user_keywords()

    q_options = {} # stores the possible options for the user to select from 
    q_num = 1 # will be used to display the results (eg. Question 1, Question 2, etc)
    posts_list = []  # keeps track of the posts and prevents the same posts from being displayed more than once
    limit_num = 5
    post_count = 0
    selected = False
    while not selected: 
        for keyword in keyword_list: # for each keyword entered by the user

            # checks if the keyword exists in either the body, title, or tag (if the length is less than 3)
            if len(keyword) < 3:
                k_posts = posts.find({'PostTypeId': '1', '$or': [
                                {'Body': {'$regex': keyword, '$options': 'i'}}, # 'i' is an option for case-insensitive
                                {'Title': {'$regex': keyword, '$options': 'i'}}, 
                                {'Tags':{'$regex': keyword, '$options': 'i'}}
                                ]}).limit(limit_num)
            else:
                k_posts = posts.find({'PostTypeId': '1', 'terms': {'$in': keyword.split()}}).limit(limit_num)
                # used to search the terms array
                # checks if the Terms field contains the keyword 
        

            # for each post, some information about the post is displayed
            for post in k_posts:

                if post['Id'] not in posts_list:
                    posts_list.append(post['Id'])
                    post_count +=1
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
        user_select = input("Select the question by typing in the number, or type in 's' to see more: ")
        
        while user_select not in (tuple(q_options.keys()) + tuple('s')): # all the possible options in a tuple ('1','2',...'s')
            user_select = input('Please enter a valid input: ')

        if user_select == 's':
            limit_num += 5
            continue
        else: # the user entered one of the question numbers
            print('You have chosen question ' + user_select + '!')
            break

    # the following displays all the fields of the question post selected by the user
    print('\n==================================================================')
    print('POST INFO: \n')
    selected_post = posts.find_one({'Id': q_options[user_select]}, {'_id': 0}) # Does not display the '_id' or ObjectId

    # increases the view count of the question post by 1 (before displaying all the fields)
    posts.update_one({'Id': q_options[user_select]}, {'$set': {'ViewCount': selected_post['ViewCount'] + 1}})

    for key,value in selected_post.items(): # prints out all the fields of a question post
        print(key + ':', value) 
    print('==================================================================')

    print('\nYou have selected question ' + user_select + '!')
    return q_options[user_select] # returns the question id