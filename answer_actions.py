from datetime import datetime
from post_question import generateRandomId

"""-----------------------------------------------------------------
vote - Allows the user to vote on a post
Purpose: Based upon the answer or question provided by the user vote on this post
by adding a new vote to the votes collection. If there is a user
logged in and said user has already voted on this answer or question the vote
is rejected. If the vote is succesfully added then we increase the
score of the post in the posts collection corresponding to the answer or question
Input: postId : The id of the question or answer on which the user is trying to vote
user:The user or "" for anonymous user
posts: The posts collection
votes: The votes collection
Output: None
-----------------------------------------------------------------"""
def vote(postId,user,posts,votes):
    postScore = 0
    #find the post that corresponds to our question
    results = posts.find({"Id": postId})
    for result in results:
        postScore = result["Score"]
    #boolean for wether the user is anonymous or not
    anonymous = False
    if (user == ""):
        anonymous = True
    #check to see if we can find a vote for this post where the userId is the same as our current user
    #using the $ in python from https://www.w3schools.com/python/python_mongodb_update.asp
    if (anonymous == False):
        results = votes.find({ "$and": [ {"PostId":postId}, { "UserId":user} ] })
        for result in results:
            #result is found terminate here since vote is rejected
            print("You have already voted on this post. Vote rejected")
            return
    
    #get a random and unique Id for this new vote
    voteId = generateRandomId(votes)
    # Used to modify the date and time format so that it matches the format shown in the Posts.json file 
    # eg. "CreationDate": "2011-02-22T21:47:22.987"
    date_time = str(datetime.today())[:-3] # takes away the last three digits
    date_time = date_time.replace(' ', 'T') # replaces the space in the middle with 'T'
    #user is not anonymous so create a new vote with a UserId set to our current user
    if anonymous == False:
        vote = [
            {"Id": str(voteId),
            "PostId": str(postId),
            "VoteTypeId": "2",
            "UserId": str(user),
            "CreationDate":date_time}]
        votes.insert_many(vote)
    #user is anonymous so create a new vote without a UserId
    else:
        vote = [
            {"Id": str(voteId),
            "PostId": str(postId),
            "VoteTypeId": "2",
            "CreationDate":date_time}]
        votes.insert_many(vote)
    #update the post in the posts collection corresponding to our answer by increasing its score by 1
    newPostScore = int(postScore)+1
    posts.update({"Id":postId},{"$set":{"Score": str(newPostScore)}})
    print("Vote added! Post "+ postId + " has also had its Score increased")
    return