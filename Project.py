"""
Music Recommender Project

Members: James Flanagan, Nikhil Patel

Pledge: I pledge my honor that I have abided by the Stevens Honor System.
"""

from functools import reduce


'''artist dictionary, stores each artist with how many times it has appeared'''
artists = {}
'''list of all user objects'''
users = []

class User():
    '''User Class object stores loaded data from file into one of four attributes - James
    Class Attributes
    name - string, the users name
    private - boolean, user is private
    artist_list_string - string, comma seperated list of all liked artists
    artist_list - list, a list of all liked artists '''
    def __init__(self, data):
        '''constructor for User class, sets attributes based off of data from the file - James'''
        self.name = data[:data.find(':')]
        self.private = self.name[-1] == '$'        
        self.artist_list_string = data[data.find(':')+1:]
        self.artist_list = artistListGenerator(self.artist_list_string, self.private)
    
    def addArtist(self, new_preferences):
        '''method to add an artist to a users artist_list, updates the artist dictionary accordingly - James'''
        if not self.private:
            list(map(removeArtistDictionary,self.artist_list))
        self.artist_list = new_preferences
        self.artist_list.sort()
        if not self.private:
            list(map(addArtistDictionary, self.artist_list))
    
    def totalLikes(self):
        '''returns the total number of artists a user likes -James'''
        return len(self.artist_list)

    def __str__(self):
        '''returns User class object as a string - James'''
        if self.artist_list != []: 
            return self.name + ':' + reduce(lambda x,y : x + ','+ y, self.artist_list)
        return self.name + ':'


def addArtistDictionary(artist):
    '''Updates the artist dictionary, adds one to the artist key -James'''
    if artist in artists:
        artists[artist] = artists[artist] + 1
    else:
        artists[artist] = 1

def removeArtistDictionary(artist):
    '''Updates the artist dictionary, removes one from the artist key -James'''
    if artist in artists:
        artists[artist] = artists[artist] - 1

def artistListGenerator(artist_list_string, private):
    '''Takes a string of artists and returns it as a list of artists, updates the artist dictionary -James'''
    if artist_list_string == '':
        return []
    if artist_list_string.endswith('\n'):
        artist_list_string = artist_list_string[:-1]

    artist_list = artist_list_string.split(',')
    if not private:
        list(map(addArtistDictionary,artist_list))
    return artist_list


def loadFile():
    '''Loads the database file and updates memory with the data - James'''
    try:
        file =  open("musicrecplus.txt", "r")
        for line in file:
            users.append(User(line))
        file.close()
    except FileNotFoundError:
        file = open("musicrecplus.txt", "x")
        print("File not found creating new file")
        file.close()


def saveFile():
    '''Turns all users into the correct string format and then writes to the database file - James'''
    user_strings = list(map(str, users))
    user_strings.sort()
    write_string = reduce(lambda x,y: x + '\n' + y, user_strings)
    file = open("musicrecplus.txt", "w")
    file.write(write_string)
    file.close()

def getUser():
    '''returns the active user, creates a new user profile is the user does not already exist -James'''
    name = input('Enter your name (put a $ symbol after your name if you wish your preferences to remain private): ')
    if len(users) != 0:
        for member in users:
            if name == member.name:
                return member
        '''New User'''
    member = User(name+':')
    users.append(member)
    enterPreferences(member)
    return member

def enterPreferences(currentUser):
    '''Takes user input to add new user preferences -James'''
    new_preference_list = []
    while True:
        new_preference = input("Enter an artist that you like (Enter to finish):")
        if new_preference == '':
            currentUser.addArtist(new_preference_list)
            return 
        new_preference = new_preference.lower()
        new_preference = new_preference.title()
        if new_preference not in new_preference_list:
            new_preference_list.append(new_preference)

def getRecommendations(currentUser):
    "Returns artist recommendations from the user with the most similarity to the current user - Nikhil"
    publicUsers = list(filter(lambda x: not x.private, users))
    publicUsers = list(filter(lambda x: x.artist_list != currentUser.artist_list, publicUsers))
    candidates = []
    favs = currentUser.artist_list
    for user in publicUsers:
        similarities = 0
        for artist in user.artist_list:
            if artist in favs:
                similarities += 1
        if similarities != len(user.artist_list):
            candidates.append(user)
    if candidates == []:
        print("No recommendations available at this time.")
        return
    recommend = candidates[0]
    maxSims = 0
    for user in candidates:
        similarities = 0
        for artist in user.artist_list:
            if artist in favs:
                similarities += 1
        if similarities > maxSims:
            recommend = user
    for artist in recommend.artist_list:
        if not artist in favs:
            print(artist)

def menu():
    '''menu for the reccomender, takes user input to select which function to activate -James'''
    while True:
        action = input( 
            '''Enter a letter to choose an option:
e- Enter preferences
r- Get recommendations
p- Show most popular artists
h- How popular is the most popular
m- Which user has the most likes
q- Save and quit\n'''
)
        
        if action == 'e':
            enterPreferences(activeUser)
        if action == 'r':
            getRecommendations(activeUser)
        if action == 'p':
            #getMostPopular() to be implemented
            pass
        if action == 'h':
            #howPopular() to be implemented
            pass
        if action == 'm':
            #getMostLikes() to be implemented
            pass
        if action == 'q':
            saveFile() 
            return
        else:
            pass

'''Program starts here'''

loadFile()
activeUser = getUser()
menu()
