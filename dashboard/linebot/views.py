# -*- coding: utf-8 -*-
# !/usr/bin/env python
import time
from django.conf import settings
from django.db.models.fields import AutoField  # calls the object written in settings.py
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import requests
from django.utils import timezone
from linebot.save_data_to_db import *
from linebot.creating_line_data import *
from linebot.convert_xml import *
from linebot.calculate_function import *
from linebot.connect_db_profile import *
from linebot.line_tamplates import *
from app.models import Site, Status , Status_Error_logger,Store_data_send_line_failed



Channel_access_token = settings.LINE_CHANNEL_ACCESS_TOKEN

print ('OK')
def index(request):
    return HttpResponse("test!!")

@csrf_exempt  # this is used for avoid csrf request from line server
def callback(request):  # สำหรับส่งการแจ้งเตือนต่างไปที่ Line Notify and Line Bot
    if request.method == "POST":  # Check if method is POST
        payload = json.loads(request.body.decode('utf-8'))  # Convert data to json
        print('first payload',payload)
        if len(payload['events']) == 0 :
            print ('Message from server to Verify')
            return HttpResponse(200)
        else :
            global Reply_token
            global User_id
            Reply_token = payload['events'][0]['replyToken']
            User_id = payload['events'][0]['source']['userId']
            if payload['events'][0]['type'] == 'follow':
                    ReplyMessage(line_templates.Gressing_msg())
                    return HttpResponse(200)
            elif payload['events'][0]['type'] == 'message':
                message = payload['events'][0]['message']['text']
                print ('message is',message)
                if message == 'test':
                    ReplyMessage(line_templates.Gressing_msg())
                    return HttpResponse(200)
                if (message[0:5]).lower() == 'orpak':
                    print(message)
                    command_payload = ((payload['events'][0]['message']['text'])[0:5]).lower()+((payload['events'][0]['message']['text'])[5:])
                    print (command_payload)
                    code_login = (command_payload[5:])
                    print ('code login is',code_login)
                    # try :
                    #     id_user = PersanalDetaillogin.objects.filter(key_login=code_login).first()
                    #     if id_user != None :
                    #         if id_user.member_status == 'none' :
                    #             global name
                    #             global company
                    #             name=id_user.name
                    #             company=id_user.company
                    #             ReplyMessage(line_templates.ensure_submit(id_user))
                    #         else:
                    #             ReplyMessage(line_templates.alreadySubmit_code(id_user))
                    #     else :
                    #         ReplyMessage(line_templates.re่ject_code())        
                    # except PersanalDetaillogin.DoesNotExist:
                    #     ReplyMessage(line_templates.re่ject_code())
                    #     return None 
            elif payload['events'][0]['type'] == 'postback':
                message = payload['events'][0]['postback']['data']
                if message == 'register'    :
                    ReplyMessage(line_templates.register_code())
                
        
    return HttpResponse(200)


@csrf_exempt  # this is used for avoid csrf request from line server
def updatedb(request):
    if request.method == "POST":  # Check if method is POST
        payload = json.loads(request.body.decode('utf-8'))  # Convert data to json
        if payload['events'][0]['type'] == 'VIS-MONITOR':  # Check if request is VIS-Monitor to update in database
            if payload['events'][0]['update_type'] == 'update_all':
                # print(payload)
                data_convert = convert_xml_json(payload)
                update_MWGT_AllData = UpdateAllDataMWGT(data_convert)
                if update_MWGT_AllData == 200 :
                    return 200
            elif payload['events'][0]['update_type'] == 'update_MWGT_OFFLINE': #ทำการ Update ให้เป็น offline
                update_MWGT_OFFLINE = UpdateMWGT_OFFLINE(payload)
                if update_MWGT_OFFLINE == True :
                    return None
            elif payload['events'][0]['update_type'] == 'update_MWGT_ONLINE': #ทำการ Update ให้เป็น online
                update_MWGT_ONLINE = UpdateMWGT_ONLINE(payload)
                if update_MWGT_ONLINE == True:
                    return None
                print(payload)
    return HttpResponse(200)


@csrf_exempt  # this is used for avoid csrf request from line server
def update_battery (request): # function สำหรับการ update สถานะ แบตเตอร์รี่ ไปที่ data base 
    if request.method == "POST":  # Check if method is POST
        payload = json.loads(request.body.decode('utf-8'))  # Convert data to json
        name_id = payload['events'][0]['name_id']
        # print (payload)
        if payload['events'][0]['type'] == 'VIS-MONITOR':  # Check if request is VIS-Monitor to update in database
            if payload['events'][0]['update_type'] == 'update_battery': # Check request ว่าใช่ update_battery หรือไม่ 
                # print(payload)
                update_BATTEY_Data = UpdateBatteryStatus(payload)
                if update_BATTEY_Data == 200 :
                    return HttpResponse (200)
                # return HttpResponse (200)
    

@csrf_exempt  # this is used for avoid csrf request from line server
def permission_check(request):
    if request.method == "POST":  # Check if method is POST
        payload = json.loads(request.body.decode('utf-8'))  # Convert data to json
        if payload['events'][0]['type'] == 'VIS-MONITOR':
            try:
                result = Site.objects.select_related().get(station_ip=payload['events'][0]['ip'])  # นำ ip มาเช็คกับตาราง Site และส่งเลข id กลับไปให้
                # return JsonResponse({"site_id": result.id,
                #                      "password": result.station_password,
                #                      "station_monitor_device": result.station_monitor_device,
                #                      "nozzles_activate": result.nozzle_mapping.nozzles_activate})  # ส่งเลข id กลับไปให้
                return JsonResponse({"site_id": result.id,
                                        "password": result.station_password,
                                            "station_monitor_device": result.station_monitor_device
                                                })  # ส่งเลข id กลับไปให้
            except Site.DoesNotExist:
                return JsonResponse({"site_id": "failed"})  # ส่งเลข failed กลับไปให้เนื่องจากไม่พบเลข ip ที่ส่งเข้า
    return HttpResponse(200)


def ReplyMessage(TextMessage):
    Token = Channel_access_token
    Reply_token_line = Reply_token
    LINE_API = 'https://api.line.me/v2/bot/message/reply'
    # print('line API {}'.format(TextMessage))
    Authorization = 'Bearer {}'.format(Token)
    # print(Authorization)
    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'Authorization': Authorization
    }

    data = {
        "replyToken": Reply_token_line,
        "messages": [TextMessage], }

    data = json.dumps(data)
    # print('data to line {}'.format(data))
    r = requests.post(LINE_API, headers=headers, data=data)
    print(r)
    return 200


def PushMessage(push_new_messasge, user_id):
    Token = Channel_access_token
    LINE_API = 'https://api.line.me/v2/bot/message/push'
    # print('line API {}'.format(push_new_messasge))

    Authorization = 'Bearer {}'.format(Token)
    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'Authorization': Authorization
    }

    data = {
        "to": user_id,
        "messages": [push_new_messasge], }

    # print('data to line {}'.format(data))
    data = json.dumps(data)
    r = requests.post(LINE_API, headers=headers, data=data)
    print(r)
    return 200


def send_notify(message, token):
    try:
        Token = 'Bearer ' + token
        LINE_ACCESS_TOKEN = Token
        url = 'https://notify-api.line.me/api/notify'
        headers = {'content-type': 'application/x-www-form-urlencoded', 'Authorization': LINE_ACCESS_TOKEN}
        r = requests.post(url, headers=headers, data={'message': message})
        print (r.text)
        return True
    except  requests.ConnectionError as err:
        print("Connected to Line notify fail")
        return False


def PushMessage_group(push_new_messasge, Token, group_id_site):
    LINE_API = 'https://api.line.me/v2/bot/message/push'
    Authorization = 'Bearer {}'.format(Token)  ##ที่ยาวๆ
    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'Authorization': Authorization
    }

    data = {
        "to": group_id_site,
        "messages": [push_new_messasge], }
    data = json.dumps(data)
    r = requests.post(LINE_API, headers=headers, data=data)
    return 200