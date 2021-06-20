import requests
from linebot.creating_flex_messages import *
from linebot.creating_picture_for_line_notify import *
from linebot.save_data_to_db import *


class creating_line_data ():
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
        def send_notify_picture(path, token,message,site_profile):
            try:
                url = "https://notify-api.line.me/api/notify"
                file = {'imageFile':open(path,'rb')}
                data = ({'message': message,})
                path_opened = True
            except :
                path_opened = False
                datetime_now = datetime.datetime.now().strftime("%d.%m.%y %H:%M")
                print ('CAN NOT OPEN URL PATH FOR LINE PICTURE NOTIFY FOR MESSAGES {} ON {}'.format(message,datetime_now))
            if  path_opened == True:
                LINE_HEADERS = {"Authorization":"Bearer "+token}
                session = requests.Session()
                r=session.post(url, headers=LINE_HEADERS, files=file, data=data)
                if r.status_code == 200 :
                    datetime_now = datetime.datetime.now().strftime("%d.%m.%y %H:%M")
                    print ('SUCCESS LINE LINE NOTIFY PICTURE FOR MESSAGES {} ON {}'.format(message,datetime_now))
                    file_path = path
                    os.remove(file_path)
                    print ('REMOVED FILE SUCCESS FOR MESSAGES {} ON {}'.format(message,datetime_now))
                    return True
                elif r.status_code != 200 :
                    datetime_now = datetime.datetime.now().strftime("%d.%m.%y %H:%M")
                    save_data_to_db.SaveDataSendLineFailedToBD('LINE_NOTIFY',path,message,site_profile)
                    print ('FAILED SEND LINE GO TO SAVE PICTURE FOR MESSAGES {} ON {}'.format(message,datetime_now))
                    return True
            else:
                return None
        def Line_Creating_MWGT_OFFLINE (line_data,site_profile):
            result_site = site_profile[0] # รับค่า return มาจาก linebot/connect_db_profile/get_site_profile ใน index ที่ 0
            day_loss = line_data[0] # รับค่า return มาจาก linebot/calculate_function/different_time_calculate โดย return มาทั้งหมด 5 index 0
            hours_loss = line_data[1] # รับค่า return มาจาก linebot/calculate_function/different_time_calculate โดย return มาทั้งหมด 5 index 1
            minutes_loss = line_data[2] # รับค่า return มาจาก linebot/calculate_function/different_time_calculate โดย return มาทั้งหมด 5 index 2
            datetime_now = line_data[3] # รับค่า return มาจาก linebot/calculate_function/different_time_calculate โดย return มาทั้งหมด 5 index 3
            MWGT_last_time = line_data[4] # รับค่า return มาจาก linebot/calculate_function/different_time_calculate โดย return มาทั้งหมด 5 index 4
            messages_header = 'MWGT-OFFLINE : '+'สถานี : ' + str(result_site.station_name)
            path_save=creating_picture_for_line_notify.CreatingPictureForMWGT('MWGT',line_data,site_profile,'OFF-LINE') #result_site.team_support.line_notify_token คือ อ้างอิงจาก site_profile --> อ้างไปที่ ตาราง Site -- > team_support --> อ้างไปที่ ตาราง Team --> line_notify_token
            result_notify=creating_line_data.send_notify_picture(path_save, result_site.team_support.line_notify_token,messages_header,site_profile)
            return creating_flex_messages.CreateNotifyFormMwgtOffline(line_data,site_profile) 
        def Line_Creating_MWGT_ONLINE (line_data,site_profile):
            result_site = site_profile[0] # รับค่า return มาจาก linebot/connect_db_profile/get_site_profile ใน index ที่ 0
            day_loss = line_data[0] # รับค่า return มาจาก linebot/calculate_function/different_time_calculate โดย return มาทั้งหมด 5 index 0
            hours_loss = line_data[1] # รับค่า return มาจาก linebot/calculate_function/different_time_calculate โดย return มาทั้งหมด 5 index 1
            minutes_loss = line_data[2] # รับค่า return มาจาก linebot/calculate_function/different_time_calculate โดย return มาทั้งหมด 5 index 2
            datetime_now = line_data[3] # รับค่า return มาจาก linebot/calculate_function/different_time_calculate โดย return มาทั้งหมด 5 index 3
            Error_start = line_data[4] # รับค่า return มาจาก linebot/calculate_function/different_time_calculate โดย return มาทั้งหมด 5 index 4
            messages_header = 'MWGT-ONLINE : '+'สถานี : ' + str(result_site.station_name)
            path_save=creating_picture_for_line_notify.CreatingPictureForMWGT('MWGT',line_data,site_profile[1],'ON-LINE') #result_site.team_support.line_notify_token คือ อ้างอิงจาก site_profile --> อ้างไปที่ ตาราง Site -- > team_support --> อ้างไปที่ ตาราง Team --> line_notify_token
            result_notify=creating_line_data.send_notify_picture(path_save, result_site.team_support.line_notify_token,messages_header,site_profile)
            return creating_flex_messages.CreateNotifyFormMwgtOnline(line_data,site_profile) 
        def Line_Creating_VIS_OFFLINE (line_data,site_profile):
            result_site = site_profile # รับค่า return มาจาก linebot/connect_db_profile/get_site_profile ใน index ที่ 0
            messages_header = 'VIS-OFFLINE : '+'สถานี : ' + str(result_site.site.station_name)
            path_save=creating_picture_for_line_notify.CreatingPictureForVis('VIS',line_data,site_profile,'OFF-LINE') #result_site.team_support.line_notify_token คือ อ้างอิงจาก site_profile --> อ้างไปที่ ตาราง Site -- > team_support --> อ้างไปที่ ตาราง Team --> line_notify_token
            result_notify=creating_line_data.send_notify_picture(path_save, result_site.site.team_support.line_notify_token,messages_header,site_profile)
            return creating_flex_messages.CreateNotifyFormVisOffline(line_data,site_profile)        
        def Line_Creating_VIS_ONLINE (line_data,site_profile):
            result_site = site_profile[1] # รับค่า return มาจาก linebot/connect_db_profile/get_site_profile ใน index ที่ 
            messages_header = 'VIS-ONLINE : '+'สถานี : ' + str(result_site.site.station_name)
            path_save=creating_picture_for_line_notify.CreatingPictureForVis('VIS',line_data,site_profile[1],'ON-LINE') #result_site.team_support.line_notify_token คือ อ้างอิงจาก site_profile --> อ้างไปที่ ตาราง Site -- > team_support --> อ้างไปที่ ตาราง Team --> line_notify_token
            result_notify=creating_line_data.send_notify_picture(path_save, result_site.site.team_support.line_notify_token,messages_header,site_profile)
            return creating_flex_messages.CreateNotifyFormVisOnline(line_data,site_profile)       
        def Line_Creating_BATTERY_LOW (site_profile):
            result_site = site_profile # รับค่า return มาจาก linebot/connect_db_profile/get_site_profile ใน index ที่ 0
            # day_loss = line_data[0] # รับค่า return มาจาก linebot/calculate_function/different_time_calculate โดย return มาทั้งหมด 5 index 0
            # hours_loss = line_data[1] # รับค่า return มาจาก linebot/calculate_function/different_time_calculate โดย return มาทั้งหมด 5 index 1
            # minutes_loss = line_data[2] # รับค่า return มาจาก linebot/calculate_function/different_time_calculate โดย return มาทั้งหมด 5 index 2
            # datetime_now = line_data[3] # รับค่า return มาจาก linebot/calculate_function/different_time_calculate โดย return มาทั้งหมด 5 index 3
            # Error_start = line_data[4] # รับค่า return มาจาก linebot/calculate_function/different_time_calculate โดย return มาทั้งหมด 5 index 4
            messages = 'BATTERY Status ' + '\n' + \
                            'Type : ' + ' Battery : LOW ' + '\n' \
                                'สถานี : ' + result_site.site.station_name + '\n' + \
                                    'IP : ' + str(result_site.site.station_ip) + '\n' + \
                                        'Serial : ' + str(result_site.NOZZLE_SN) + '\n' + \
                                            'หน้าที่ : ' + str(result_site.NOZZLE_pump_log_address) + '\n' + \
                                                'มือจ่าย  : ' + str(result_site.NOZZLE_num) + '\n' + \
                                            'ระดับแรงดัน : ' + str(result_site.NOZZLE_Battery_Status_Volts) + ' V.'+ '\n' \
                                                    + 'ช่างเขต : ' + result_site.site.team_support.team_name
            return creating_line_data.send_notify(messages , result_site.site.team_support.line_notify_token) #result_site.team_support.line_notify_token คือ อ้างอิงจาก site_profile --> อ้างไปที่ ตาราง Site -- > team_support --> อ้างไปที่ ตาราง Team --> line_notify_token
        def Line_Creating_BATTERY_FAILED (site_profile):
            result_site = site_profile # รับค่า return มาจาก linebot/connect_db_profile/get_site_profile ใน index ที่ 0
            # day_loss = line_data[0] # รับค่า return มาจาก linebot/calculate_function/different_time_calculate โดย return มาทั้งหมด 5 index 0
            # hours_loss = line_data[1] # รับค่า return มาจาก linebot/calculate_function/different_time_calculate โดย return มาทั้งหมด 5 index 1
            # minutes_loss = line_data[2] # รับค่า return มาจาก linebot/calculate_function/different_time_calculate โดย return มาทั้งหมด 5 index 2
            # datetime_now = line_data[3] # รับค่า return มาจาก linebot/calculate_function/different_time_calculate โดย return มาทั้งหมด 5 index 3
            # Error_start = line_data[4] # รับค่า return มาจาก linebot/calculate_function/different_time_calculate โดย return มาทั้งหมด 5 index 4
            messages = 'BATTERY Status ' + '\n' + \
                            'Type : ' + ' Battery : FAILED ' + '\n' \
                                'สถานี : ' + result_site.site.station_name + '\n' + \
                                    'IP : ' + str(result_site.site.station_ip) + '\n' + \
                                        'Serial : ' + str(result_site.NOZZLE_SN) + '\n' + \
                                            'หน้าที่ : ' + str(result_site.NOZZLE_pump_log_address) + '\n' + \
                                                'มือจ่าย  : ' + str(result_site.NOZZLE_num) + '\n' + \
                                            'ระดับแรงดัน : ' + str(result_site.NOZZLE_Battery_Status_Volts) + ' V.'+ '\n' \
                                                    + 'ช่างเขต : ' + result_site.site.team_support.team_name
            return creating_line_data.send_notify(messages , result_site.site.team_support.line_notify_token) #result_site.team_support.line_notify_token คือ อ้างอิงจาก site_profile --> อ้างไปที่ ตาราง Site -- > team_support --> อ้างไปที่ ตาราง Team --> line_notify_token
        def Line_Creating_BATTERY_NORMAL (site_profile):
            result_site = site_profile # รับค่า return มาจาก linebot/connect_db_profile/get_site_profile ใน index ที่ 0
            # day_loss = line_data[0] # รับค่า return มาจาก linebot/calculate_function/different_time_calculate โดย return มาทั้งหมด 5 index 0
            # hours_loss = line_data[1] # รับค่า return มาจาก linebot/calculate_function/different_time_calculate โดย return มาทั้งหมด 5 index 1
            # minutes_loss = line_data[2] # รับค่า return มาจาก linebot/calculate_function/different_time_calculate โดย return มาทั้งหมด 5 index 2
            # datetime_now = line_data[3] # รับค่า return มาจาก linebot/calculate_function/different_time_calculate โดย return มาทั้งหมด 5 index 3
            # Error_start = line_data[4] # รับค่า return มาจาก linebot/calculate_function/different_time_calculate โดย return มาทั้งหมด 5 index 4
            messages = 'BATTERY Status ' + '\n' + \
                            'Type : ' + ' Battery : NORMAL ' + '\n' \
                                'สถานี : ' + result_site.site.station_name + '\n' + \
                                    'IP : ' + str(result_site.site.station_ip) + '\n' + \
                                        'Serial : ' + str(result_site.NOZZLE_SN) + '\n' + \
                                            'หน้าที่ : ' + str(result_site.NOZZLE_pump_log_address) + '\n' + \
                                                'มือจ่าย  : ' + str(result_site.NOZZLE_num) + '\n' + \
                                            'ระดับแรงดัน : ' + str(result_site.NOZZLE_Battery_Status_Volts) + ' V.'+ '\n' \
                                                    + 'ช่างเขต : ' + result_site.site.team_support.team_name
            return creating_line_data.send_notify(messages , result_site.site.team_support.line_notify_token) #result_site.team_support.line_notify_token คือ อ้างอิงจาก site_profile --> อ้างไปที่ ตาราง Site -- > team_support --> อ้างไปที่ ตาราง Team --> line_notify_token       
        def Line_Creating_NOZZLE_OFFLINE (line_data,site_profile):
            result_site = site_profile # รับค่า return มาจาก linebot/connect_db_profile/get_site_profile ใน index ที่ 0
            day_loss = line_data[0] # รับค่า return มาจาก linebot/calculate_function/different_time_calculate โดย return มาทั้งหมด 5 index 0
            hours_loss = line_data[1] # รับค่า return มาจาก linebot/calculate_function/different_time_calculate โดย return มาทั้งหมด 5 index 1
            minutes_loss = line_data[2] # รับค่า return มาจาก linebot/calculate_function/different_time_calculate โดย return มาทั้งหมด 5 index 2
            datetime_now = line_data[3] # รับค่า return มาจาก linebot/calculate_function/different_time_calculate โดย return มาทั้งหมด 5 index 3
            Error_start = line_data[4] # รับค่า return มาจาก linebot/calculate_function/different_time_calculate โดย return มาทั้งหมด 5 index 4
            messages = 'NOZZLE Status ' + '\n' + \
                            'Type : ' + ' การติดต่อ : ไม่ปกติ' + '\n'\
                                'สถานี : ' + result_site.site.station_name + '\n' + \
                                    'IP : ' + result_site.site.station_ip + '\n' + \
                                        'หน้าจ่ายที่  : ' + result_site.NOZZLE_pump_log_address + '\n' + \
                                            'มืือจ่าย : ' + result_site.NOZZLE_num + '\n' + \
                                        'ติดต่อไม่ได้เมื่อ : ' + Error_start + '\n' + \
                                            'ติดต่อได้ล่าสุด : ' + datetime_now + '\n' + \
                                                'ขาดการติดต่อนาน : ' + str(day_loss) + \
                                                    ' วัน ' + str(hours_loss) + \
                                                        ' ชม ' + str(minutes_loss) + \
                                                            ' นาที' + '\n' + 'ช่างเขต : ' + result_site.site.team_support.team_name
            return creating_line_data.send_notify(messages , result_site.site.team_support.line_notify_token) #result_site.team_support.line_notify_token คือ อ้างอิงจาก site_profile --> อ้างไปที่ ตาราง Site -- > team_support --> อ้างไปที่ ตาราง Team --> line_notify_token
        def Line_Creating_NOZZLE_ONLINE (line_data,site_profile):
            result_site = site_profile # รับค่า return มาจาก linebot/connect_db_profile/get_site_profile ใน index ที่ 0
            day_loss = line_data[0] # รับค่า return มาจาก linebot/calculate_function/different_time_calculate โดย return มาทั้งหมด 5 index 0
            hours_loss = line_data[1] # รับค่า return มาจาก linebot/calculate_function/different_time_calculate โดย return มาทั้งหมด 5 index 1
            minutes_loss = line_data[2] # รับค่า return มาจาก linebot/calculate_function/different_time_calculate โดย return มาทั้งหมด 5 index 2
            datetime_now = line_data[3] # รับค่า return มาจาก linebot/calculate_function/different_time_calculate โดย return มาทั้งหมด 5 index 3
            Error_start = line_data[4] # รับค่า return มาจาก linebot/calculate_function/different_time_calculate โดย return มาทั้งหมด 5 index 4
            messages = 'NOZZLE Status ' + '\n' + \
                            'Type : ' + ' การติดต่อ : ปกติ' + '\n'\
                                'สถานี : ' + result_site.site.station_name + '\n' + \
                                    'IP : ' + result_site.site.station_ip + '\n' + \
                                        'หน้าจ่ายที่  : ' + result_site.NOZZLE_pump_log_address + '\n' + \
                                            'มืือจ่าย : ' + result_site.NOZZLE_num + '\n' + \
                                        'ติดต่อไม่ได้เมื่อ : ' + Error_start + '\n' + \
                                            'ติดต่อได้ล่าสุด : ' + datetime_now + '\n' + \
                                                'ขาดการติดต่อรวม : ' + str(day_loss) + \
                                                    ' วัน ' + str(hours_loss) + \
                                                        ' ชม ' + str(minutes_loss) + \
                                                            ' นาที' + '\n' + 'ช่างเขต : ' + result_site.site.team_support.team_name
            return creating_line_data.send_notify(messages , result_site.site.team_support.line_notify_token) #result_site.team_support.line_notify_token คือ อ้างอิงจาก site_profile --> อ้างไปที่ ตาราง Site -- > team_support --> อ้างไปที่ ตาราง Team --> line_notify_token