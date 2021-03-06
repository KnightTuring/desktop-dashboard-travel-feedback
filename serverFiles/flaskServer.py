from flask import Flask, jsonify
from flask import abort
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import json
from collections import defaultdict
from textblob.classifiers import NaiveBayesClassifier
from pyfcm import FCMNotification

app = Flask(__name__)

'''
Every user that gives feedback is an instance of this class
'''
class User:
    name=" "
    overallRating=" "
    transportReview=" "
    hotelReview=" "

    def set_name(self,new_name):
        self.name = new_name

    def set_details(self,new_overallRating,new_transportReview,new_hotelReview):
        self.overallRating = new_overallRating
        self.hotelReview = new_hotelReview
        self.transportReview = new_transportReview

    def get_name(self):
        return self.name

    def get_hotel_review(self):
        return self.hotelReview

    def get_overall_rating(self):
        return self.overallRating


'''
Initialization method
'''
@app.route('/init',methods=['GET'])
def main():
    ref = db.reference('/trips')
    # print ref.get()
    print 'Pulling Firebase data'
    writeJSONFile(ref.get())

    print'Loading JSON'

    with open('feedback.json', 'r') as f:
        distroDict = json.load(f)

    print(distroDict)
    # get list of all cities
    citiesList = list(distroDict)

    #VERY IMPORTANT
    dMap.clear()

    # for each city populate the corresponding User object list
    for i in citiesList:
        populateCityUserList(i, distroDict)
    status = 'OK'
    return jsonify({'status':status})

@app.route('/get_positive_feed_count/<string:cityName>',methods=['GET'])
def getPositiveFeedCount(cityName):
    userObjectList = []
    count = 0
    print dMap[cityName]
    userObjectList = getGoodFeedback(dMap[cityName])
    count = len(userObjectList)
    return jsonify({'status':'OK','count':count})

@app.route('/get_negative_feed_count/<string:cityName>',methods=['GET'])
def getNegativeFeedback(cityName):
    userObjectList = []
    count = 0
    print dMap[cityName]
    userObjectList = getBadFeedback(dMap[cityName])
    count = len(userObjectList)
    return jsonify({'status': 'OK', 'count': count})

@app.route('/get_total_feed_count/<string:cityName>',methods=['GET'])
def getTotalFeedback(cityName):
    userObjectList = []
    count = 0
    userObjectList = getGoodFeedback(dMap[cityName])
    count = count + len(userObjectList)
    userObjectList = getBadFeedback(dMap[cityName])
    count = count + len(userObjectList)
    return jsonify({'status':'OK' , 'count':count})

@app.route('/get_positive_user_feed/<string:cityName>',methods=['GET'])
def getPositiveUserFeed(cityName):
    userObjectList = []

    userObjectList = getGoodFeedback(dMap[cityName])
    dictUser = {}
    for user in userObjectList:
        #print user.get_name()
        #print user.get_hotel_review()
        userName = user.get_name()
        hotelRev = user.get_hotel_review()
        dictUser.update({userName:hotelRev})
    dictUser.update({'status':'OK'})
    return jsonify(dictUser)

@app.route('/get_negative_user_feed/<string:cityName>',methods = ['GET'])
def getNegativeUserFeed(cityName):
    userObjectList= []
    userObjectList = getBadFeedback(dMap[cityName])
    dictUser = {}
    for user in userObjectList:
        userName = user.get_name()
        hotelRev = user.get_hotel_review()
        dictUser.update({userName:hotelRev})
    dictUser.update({'status':'OK'})
    return jsonify(dictUser)

@app.route('/get_classifier_accuracy',methods=['GET'])
def getClassifierAccuracy():
    test = [
        ('very bad','negative'),
        ('quality needs to be maintained','negative'),
        ('great arrangements','positive'),
        ('good experience','positive')
    ]
    acc = cl.accuracy(test)

    return jsonify({'accuracy':acc , 'status':'OK'})

@app.route('/send_push_notif_negative/<string:cityName>', methods=['GET'])
def sendPushNotif(cityName):
    # api-key should be 'Server key' at console.firebase.google.com (your project page), under CLOUD MESSAGING tab.
    push_service = FCMNotification(api_key="AAAA9oQvUyg:APA91bGNXpgabj-nGXKv-Njelm9pzKYdanbVWM9-hLKVOZZOt3H2xFTcIsfzbz9stzgCLi6D5JzjYvkPxZEKhVECP1ZOPtMJyT52MJWNLr7hPGjOSi9_TcKBmH6Cs7azN_XmZEW9fylX")
    #list of account tokens
    registration_ids = []
    registration_ids = getAdminTokenFCM();
    print 'Received list of admin FCM token', registration_ids
    '''
    Now get negative feed count
    '''
    userObjectList = []
    count = 0
    print dMap[cityName]
    userObjectList = getBadFeedback(dMap[cityName])
    count = len(userObjectList)
    '''
    Negative count stored in count
    '''
    message_title = "Negative Feedback"
    message_body = cityName+" has "+str(count)+" negative feedback"
    print 'sending push notif'
    result = push_service.notify_multiple_devices(registration_ids=registration_ids ,message_title=message_title, message_body=message_body )
    return jsonify({'status':'OK','serviceStatus':result})

@app.route('/get_average_score/<string:cityName>')
def getAverageScore(cityName):
    score = getAvgScore(dMap[cityName])
    return jsonify({'status':'OK' , 'score':score})

def getAdminTokenFCM():
    refToken = db.reference('/adminToken')
    fcmTokenList = []
    print 'refToken is', refToken.get()
    tokenDict = refToken.get()
    adminList = list(tokenDict)
    print 'Admin list is',adminList
    for admin in adminList:
        fcmToken = tokenDict[admin]['token']
        fcmTokenList.append(str(fcmToken))
    print 'FCM token list retrieved',fcmTokenList
    return fcmTokenList


'''
This method transalates JSON into a map data structure that has 
cityName(KEY) ---> User object (LIST)
'''
def populateCityUserList(cityName,distros_dict):
    userList = []
    userList = list(distros_dict[cityName])
    #print userList
    for user in userList:
        #print ("For user",user)
        #print(distros_dict[c.cityName][user]['OverallRating'])
        userObj = User()
        userObj.set_name(user)
        userObj.set_details(distros_dict[cityName][user]['OverallRating'],
                            distros_dict[cityName][user]['TransportReview'],
                            distros_dict[cityName][user]['HotelReview'])
        dMap[cityName].append(userObj)


'''
Return good feedback from given list of User object
'''
def getGoodFeedback(userObjectList):
    outputList = []
    print 'GOOD FEEDBACK RECIEVED LENGTH',len(userObjectList)
    for user in userObjectList:
        label = cl.classify(user.get_hotel_review())
        if label == 'positive':
            outputList.append(user)
    #print outputList
    return outputList
'''
Return bad feedback from given list of User object
'''
def getBadFeedback(userObjectList):
    outputList = []
    print 'BAD FEEDBACK RECIEVED LENGTH', len(userObjectList)
    for user in userObjectList:
        label = cl.classify(user.get_hotel_review())
        if label == 'negative':
            outputList.append(user)
    # print outputList
    return outputList

'''
Return bad feedback from given list of User object

def getBadFeedback(userObjectList):
    outputList = []
    for user in userObjectList:
        label = cl.classify(user.get_hotel_review())
        if label == 'negative':
            outputList.append(user)
    return outputList
'''

'''
Return average score of a city
'''
def getAvgScore(userObjectList):
    total = 0
    sum = 0
    total =len(userObjectList)
    print 'Total is',total
    for user in userObjectList:
        sum = sum + int(user.get_overall_rating())
        print 'sum is', sum
    avg = sum/total
    return avg

'''
This method writes data to JSON file
'''
def writeJSONFile(data):
    print 'writing data to JSON file'
    with open('feedback.json', 'w') as outfile:
        json.dump(data, outfile)
    print 'written to JSON file'

cred = credentials.Certificate('Travel Junction-1f5057e2d3c8.json')

firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://travel-junction.firebaseio.com',
        'databaseAuthVariableOverride': None
    })

citiesList = []
dMap = defaultdict(list)
train = [
    ('very good experience','positive'),
    ('good','positive'),
    ('good service','positive'),
    ('excellent','positive'),
    ('luxurious', 'positive'),
    ('loved it, looking forward to more','positive'),
    ('had a great time','positive'),
    ('very good','positive'),
    ('awesome experience','positive'),
    ('amazing time','positive'),
    ('very bad','negative'),
    ('horrible time', 'negative'),
    ('worst service ever', 'negative'),
    ('waste of time', 'negative'),
    ('waste of money', 'negative'),
    ('expected much better', 'negative'),
    ('regret decision', 'negative'),
    ('not very good','negative'),
    ('bad','negative')
]

'''
with open('dataset.csv','r') as fp:
    cl =NaiveBayesClassifier(fp, format="csv")
'''

cl = NaiveBayesClassifier(train)


'''
-------------------MAIN METHOD----------------------
'''
if __name__=="__main__":
    #app.run(host="192.168.1.37" , debug=True , port=8000)
    app.run()