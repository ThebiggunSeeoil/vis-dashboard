# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse
from django.http import JsonResponse
from django import template
import json
from django.utils import timezone
from dateutil.relativedelta import relativedelta, SA, TH
from app.models import Team,Site,Nozzle,Status,Status_Error_logger,VIS_ip_address ,Setup_Config
from django.db.models import OuterRef, Subquery, Count, Min 

# @login_required(login_url="/login/")
# def index(request):
#
#     context = {}
#     context['segment'] = 'index'
#
#     html_template = loader.get_template( 'index.html' )
#     return HttpResponse(html_template.render(context, request))

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
                                                'BATTERY_status_check':data['NOZZLE_Battery_Status_Volts'],
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
                    value = {'Unit_log_address': GET_VIS_DATA_ALL_CHECK['Unit_log_address'] ,'nozzle':[]}
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

@login_required(login_url="/login/")
def index(request):
    if request.user.is_authenticated:
        VIS_SUM_OFFLINE = Status.objects.filter(VIS_status='offline',site__station_active=True).values('DataUnitMap_IP').annotate(dcount=Count('DataUnitMap_IP')).count()
        MWGT_SUM_OFFLINE = Status.objects.filter(MWGT_status='offline',site__station_active=True).values('DataUnitMap_IP').annotate(dcount=Count('DataUnitMap_IP')).count()
        TOTAL_SITE_ACTIVE = Site.objects.filter(station_active=True).values('station_ip').annotate(dcount=Count('station_ip')).count()
        MWGT_LAST_OFFLINE = Status.objects.filter(MWGT_status='offline',site__station_active=True).latest('Timestramp')
        NOZZLE_OFFLINE = Status.objects.filter(NOZZLE_status_check='offline',site__station_active=True).count()
        NOZZLE_LAST_OFFLINE = Status.objects.filter(NOZZLE_status_check='offline',site__station_active=True).latest('Timestramp')
        BATTERY_OFFLINE = Status.objects.filter(BATTERY_status_check='low', site__station_active=True).count()
        BATTERY_LAST_OFFLINE = Status.objects.filter(BATTERY_status_check='low', site__station_active=True).latest('Timestramp')
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
                time_def_check = different_time_calculate(timezone.now(),data.VIS_last_time)
                vis_result.append({'name':data.site,'ip_address':data.site.station_ip,'type':'VIS',
                                   'NOZZLE_Last_conn':data.NOZZLE_Last_conn,'time_dif':{'day':time_def_check[0],'hour':time_def_check[1],'minutes':time_def_check[2],'hours_deff':time_def_check[3]},
                                    'NOZZLE_Battery_Status':data.NOZZLE_Battery_Status_Volts ,
                                        'TEAM_ID':data.site.team_support.team ,
                                            'TEAM_NAME': data.site.team_support.team_name ,'TIME_UPDATE':timezone.now()})
        for data in GET_MWGT_DATA:
            if data.DataUnitMap_IP not in mwgt_check:
                mwgt_check.append(data.DataUnitMap_IP)
                # vis_check2.append(data)
                time_def_check = different_time_calculate(timezone.now(),data.MWGT_last_time)
                mwgt_result.append({'name':data.site,'ip_address':data.site.station_ip,'type':'MWGT',
                                   'NOZZLE_Last_conn':data.NOZZLE_Last_conn,'time_dif':{'day':time_def_check[0],'hour':time_def_check[1],'minutes':time_def_check[2],'hours_deff':time_def_check[3]},
                                    'NOZZLE_Battery_Status':data.NOZZLE_Battery_Status_Volts ,
                                        'TEAM_ID':data.site.team_support.team ,
                                            'TEAM_NAME': data.site.team_support.team_name , 'TIME_UPDATE':timezone.now()})
                # print('mwgt_result',mwgt_result)
        for data in GET_NOZZLE_DATA:
            time_def_check = different_time_calculate(timezone.now(),data.MWGT_last_time)
            # print('time_def_check',time_def_check)
            # print('time',data.MWGT_last_time)
            nozzle_result.append({'name':data.site,'ip_address':data.site.station_ip,'type':'NOZZLE',
                               'NOZZLE_Last_conn':data.NOZZLE_Last_conn,'time_dif':{'day':time_def_check[0],'hour':time_def_check[1],'minutes':time_def_check[2],'hours_deff':time_def_check[3]},
                                'NOZZLE_Battery_Status':data.NOZZLE_Battery_Status_Volts ,
                                    'TEAM_ID':data.site.team_support.team ,
                                        'TEAM_NAME': data.site.team_support.team_name , 'NOZZLE_pump_log_address':data.NOZZLE_pump_log_address , 'NOZZLE_num':data.NOZZLE_num , 'TIME_UPDATE':timezone.now()})
            # print('mwgt_result',nozzle_result)
        for data in GET_BATTERY_DATA:
            time_def_check = different_time_calculate(timezone.now(),data.MWGT_last_time)
            battery_result.append({'name':data.site,'ip_address':data.site.station_ip,'type':'BATT',
                               'NOZZLE_Last_conn':data.NOZZLE_Last_conn,'time_dif':{'day':time_def_check[0],'hour':time_def_check[1],'minutes':time_def_check[2],'hours_deff':time_def_check[3]},
                                'NOZZLE_Battery_Status':data.NOZZLE_Battery_Status_Volts ,
                                    'TEAM_ID':data.site.team_support.team ,
                                        'TEAM_NAME': data.site.team_support.team_name , 'NOZZLE_pump_log_address':data.NOZZLE_pump_log_address , 'NOZZLE_num':data.NOZZLE_num , 'TIME_UPDATE':timezone.now()})
            # print('mwgt_result',battery_result)
        return render(request,'index.html',{'TIME_UPDATE':timezone.now(),'VIS_SUM_OFFLINE':VIS_SUM_OFFLINE,'MWGT_SUM_OFFLINE':MWGT_SUM_OFFLINE,
                                                'TOTAL_SITE_ACTIVE':TOTAL_SITE_ACTIVE,'MWGT_LAST_OFFLINE':MWGT_LAST_OFFLINE,'NOZZLE_OFFLINE':NOZZLE_OFFLINE,
                                                    'NOZZLE_LAST_OFFLINE':NOZZLE_LAST_OFFLINE,'BATTERY_OFFLINE':BATTERY_OFFLINE,'BATTERY_LAST_OFFLINE':BATTERY_LAST_OFFLINE,
                                                        'VIS_DETAIL':vis_result ,'MWTG_DETAIL':mwgt_result ,'NOZZLE_DETAIL':nozzle_result ,'BATTERY_DETAIL':battery_result, 
                                                            'time_alert_alarm_hours':time_alert_alarm_hours,'time_alert_warning_hours':time_alert_warning_hours,'battery_level_alarm_volt':battery_level_alarm_volt,
                                                                'battery_level_low_volt':battery_level_low_volt,'battery_level_failed_volt':battery_level_failed_volt})

@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:
        
        load_template      = request.path.split('/')[-1]
        context['segment'] = load_template
        
        html_template = loader.get_template( load_template )
        return HttpResponse(html_template.render(context, request))
        
    except template.TemplateDoesNotExist:

        html_template = loader.get_template( 'page-404.html' )
        return HttpResponse(html_template.render(context, request))

    except:
    
        html_template = loader.get_template( 'page-500.html' )
        return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def visstatus(request):
    data = []
    data_site_name_id = Status.objects.values('name_id', 'site__station_name','site__station_ip','site__station_monitor_device' ,'MWGT_status','VIS_status','NOZZLE_status_check','NOZZLE_Battery_Status_Volts','VIS_last_time','Unit_log_address').annotate(dcount=Count('Unit_log_address')).filter(site__station_active=True).order_by('name_id')
    data_status = Status.objects.values().filter(site__station_active=True)
    nozzle_count = Nozzle.objects.values().filter(site__station_active=True)
    results = prepare_nozzle(data_site_name_id, data_status,nozzle_count)
    # nozzle_count = Nozzle.objects.values().filter(data_unit_ip='10.23.32.114',site__station_active=True)
    # for i in nozzle_count :
    #     print(i)
    return render (request,'vis-status.html',{'sites_data':results , 'TIME_UPDATE':timezone.now()})

@login_required(login_url="/login/")
def visstatus_test(request):
    return render (request,'vis-backup.html')
    # return render (request,'backup2.html')

def search (request):
    search =request.GET['title']
    data_site_name_id = Status.objects.values('name_id', 'site__station_name', 'site__station_ip',
                                              'site__station_monitor_device', 'MWGT_status', 'VIS_status',
                                              'NOZZLE_status_check', 'NOZZLE_Battery_Status_Volts', 'VIS_last_time',
                                              'Unit_log_address').annotate(dcount=Count('Unit_log_address')).filter(site__station_name__contains=search,
        site__station_active=True).order_by('name_id')
    data_status = Status.objects.values().filter(site__station_name__contains=search,site__station_active=True)
    nozzle_count = Nozzle.objects.values().filter(site__station_active=True)
    results = prepare_nozzle(data_site_name_id, data_status,nozzle_count)
    return render (request,'vis-status.html',{'sites_data':results , 'TIME_UPDATE':timezone.now()})