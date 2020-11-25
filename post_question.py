import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
from datetime import datetime
import random

"""-----------------------------------------------------------------
postQuestion - User will post a question
Purpose: Ask user for a question and insert to db
Params: posts, tags (collections)
-----------------------------------------------------------------"""
def postQuestion(p_col, t_col, user):
    global posts, tags
    posts, tags = p_col, t_col
    
    
    # returns a dictionary with the title, body, and tag(s) as its keys
    # eg. {'title': 't', 'body': 'b', 'tag': ['123']}
    q_dict = q_input(user)



    # Used to modify the date and time format so that it matches the format shown in the Posts.json file 
    # eg. "CreationDate": "2011-02-22T21:47:22.987"
    date_time = str(datetime.today())[:-3] # takes away the last three digits
    date_time = date_time.replace(' ', 'T') # replaces the space in the middle with 'T'

    question = {'Id': generateRandomId(posts), 'PostTypeId': '1', 'CreationDate': date_time, 'Score': 0, 'ViewCount': 0, 
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

        # if current key is OwnerUserId and its blank, then continue
        if key == 'OwnerUserId' and len(value) == 0: 
            continue
        elif key != 'Tags': # because modified_tags is already added to question            
            question[key] = value
        

    posts.insert_one(question) # inserts the question into the database
    print('Your question has been posted!')


"""-----------------------------------------------------------------
The user will be asked to enter a title, a body, and tags (which can be zero tags or more), which will then be
recorded in te database with a unique id

Input: (optional) user ID. If the user is anonymous (has no user ID), then the default argument will be an empty string.

Output: returns a dictionary (known as q_info_dict) with the title, body, and tags as its keys,
where title and body are returned as strings, and the tags are returned as a list of strings
eg. {'title': _____, 'body': ______, 'tag': [__,___,__]}

-----------------------------------------------------------------"""
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
        user_tag = input("Enter a tag (one tag at a time): ").lower()

        while user_tag.strip() == '': # if the user enters an empty string
            user_tag = input("Invalid Input. Enter a tag (one tag at a time): ").lower()

        # if the tag has not already been entered before (regardless of upper/lower case)
        if user_tag not in tag_list: 
            tag_list.append(user_tag.strip()) # strip() is used in case there are random spaces used eg. "   tag  "
            
        else: # if the tag has already been entered
            print("You have already entered this tag. Please enter another tag.") # prevents the duplication of tags
        
        ask_tag = input("Would you like to enter another tag? (Enter 'y' for yes or 'n' for no): ").lower()

        if ask_tag == 'n':
            break

    q_info_dict['Tags'] = tag_list # adds the list of tags as a value to the key 'tag'


    # Add tag count if tag already exists, otherwise insert tag and its count as 1
    tag_collection = tags # in actual project, should be called Tags

    for tag in tag_list: # for each tag entered by the user
        tag_results = tag_collection.find_one({"TagName": tag.lower()}) # only one result is expected
        
        if tag_results != None: # the tag name exists
            tag_collection.update_one({"TagName": tag.lower()}, ({"$set": {"Count": tag_results['Count'] + 1}}))
            # increases the tag count by 1
        else:
            pid = generateRandomId(posts) # generates a unique id for the tag
            tag_collection.insert_one({'Id': pid, 'TagName': tag, 'Count': 1}) # new tag with an initial count of 1


    return q_info_dict

"""----------------------------------------------------------------
Generates a unique pid. If the pid already exists, then it will generate another one. 
In order to be fast it tries to generate an Id between 10 and 1000 by
getting a random number in this range. If it can find one that is unique -> done.
If not we increase the lower and uper range of our bounds by a factor of one hundred and try again.
Do this until we get a unique Id.
Input: none
Output: unique pid as a string

----------------------------------------------------------------"""
def generateRandomId(collection):
    lower = 10
    higher = 1000
    q_pid = str(random.randint(lower,higher))
    results = collection.find({'Id': q_pid})
    
    while results.count():
        lower = lower * 100
        higher = higher * 100
        q_pid = str(random.randint(lower,higher))
        results = collection.find({'Id': q_pid})

    return q_pid