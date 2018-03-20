import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import json
from collections import defaultdict
from textblob.classifiers import NaiveBayesClassifier
# setup user object

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

'''
class City:
    cityName=" "
    userFeedbackList = []
    def __init__(self, new_cityName):
        self.cityName = new_cityName

    def populateList(self, u=User()):
        self.userFeedbackList.append(u)

    def getList(self):
        return self.userFeedbackList
'''

def writeJSONFile(data):
    print 'writing data to JSON file'
    with open('feedback.json', 'w') as outfile:
        json.dump(data, outfile)
    print 'written to JSON file'


def populateCityUserList(dMapLocal,cityName,distros_dict):
    userList = []
    userList = list(distros_dict[cityName])
    print userList
    for user in userList:
        #print ("For user",user)
        #print(distros_dict[c.cityName][user]['OverallRating'])
        userObj = User()
        userObj.set_name(user)
        userObj.set_details(distros_dict[cityName][user]['OverallRating'],
                            distros_dict[cityName][user]['TransportReview'],
                            distros_dict[cityName][user]['HotelReview'])
        dMapLocal[cityName].append(userObj)

def getGoodFeedback(userObjectList):
    outputList = []
    for user in userObjectList:
        label = cl.classify(user.get_hotel_review())
        if label == 'positive':
            outputList.append(user)
    return outputList

def getBadFeedback(userObjectList):
    outputList = []
    for user in userObjectList:
        label = cl.classify(user.get_hotel_review())
        if label == 'negative':
            outputList.append(user)
    return outputList

def main():
    ref = db.reference('/trips')
    #print ref.get()
    writeJSONFile(ref.get())

    with open('feedback.json' , 'r') as f:
        distroDict = json.load(f)

    citiesList = []
    citiesList = list(distroDict)

    dMap = defaultdict(list)
    for i in citiesList:
        populateCityUserList(dMap,i,distroDict)

    #print dMap['Delhi']
    '''
    for city in citiesList:
        print("In city",city)
        userObjList = dMap[city]
        for user in userObjList:
            print user.get_name()
    '''

    badFeedbackUserObjList = []
    goodFeedbackUserObjList = []
    cityName = raw_input("Enter city name")
    goodFeedbackUserObjList = getGoodFeedback(dMap[cityName])
    badFeedbackUserObjList = getBadFeedback(dMap[cityName])

    print 'GOOD FEEDBACK'
    print len(goodFeedbackUserObjList)
    for user in goodFeedbackUserObjList:
        print(user.get_name())
        print(user.get_hotel_review())
        print '----------------'

    print 'BAD FEEDBACK'
    for user in badFeedbackUserObjList:
        print(user.get_name())
        print(user.get_hotel_review())
        print '-------------------'


cred=credentials.Certificate('Travel Junction-1f5057e2d3c8.json')

firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://travel-junction.firebaseio.com',
        'databaseAuthVariableOverride': None
    })

train = [
    ('very good experience','positive'),
    ('good','positive'),
    ('excellent','positive'),
    ('loved it, looking forward to more','positive'),
    ('had a great time','positive'),
    ('very good','positive'),
    ('awesome experience','positive'),
    ('amazing time','positive'),
    ('luxurious and good service','positive'),
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
cl = NaiveBayesClassifier(train)


if __name__=="__main__":
    main()






