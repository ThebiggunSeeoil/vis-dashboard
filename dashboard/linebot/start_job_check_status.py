from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse
from django.http import JsonResponse
from django import template
from linebot.calculate_function import *
import json
import datetime
import requests
from .views import *
from linebot.connect_db_profile import *
from linebot.save_data_to_db  import *
from linebot.creating_line_data import *
from django.utils import timezone
from dateutil.relativedelta import relativedelta, SA, TH
from app.models import Team,Site,Nozzle,Status,Status_Error_logger,VIS_ip_address ,Setup_Config
from django.db.models import OuterRef, Subquery, Count, Min 
from linebot.creating_flex_messages import *
from django.db.models import Q # Q คือโมเดล สำหรับเลืือก data ที่แทน !=


class start_job_check_status :
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
    
    def start_check_battery():
        print ('start check battery')
        try :
            for battery_check in Status.objects.all().filter(site__station_active=True,BATTERY_status_check = 'low') :
                print (battery_check.name_id)
        except :
            print ('Cannot check battery status')
        
    def start_check_device ():
        #Start to check VIS
        # try :
        time_threshold = timezone.now() - datetime.timedelta(hours=1) 
        VIS_TIME_NOW = Status.objects.all().filter(~Q(VIS_status='offline'),site__station_active=True,VIS_last_time__lte=time_threshold).distinct() #values('name_id').distinct() กำหนดให้มีการดึงค่าที่ซ้ำกัน คือค่า name_id มาแค่ 1 ค่า ข้อสำคัญคือใ .values ใส่ได้แค่ 1 ค่าเท่านั้น ~Q(VIS_status='offline') เลือกเป็นค่าที่ไม่เท่ากับ
        for vis_site in VIS_TIME_NOW : # ถ้าพบว่ามี name_id ไหนที่ขาดการ update time เกินค่าที่กำหนดไว้ ให้เข้ามาทำงานต่อด้านล่างนี้ 
            # vis_site.name_id
            try : # หากมีสถานีในมีเวลาเกินกว่าที่กำหนด ให้เข้ามาทำด้านล่างนี้ ด้วยการ Update VIS_status='offline'
                # set_vis_to_offline = Status.objects.filter(name_id=1077).update(VIS_status=vis_site.name_id,Timestramp=timezone.now())
                set_vis_to_offline = Status.objects.filter(name_id=1214).update(VIS_status='offline',Timestramp=timezone.now()) # for local testing
                result_calculate_time = calculate_function.different_time_calculate(timezone.now(),vis_site.VIS_last_time) #ส่งไปทำงานที่ linebot/calculate เพือ get data ต่างๆที่เกี่ยวข้องกับเวลา site_profile[1].MWGT_last_time คือ MWGT ที่ติดต่อได้ครั้้งล่าสุุด)
                # บันทึก VIS OFFLINE ไปที่ DB Status_Error_logger
                # SaveRecord= save_data_to_db.SaveRecordStatusErrorLogger(vis_site.name_id,'VIS-OFFLINE')
                save_data_to_db.SaveRecordStatusErrorLogger(1214,'VIS-OFFLINE') # for local testing
                # บันทึก VIS OFFLINE เรียบร้อยแล้ว ก็ไปทำการ send line notify ต่อ
                creating_line_data.Line_Creating_VIS_OFFLINE(result_calculate_time,vis_site)
                # data = start_job_check_status.send_notify(send_line_notify[0], send_line_notify[1]) #line_notify_preparing[1] คือ line token index[0] คือ messages ที่ต้องการจะส่ง
                # print ('set offline success for ',vis_site.name_id)
                break # for testing
            except Status.DoesNotExist:
                print ('cannot set offline for',vis_site['name_id'])
    # except :
        #     print ('Can not start check vis status')
            
    def start_check_nozzle ():
        #Start to check VIS
        try :
            time_threshold = timezone.now() - datetime.timedelta(hours=1) 
            VIS_TIME_NOW = Status.objects.all().filter(site__station_active=True,Timestramp__lte=time_threshold) #values('name_id').distinct() กำหนดให้มีการดึงค่าที่ซ้ำกัน คือค่า name_id มาแค่ 1 ค่า ข้อสำคัญคือใ .values ใส่ได้แค่ 1 ค่าเท่านั้น ~Q(VIS_status='offline') เลือกเป็นค่าที่ไม่เท่ากับ
            for vis_site in VIS_TIME_NOW : # ถ้าพบว่ามี name_id ไหนที่ขาดการ update time เกินค่าที่กำหนดไว้ ให้เข้ามาทำงานต่อด้านล่างนี้ 
                try : # หากมีสถานีในมีเวลาเกินกว่าที่กำหนด ให้เข้ามาทำด้านล่างนี้ ด้วยการ Update VIS_status='offline'
                    set_vis_to_offline = Status.objects.filter(name_id=vis_site.name_id,NOZZLE_SN=vis_site.NOZZLE_SN,NOZZLE_status=vis_site.NOZZLE_status).update(NOZZLE_status_check='offline')
                    result_calculate_time = calculate_function.different_time_calculate(timezone.now(),vis_site.Timestramp) #ส่งไปทำงานที่ linebot/calculate เพือ get data ต่างๆที่เกี่ยวข้องกับเวลา site_profile[1].MWGT_last_time คือ MWGT ที่ติดต่อได้ครั้้งล่าสุุด)
                    # บันทึก VIS OFFLINE ไปที่ DB Status_Error_logger
                    SaveRecord= save_data_to_db.SaveRecordStatusErrorLogger(vis_site.name_id,'NOZZLE-OFFLINE')
                    # บันทึก VIS OFFLINE เรียบร้อยแล้ว ก็ไปทำการ send line notify ต่อ
                    send_line_notify = creating_line_data.Line_Creating_NOZZLE_OFFLINE(result_calculate_time,vis_site)
                    data = start_job_check_status.send_notify(send_line_notify[0], send_line_notify[1]) #line_notify_preparing[1] คือ line token index[0] คือ messages ที่ต้องการจะส่ง
                    print ('set offline success for ',vis_site.name_id)
                except Status.DoesNotExist:
                    print ('cannot set offline for',vis_site['name_id'])
        except :
            print ('Can not start check vis status')
        #Start to check Battery
        
            
                
        
    
    # 