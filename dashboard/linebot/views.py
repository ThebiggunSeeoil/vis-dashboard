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
        if payload['events'][0]['type'] == 'VIS-MONITOR':  # Check if request is VIS-Monitor to update in database
            if payload['events'][0]['update_type'] == 'notify_MWGT_OFFLINE':     #เมื่อมีการ POST แจ้ง MWGT OFFLINE เข้า
                print(payload['events'][0]['data'])
                site_profile = get_site_profile(payload,'notify_MWGT_OFFLINE') #ส่งไป get data profile ที่ connect_db_profile
                SaveRecord= SaveRecordStatusErrorLogger(payload)
                result_calculate_time = different_time_calculate(timezone.now(),site_profile[1].MWGT_last_time) #ส่งไปทำงานที่ linebot/calculate เพือ get data ต่างๆที่เกี่ยวข้องกับเวลา site_profile[1].MWGT_last_time คือ MWGT ที่ติดต่อได้ครั้้งล่าสุุด)
                line_notify_preparing = Line_Creating_MWGT_OFFLINE(result_calculate_time,site_profile)#ส่งไปทำงานที่ linebot/creating_line_data/Line_Creating_MWGT_OFFLINE ร
                result_notify = send_notify(line_notify_preparing[0], line_notify_preparing[1]) #line_notify_preparing[1] คือ line token index[0] คือ messages ที่ต้องการจะส่ง
                if result_notify == False:  # ถ้าส่ง Line ไม่ผ่านให้เข้ามาด้านล่าง
                    result_save = SaveDataSendLineFailedToBD(site_profile,line_notify_preparing[0]) #ส่งไป line notify data ไป save ที่ linebot/save_data_to_db/SaveDataSendLineFailedToBD
                    if result_save == True :
                        return None
                # print('SaveRecord',SaveRecord)
                return JsonResponse({"Logger_id": SaveRecord.id})# ส่ง id ที่ logger save กลับไปให้เครื่องลูกเพื่อบันทึกเป็น record
            elif payload['events'][0]['update_type'] == 'notify_MWGT_ONLINE': #เมื่อมีการ POST แจ้ง MWGT กลับมา ONLINE แล้ว
                update_status_error = UpdateStatusLoggerBackToOnline(payload) #ส่งค่าที่ได้รับ ไป update ที่ linebot/save_data_to_db/UpdateStatusLoggerBackToOnline
                if update_status_error == True :
                    site_profile = get_site_profile(payload,'notify_MWGT_ONLINE')  # ส่งไป get data profile ที่ connect_db_profile
                    result_calculate_time = different_time_calculate(site_profile[2].Error_stop,site_profile[2].Error_start)  # ส่งไปทำงานที่ linebot/calculate เพือ get data ต่างๆที่เกี่ยวข้องกับเวลา site_profile[1].Error_start คือ MWGT ที่เริ่มมีการ offline)
                    print(result_calculate_time)
                    UpdateRecord   = UpdateRecordStatusErrorLogger(payload)
                    if UpdateRecord == True :
                        line_notify_preparing = Line_Creating_MWGT_ONLINE(result_calculate_time,site_profile)  # ส่งไปทำงานที่ linebot/creating_line_data/Line_Creating_MWGT_ONLINE
                        print(line_notify_preparing)
                        result_notify = send_notify(line_notify_preparing[0], line_notify_preparing[1])  # line_notify_preparing[1] คือ line token index[0] คือ messages ที่ต้องการจะส่ง
                        if result_notify == False:  # ถ้าส่ง Line ไม่ผ่านให้เข้ามาด้านล่าง
                            result_save = SaveDataSendLineFailedToBD(site_profile, line_notify_preparing[0])  # ส่งไป line notify data ไป save ที่ linebot/save_data_to_db/SaveDataSendLineFailedToBD
                            if result_save == True:
                                return None
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
def permission_check(request):
    if request.method == "POST":  # Check if method is POST
        payload = json.loads(request.body.decode('utf-8'))  # Convert data to json
        if payload['events'][0]['type'] == 'VIS-MONITOR':
            try:
                result = Site.objects.select_related().get(
                    station_ip=payload['events'][0]['ip'])  # นำ ip มาเช็คกับตาราง Site และส่งเลข id กลับไปให้
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