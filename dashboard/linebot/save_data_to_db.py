# สำหรับบันทึกข้อมูลที่ต้องการลงไปที่ DB
from django.utils import timezone
import dateutil.parser
import datetime
from app.models import Site, Status , Status_Error_logger,Store_data_send_line_failed,battery_status,LinegroupId
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden, JsonResponse
from dateutil.relativedelta import relativedelta, SA, TH
def SaveDataSendLineFailedToBD (request,site_profile): # สำหรับ save ข้อมูล line notify ที่ไม่สามารถส่งได้
    result_site = site_profile[0]
    result_status = site_profile[1]
    message_save = request
    try :
        save_record = Store_data_send_line_failed()
        save_record.site = result_site.name
        save_record.name_id = result_site.name_id
        save_record.team_name = result_site.team_support.team
        save_record.date_failed = timezone.now()
        save_record.messages = message_save
        save_record.status_send = 'failed'
        save_record.save(request)
        return True
    except :
        print('Cannot SaveDataSendLineFailedToBD')
        return False

def SaveRecordStatusErrorLogger (request): #สำหรับ save record สำหรับ ERROR ต่างๆ
    try :
        # บันทึก Error ไปที่ database
        payload = request
        save_record = Status_Error_logger()
        save_record.site_id = payload['events'][0]['data']
        save_record.name_id = payload['events'][0]['data']
        save_record.Error_type = 'MWGT-ERROR'
        save_record.Error_start = timezone.now()
        save_record.Timestramp = timezone.now()
        save_record.save(request)
        return  save_record # return save_record ออกไปเพื่อให้ return ID ล่าสุดที่ทำการบันทึกออกไป
    except :
        print('Cannot SaveRecordStatusErrorLogger /linebot/save_data_to_db/')

def UpdateRecordStatusErrorLogger (request): #สำหรับ save record สำหรับ ERROR ต่างๆ
    try:
        Status_Error_logger.objects.filter(id=request['events'][0]['Logger_id']).update(Error_stop=timezone.now()) # ทำการ Update Error_stop time ไปที่ db
        # Do something such send line notify
        print("Update MWGT Back to ONLINE Succeed ")
        return True
    except Status.DoesNotExist:
        # Do something such send line notify
        print('Cannot UpdateRecordStatusErrorLogger /linebot/save_data_to_db/')
        return False

def UpdateStatusLoggerBackToOnline(request):
    try :
        payload = request
        print(payload)
        print(payload['events'][0]['data'])
        print(payload['events'][0]['Logger_id'])
        Status_Error_logger.objects.filter(id=payload['events'][0]['Logger_id']).update(Error_stop=timezone.now()) # ทำการ Update Error_stop time ไปที่ db
        # Do something such send line notify
        print("Update MWGT Back to ONLINE Succeed /linebot/save_data_to_db/UpdateStatusLoggerBackToOnline ")
        return True
    except Status.DoesNotExist:
        # Do something such send line notify
        print("Don't find site id for update MWGT Failed ")
        return False

def UpdateMWGT_OFFLINE(request):
    payload = request
    try:
        Status.objects.filter(name_id=payload['events'][0]['site_id']).update(MWGT_status='offline',Timestramp=timezone.now())
        # Do something such send line notify
        print("Update MWGT Failed Succeed ")
        return True
    except Status.DoesNotExist:
        # Do something such send line notify
        print("Don't find site id for update MWGT Failed ")
        return False

def UpdateMWGT_ONLINE(request):
    payload = request
    try:
        Status.objects.filter(name_id=payload['events'][0]['site_id']).update(MWGT_status='online',Timestramp=timezone.now())
        # Do something such send line notify
        print("Update MWGT Online Succeed ")
        return True
    except Status.DoesNotExist:
        # Do something such send line notify
        print("Don't find site id for update MWGT Failed ")
        return False

def UpdateAllDataMWGT(request):
    payload = request
    print ('payload nozzle is',request)
    for data_nozzle in (payload):  # Loop each nozzle for update into database
        try:
            # Check if nozzle already in db or not if YES go next step
            prepare_data = Status.objects.get(name_id=data_nozzle['name_id'],
                                              NOZZLE_pump_log_address=data_nozzle['pump_log_address'],
                                              NOZZLE_num=data_nozzle['nozzle_num'])
            # Update each filed into db
            Status.objects.filter(name_id=prepare_data.name_id,
                                  NOZZLE_pump_log_address=prepare_data.NOZZLE_pump_log_address,
                                  NOZZLE_num=prepare_data.NOZZLE_num).update(
                                        name_id=data_nozzle['name_id'],
                                        MWGT_last_time=timezone.now(),
                                        VIS_last_time=timezone.now(),
                                        MWGT_status=data_nozzle['MWGT_status'],
                                        VIS_status=data_nozzle['VIS_status'],
                                        RTC=data_nozzle['RTC'],
                                        DESC=data_nozzle['DESC'],
                                        DataUnitMap_Status=data_nozzle['DataUnitMap_Status'],
                                        DataUnitMap_StatusDesc=data_nozzle['DataUnitMap_StatusDesc'],
                                        DataUnitMap_IP=data_nozzle['DataUnitMap_IP'],
                                        Unit_log_LgAddr=data_nozzle['Unit_log_LgAddr'],
                                        Unit_log_address=data_nozzle['Unit_log_address'],
                                        Unit_GWTypS=data_nozzle['Unit_GWTypS'],
                                        Unit_sw_location=data_nozzle['Unit_sw_location'],
                                        Unit_sw_version=data_nozzle['Unit_sw_version'],
                                        Unit_hw_version=data_nozzle['Unit_hw_version'],
                                        Unit_status_code=data_nozzle['Unit_status_code'],
                                        Unit_status_desc=data_nozzle['Unit_status_desc'],
                                        NOZZLE_pump_log_address=data_nozzle['pump_log_address'],
                                        NOZZLE_num=data_nozzle['nozzle_num'],
                                        NOZZLE_status=data_nozzle['nozzle_status'],
                                        NOZZLE_SW_Version=data_nozzle['sw_version'],
                                        NOZZLE_HW_Version=data_nozzle['hw_version'],
                                        NOZZLE_SN=data_nozzle['SN'],
                                        NOZZLE_Last_conn=data_nozzle['last_conn'],
                                        NOZZLE_Battery_Status=data_nozzle['battery_status'],
                                        NOZZLE_Battery_BatPrcnt=data_nozzle['BatPrcnt'],
                                        site_id=data_nozzle['site_id'],
                                        Timestramp=timezone.now())
        except Status.DoesNotExist:  # Check if nozzle already in db or not if NO go next step to insert into
            save_record = Status()
            save_record.name_id = data_nozzle['name_id']
            save_record.MWGT_last_time = timezone.now()
            save_record.VIS_last_time = timezone.now()
            save_record.MWGT_status = data_nozzle['MWGT_status']
            save_record.VIS_status = data_nozzle['VIS_status']
            save_record.RTC = data_nozzle['RTC']
            save_record.DESC = data_nozzle['DESC']
            save_record.DataUnitMap_Status = data_nozzle['DataUnitMap_Status']
            save_record.DataUnitMap_StatusDesc = data_nozzle['DataUnitMap_StatusDesc']
            save_record.DataUnitMap_IP = data_nozzle['DataUnitMap_IP']
            save_record.Unit_log_LgAddr = data_nozzle['Unit_log_LgAddr']
            save_record.Unit_log_address = data_nozzle['Unit_log_address']
            save_record.Unit_GWTypS = data_nozzle['Unit_GWTypS']
            save_record.Unit_sw_location = data_nozzle['Unit_sw_location']
            save_record.Unit_sw_version = data_nozzle['Unit_sw_version']
            save_record.Unit_hw_version = data_nozzle['Unit_hw_version']
            save_record.Unit_status_code = data_nozzle['Unit_status_code']
            save_record.Unit_status_desc = data_nozzle['Unit_status_desc']
            save_record.NOZZLE_pump_log_address = data_nozzle['pump_log_address']
            save_record.NOZZLE_num = data_nozzle['nozzle_num']
            save_record.NOZZLE_status = data_nozzle['nozzle_status']
            save_record.NOZZLE_SW_Version = data_nozzle['sw_version']
            save_record.NOZZLE_HW_Version = data_nozzle['hw_version']
            save_record.NOZZLE_SN = data_nozzle['SN']
            save_record.NOZZLE_Last_conn = data_nozzle['last_conn']
            save_record.NOZZLE_Battery_Status = data_nozzle['battery_status']
            save_record.NOZZLE_Battery_BatPrcnt = data_nozzle['BatPrcnt']
            save_record.site_id = data_nozzle['site_id']
            save_record.save(request)
    return HttpResponse(200)  # Response back to request

def UpdateBatteryStatus(request):
    payload = request['events'][0]['battery_detail']
    name_id = request['events'][0]['name_id']
    print ('payload battery is',payload)
    for data_battery in payload :  # Loop each nozzle for update into database
        new_date_stamp = datetime.datetime.now().strftime("%Y") + str((data_battery['date_stamp'][2:]))
        # new_date_stamp ใช้สำหรับแปลงปี 21 ที่ส่งมาให้เป็น 2021 ตาม sql server format
        try:
            # Check if battery already in db or not if YES go next step
            prepare_data = battery_status.objects.get(name_id=name_id,
                                                            date_stamp=new_date_stamp,
                                                                    sn=data_battery['SN'])
            # If duplicate data no need to insert to db
            print ('Duplicate data battery ')
            
        except battery_status.DoesNotExist:  # Check if battery already in db or not if NO go next step to insert into
            save_record = battery_status()
            save_record.site_id = name_id
            save_record.name_id = name_id
            save_record.date_stamp = new_date_stamp
            save_record.mac = data_battery['MAC']
            save_record.sn = data_battery['SN']
            save_record.fwtype = data_battery['FwType']
            save_record.version = data_battery['Ver']
            save_record.devtype = data_battery['DevType']
            save_record.din = data_battery['DIN']
            save_record.battery_vcclevel = data_battery['Battery_VccLevel']
            save_record.battery_level = data_battery['BatLevel']
            save_record.temp = data_battery['Temp']
            save_record.fwu = data_battery['FWU']
            save_record.save(request)

        # ทำการ update สถานะ battery ไปที่ Status
        # print (data_battery['SN'])
        # print (data_battery['SN'].strip())
        # print (len(data_battery['SN']))
        # print (len(data_battery['SN'].strip()))
        try :
            update_battery_to_status = Status.objects.filter(name_id=name_id,NOZZLE_SN=data_battery['SN'].strip()).update(NOZZLE_Battery_Status_Volts=data_battery['BatLevel'].strip())
            print ('update_battery_to_status is',update_battery_to_status)
            print ('Update battery to status Succeed')
        except Status.DoesNotExist:
            print ('Cannot update battery to status')
            
    return 200  # Response back to request

{'destination': 'Ud1d574db1a010fa89cf41e891e10f6bd', 
 'events': [{'type': 'join', 'timestamp': 1623757824955, 'source': 
     {'type': 'group', 'groupId': 'C6f08cd7ac176721b1be16ddca5fbec0b'}, 
     'replyToken': 'f8ec604ea462418a82391cbcd02aee2a', 'mode': 'active'}]}

def CreateLineGroup(request,group_name):
    group_id = request['events'][0]['source']['groupId']
    try:
        # Check if nozzle already in db or not if YES go next step
        prepare_data = LinegroupId.objects.get(group_id=group_id)
        # Update each filed into db
        LinegroupId.objects.filter(group_id=group_id).update(
                                        group_name=group_name,
                                            Timestramp=timezone.now())
    except LinegroupId.DoesNotExist:  # Check if nozzle already in db or not if NO go next step to insert into
        save_record = LinegroupId()
        save_record.group_id = group_id
        save_record.group_name = group_name
        save_record.save(request)
    return HttpResponse(200)  # Response back to request









