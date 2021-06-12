import requests
import json
from django.conf import settings 

def Check_rich_munu_to_user (userId):
    LINE_API = 'https://api.line.me/v2/bot/user/' + Main_rich_memu_id + '/richmenu'
    PARAMS = {'userId' : userId}
    Authorization = 'Bearer {}'.format(Channel_access_token)
    headers = {'Authorization': Authorization,}
    r = requests.get(LINE_API, headers=headers, params=PARAMS)
    data = r.json()
    #print(data)
    return 200

def Link_rich_menu_to_user (rich_menu_id,User_id):
    print ('ID is {}'.format(rich_menu_id))
    LINE_API = 'https://api.line.me/v2/bot/user/' + User_id + '/richmenu/' + rich_menu_id
    PARAMS = {'richMenuId' : rich_menu_id,'userId': User_id}
    Authorization = 'Bearer {}'.format(settings.LINE_CHANNEL_ACCESS_TOKEN)
    headers = {'Authorization': Authorization, 'Content=Type' : 'application/json' }
    r = requests.post(LINE_API, headers=headers, params=PARAMS)
    data = r.json()
    print(data)
    return 200

def Unlink_rich_menu_to_user (userId):
    LINE_API = 'https://api.line.me/v2/bot/user/' + userId + '/richmenu/'
    PARAMS = {'userId': userId}
    Authorization = 'Bearer {}'.format(Channel_access_token)
    headers = {'Authorization': Authorization, 'Content=Type' : 'application/json' }
    r = requests.delete(LINE_API, headers=headers, params=PARAMS)
    r.json()
    respons = r.status_code
    if respons == 200 :
        #print('OK')
        return 'OK'
    else:
        print('NOK')



def Rich_menu_Payload (payload,type):
    userID_data = payload['events'][0]['source']['userId']
    print ('UserID data in rich function is {}'.format(userID_data))
    print('type for rich is {}'.format(type))
    Link_rich_menu_to_user(userID_data,type)

def Unlink_Rich_menu_Payload (payload):
    userID_data = payload['events'][0]['source']['userId']
    Unlink_rich_menu_to_user(userID_data)


