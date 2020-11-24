import sys
from pymongo import MongoClient
from user_report import ask_for_user_id, checks_for_user_id, showReport, nullReport
from post_question import postQuestion
from search_question import searchQuestions
from question_actions import create_answer, list_answers
from answer_actions import vote

def main():
    # TODO clarify error check on invalid port?
    port = sys.argv[1]

    client = MongoClient('mongodb://localhost:' + port)

    # open database
    db = client["291db"]

    # open collections
    global posts, tags, votes
    posts, tags, votes = db["posts"], db["tags"], db["votes"]

    # user global var
    global user
    user = ""

    # allow for user id provision
    chooseUser()

    # show main menu
    mainMenu()

def exit():
    #global user
    #user = ""
    # this will print when exit() is called
    print("\nGoodbye!\n")

    # standard python exit
    sys.exit()


"""-----------------------------------------------------------------
chooseUser - Allow user to propvide user_id
Purpose: Show appropriate report for user_id
-----------------------------------------------------------------"""
def chooseUser():
    # ask user for user_id
    user_id = ask_for_user_id()
    
    # confirm that user exists in db
    confirm_user = checks_for_user_id(user_id, votes, posts)

    # if user exists showReport()
    if confirm_user:
        showReport(user_id, votes, posts)

        # set user 
        global user

        user = user_id

    # if a user id has been provided but no match in db
    elif user_id != '' and not confirm_user:
        nullReport(user_id)
        user = user_id

"""-----------------------------------------------------------------
mainMenu - This will show the menu
Purpose: User can select which action to take
-----------------------------------------------------------------"""
def mainMenu():
    print("Main menu:")
    print("Enter 1 to provide a user id to use")
    print("Enter 2 to post a question")
    print("Enter 3 to search for a question")
    print("Enter 4 to exit")
    action = input("What action would you like to take?: ") 

    #loops untill a valid choice is made
    while (True):
        # user wants to provide user_id
        if action == '1':
            chooseUser()
            mainMenu()

        # user wants to post a question
        elif action == '2':
            postQuestion(posts, tags, user)
            mainMenu()

        # user wants to search a question
        elif action == '3':
            result = searchQuestions(posts)
            if result == None:
                mainMenu()
            question_action(result)

        # user chose to exit
        elif action == '4':
            exit()

        # user did not make a valid choice, get a new choice
        else:
            
            action = input("Invalid action please choose a valid action from either '1','2','3','4': ")

"""-----------------------------------------------------------------
The user selects a question action.
Input: qid - Id of Question
Output: None
-----------------------------------------------------------------"""
def question_action(qid):
    print('==================================================================')
    print("Question Actions:")
    print("Enter 1 to post an answer to this question")
    print("Enter 2 to list the answers of the question (from there you can place a vote on an answer")
    print("Enter 3 to go back to main menu")
    print("Enter 4 to exit")
    action = input("What action would you like to take?: ") 
    while (True):

        # user chose to post answer to this post
        if action == '1':
            body = input("What would you like the answer to say?: ")
            create_answer(qid, body, user, posts)
            mainMenu()

        # user chose to list answer to a question
        elif action == '2':
            answersResult = list_answers(qid, posts)
            answers = answersResult[0]
            answersLength = answersResult[1]
            if answersLength == 0:
                print("There are no answers for this Question")
                mainMenu()
            
            while (True):
                choice = input("Select the index number of the answer you would like to select or enter 'exit' to exit or 'menu' to go back to main menu: ")
                if (choice.lower() == "exit"):
                    exit()
                elif (choice.lower() == "menu"):
                    mainMenu()
                else:
                    try:
                        if (int(choice)>=answersLength):
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
                        vote(str(chosenId),user,posts,votes)
                        mainMenu()
                    elif (voteChoice.lower() == "no"):
                        mainMenu()
                    elif (voteChoice.lower() == "menu"):
                        mainMenu()
                    elif (voteChoice.lower() == "exit"):
                        exit()
                    else:
                        print("Not a valid choice") 
                mainMenu()
    
        # user wants to go back
        elif action == '3':
            mainMenu()

        # user chose to exit
        elif action == '4':
            exit()

        # users did not make a valid choice, get a new choice
        else:
            action = input("Invalid action please choose a valid action from either '1','2','3','4': ")

# run program
main()