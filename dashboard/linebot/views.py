# -*- coding: utf-8 -*-
# !/usr/bin/env python
import time
from django.conf import settings
# calls the object written in settings.py
from django.db.models.fields import AutoField
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from linebot.rich_menu_function import *
import requests
from django.utils import timezone
from linebot.save_data_to_db import *
from linebot.creating_line_data import *
from linebot.creating_flex_messages import *
from linebot.convert_xml import *
from linebot.calculate_function import *
from linebot.connect_db_profile import *
from linebot.line_tamplates import *
from app.models import Site, Status, Status_Error_logger, Store_data_send_line_failed, PersanalDetaillogin
from django.db.models import OuterRef, Subquery, Count, Min 
Channel_access_token = settings.LINE_CHANNEL_ACCESS_TOKEN
def index(request):
    return HttpResponse("test!!")

@csrf_exempt  # this is used for avoid csrf request from line server
def callback(request):  # สำหรับส่งการแจ้งเตือนต่างไปที่ Line Notify and Line Bot
    if request.method == "POST":  # Check if method is POST
        payload = json.loads(request.body.decode('utf-8'))  # Convert data to json
        print('first payload', payload)
        global name
        global company
        if len(payload['events']) == 0:
            print('Message from server to Verify')
            return HttpResponse(200)
        else:
            payloads = json.loads(request.body.decode('utf-8'))
            payload = {'events': []}
            global Reply_token
            global User_id
            Reply_token = payloads['events'][0]['replyToken']
            # User_id = payloads['events'][0]['source']['userId']
            # วน loop เพื่อเช็คว่า ทีการส่ง request postback มาหรือไม่
            for payload_check in payloads['events']:
                if 'postback' in payload_check['type']:
                    payload['events'].insert(-1, payload_check)
                    if payload['events'][0]['type'] == 'postback':
                        message = payload['events'][0]['postback']['data']
                        if message == 'new_register':
                            ReplyMessage(line_templates.register_code())
                        elif message == 'GetAllStatus':
                            dt = datetime.datetime.now().strftime("%d-%m-%d %H:%M")
                            VIS_SUM_OFFLINE = Status.objects.filter(VIS_status='offline',site__station_active=True).values('DataUnitMap_IP').annotate(dcount=Count('DataUnitMap_IP')).count()
                            MWGT_SUM_OFFLINE = Status.objects.filter(MWGT_status='offline',site__station_active=True).values('DataUnitMap_IP').annotate(dcount=Count('DataUnitMap_IP')).count()
                            TOTAL_SITE_ACTIVE = Site.objects.filter(station_active=True).values('station_ip').annotate(dcount=Count('station_ip')).count()
                            NOZZLE_OFFLINE = Status.objects.filter(NOZZLE_status_check='offline',site__station_active=True).count()
                            BATTERY_OFFLINE = Status.objects.filter(BATTERY_status_check='low', site__station_active=True).count()
                            update_vis = CreateAllStatusVIS(dt,VIS_SUM_OFFLINE,MWGT_SUM_OFFLINE,NOZZLE_OFFLINE,BATTERY_OFFLINE,TOTAL_SITE_ACTIVE)
                            ReplyMessage(update_vis)
                            print ('GetAllStatus')
                        elif message == 'vis_status':
                            User_id = payloads['events'][0]['source']['userId']
                            user_type = PersanalDetaillogin.objects.filter(line_id=User_id).first()
                            print ('user_id ',User_id)
                            print ('name is',user_type.name)
                            print ('user type',user_type.user_type)
                            print ('user team',user_type.if_technician)
                        elif message == 'register':
                            User_id = payloads['events'][0]['source']['userId']
                            # active_user = PersanalDetaillogin.objects.values('member_status').filter(line_id=User_id).first()
                            user_type = PersanalDetaillogin.objects.filter(line_id=User_id).first()
                            # print ('user_type is',user_type.user_type)
                            if user_type.member_status == True:
                                print('user active ok')
                                try:
                                    User_id = payloads['events'][0]['source']['userId']
                                    # id_user = PersanalDetaillogin.objects.filter(line_id=User_id).first()
                                    if user_type != None:
                                        print('user_type check pass')
                                        if str(user_type.user_type) in ('customer', 'manager', 'user'):
                                            print('user  is manager ')
                                            Link_rich_menu_to_user(settings.SECOND_LEVEL, user_type.line_id)
                                            updaterich_menu = PersanalDetaillogin.objects.filter(line_id=User_id).update(richmenu_id=settings.SECOND_LEVEL)
                                            ReplyMessage(line_templates.login())
                                        elif str(user_type.user_type) in ('call center', 'supervisor', 'technician'):
                                            print('user  is normal ')
                                            Link_rich_menu_to_user(settings.FIRST_LEVEL, user_type.line_id)
                                            updaterich_menu = PersanalDetaillogin.objects.filter(line_id=User_id).update(richmenu_id=settings.FIRST_LEVEL)
                                            ReplyMessage(line_templates.login())
                                        print('end')
                                    else:
                                        print('NOT OK user_id')
                                        ReplyMessage(line_templates.re่ject_not_register())
                                except PersanalDetaillogin.DoesNotExist:
                                    print('NO DATA user_id')
                            else:
                                print('active_user is', user_type.user_type)
                                ReplyMessage(line_templates.re่ject_not_register())
                        elif message == 'REGISTER-OK':
                            User_id = payloads['events'][0]['source']['userId']
                            # ส่ง user_id ไปที่ line server เพื่อขอ name id
                            data_user = Get_profile(User_id)
                            # รับค่า display name
                            user_id_display_name = data_user['displayName']
                            register_user = PersanalDetaillogin.objects.filter(name=name, company=company).update(member_status=True, line_id=User_id, line_id_name=user_id_display_name)
                            ReplyMessage(line_templates.registed())
                        elif message == 'logout':
                            try:
                                User_id = payloads['events'][0]['source']['userId']
                                user_type = PersanalDetaillogin.objects.filter(line_id=User_id).first()
                                # id_user = PersanalDetaillogin.objects.filter(line_id=User_id).first()
                                if user_type != None:
                                    print('user_type check pass')
                                    if str(user_type.user_type) in ('customer', 'manager', 'user'):
                                        print('user  is manager ')
                                        Link_rich_menu_to_user(settings.FIRST_MENU, user_type.line_id)
                                        updaterich_menu = PersanalDetaillogin.objects.filter(line_id=User_id).update(richmenu_id=settings.FIRST_MENU)
                                        ReplyMessage(line_templates.logout())
                                    elif str(user_type.user_type) in ('call center', 'supervisor', 'technician'):
                                        print('user  is normal ')
                                        Link_rich_menu_to_user(settings.FIRST_MENU, user_type.line_id)
                                        updaterich_menu = PersanalDetaillogin.objects.filter(line_id=User_id).update(richmenu_id=settings.FIRST_MENU)
                                        ReplyMessage(line_templates.logout())
                                    print('end')
                                else:
                                    print('NOT OK user_id')
                                    ReplyMessage(line_templates.re่ject_not_register())
                            except PersanalDetaillogin.DoesNotExist:
                                print('NO DATA user_id')
                        return HttpResponse(200)
            for payload_check in payloads['events']:
                if 'postback' not in payload_check['type']:
                    payload['events'].insert(-1, payload_check)
                    if payload['events'][0]['type'] == 'follow':
                        ReplyMessage(line_templates.Gressing_msg())
                        return HttpResponse(200)
                    elif payload['events'][0]['type'] == 'join':
                        group_id = payloads['events'][0]['source']['groupId']
                        group_line_name = Get_groupProfile(group_id)
                        CreateLineGroup(payload, group_line_name['groupName'])
                        return HttpResponse(200)
                    elif payload['events'][0]['type'] == 'leave':
                        print('BOT Leaved ')
                        return HttpResponse(200)
                    elif payload['events'][0]['type'] == 'message':
                        message = payload['events'][0]['message']['text']
                        print('message is', message)
                        if (message[0:5]).lower() == 'orpak':
                            print(message)
                            command_payload = ((payload['events'][0]['message']['text'])[0:5]).lower()+((payload['events'][0]['message']['text'])[5:])
                            print(command_payload)
                            code_login = (command_payload[5:])
                            print('code login is', code_login)
                            try:
                                id_user = PersanalDetaillogin.objects.filter(key_login=code_login).first()
                                if id_user != None:
                                    if id_user.member_status == False:
                                        name = id_user.name
                                        company = id_user.company
                                        ReplyMessage(line_templates.ensure_submit(id_user))
                                    else:
                                        ReplyMessage(line_templates.alreadySubmit_code(id_user))
                                else:
                                    ReplyMessage(line_templates.re่ject_code())
                            except PersanalDetaillogin.DoesNotExist:
                                ReplyMessage(line_templates.re่ject_code())
                                return None
    return HttpResponse(200)


@csrf_exempt  # this is used for avoid csrf request from line server
def updatedb(request):
    if request.method == "POST":  # Check if method is POST
        payload = json.loads(request.body.decode('utf-8'))  # Convert data to json
        # Check if request is VIS-Monitor to update in database
        if payload['events'][0]['type'] == 'VIS-MONITOR':
            if payload['events'][0]['update_type'] == 'update_all':
                # print(payload)
                data_convert = convert_xml_json(payload)
                update_MWGT_AllData = UpdateAllDataMWGT(data_convert)
                if update_MWGT_AllData == 200:
                    return 200
            # ทำการ Update ให้เป็น offline
            elif payload['events'][0]['update_type'] == 'update_MWGT_OFFLINE':
                update_MWGT_OFFLINE = UpdateMWGT_OFFLINE(payload)
                if update_MWGT_OFFLINE == True:
                    return None
            # ทำการ Update ให้เป็น online
            elif payload['events'][0]['update_type'] == 'update_MWGT_ONLINE':
                update_MWGT_ONLINE = UpdateMWGT_ONLINE(payload)
                if update_MWGT_ONLINE == True:
                    return None
                print(payload)
    return HttpResponse(200)


@csrf_exempt  # this is used for avoid csrf request from line server
def update_battery(request):  # function สำหรับการ update สถานะ แบตเตอร์รี่ ไปที่ data base
    if request.method == "POST":  # Check if method is POST
        payload = json.loads(request.body.decode('utf-8'))  # Convert data to json
        name_id = payload['events'][0]['name_id']
        # print (payload)
        # Check if request is VIS-Monitor to update in database
        if payload['events'][0]['type'] == 'VIS-MONITOR':
            # Check request ว่าใช่ update_battery หรือไม่
            if payload['events'][0]['update_type'] == 'update_battery':
                # print(payload)
                update_BATTEY_Data = UpdateBatteryStatus(payload)
                if update_BATTEY_Data == 200:
                    return HttpResponse(200)
                # return HttpResponse (200)


@csrf_exempt  # this is used for avoid csrf request from line server
def permission_check(request):
    if request.method == "POST":  # Check if method is POST
        payload = json.loads(request.body.decode('utf-8')
                             )  # Convert data to json
        if payload['events'][0]['type'] == 'VIS-MONITOR':
            try:
                # นำ ip มาเช็คกับตาราง Site และส่งเลข id กลับไปให้
                result = Site.objects.select_related().get(
                    station_ip=payload['events'][0]['ip'])
                # return JsonResponse({"site_id": result.id,
                #                      "password": result.station_password,
                #                      "station_monitor_device": result.station_monitor_device,
                #                      "nozzles_activate": result.nozzle_mapping.nozzles_activate})  # ส่งเลข id กลับไปให้
                return JsonResponse({"site_id": result.id,
                                        "password": result.station_password,
                                            "station_monitor_device": result.station_monitor_device})  # ส่งเลข id กลับไปให้
            except Site.DoesNotExist:
                # ส่งเลข failed กลับไปให้เนื่องจากไม่พบเลข ip ที่ส่งเข้า
                return JsonResponse({"site_id": "failed"})
    return HttpResponse(200)


def Get_profile(User_ID):
    LINE_API = 'https://api.line.me/v2/bot/profile/' + User_ID
    Authorization = 'Bearer {}'.format(Channel_access_token)
    headers = {'Authorization': Authorization, }
    r = requests.get(LINE_API, headers=headers)
    data = r.json()
    print('Already setup defult richmenu', data)
    return data


def Get_groupProfile(GroupId):
    LINE_API = 'https://api.line.me/v2/bot/group/' + GroupId+'/summary'
    Authorization = 'Bearer {}'.format(Channel_access_token)
    headers = {'Authorization': Authorization, }
    r = requests.get(LINE_API, headers=headers)
    data = r.json()
    # print('Already setup defult richmenu', data)
    return data


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
        headers = {'content-type': 'application/x-www-form-urlencoded',
                        'Authorization': LINE_ACCESS_TOKEN}
        r = requests.post(url, headers=headers, data={'message': message})
        print(r.text)
        return True
    except requests.ConnectionError as err:
        print("Connected to Line notify fail")
        return False


def PushMessage_group(push_new_messasge, Token, group_id_site):
    LINE_API = 'https://api.line.me/v2/bot/message/push'
    Authorization = 'Bearer {}'.format(Token)  # ที่ยาวๆ
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
