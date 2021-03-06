from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse
from django.http import JsonResponse
from django import template
import json
import datetime
from django.utils import timezone
from dateutil.relativedelta import relativedelta, SA, TH
from app.models import Team,Site,Nozzle,Status,Status_Error_logger,VIS_ip_address ,Setup_Config
from django.db.models import OuterRef, Subquery, Count, Min 
from linebot.creating_flex_messages import *

class connect_data_to_db ():
    def prepare_nozzle (GET_VIS_DATA,GET_VIS_DATA_ALL,NOZZLE) :
        vis_check = [] #สำหรับเก็บค่า name_id เพื่อป้องกันไม่ให้มีการบันทึกซ้ำ
        vis_result = []
        #ส่วนสำหรับ นำค่าที่ได้จากตาราง site ที่เป็น name_id เอามาเพิ่มข้อมูล 'Unit_log_address':[] เข้าไปเพื่อใช้ในการเก็บข้อมูลของ nozzle
        for data in GET_VIS_DATA:
            # print(data)
            if data['name_id'] not in vis_check:  # ทำการเช็คว่า name_id มีเก็บไว้ใน vis_check = [] หรือไม่ถ้ายังไม่มีก็จะทำข้างล่างจนเสร็จก่อน แล้วค่อยนำ name_id ไปบันทึกไว้เพื่อป้องกันการ loop รอบอื่นๆมาทำซ้ำอีก
                vis_check.append(data['name_id'])  # ทำการนำ name_id ไปบันทึกไว้ที่ vis_check = []
                data = {'name_id': data['name_id'],
                        'log_address_check': [],
                        'pump_log_address_check': [],
                        'nozzle_data_check': [],
                        'log_address_count': [],
                        'pump_log_address_count': [],
                        'nozzle_data_count': [],
                        'site_name':data['site__station_name'],
                            'station_ip':data['site__station_ip'],
                                'station_monitor_device': data['site__station_monitor_device'],
                                        'MWGT_status':data['MWGT_status'],
                                            'VIS_status':data['VIS_status'],
                                                'NOZZLE_status_check':data['NOZZLE_status_check'],
                                                    'BATTERY_status_check':data['BATTERY_status_check'],
                                                        'VIS_last_time':data['VIS_last_time'],
                                                            
                        'Unit_log_address': []}  # สร้างข้อมูลไว้ สำหรับโยนเข้าไปเก็บไว้ใน vis_result = []
                vis_result.append(data)  # นำ data ไปเก็บไว้ใน vis_result = [] เพื่อเอาไปใช้ใน function อื่น
        # for vis_1 in vis_result :
        #     print('vis 1 ',vis_1)
        for name_id in vis_result:
            for data in NOZZLE:
                if data['site_id'] == name_id['name_id']:
                    name_id['nozzle_data_check'].append(data['nozzle_num'])
                    if data['pump_log_address'] not in name_id['pump_log_address_check']:
                        name_id['pump_log_address_check'].append(data['pump_log_address'])
                    if data['log_address'] not in name_id['log_address_check']:
                        name_id['log_address_check'].append(data['log_address'])
            for count in vis_result:
                count_log = len(count['pump_log_address_check'])
                count_num = len(count['nozzle_data_check'])
                count_log_main = len(count['log_address_check'])
                count['pump_log_address_count'] = count_log
                count['nozzle_data_count'] = count_num
                count['log_address_count'] = count_log_main

        GET_VIS_DATA_ALL_CHECK_STORE = [] #สำหรับเก็บค่า Unit_log_address เพื่อป้องกันไม่ให้มีการบันทึกซ้ำ
        for Unit_check in vis_result :
            for GET_VIS_DATA_ALL_CHECK in GET_VIS_DATA_ALL :
                log_check = str(GET_VIS_DATA_ALL_CHECK['name_id']) + str(GET_VIS_DATA_ALL_CHECK['Unit_log_address'])
                if GET_VIS_DATA_ALL_CHECK['name_id'] == Unit_check['name_id']:
                    if log_check not in GET_VIS_DATA_ALL_CHECK_STORE:
                        GET_VIS_DATA_ALL_CHECK_STORE.append(log_check)
                        value = {'Unit_log_address': GET_VIS_DATA_ALL_CHECK['Unit_log_address'],'DataUnitMap_IP': GET_VIS_DATA_ALL_CHECK['DataUnitMap_IP'] ,'nozzle':[]}
                        Unit_check['Unit_log_address'].append(value)

        GET_NOZZLE_CHECK_STORE = [] #สำหรับเก็บค่า Unit_log_address เพื่อป้องกันไม่ให้มีการบันทึกซ้ำ
        for nozzle_check in vis_result  :
            for GET_VIS_DATA_ALL_CHECK in GET_VIS_DATA_ALL:
                if GET_VIS_DATA_ALL_CHECK['name_id'] == nozzle_check['name_id']:
                    log_check = str(GET_VIS_DATA_ALL_CHECK['name_id']) + str(GET_VIS_DATA_ALL_CHECK['Unit_log_address'])
                    value = {'Unit_log_address': GET_VIS_DATA_ALL_CHECK['Unit_log_address'] ,'nozzle':[]}
                    for nozzle_loop in nozzle_check['Unit_log_address'] :
                        if nozzle_loop['Unit_log_address'] == GET_VIS_DATA_ALL_CHECK['Unit_log_address']:
                            nozzle_loop['nozzle'].append(GET_VIS_DATA_ALL_CHECK)
        # print(vis_result)
        return (vis_result)
    def RequestDataDBByUserRequestByIpAddress(user_type,ip_address_request):
        data = []
        data_site_name_id = Status.objects.values('name_id', 'site__station_name','site__station_ip','site__station_monitor_device' ,'MWGT_status','VIS_status','NOZZLE_status_check','BATTERY_status_check','VIS_last_time','Unit_log_address').annotate(dcount=Count('Unit_log_address')).filter(site__station_active=True,site__station_ip=ip_address_request).order_by('name_id')
        data_status = Status.objects.values().filter(site__station_active=True,site__station_ip=ip_address_request)
        nozzle_count = Nozzle.objects.values().filter(site__station_active=True,site__station_ip=ip_address_request)
        results = connect_data_to_db.prepare_nozzle(data_site_name_id, data_status,nozzle_count)
        return creating_flex_messages.CreateFormDetailByIpAddress(results)  
    def different_time_calculate(TimeZone,TimeCalculate):
        # print(TimeCalculate)
        # TimeCalculateDetail = TimeCalculate[1].MWGT_last_time
        # print('TimeCalculateDetail',TimeCalculate)
        different_time = relativedelta(TimeZone,TimeCalculate)  # คำนวณหาผลต่างระหว่างวันที่ Now กับ MWGT_last_time
        day_loss = different_time.days  # แสดงผลลัพท์เป็นจำนวนวัน จาก different_time
        hours_loss = different_time.hours  # แสดงผลลัพท์เป็นจำนวน ชั่วโมง จาก different_time
        minutes_loss = different_time.minutes  # แสดงผลลัพท์เป็นจำนวนวัน นาที different_time
        hours_count = TimeZone - TimeCalculate
        hours_def = hours_count.total_seconds()
        hours_deff = (hours_def/60)/60 # คำนวณผลต่างของเวลามให้แสดงผลในรูปแบบชั่วโมง
        # print (hours_deff)
        # datetime_now = datetime.datetime.now().strftime("%d-%m-%y %H:%M")
        # MWGT_last_time = TimeCalculate.strftime("%d-%m-%y %H:%M")    # แปลง datetime
        # print('TimeCalculateDetail',TimeCalculate)
        # print('different_time',different_time)
        # print('day_loss',day_loss)
        # print('hours_loss',hours_loss)
        # print('minutes_loss',minutes_loss)
        # print('datetime_now',datetime_now)
        # print('MWGT_last_time',MWGT_last_time)
        return day_loss , hours_loss , minutes_loss , hours_deff 
    def RequestDataDBForMGR():
        dt = datetime.datetime.now().strftime("%d-%m-%d %H:%M")
        VIS_SUM_OFFLINE = Status.objects.filter(VIS_status='offline',site__station_active=True).values('DataUnitMap_IP').annotate(dcount=Count('DataUnitMap_IP')).count()
        MWGT_SUM_OFFLINE = Status.objects.filter(MWGT_status='offline',site__station_active=True).values('DataUnitMap_IP').annotate(dcount=Count('DataUnitMap_IP')).count()
        TOTAL_SITE_ACTIVE = Site.objects.filter(station_active=True).values('station_ip').annotate(dcount=Count('station_ip')).count()
        NOZZLE_OFFLINE = Status.objects.filter(NOZZLE_status_check='offline',site__station_active=True).count()
        BATTERY_OFFLINE = Status.objects.filter(BATTERY_status_check='low', site__station_active=True).count()
        return creating_flex_messages.CreateFormAllStatusForMGR(dt,VIS_SUM_OFFLINE,MWGT_SUM_OFFLINE,NOZZLE_OFFLINE,BATTERY_OFFLINE,TOTAL_SITE_ACTIVE)
    def RequestAllDataForTechnician(user_type,message):
        dt = datetime.datetime.now().strftime("%d-%m-%d %H:%M")
        VIS_SUM_OFFLINE = Status.objects.filter(VIS_status='offline',site__station_active=True,site__team_support=user_type.if_technician).values('DataUnitMap_IP').annotate(dcount=Count('DataUnitMap_IP')).count()
        MWGT_SUM_OFFLINE = Status.objects.filter(MWGT_status='offline',site__station_active=True,site__team_support=user_type.if_technician).values('DataUnitMap_IP').annotate(dcount=Count('DataUnitMap_IP')).count()
        TOTAL_SITE_ACTIVE = Site.objects.filter(station_active=True,team_support=user_type.if_technician).values('station_ip').annotate(dcount=Count('station_ip')).count()
        NOZZLE_OFFLINE = Status.objects.filter(NOZZLE_status_check='offline',site__station_active=True,site__team_support=user_type.if_technician).count()
        BATTERY_OFFLINE = Status.objects.filter(BATTERY_status_check='low', site__station_active=True,site__team_support=user_type.if_technician).count()
        return creating_flex_messages.CreateFormAllStatusForFirstLevel(dt,VIS_SUM_OFFLINE,MWGT_SUM_OFFLINE,NOZZLE_OFFLINE,BATTERY_OFFLINE,TOTAL_SITE_ACTIVE,user_type)
    def RequestAllDataForAllUser(user_type,message):
        dt = datetime.datetime.now().strftime("%d-%m-%d %H:%M")
        VIS_SUM_OFFLINE = Status.objects.filter(VIS_status='offline',site__station_active=True).values('DataUnitMap_IP').annotate(dcount=Count('DataUnitMap_IP')).count()
        MWGT_SUM_OFFLINE = Status.objects.filter(MWGT_status='offline',site__station_active=True).values('DataUnitMap_IP').annotate(dcount=Count('DataUnitMap_IP')).count()
        TOTAL_SITE_ACTIVE = Site.objects.filter(station_active=True).values('station_ip').annotate(dcount=Count('station_ip')).count()
        NOZZLE_OFFLINE = Status.objects.filter(NOZZLE_status_check='offline',site__station_active=True).count()
        BATTERY_OFFLINE = Status.objects.filter(BATTERY_status_check='low', site__station_active=True).count()
        return creating_flex_messages.CreateFormAllStatusForFirstLevel(dt,VIS_SUM_OFFLINE,MWGT_SUM_OFFLINE,NOZZLE_OFFLINE,BATTERY_OFFLINE,TOTAL_SITE_ACTIVE,user_type)
    def RequestDataDBForTechnician(user_type,message):
        VIS_SUM_OFFLINE = Status.objects.filter(VIS_status='offline',site__station_active=True,site__team_support=user_type.if_technician).values('DataUnitMap_IP').annotate(dcount=Count('DataUnitMap_IP')).count()
        MWGT_SUM_OFFLINE = Status.objects.filter(MWGT_status='offline',site__station_active=True,site__team_support=user_type.if_technician).values('DataUnitMap_IP').annotate(dcount=Count('DataUnitMap_IP')).count()
        if message in ('nozzle_status','battery_status') :
            TOTAL_SITE_ACTIVE = Nozzle.objects.filter(site__station_active=True,active_nozzle=True,site__team_support=user_type.if_technician).values('id').count()
        if message not in ('nozzle_status','battery_status') :
            TOTAL_SITE_ACTIVE = Site.objects.filter(station_active=True,team_support=user_type.if_technician).values('station_ip').annotate(dcount=Count('station_ip')).count()
        # MWGT_LAST_OFFLINE = Status.objects.filter(MWGT_status='offline',site__station_active=True).latest('Timestramp')
        NOZZLE_OFFLINE = Status.objects.filter(NOZZLE_status_check='offline',site__station_active=True,site__team_support=user_type.if_technician).count()
        # NOZZLE_LAST_OFFLINE = Status.objects.filter(NOZZLE_status_check='offline',site__station_active=True).latest('Timestramp')
        BATTERY_OFFLINE = Status.objects.filter(BATTERY_status_check='low', site__station_active=True,site__team_support=user_type.if_technician).count()
        # BATTERY_LAST_OFFLINE = Status.objects.filter(BATTERY_status_check='low', site__station_active=True).latest('Timestramp')
        GET_VIS_DATA = Status.objects.select_related('site').filter(VIS_status='offline',site__station_active=True,site__team_support=user_type.if_technician)
        GET_MWGT_DATA = Status.objects.select_related('site').filter(MWGT_status='offline', site__station_active=True,site__team_support=user_type.if_technician)
        GET_NOZZLE_DATA = Status.objects.select_related('site').filter(NOZZLE_status_check='offline', site__station_active=True,site__team_support=user_type.if_technician)
        GET_BATTERY_DATA = Status.objects.select_related('site').filter(BATTERY_status_check='low',site__station_active=True,site__team_support=user_type.if_technician)
        STATUS_CONFIG = Setup_Config.objects.values()
        for setup_config in STATUS_CONFIG :
            time_alert_alarm_hours = setup_config['time_alert_alarm_hours']
            time_alert_warning_hours = setup_config['time_alert_warning_hours']
            battery_level_alarm_volt = setup_config['battery_level_alarm_volt']
            battery_level_low_volt = setup_config['battery_level_low_volt']
            battery_level_failed_volt = setup_config['battery_level_failed_volt']
        data_store = []
        vis_check = []
        mwgt_check = []
        vis_result = []
        mwgt_result = []
        nozzle_result = []
        battery_result = []
        for data in GET_VIS_DATA:
            if data.DataUnitMap_IP not in vis_check:
                vis_check.append(data.DataUnitMap_IP)
                # vis_check2.append(data)
                time_def_check = connect_data_to_db.different_time_calculate(timezone.now(),data.VIS_last_time)
                vis_result.append({'name':data.site,'ip_address':data.site.station_ip,'type':'VIS',
                                    'NOZZLE_Last_conn':data.NOZZLE_Last_conn,'time_dif':{'day':time_def_check[0],'hour':time_def_check[1],'minutes':time_def_check[2],'hours_deff':time_def_check[3]},
                                    'NOZZLE_Battery_Status':data.NOZZLE_Battery_Status_Volts ,
                                        'TEAM_ID':data.site.team_support.team ,
                                            'TEAM_NAME': data.site.team_support.team_name , 'VIS_last_time':data.VIS_last_time,
                                                'TIME_UPDATE':timezone.now()})
        for data in GET_MWGT_DATA:
            if data.DataUnitMap_IP not in mwgt_check:
                mwgt_check.append(data.DataUnitMap_IP)
                # vis_check2.append(data)
                time_def_check = connect_data_to_db.different_time_calculate(timezone.now(),data.MWGT_last_time)
                mwgt_result.append({'name':data.site,'ip_address':data.site.station_ip,'type':'MWGT',
                                    'NOZZLE_Last_conn':data.NOZZLE_Last_conn,'time_dif':{'day':time_def_check[0],'hour':time_def_check[1],'minutes':time_def_check[2],'hours_deff':time_def_check[3]},
                                    'NOZZLE_Battery_Status':data.NOZZLE_Battery_Status_Volts ,'MWGT_last_time':data.MWGT_last_time,
                                        'TEAM_ID':data.site.team_support.team ,
                                            'TEAM_NAME': data.site.team_support.team_name , 'DataUnitMap_IP':data.DataUnitMap_IP,
                                                'MWGT_last_time':data.MWGT_last_time,'TIME_UPDATE':timezone.now()})
                # print('mwgt_result',mwgt_result)
        for data in GET_NOZZLE_DATA:
            time_def_check = connect_data_to_db.different_time_calculate(timezone.now(),data.MWGT_last_time)
            # print('time_def_check',time_def_check)
            # print('time',data.MWGT_last_time)
            nozzle_result.append({'name':data.site,'ip_address':data.site.station_ip,'type':'NOZZLE',
                                'NOZZLE_Last_conn':data.NOZZLE_Last_conn,'time_dif':{'day':time_def_check[0],'hour':time_def_check[1],'minutes':time_def_check[2],'hours_deff':time_def_check[3]},
                                'NOZZLE_Battery_Status':data.NOZZLE_Battery_Status_Volts ,
                                    'TEAM_ID':data.site.team_support.team ,'VIS_last_time':data.VIS_last_time,'Unit_log_address':data.Unit_log_address,
                                        'TEAM_NAME': data.site.team_support.team_name , 'NOZZLE_pump_log_address':data.NOZZLE_pump_log_address , 'NOZZLE_num':data.NOZZLE_num , 'TIME_UPDATE':timezone.now()})
            # print('mwgt_result',nozzle_result)
        for data in GET_BATTERY_DATA:
            time_def_check = connect_data_to_db.different_time_calculate(timezone.now(),data.MWGT_last_time)
            battery_result.append({'name':data.site,'ip_address':data.site.station_ip,'type':'BATT',
                                'NOZZLE_Last_conn':data.NOZZLE_Last_conn,'time_dif':{'day':time_def_check[0],'hour':time_def_check[1],'minutes':time_def_check[2],'hours_deff':time_def_check[3]},
                                'NOZZLE_Battery_Status':data.NOZZLE_Battery_Status_Volts ,
                                    'TEAM_ID':data.site.team_support.team ,'BATTERY_status_check':data.BATTERY_status_check,'NOZZLE_SN':data.NOZZLE_SN,
                                        'NOZZLE_Battery_Status_Volts':data.NOZZLE_Battery_Status_Volts,'TEAM_NAME': data.site.team_support.team_name , 'NOZZLE_pump_log_address':data.NOZZLE_pump_log_address , 'NOZZLE_num':data.NOZZLE_num , 'TIME_UPDATE':timezone.now()})
            # print('mwgt_result',battery_result)
        data = {'user_type':user_type,'TIME_UPDATE':timezone.now(),'VIS_SUM_OFFLINE':VIS_SUM_OFFLINE,'MWGT_SUM_OFFLINE':MWGT_SUM_OFFLINE,
                                                'TOTAL_SITE_ACTIVE':TOTAL_SITE_ACTIVE,'NOZZLE_OFFLINE':NOZZLE_OFFLINE,
                                                    'BATTERY_OFFLINE':BATTERY_OFFLINE,
                                                        'VIS_DETAIL':vis_result ,'MWTG_DETAIL':mwgt_result ,'NOZZLE_DETAIL':nozzle_result ,'BATTERY_DETAIL':battery_result, 
                                                            'time_alert_alarm_hours':time_alert_alarm_hours,'time_alert_warning_hours':time_alert_warning_hours,'battery_level_alarm_volt':battery_level_alarm_volt,
                                                                'battery_level_low_volt':battery_level_low_volt,'battery_level_failed_volt':battery_level_failed_volt}
        if message == 'vis_status' :
            return creating_flex_messages.CreateFormVisFlexMessageDetail(data,user_type)
        elif message == 'mwgt_status' :
            return creating_flex_messages.CreateFormMwgtFlexMessageDetail(data,user_type)
        elif message == 'nozzle_status':
            return creating_flex_messages.CreateFormNozzleFlexMessageDetail(data,user_type)
        elif message == 'battery_status':
            return creating_flex_messages.CreateFormBatteryFlexMessageDetail(data,user_type)
    def RequestLastVisStatusRecord(name_id): # สำหรับเช็ค status vis ล่าสุดเพื่อตอบกลับไปให้เครื่อง VIS ดำเนินการต่อ
        # for vis_check in (payload):  # Loop each nozzle for update into database
        name_id = name_id['events'][0]['name_id']
        try :
            vis_last_status = Status.objects.filter(name_id=name_id).values('VIS_status').distinct().first()
            if vis_last_status != None :
                return vis_last_status['VIS_status'] # หากค้นหาข้อมูลเจอ หรือเคยมีการบันทึกไว้ก่อนหน้า
            else :
                vis_last_status = 'not_found'
                return vis_last_status # หากค้นหาไม่เจอ หรือ สถานีใหม่ ที่ยังไม่เคยรับข้อมูลเข้า
            # for i in vis_last_status :
            #     print (i)
            # return vis_last_status['VIS_status'] # สำหรับเช็ค status vis ล่าสุดเพื่อตอบกลับไปให้เครื่อง VIS ดำเนินการต่อ
        except Status.DoesNotExist:
            print ('Cannot sent battery back to Decive')
    def RequestDataDBForAllUser(user_type,message):
        VIS_SUM_OFFLINE = Status.objects.filter(VIS_status='offline',site__station_active=True).values('DataUnitMap_IP').annotate(dcount=Count('DataUnitMap_IP')).count()
        MWGT_SUM_OFFLINE = Status.objects.filter(MWGT_status='offline',site__station_active=True).values('DataUnitMap_IP').annotate(dcount=Count('DataUnitMap_IP')).count()
        if message in ('nozzle_status','battery_status') :
            TOTAL_SITE_ACTIVE = Nozzle.objects.filter(site__station_active=True,active_nozzle=True,).values('id').count()
        if message not in ('nozzle_status','battery_status') :
            TOTAL_SITE_ACTIVE = Site.objects.filter(station_active=True).values('station_ip').annotate(dcount=Count('station_ip')).count()
        # MWGT_LAST_OFFLINE = Status.objects.filter(MWGT_status='offline',site__station_active=True).latest('Timestramp')
        # MWGT_LAST_OFFLINE = Status.objects.filter(MWGT_status='offline',site__station_active=True).latest('Timestramp')
        NOZZLE_OFFLINE = Status.objects.filter(NOZZLE_status_check='offline',site__station_active=True).count()
        # NOZZLE_LAST_OFFLINE = Status.objects.filter(NOZZLE_status_check='offline',site__station_active=True).latest('Timestramp')
        BATTERY_OFFLINE = Status.objects.filter(BATTERY_status_check='low', site__station_active=True).count()
        # BATTERY_LAST_OFFLINE = Status.objects.filter(BATTERY_status_check='low', site__station_active=True).latest('Timestramp')
        GET_VIS_DATA = Status.objects.select_related('site').filter(VIS_status='offline',site__station_active=True)
        GET_MWGT_DATA = Status.objects.select_related('site').filter(MWGT_status='offline', site__station_active=True)
        GET_NOZZLE_DATA = Status.objects.select_related('site').filter(NOZZLE_status_check='offline', site__station_active=True)
        GET_BATTERY_DATA = Status.objects.select_related('site').filter(BATTERY_status_check='low',site__station_active=True)
        STATUS_CONFIG = Setup_Config.objects.values()
        for setup_config in STATUS_CONFIG :
            time_alert_alarm_hours = setup_config['time_alert_alarm_hours']
            time_alert_warning_hours = setup_config['time_alert_warning_hours']
            battery_level_alarm_volt = setup_config['battery_level_alarm_volt']
            battery_level_low_volt = setup_config['battery_level_low_volt']
            battery_level_failed_volt = setup_config['battery_level_failed_volt']
        data_store = []
        vis_check = []
        mwgt_check = []
        vis_result = []
        mwgt_result = []
        nozzle_result = []
        battery_result = []
        for data in GET_VIS_DATA:
            if data.DataUnitMap_IP not in vis_check:
                vis_check.append(data.DataUnitMap_IP)
                # vis_check2.append(data)
                time_def_check = connect_data_to_db.different_time_calculate(timezone.now(),data.VIS_last_time)
                vis_result.append({'name':data.site,'ip_address':data.site.station_ip,'type':'VIS',
                                    'NOZZLE_Last_conn':data.NOZZLE_Last_conn,'time_dif':{'day':time_def_check[0],'hour':time_def_check[1],'minutes':time_def_check[2],'hours_deff':time_def_check[3]},
                                    'NOZZLE_Battery_Status':data.NOZZLE_Battery_Status_Volts ,
                                        'TEAM_ID':data.site.team_support.team ,
                                            'TEAM_NAME': data.site.team_support.team_name , 'VIS_last_time':data.VIS_last_time,
                                                'TIME_UPDATE':timezone.now()})
        for data in GET_MWGT_DATA:
            if data.DataUnitMap_IP not in mwgt_check:
                mwgt_check.append(data.DataUnitMap_IP)
                # vis_check2.append(data)
                time_def_check = connect_data_to_db.different_time_calculate(timezone.now(),data.MWGT_last_time)
                mwgt_result.append({'name':data.site,'ip_address':data.site.station_ip,'type':'MWGT',
                                    'NOZZLE_Last_conn':data.NOZZLE_Last_conn,'time_dif':{'day':time_def_check[0],'hour':time_def_check[1],'minutes':time_def_check[2],'hours_deff':time_def_check[3]},
                                    'NOZZLE_Battery_Status':data.NOZZLE_Battery_Status_Volts ,
                                        'TEAM_ID':data.site.team_support.team ,'DataUnitMap_IP':data.DataUnitMap_IP,'MWGT_last_time':data.MWGT_last_time,
                                            'TEAM_NAME': data.site.team_support.team_name , 'TIME_UPDATE':timezone.now()})
                # print('mwgt_result',mwgt_result)
        for data in GET_NOZZLE_DATA:
            time_def_check = connect_data_to_db.different_time_calculate(timezone.now(),data.MWGT_last_time)
            # print('time_def_check',time_def_check)
            # print('time',data.MWGT_last_time)
            nozzle_result.append({'name':data.site,'ip_address':data.site.station_ip,'type':'NOZZLE',
                                'NOZZLE_Last_conn':data.NOZZLE_Last_conn,'time_dif':{'day':time_def_check[0],'hour':time_def_check[1],'minutes':time_def_check[2],'hours_deff':time_def_check[3]},
                                'NOZZLE_Battery_Status':data.NOZZLE_Battery_Status_Volts ,
                                    'TEAM_ID':data.site.team_support.team ,'VIS_last_time':data.VIS_last_time,'Unit_log_address':data.Unit_log_address,
                                        'TEAM_NAME': data.site.team_support.team_name , 'NOZZLE_pump_log_address':data.NOZZLE_pump_log_address , 'NOZZLE_num':data.NOZZLE_num , 'TIME_UPDATE':timezone.now()})
            # print('mwgt_result',nozzle_result)
        for data in GET_BATTERY_DATA:
            time_def_check = connect_data_to_db.different_time_calculate(timezone.now(),data.MWGT_last_time)
            battery_result.append({'name':data.site,'ip_address':data.site.station_ip,'type':'BATT',
                                'NOZZLE_Last_conn':data.NOZZLE_Last_conn,'time_dif':{'day':time_def_check[0],'hour':time_def_check[1],'minutes':time_def_check[2],'hours_deff':time_def_check[3]},
                                'NOZZLE_Battery_Status':data.NOZZLE_Battery_Status_Volts ,'NOZZLE_SN':data.NOZZLE_SN,
                                    'TEAM_ID':data.site.team_support.team , 'BATTERY_status_check':data.BATTERY_status_check,'NOZZLE_Battery_Status_Volts':data.NOZZLE_Battery_Status_Volts,
                                        'TEAM_NAME': data.site.team_support.team_name , 'NOZZLE_pump_log_address':data.NOZZLE_pump_log_address , 'NOZZLE_num':data.NOZZLE_num , 'TIME_UPDATE':timezone.now()})
            # print('mwgt_result',battery_result)
        data = {'user_type':user_type,'TIME_UPDATE':timezone.now(),'VIS_SUM_OFFLINE':VIS_SUM_OFFLINE,'MWGT_SUM_OFFLINE':MWGT_SUM_OFFLINE,
                                                'TOTAL_SITE_ACTIVE':TOTAL_SITE_ACTIVE,'NOZZLE_OFFLINE':NOZZLE_OFFLINE,
                                                    'BATTERY_OFFLINE':BATTERY_OFFLINE,
                                                        'VIS_DETAIL':vis_result ,'MWTG_DETAIL':mwgt_result ,'NOZZLE_DETAIL':nozzle_result ,'BATTERY_DETAIL':battery_result, 
                                                            'time_alert_alarm_hours':time_alert_alarm_hours,'time_alert_warning_hours':time_alert_warning_hours,'battery_level_alarm_volt':battery_level_alarm_volt,
                                                                'battery_level_low_volt':battery_level_low_volt,'battery_level_failed_volt':battery_level_failed_volt}
        if message == 'vis_status' :
            return creating_flex_messages.CreateFormVisFlexMessageDetail(data,user_type)
        elif message == 'mwgt_status' :
            return creating_flex_messages.CreateFormMwgtFlexMessageDetail(data,user_type)
        elif message == 'nozzle_status':
            return creating_flex_messages.CreateFormNozzleFlexMessageDetail(data,user_type)
        elif message == 'battery_status':
            return creating_flex_messages.CreateFormBatteryFlexMessageDetail(data,user_type)