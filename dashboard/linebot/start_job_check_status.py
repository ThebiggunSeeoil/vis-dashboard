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
from django.db.models import Q # Q คือโมเดล สำหรับเลืือก data ที่แทน !=


class start_job_check_status :
    def start_check_battery():
        print ('start check battery')
        try :
            for battery_check in Status.objects.all().filter(site__station_active=True,BATTERY_status_check = 'low') :
                print (battery_check.name_id)
        except :
            print ('Cannot check battery status')
        
    def start_check_vis ():
        time_threshold = timezone.now() - datetime.timedelta(hours=1)
        VIS_TIME_NOW = Status.objects.all().filter(~Q(VIS_status='offline'),site__station_active=True,VIS_last_time__lte=time_threshold).values('name_id').distinct() #values('name_id').distinct() กำหนดให้มีการดึงค่าที่ซ้ำกัน คือค่า name_id มาแค่ 1 ค่า ข้อสำคัญคือใ .values ใส่ได้แค่ 1 ค่าเท่านั้น ~Q(VIS_status='offline') เลือกเป็นค่าที่ไม่เท่ากับ
        for vis_site in VIS_TIME_NOW : # ถ้าพบว่ามี name_id ไหนที่ขาดการ update time เกินค่าที่กำหนดไว้ ให้เข้ามาทำงานต่อด้านล่างนี้ 
            try :
                set_vis_to_offline = Status.objects.filter(name_id=vis_site['name_id']).update(VIS_status='offline',Timestramp=timezone.now())
                print ('set offline success for ',vis_site['name_id'])
            except Status.DoesNotExist:
                print ('cannot set offline for',vis_site['name_id'])      
        return 200
    
    