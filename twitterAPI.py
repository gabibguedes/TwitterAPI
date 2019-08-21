import requests
from os import system
import json
from tokens import API_TOKEN, API_TOKEN_SECRET
import base64
import urllib.parse

TOKEN = ''

def create_barear_token():
    global TOKEN
    OAUTH2_TOKEN = 'https://api.twitter.com/oauth2/token'
    consumer_key = urllib.parse.quote(API_TOKEN)
    consumer_secret = urllib.parse.quote(API_TOKEN_SECRET)
    bearer_token = consumer_key + ':' + consumer_secret
    base64_encoded_bearer_token = base64.b64encode(bearer_token.encode('utf-8'))
    headers = {
        "Authorization": "Basic " + base64_encoded_bearer_token.decode('utf-8') + "",
        "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
        "Content-Length": "29"}

    response = requests.post(OAUTH2_TOKEN, headers=headers, data={'grant_type': 'client_credentials'})
    to_json = response.json()
    TOKEN = to_json['access_token']


def get_user_id(username):
    header = {'authorization': 'Bearer ' + TOKEN}
    url = 'https://api.twitter.com/1.1/users/show.json?screen_name=' + username
    r = requests.get(url, headers=header)
    user = json.loads(r.text)
    return user['id']

def get_list(id, relationship, cursor=-1): 
    header = {'authorization': 'Bearer ' + TOKEN}
    url = 'https://api.twitter.com/1.1/'+ relationship + '/list.json?user_id=' + str(id) + '&count=200&cursor=' + str(cursor) 
    r = requests.get(url, headers=header)
    response = json.loads(r.text)
    next_page = response['next_cursor']
    friends = response['users']
    
    if next_page != 0:
        friends = [*friends, *get_list(id, relationship, next_page)]
    
    return friends

def print_user_list(users):
    for user in users:
        print(user['name'])

def compare(listA, listB):
    result = []
    for item in listA:
        if item in listB:
            result.append(item)
    return result

def show_options(username):
    system('clear')
    print('Hello {} what do you wanna do?\n'.format(username))
    print('1 - See your followers')
    print('2 - See your friends')
    print('3 - See which frinds follow you back')
    print('4 - Exit')

    return int(input('\noption:'))

def menu(user_id, username):
    op = show_options(username)
    system('clear')
    if op == 1:
        print('Here are your Followers:')
        followers = get_list(user_id, 'followers') 
        print_user_list(followers)
        size = len(followers)
        print('\nYou have {} followers!!'.format(size))
        input('\nPress ENTER to exit')
        menu(user_id, username)

    elif op == 2:
        print('Here are your Friends:')
        friends = get_list(user_id, 'friends') 
        print_user_list(friends)
        size = len(friends)
        print('\nYou have {} friends!!'.format(size))
        input('\nPress ENTER to exit')
        menu(user_id, username)
        
    elif op == 3:
        print('Here are your friends who follow you back:')
        followers = get_list(user_id, 'followers')
        friends = get_list(user_id, 'friends')
        people = compare(followers, friends)
        print_user_list(people)
        size = len(people)
        print('\nThere are {} people on this list!!'.format(size))
        input('\nPress ENTER to exit')
        menu(user_id, username)

    elif op == 4:
        print('Bye bye')
        return
    
    else:    
        print('Sorry, didnt understand')
        input('\nPress ENTER to return to menu')
        menu(userid, username)

if __name__ == '__main__':
    create_barear_token()
    username = input('Write your username: ')
    user_id = get_user_id(username)
    menu(user_id,username)
