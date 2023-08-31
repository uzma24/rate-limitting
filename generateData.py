import datetime
import random
import time
import json



#returns the dictionary of users,timestamp
#return list
#put into userData.txt 

def generateUsers():
    #[{userID: "", timestamp: "", requestID: ""},
    # {userID: "", timestamp: "", requestID: ""},
    # ....
    # ....
    # {userID: "", timestamp: "", requestID: ""}]

    dataArr = []

    pgmWindowInMinutes = 2
    endTimeStampinMin = datetime.datetime.now().minute + pgmWindowInMinutes
    currentTimeStamp = datetime.datetime.now().minute
    userIDList = ["user1", "user2", "user3", "user4"]
    
    counter = 0

    while(datetime.datetime.now().minute < endTimeStampinMin):
        print(datetime.datetime.now().second)
        request = {}
        userID = " "
        currentTimeStamp = " "
        if counter > 10:
            break
        if datetime.datetime.now().minute != currentTimeStamp:
            counter = 0
            userId = random.choice(userIDList)
            currentTimeStamp = datetime.datetime.now().minute
        
        request = {"userID": userId, "timeStamp": currentTimeStamp}
        dataArr.append(request)
    
    with open('userData.json', 'w') as fout:
        json.dump(dataArr, fout)


# def driver():
#     const ftchFromFile = ";;;"
#     //ftchFromFile iske andar Arrat
    
#     let timeStampLeaky = ct.current
#     let data of fArray:
#       leaky_bucket(data.userId, .,. ,)
#     console.log( ct.current - timeStampLeaky  )
   
#    timeStampTOken = ct.current
#    let data of fArray:
#       token(data.userId, .,. ,)
#     console.log( ct.current - timeStampTOken  )
print("generating users....")
generateUsers()
print("data generated!!")