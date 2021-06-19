# สำหรับบันทึกข้อมูลที่ต้องการลงไปที่ DB
from django.utils import timezone
import dateutil.parser
import datetime
from app.models import Site, Status , Status_Error_logger,Store_data_send_line_failed,battery_status,LinegroupId,Setup_Config
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden, JsonResponse
from dateutil.relativedelta import relativedelta, SA, TH

class save_data_to_db ():
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
    def SaveRecordStatusErrorLogger (request,type_save): #สำหรับ save record สำหรับ ERROR ต่างๆ
        try :
            # บันทึก Error ไปที่ database
            save_record = Status_Error_logger()
            save_record.site_id = request
            save_record.name_id = request
            save_record.Error_type = type_save
            save_record.Error_start = timezone.now()
            save_record.Timestramp = timezone.now()
            save_record.save(request)
            return  save_record # return save_record ออกไปเพื่อให้ return ID ล่าสุดที่ทำการบันทึกออกไป
        except :
            print('Cannot SaveRecordStatusErrorLogger /linebot/save_data_to_db/')
    def SaveRecordBatteryErrorLogger (site_detail,request,type_save): #สำหรับ save record สำหรับ ERROR ต่างๆ
        # try :
            # บันทึก Error ไปที่ database
        save_record = Status_Error_logger()
        save_record.site_id = site_detail.name_id
        save_record.name_id = site_detail.name_id
        save_record.Error_type = type_save
        save_record.Unit_log_LgAddr = site_detail.NOZZLE_pump_log_address
        save_record.NOZZLE_num = site_detail.NOZZLE_num
        save_record.NOZZLE_SN = site_detail.NOZZLE_SN
        save_record.NOZZLE_Battery_Status_Volts = request['BatLevel']
        save_record.Timestramp = timezone.now()
        save_record.save(request)
        return  save_record # return save_record ออกไปเพื่อให้ return ID ล่าสุดที่ทำการบันทึกออกไป
        # except :
        #     print('Cannot SaveRecordStatusErrorLogger /linebot/save_data_to_db/')      
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
    def UpdateStatusLoggerBATTERYBackToNormal(request,NOZZLE_SN):
        try :
            Status_Error_logger.objects.filter(Error_stop__isnull=True,name_id=request,Error_type = 'BATTERY_LOW',NOZZLE_SN=NOZZLE_SN.strip()).update(Error_stop=timezone.now()) # ทำการ Update Error_stop time ไปที่ db
            Status_Error_logger.objects.filter(Error_stop__isnull=True,name_id=request,Error_type = 'BATTERY_FAILED',NOZZLE_SN=NOZZLE_SN.strip()).update(Error_stop=timezone.now()) # ทำการ Update Error_stop time ไปที่ db
            # Do something such send line notify
            print("SUCCESS Update BATTERY Back to ONLINE Succeed for name_id : {} Nozzle : {}".format(request,NOZZLE_SN))
            return True
        except Status.DoesNotExist:
            # Do something such send line notify
            print("FAILED Update BATTERY Back to ONLINE Succeed for name_id : {} Nozzle : {}".format(request,NOZZLE_SN))
            return False
    def UpdateStatusVISBackToOnline(request):
        try :
            payload = request
            print(payload)
            print(payload['events'][0]['data'])
            # print(payload['events'][0]['Logger_id'])
            Status_Error_logger.objects.filter(Error_type='VIS-OFFLINE',Error_stop__isnull=True,name_id=payload['events'][0]['data']).update(Error_stop=timezone.now()) # ทำการ Update Error_stop time ไปที่ db
            # Do something such send line notify
            print("Update VIS Back to ONLINE Succeed /linebot/save_data_to_db/UpdateStatusLoggerBackToOnline ")
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
    def UpdateVIS_ONLINE(request):
        payload = request
        try:
            Status.objects.filter(name_id=payload['events'][0]['site_id']).update(VIS_status='online',Timestramp=timezone.now())
            # Do something such send line notify
            print("Update VIS Online Succeed ")
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
        # for vis_check in (payload):  # Loop each nozzle for update into database
        #     try :
        #         vis_status = Status.objects.get(name_id=data_nozzle['name_id']).values('VIS_status')
        #         print ('vis_status is',vis_status)
        #         return vis_status
        #         break
        #     except Status.DoesNotExist:
        #         print ('Cannot sent battery back to Decive')
              # Response back to request
    def UpdateStatusAfterBatteryLastCheck(name_id,battery_volt,NOZZLE_SN,battery_detail):
        battery_volt = battery_volt.strip()
        name_id = name_id
        print ('name_id',name_id)
        print ('battery_volt',battery_volt)
        print ('NOZZLE_SN',NOZZLE_SN)
        # ตรวจสอบข้อมูลการตั้งค่า Battery เพื่อกำหนดค่า low normal alarm
        
        for setup in Setup_Config.objects.all() :
            low = setup.battery_level_low_volt
            alarm = setup.battery_level_alarm_volt
            failed = setup.battery_level_failed_volt
            print (low,alarm,failed)
        if float(battery_volt) > float(low) :
            battery_type = 'normal'
            try :
                notify_check = Status.objects.filter(name_id=name_id,NOZZLE_SN=NOZZLE_SN).values('BATTERY_status_check')
                site_detail = Status.objects.select_related().get(name_id=name_id,NOZZLE_SN=NOZZLE_SN)
                print ('notify_check',notify_check)
                print ('check_status_battery_first ',notify_check[0]['BATTERY_status_check'])
                if notify_check[0]['BATTERY_status_check'] == 'normal' :
                    try :
                        update_battery_to_status = Status.objects.filter(name_id=name_id,NOZZLE_SN=NOZZLE_SN).update(BATTERY_status_check=battery_type,NOZZLE_Battery_Status_Volts=battery_volt)
                        if update_battery_to_status > 0 :
                            print ('SECCESS Update battery status for name_id {} nozzle_sn {}'.format(name_id,NOZZLE_SN))
                            return True
                        else :
                            print ('FAILED Update battery status for name_id {} nozzle_sn {}'.format(name_id,NOZZLE_SN))
                            return True
                    except Status.DoesNotExist:
                        print ('No data filed to update battery to status')
                elif notify_check[0]['BATTERY_status_check'] != 'normal' :
                    # result_status_error_logger = Status_Error_logger.objects.all().filter(name_id=name_id,Error_type='BATTERY_LOW').order_by('-Timestramp').first()
                    send_line_notify = creating_line_data.Line_Creating_BATTERY_NORMAL(site_detail)
                    if send_line_notify == True :
                        print ('SECCESS send notify battery back to normal for name_id {} nozzle_sn {}'.format(name_id,NOZZLE_SN))
                    elif send_line_notify != False :
                        print ('FAILED send notify battery back to normal  for name_id {} nozzle_sn {}'.format(name_id,NOZZLE_SN))
                    Status.objects.filter(name_id=name_id,NOZZLE_SN=NOZZLE_SN).update(BATTERY_status_check=battery_type,NOZZLE_Battery_Status_Volts=battery_volt,BATTERY_notify_low=False,BATTERY_notify_alarm=False)
                    print ('SUCCESS update status Line Notify to False  for name_id {} nozzle_sn {}'.format(name_id,NOZZLE_SN))
                    save_data_to_db.UpdateStatusLoggerBATTERYBackToNormal(name_id,NOZZLE_SN)
                    print ('SUCCESS update battery to status back to normal  for name_id {} nozzle_sn {}'.format(name_id,NOZZLE_SN))
            except :
                print ('ERROR update battery to status back to normal  for name_id {} nozzle_sn {}'.format(name_id,NOZZLE_SN))   
        elif float(battery_volt) >= float(alarm) :
            battery_type = 'low'
            try :
                notify_check = Status.objects.filter(name_id=name_id,NOZZLE_SN=NOZZLE_SN).values('BATTERY_notify_low')
                site_detail = Status.objects.select_related().get(name_id=name_id,NOZZLE_SN=NOZZLE_SN)
                print ('check_status_battery_first ',notify_check[0]['BATTERY_notify_low'])
                if notify_check[0]['BATTERY_notify_low'] == 'False' :
                    print ('yes')
                    # go to sent notify list
                    try : 
                        SaveRecord= save_data_to_db.SaveRecordBatteryErrorLogger(site_detail,battery_detail,'BATTERY_LOW')# for local testing
                        send_line_notify = creating_line_data.Line_Creating_BATTERY_LOW(site_detail)
                        if send_line_notify == True :
                            print ('SECCESS send notify battery low for name_id {} nozzle_sn {}'.format(name_id,NOZZLE_SN))
                        elif send_line_notify != False :
                            print ('FAILED send notify battery low for name_id {} nozzle_sn {}'.format(name_id,NOZZLE_SN))
                        update_battery_to_status = Status.objects.filter(name_id=name_id,NOZZLE_SN=NOZZLE_SN).update(BATTERY_notify_low=True,BATTERY_status_check=battery_type,NOZZLE_Battery_Status_Volts=battery_volt)
                        print ('SUCCESS update battery to status is low for name_id {} nozzle_sn {}'.format(name_id,NOZZLE_SN))
                    except Status.DoesNotExist:
                        print ('ERROR update battery to status is low for name_id {} nozzle_sn {}'.format(name_id,NOZZLE_SN)) 
                elif notify_check[0]['BATTERY_notify_low'] == 'True' :
                    update_battery_to_status = Status.objects.filter(name_id=name_id,NOZZLE_SN=NOZZLE_SN).update(BATTERY_notify_low=True,BATTERY_status_check=battery_type,NOZZLE_Battery_Status_Volts=battery_volt)
                    return True
            except Status.DoesNotExist:
                print ('DO NOT FOUND data for update battery for name_id {} nozzle_sn {}'.format(name_id,NOZZLE_SN)) 
        elif float(battery_volt) <= float(failed) :
            battery_type = 'failed'
            try :
                notify_check = Status.objects.filter(name_id=name_id,NOZZLE_SN=NOZZLE_SN).values('BATTERY_notify_alarm')
                site_detail = Status.objects.select_related().get(name_id=name_id,NOZZLE_SN=NOZZLE_SN)
                print ('check_status_battery_first ',notify_check[0]['BATTERY_notify_alarm'])
                if notify_check[0]['BATTERY_notify_alarm'] == 'False' :
                    print ('yes')
                    # go to sent notify list
                    try : 
                        SaveRecord= save_data_to_db.SaveRecordBatteryErrorLogger(site_detail,battery_detail,'BATTERY_FAILED')# for local testing
                        send_line_notify = creating_line_data.Line_Creating_BATTERY_FAILED(site_detail)
                        if send_line_notify == True :
                            print ('SECCESS send notify battery failed for name_id {} nozzle_sn {}'.format(name_id,NOZZLE_SN))
                        elif send_line_notify != False :
                            print ('FAILED send notify battery failed for name_id {} nozzle_sn {}'.format(name_id,NOZZLE_SN))
                        update_battery_to_status = Status.objects.filter(name_id=name_id,NOZZLE_SN=NOZZLE_SN).update(BATTERY_notify_alarm=True,BATTERY_status_check=battery_type,NOZZLE_Battery_Status_Volts=battery_volt)
                        print ('SUCCESS update battery to status is failed for name_id {} nozzle_sn {}'.format(name_id,NOZZLE_SN))
                    except Status.DoesNotExist:
                        print ('ERROR update battery to status is failed for name_id {} nozzle_sn {}'.format(name_id,NOZZLE_SN)) 
                elif notify_check[0]['BATTERY_notify_low'] == 'True' :
                    update_battery_to_status = Status.objects.filter(name_id=name_id,NOZZLE_SN=NOZZLE_SN).update(BATTERY_notify_alarm=True,BATTERY_status_check=battery_type,NOZZLE_Battery_Status_Volts=battery_volt)
                    return True
            except Status.DoesNotExist:
                print ('DO NOT FOUND data for update battery for name_id {} nozzle_sn {}'.format(name_id,NOZZLE_SN)) 
    def UpdateBatteryStatus(request):
        payload = request['events'][0]['battery_detail']
        name_id = request['events'][0]['name_id']
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
                # ส่ง record ไปทำการ update status at table Status for update battery_status_check
                save_data_to_db.UpdateStatusAfterBatteryLastCheck(name_id,data_battery['BatLevel'],data_battery['SN'].strip(),data_battery)
                # save_data_to_db.UpdateStatusAfterBatteryLastCheck(name_id,'3.7',data_battery['SN'].strip(),data_battery) # จำลองส่งค่า bat ต่ำๆเข้าไป
        return 200  # Response back to request
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









