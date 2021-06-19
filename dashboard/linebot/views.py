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
from linebot.connect_data_to_db import *
from linebot.convert_xml import *
from linebot.calculate_function import *
from linebot.connect_db_profile import *
from linebot.start_job_check_status import *
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
                        User_id = payloads['events'][0]['source']['userId']
                        user_type = PersanalDetaillogin.objects.filter(line_id=User_id).first()
                        if message == 'new_register':
                            ReplyMessage(line_templates.register_code())
                        elif message == 'GetAllStatus':
                            ReplyMessage(connect_data_to_db.RequestDataDBForMGR())
                        elif message == 'vis_status':
                            if user_type.user_type.id == 6 : #6 คือ id ของ technician
                                ReplyMessage(connect_data_to_db.RequestDataDBForTechnician(user_type,message))
                            if user_type.user_type.id != 6 : # กรณีเป็น user ทั่่วไปที่ไม่ใช่ technician
                                ReplyMessage(connect_data_to_db.RequestDataDBForAllUser(user_type,message))
                        elif message == 'mwgt_status':
                            if user_type.user_type.id == 6 : #6 คือ id ของ technician
                                ReplyMessage(connect_data_to_db.RequestDataDBForTechnician(user_type,message))
                            if user_type.user_type.id != 6 : # กรณีเป็น user ทั่่วไปที่ไม่ใช่ technician
                                ReplyMessage(connect_data_to_db.RequestDataDBForAllUser(user_type,message))
                        elif message == 'nozzle_status':
                            if user_type.user_type.id == 6 : #6 คือ id ของ technician
                                ReplyMessage(connect_data_to_db.RequestDataDBForTechnician(user_type,message))
                            if user_type.user_type.id != 6 : # กรณีเป็น user ทั่่วไปที่ไม่ใช่ technician
                                ReplyMessage(connect_data_to_db.RequestDataDBForAllUser(user_type,message))
                        elif message == 'battery_status':
                            if user_type.user_type.id == 6 : #6 คือ id ของ technician
                                ReplyMessage(connect_data_to_db.RequestDataDBForTechnician(user_type,message))
                            if user_type.user_type.id != 6 : # กรณีเป็น user ทั่่วไปที่ไม่ใช่ technician
                                ReplyMessage(connect_data_to_db.RequestDataDBForAllUser(user_type,message))
                        elif message == 'TechGetAllStatus':
                            if user_type.user_type.id == 6 : #6 คือ id ของ technician
                                ReplyMessage(connect_data_to_db.RequestAllDataForTechnician(user_type,message))
                            if user_type.user_type.id != 6 : # กรณีเป็น user ทั่่วไปที่ไม่ใช่ technician
                                ReplyMessage(connect_data_to_db.RequestAllDataForAllUser(user_type,message))
                        elif message == 'register':
                            User_id = payloads['events'][0]['source']['userId']
                            user_type = PersanalDetaillogin.objects.filter(line_id=User_id).first()
                            if user_type.member_status == True:
                                try:
                                    User_id = payloads['events'][0]['source']['userId']
                                    if user_type != None:
                                        print('user_type check pass')
                                        if str(user_type.user_type) in ('customer', 'manager', 'user'):
                                            Link_rich_menu_to_user(settings.SECOND_LEVEL, user_type.line_id)
                                            updaterich_menu = PersanalDetaillogin.objects.filter(line_id=User_id).update(richmenu_id=settings.SECOND_LEVEL)
                                            ReplyMessage(line_templates.login())
                                        elif str(user_type.user_type) in ('call center', 'supervisor', 'technician'):
                                            Link_rich_menu_to_user(settings.FIRST_LEVEL, user_type.line_id)
                                            updaterich_menu = PersanalDetaillogin.objects.filter(line_id=User_id).update(richmenu_id=settings.FIRST_LEVEL)
                                            ReplyMessage(line_templates.login())
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
                                if user_type != None:
                                    if str(user_type.user_type) in ('customer', 'manager', 'user'):
                                        print('user  is manager ')
                                        Link_rich_menu_to_user(settings.FIRST_MENU, user_type.line_id)
                                        updaterich_menu = PersanalDetaillogin.objects.filter(line_id=User_id).update(richmenu_id=settings.FIRST_MENU)
                                        ReplyMessage(line_templates.logout())
                                    elif str(user_type.user_type) in ('call center', 'supervisor', 'technician'):
                                        Link_rich_menu_to_user(settings.FIRST_MENU, user_type.line_id)
                                        updaterich_menu = PersanalDetaillogin.objects.filter(line_id=User_id).update(richmenu_id=settings.FIRST_MENU)
                                        ReplyMessage(line_templates.logout())
                                else:
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
                        User_id = payloads['events'][0]['source']['userId']
                        user_type = PersanalDetaillogin.objects.filter(line_id=User_id).first()
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
                        elif (message[0:5]).lower() == 'check':
                            ip_address_request = (message[5:])
                            ReplyMessage(connect_data_to_db.RequestDataDBByUserRequestByIpAddress(user_type,ip_address_request))
                        elif message in ('list','รายชื่อ'):
                            print (message)
                            # ip_address_request = (message[5:])
                            # ReplyMessage(connect_data_to_db.RequestDataDBByUserRequestByIpAddress(user_type,ip_address_request))
    return HttpResponse(200)


@csrf_exempt  # this is used for avoid csrf request from line server
def updatedb(request):
    if request.method == "POST":  # Check if method is POST
        payload = json.loads(request.body.decode('utf-8'))  # Convert data to json
        if payload['events'][0]['type'] == 'VIS-MONITOR': # Check if request is VIS-Monitor to update in database
            if payload['events'][0]['update_type'] == 'update_all':
                # data_convert = convert_xml_json(payload)
                update_MWGT_AllData = convert_xml.convert_xml_json(payload)
                get_last_vis_status = connect_data_to_db.RequestLastVisStatusRecord(payload)#เข้าไปขอ สถานะ vis_status ล่าสุดเพื่อส่งไปที่ VIS console
                print ('vis last status ',get_last_vis_status)
                # print ('update_MWGT_AllData ',update_MWGT_AllData)
                # return HttpResponse(200)
                return JsonResponse({"vis_status": get_last_vis_status })# ส่ง id ที่ logger save กลับไปให้เครื่องลูกเพื่อบันทึกเป็น record
            elif payload['events'][0]['update_type'] == 'get_status':
                get_last_vis_status = connect_data_to_db.RequestLastVisStatusRecord(payload)#เข้าไปขอ สถานะ vis_status ล่าสุดเพื่อส่งไปที่ VIS console
                print ('vis last status ',get_last_vis_status)
                return JsonResponse({"vis_status": get_last_vis_status })# ส่ง id ที่ logger save กลับไปให้เครื่องลูกเพื่อบันทึกเป็น record
            # ทำการ Update ให้เป็น offline
            elif payload['events'][0]['update_type'] == 'update_MWGT_OFFLINE':
                update_MWGT_OFFLINE = save_data_to_db.UpdateMWGT_OFFLINE(payload)
                # if update_MWGT_OFFLINE == True:
                #     return None
            # ทำการ Update ให้เป็น online
            elif payload['events'][0]['update_type'] == 'update_MWGT_ONLINE':
                update_MWGT_ONLINE = save_data_to_db.UpdateMWGT_ONLINE(payload)
                # if update_MWGT_ONLINE == True:
                #     return None
                # print(payload)
            # ทำการ Update ให้เป็น online
            elif payload['events'][0]['update_type'] == 'update_VIS_ONLINE':
                update_VIS_ONLINE = save_data_to_db.UpdateVIS_ONLINE(payload)
                # if update_VIS_ONLINE == True:
                #     return None
                # print(payload)
            # แจ้งเตือน line notify ไปที่ line group at OFFLINE
            elif payload['events'][0]['update_type'] == 'notify_MWGT_OFFLINE':     #เมื่อมีการ POST แจ้ง MWGT OFFLINE เข้า
                print(payload['events'][0]['data'])
                site_profile = connect_db_profile.get_site_profile(payload,'notify_MWGT_OFFLINE') #ส่งไป get data profile ที่ connect_db_profile
                SaveRecord= save_data_to_db.SaveRecordStatusErrorLogger(site_profile[1].name_id,'MWGT-OFFLINE') #ส่งค่า 'MWGT-OFFLINE' ไป save ลง DB
                result_calculate_time = calculate_function.different_time_calculate(timezone.now(),site_profile[1].MWGT_last_time) #ส่งไปทำงานที่ linebot/calculate เพือ get data ต่างๆที่เกี่ยวข้องกับเวลา site_profile[1].MWGT_last_time คือ MWGT ที่ติดต่อได้ครั้้งล่าสุุด)
                line_notify_preparing = creating_line_data.Line_Creating_MWGT_OFFLINE(result_calculate_time,site_profile)#ส่งไปทำงานที่ linebot/creating_line_data/Line_Creating_MWGT_OFFLINE ร
                # result_notify = send_notify(line_notify_preparing[0], line_notify_preparing[1]) #line_notify_preparing[1] คือ line token index[0] คือ messages ที่ต้องการจะส่ง
                if line_notify_preparing == False:  # ถ้าส่ง Line ไม่ผ่านให้เข้ามาด้านล่าง
                    result_save = save_data_to_db.SaveDataSendLineFailedToBD(site_profile,line_notify_preparing[0]) #ส่งไป line notify data ไป save ที่ linebot/save_data_to_db/SaveDataSendLineFailedToBD
                    if result_save == True :
                        return None
                # print('SaveRecord',SaveRecord)
                return JsonResponse({"Logger_id": SaveRecord.id})# ส่ง id ที่ logger save กลับไปให้เครื่องลูกเพื่อบันทึกเป็น record
            # แจ้งเตือน line notify ไปที่ line group at BACK TO ONLINE
            elif payload['events'][0]['update_type'] == 'notify_MWGT_ONLINE': #เมื่อมีการ POST แจ้ง MWGT กลับมา ONLINE แล้ว
                update_status_error = save_data_to_db.UpdateStatusLoggerBackToOnline(payload) #ส่งค่าที่ได้รับ ไป update ที่ linebot/save_data_to_db/UpdateStatusLoggerBackToOnline
                if update_status_error == True :
                    site_profile = connect_db_profile.get_site_profile(payload,'notify_MWGT_ONLINE')  # ส่งไป get data profile ที่ connect_db_profile
                    result_calculate_time = calculate_function.different_time_calculate(site_profile[2].Error_stop,site_profile[2].Error_start)  # ส่งไปทำงานที่ linebot/calculate เพือ get data ต่างๆที่เกี่ยวข้องกับเวลา site_profile[1].Error_start คือ MWGT ที่เริ่มมีการ offline)
                    print(result_calculate_time)
                    # UpdateRecord   = save_data_to_db.UpdateRecordStatusErrorLogger(payload)
                    # if UpdateRecord == True :
                    line_notify_preparing = creating_line_data.Line_Creating_MWGT_ONLINE(result_calculate_time,site_profile)  # ส่งไปทำงานที่ linebot/creating_line_data/Line_Creating_MWGT_ONLINE
                    # print(line_notify_preparing)
                    # result_notify = send_notify(line_notify_preparing[0], line_notify_preparing[1])  # line_notify_preparing[1] คือ line token index[0] คือ messages ที่ต้องการจะส่ง
                    if line_notify_preparing == False:  # ถ้าส่ง Line ไม่ผ่านให้เข้ามาด้านล่าง
                        result_save = save_data_to_db.SaveDataSendLineFailedToBD(site_profile, line_notify_preparing[0])  # ส่งไป line notify data ไป save ที่ linebot/save_data_to_db/SaveDataSendLineFailedToBD
                        if result_save == True:
                            return None
                return HttpResponse (200)
            elif payload['events'][0]['update_type'] == 'notify_VIS_ONLINE': #เมื่อมีการ POST แจ้ง MWGT กลับมา ONLINE แล้ว
                update_status_error = save_data_to_db.UpdateStatusVISBackToOnline(payload) #ส่งค่าที่ได้รับ ไป update ที่ linebot/save_data_to_db/UpdateStatusLoggerBackToOnline
                if update_status_error == True :
                    site_profile = connect_db_profile.get_site_profile(payload,'notify_VIS_ONLINE')  # ส่งไป get data profile ที่ connect_db_profile
                    result_calculate_time = calculate_function.different_time_calculate(site_profile[2].Error_stop,site_profile[2].Error_start)  # ส่งไปทำงานที่ linebot/calculate เพือ get data ต่างๆที่เกี่ยวข้องกับเวลา site_profile[1].Error_start คือ MWGT ที่เริ่มมีการ offline)
                    print(result_calculate_time)
                    # UpdateRecord   = save_data_to_db.UpdateRecordStatusErrorLogger(payload)
                    # if UpdateRecord == True :
                    line_notify_preparing = creating_line_data.Line_Creating_VIS_ONLINE(result_calculate_time,site_profile)  # ส่งไปทำงานที่ linebot/creating_line_data/Line_Creating_MWGT_ONLINE
                    # print(line_notify_preparing)
                    # result_notify = send_notify(line_notify_preparing[0], line_notify_preparing[1])  # line_notify_preparing[1] คือ line token index[0] คือ messages ที่ต้องการจะส่ง
                    if line_notify_preparing == False:  # ถ้าส่ง Line ไม่ผ่านให้เข้ามาด้านล่าง
                        result_save = save_data_to_db.SaveDataSendLineFailedToBD(site_profile, line_notify_preparing[0])  # ส่งไป line notify data ไป save ที่ linebot/save_data_to_db/SaveDataSendLineFailedToBD
                        if result_save == True:
                            return None
                return HttpResponse (200)
    
    
    return HttpResponse(200)

@csrf_exempt
def task_jobs(request): # ส่วนสำหรับ job ในการเช็คสถานะ VIS Nozzle Battery
    if request.method == "POST":  # Check if method is POST
        payload = json.loads(request.body.decode('utf-8'))  # Convert data to json
        if payload['events'][0]['type'] == 'TASK_JOBS':
            JOB = payload['events'][0]['job_request']
            if JOB  == 'start_check_device' :
                start_job_check_status.start_check_device()
            elif JOB  == 'check_nozzle' :
                start_job_check_status.start_check_nozzle()
            
        
    return HttpResponse (200)

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
                update_BATTEY_Data = save_data_to_db.UpdateBatteryStatus(payload)
                if update_BATTEY_Data == 200:
                    return HttpResponse(200)
                # return HttpResponse (200)

@csrf_exempt  # this is used for avoid csrf request from line server
def permission_check(request):
    if request.method == "POST":  # Check if method is POST
        payload = json.loads(request.body.decode('utf-8'))  # Convert data to json
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
