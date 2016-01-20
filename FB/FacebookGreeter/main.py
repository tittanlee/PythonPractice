__author__ = 'dgraziotin'
"""
This program is free software. It comes without any warranty, to
the extent permitted by applicable law. You can redistribute it
and/or modify it under the terms of the Do What The Fuck You Want
To Public License, Version 2, as published by Sam Hocevar. See
http://sam.zoy.org/wtfpl/COPYING for more details.
 """
import access
import dbmanager

class Friend(object):
    def __init__(self, first_name, last_name, id, locale):
        self.first_name = first_name
        self.last_name = last_name
        self.id = id
        self.locale = locale
        self.greeted = False

    def __unicode__(self):
        return unicode("Name: " + unicode(self.first_name) + " " + unicode(self.last_name) + \
                " id: " + self.id + " locale: " + self.locale + " greeted: " + str(self.greeted))

    def __repr__(self):
        return self.__unicode__().encode('utf-8')


class FriendsManager(object):
    def __init__(self, graph_api):
        self.graph_api = graph_api
        self.dbmanager = dbmanager.DBManager()
        self.friends = self.get_friends()

        if not self.friends:
            self.friends = []
            self.friends = self.process_friends()
            self.save_friends()

    def fetch_friends_list(self):
        friends_list = self.graph_api.get_object('/me/friends')['data']
        return friends_list

    def fetch_friend_object(self, id):
        friend_detail = self.graph_api.get_object(id)
        friend = Friend(friend_detail['first_name'],friend_detail['last_name'],friend_detail['id'],friend_detail['locale'])
        return friend

    def process_friends(self):
        friends_list = self.fetch_friends_list()
        for friend in friends_list:
            print ("Processing " + friend['name'])
            self.friends.append(self.fetch_friend_object(friend['id']))
        return self.friends

    def save_friends(self):
        self.dbmanager.save("friends",self.friends)

    def get_friends(self):
        return self.dbmanager.get("friends")

    def get_not_greeted_friends(self):
        not_greeted_friends = []
        for friend in self.friends:
            if not friend.greeted:
                not_greeted_friends.append(friend)
        return not_greeted_friends

    def send_greet(self, friend, greeter):
        greetings = greeter.greet(friend)
        try:
            self.graph_api.put_wall_post(message=greetings,profile_id=friend.id)
            friend.greeted = True
            return True
        except Exception as e:
            print(e)
            friend.greeted = False
            return False


    def greet_friends(self, greeter):
        not_greeted_friends = self.get_not_greeted_friends()
        print ("Going to greet " + str(len(not_greeted_friends)) + " friends")
        for friend in not_greeted_friends:
            if not friend.greeted:
                if self.send_greet(friend, greeter):
                    print ("Greet sent to " + friend.first_name + " " + friend.last_name)
                    friend.greeted = True
                else:
                    print ("Greet not sent to " + friend.first_name + " " + friend.last_name)
                    friend.greeted = False
                self.save_friends()
        not_greeted_friends = self.get_not_greeted_friends()
        print ("\n\n\nFinished. \nNot Greeted:" + str(len(not_greeted_friends)))
        for friend in not_greeted_friends:
            print (friend)





class Greeter(object):
        
    def greet(self, friend):
        if friend.locale == u'it_IT':
            return self.it_IT(friend)
        else:
            return self.en_US(friend)
        
    def it_IT(self, friend):
        return  """Caro/a """ + friend.first_name + """ """ + friend.last_name + """, visti gli attuali e futuri cambiamenti di FB su come trattare la nostra privacy, ho deciso di disiscrivermi. Spero di poter rimanere in contatto:
e-mail/Google Talk: your-google-id@gmail.com
mobile: 12345678910
Skype: your-skype-name
Twitter: @your-twitter-name
[add as many as you want]

Cordiali Saluti (Messaggio generato automaticamente)"""
    def en_US(self, friend):
        return """Dear """ + friend.first_name + """ """ + friend.last_name + """, because of the current and future ways FB will handle our privacy, I decided to unsubscribe. I hope to stay in touch with you:
e-mail/Google Talk: your-google-id@gmail.com
mobile: 12345678910
Skype: your-skype-name
Twitter: @your-twitter-name
[add as many as you want]

Best Regards (Message sent automatically)"""


if __name__=="__main__":
    graph = access.FBOAuth().get_graph_api()
    me = graph.get_object("/me")
    print(me)

    data = graph.request('search', {'q':'免費廣告', 'type':'group'})
    print(data)

    # friends_manager = FriendsManager(graph)
    # greeter = Greeter()

    # friends_manager.greet_friends(greeter)






    
