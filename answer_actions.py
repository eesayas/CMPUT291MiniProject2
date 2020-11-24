from datetime import datetime
from post_question import generateRandomId
def vote(postId,user,posts,votes):
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
    voteId = generateRandomId(posts)
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