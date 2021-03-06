import io
import urllib.parse
import sys
import time
import datetime
import os
from PIL import Image, ImageDraw, ImageFont

class creating_picture_for_line_notify():
    def CreatingPictureForVis(device,line_data,site_profile,Status):
        print ('driver is',device)
        if device == 'VIS' :
            if Status == 'OFF-LINE':
                Header_type = 'VIS : OFFLINE'
                Header_IP_TYPE = 'VIS : IP '
                Status = 'OFF-LINE'
                color_status = 'rgb(255,0,0)'
            elif Status == 'ON-LINE':
                Header_type = 'VIS : ONFLINE'
                Header_IP_TYPE = 'VIS : IP '
                Status = 'ON-LINE'
                color_status = 'rgb(124,252,0)'
        print ('header is',Header_type)   
        if Status == 'OFF-LINE' :
            result_site = site_profile # รับค่า return มาจาก linebot/connect_db_profile/get_site_profile ใน index ที่ 0
            day_loss = line_data[0] # รับค่า return มาจาก linebot/calculate_function/different_time_calculate โดย return มาทั้งหมด 5 index 0
            hours_loss = line_data[1] # รับค่า return มาจาก linebot/calculate_function/different_time_calculate โดย return มาทั้งหมด 5 index 1
            minutes_loss = line_data[2] # รับค่า return มาจาก linebot/calculate_function/different_time_calculate โดย return มาทั้งหมด 5 index 2
            datetime_now = line_data[3] # รับค่า return มาจาก linebot/calculate_function/different_time_calculate โดย return มาทั้งหมด 5 index 3
            VIS_last_time = line_data[4] # รับค่า return มาจาก linebot/calculate_function/different_time_calculate โดย return มาทั้งหมด 5 index 4
            dt_save = datetime.datetime.now().strftime("%d-%m-%y-%H:%M")
            file_path = 'line_folder/picture_store/VIS-FORM.jpg'  # Window Server
            path_font_check = 'line_folder/font/THSarabunNew.ttf'
            path_save_check = 'line_folder/picture_for_send/'+ 'VIS-OFFLINE-' +dt_save+'.jpg'
            module_dir = os.path.dirname(__file__)  # get current directory
            path = os.path.join(module_dir, file_path)# Window Server
            path_font = os.path.join(module_dir, path_font_check)# Window Server
            patch_save = os.path.join(module_dir, path_save_check)# Window Server
            image = Image.open(path)
            imageSizeW, imageSizeH = image.size
            draw = ImageDraw.Draw(image)
            color = 'rgb(0, 0, 0)'  # black color
            fnt_hardder = ImageFont.truetype(path_font, 120)
            fnt_report_name = ImageFont.truetype(path_font, 70)
            fnt_report_detail = ImageFont.truetype(path_font, 80)
            fnt_report_sub_detail = ImageFont.truetype(path_font, 50)
            draw.text((450, 300), datetime_now, fill=color, font=fnt_hardder)
            draw.text((490,430), Header_type, fill=color_status, font=fnt_hardder)
            draw.text((140, 620), 'สถานี : ' + result_site.site.station_name, fill=color, font=fnt_report_name)
            draw.text((140,700), Header_IP_TYPE  + str(result_site.site.station_ip), fill=color, font=fnt_report_name)
            draw.text((140,780), 'สถานะ ' , fill=color, font=fnt_report_name)
            draw.text((1080,780), Status, fill=color_status, font=fnt_report_name)
            draw.text((140,880), 'ติดต่อไม่ได้เมื่อ ' , fill=color, font=fnt_report_name)
            draw.text((980, 880), str(datetime_now), fill=color, font=fnt_report_name)
            draw.text((140,980), 'ติดต่อได้ครั้งล่าสุด ' , fill=color, font=fnt_report_name)
            draw.text((980, 980), str(VIS_last_time), fill=color, font=fnt_report_name)
            draw.text((140,1080), 'ขาดการติดต่อนาน ' , fill=color, font=fnt_report_name)
            draw.text((890, 1080), str(day_loss)+' วัน '+str(hours_loss)+' ชม. '+ str(minutes_loss)+' นาที', fill=color, font=fnt_report_name)
            draw.text((140, 1180), str('ทีมงาน : '), fill=color, font=fnt_report_name)
            draw.text((890, 1180), str('คุณ : '+result_site.site.team_support.team_name), fill=color, font=fnt_report_name)
            dt_save = datetime.datetime.now().strftime("%d-%m-%y-%H:%M")
            # path_save = 'line_folder/picture_for_send/'+ 'VIS-OFFLINE-' +'dt_save'+'.jpg'
            image.save(patch_save, optimize=True, quality=20)
            return (patch_save)
        elif Status == 'ON-LINE' :
            result_site = site_profile # รับค่า return มาจาก linebot/connect_db_profile/get_site_profile ใน index ที่ 0
            day_loss = line_data[0] # รับค่า return มาจาก linebot/calculate_function/different_time_calculate โดย return มาทั้งหมด 5 index 0
            hours_loss = line_data[1] # รับค่า return มาจาก linebot/calculate_function/different_time_calculate โดย return มาทั้งหมด 5 index 1
            minutes_loss = line_data[2] # รับค่า return มาจาก linebot/calculate_function/different_time_calculate โดย return มาทั้งหมด 5 index 2
            datetime_now = line_data[3] # รับค่า return มาจาก linebot/calculate_function/different_time_calculate โดย return มาทั้งหมด 5 index 3
            VIS_last_time = line_data[4] # รับค่า return มาจาก linebot/calculate_function/different_time_calculate โดย return มาทั้งหมด 5 index 4
            dt_save = datetime.datetime.now().strftime("%d-%m-%y-%H:%M")
            file_path = 'line_folder/picture_store/VIS-FORM.jpg'  # Window Server
            path_font_check = 'line_folder/font/THSarabunNew.ttf'
            path_save_check = 'line_folder/picture_for_send/'+ 'VIS-OFFLINE-' +dt_save+'.jpg'
            module_dir = os.path.dirname(__file__)  # get current directory
            path = os.path.join(module_dir, file_path)# Window Server
            path_font = os.path.join(module_dir, path_font_check)# Window Server
            patch_save = os.path.join(module_dir, path_save_check)# Window Server
            image = Image.open(path)
            imageSizeW, imageSizeH = image.size
            draw = ImageDraw.Draw(image)
            color = 'rgb(0, 0, 0)'  # black color
            fnt_hardder = ImageFont.truetype(path_font, 120)
            fnt_report_name = ImageFont.truetype(path_font, 70)
            fnt_report_detail = ImageFont.truetype(path_font, 80)
            fnt_report_sub_detail = ImageFont.truetype(path_font, 50)
            draw.text((450, 300), datetime_now, fill=color, font=fnt_hardder)
            draw.text((490,430), Header_type, fill=color_status, font=fnt_hardder)
            draw.text((140, 620), 'สถานี : ' + result_site.site.station_name, fill=color, font=fnt_report_name)
            draw.text((140,700), Header_IP_TYPE  + str(result_site.site.station_ip), fill=color, font=fnt_report_name)
            draw.text((140,780), 'สถานะ ' , fill=color, font=fnt_report_name)
            draw.text((1080,780), Status, fill=color_status, font=fnt_report_name)
            draw.text((140,880), 'ติดต่อไม่ได้เมื่อ ' , fill=color, font=fnt_report_name)
            draw.text((980, 880), str(datetime_now), fill=color, font=fnt_report_name)
            draw.text((140,980), 'ติดต่อได้แล้วเมื่อ ' , fill=color, font=fnt_report_name)
            draw.text((980, 980), str(VIS_last_time), fill=color, font=fnt_report_name)
            draw.text((140,1080), 'ขาดการติดต่อรวม ' , fill=color, font=fnt_report_name)
            draw.text((890, 1080), str(day_loss)+' วัน '+str(hours_loss)+' ชม. '+ str(minutes_loss)+' นาที', fill=color, font=fnt_report_name)
            draw.text((140, 1180), str('ทีมงาน : '), fill=color, font=fnt_report_name)
            draw.text((890, 1180), str('คุณ : '+result_site.site.team_support.team_name), fill=color, font=fnt_report_name)
            dt_save = datetime.datetime.now().strftime("%d-%m-%y-%H:%M")
            # path_save = 'line_folder/picture_for_send/'+ 'VIS-OFFLINE-' +'dt_save'+'.jpg'
            image.save(patch_save, optimize=True, quality=20)
            return (patch_save)
    def CreatingPictureForMWGT(device,line_data,site_profile,Status):
        print ('driver is',device)
        if device == 'MWGT' :
            if Status == 'OFF-LINE':
                Header_type = 'MWGT : OFFLINE'
                Header_IP_TYPE = 'MWGT : IP '
                Status = 'OFF-LINE'
                color_status = 'rgb(255,0,0)'
            elif Status == 'ON-LINE':
                Header_type = 'MWGT : ONLINE'
                Header_IP_TYPE = 'MWGT : IP '
                Status = 'ON-LINE'
                color_status = 'rgb(124,252,0)'
        if Status == 'OFF-LINE' :
            result_site = site_profile[1] # รับค่า return มาจาก linebot/connect_db_profile/get_site_profile ใน index ที่ 0
            day_loss = line_data[0] # รับค่า return มาจาก linebot/calculate_function/different_time_calculate โดย return มาทั้งหมด 5 index 0
            hours_loss = line_data[1] # รับค่า return มาจาก linebot/calculate_function/different_time_calculate โดย return มาทั้งหมด 5 index 1
            minutes_loss = line_data[2] # รับค่า return มาจาก linebot/calculate_function/different_time_calculate โดย return มาทั้งหมด 5 index 2
            datetime_now = line_data[3] # รับค่า return มาจาก linebot/calculate_function/different_time_calculate โดย return มาทั้งหมด 5 index 3
            VIS_last_time = line_data[4] # รับค่า return มาจาก linebot/calculate_function/different_time_calculate โดย return มาทั้งหมด 5 index 4
            dt_save = datetime.datetime.now().strftime("%d-%m-%y-%H:%M")
            file_path = 'line_folder/picture_store/VIS-FORM.jpg'  # Window Server
            path_font_check = 'line_folder/font/THSarabunNew.ttf'
            path_save_check = 'line_folder/picture_for_send/'+ 'VIS-OFFLINE-' +dt_save+'.jpg'
            module_dir = os.path.dirname(__file__)  # get current directory
            path = os.path.join(module_dir, file_path)# Window Server
            path_font = os.path.join(module_dir, path_font_check)# Window Server
            patch_save = os.path.join(module_dir, path_save_check)# Window Server
            image = Image.open(path)
            imageSizeW, imageSizeH = image.size
            draw = ImageDraw.Draw(image)
            color = 'rgb(0, 0, 0)'  # black color
            fnt_hardder = ImageFont.truetype(path_font, 120)
            fnt_report_name = ImageFont.truetype(path_font, 70)
            fnt_report_detail = ImageFont.truetype(path_font, 80)
            fnt_report_sub_detail = ImageFont.truetype(path_font, 50)
            draw.text((450, 300), datetime_now, fill=color, font=fnt_hardder)
            draw.text((490,430), Header_type, fill=color_status, font=fnt_hardder)
            draw.text((140, 620), 'สถานี : ' + result_site.site.station_name, fill=color, font=fnt_report_name)
            draw.text((140,700), Header_IP_TYPE  + str(result_site.site.mwgt_ip), fill=color, font=fnt_report_name)
            draw.text((140,780), 'สถานะ ' , fill=color, font=fnt_report_name)
            draw.text((1080,780), Status, fill=color_status, font=fnt_report_name)
            draw.text((140,880), 'ติดต่อไม่ได้เมื่อ ' , fill=color, font=fnt_report_name)
            draw.text((980, 880), str(datetime_now), fill=color, font=fnt_report_name)
            draw.text((140,980), 'ติดต่อได้ครั้งล่าสุด ' , fill=color, font=fnt_report_name)
            draw.text((980, 980), str(VIS_last_time), fill=color, font=fnt_report_name)
            draw.text((140,1080), 'ขาดการติดต่อนาน ' , fill=color, font=fnt_report_name)
            draw.text((890, 1080), str(day_loss)+' วัน '+str(hours_loss)+' ชม. '+ str(minutes_loss)+' นาที', fill=color, font=fnt_report_name)
            draw.text((140, 1180), str('ทีมงาน : '), fill=color, font=fnt_report_name)
            draw.text((890, 1180), str('คุณ : '+result_site.site.team_support.team_name), fill=color, font=fnt_report_name)
            dt_save = datetime.datetime.now().strftime("%d-%m-%y-%H:%M")
            # path_save = 'line_folder/picture_for_send/'+ 'MWGT-OFFLINE-' +dt_save+'.jpg'
            image.save(patch_save, optimize=True, quality=20)
            return (patch_save)
        elif Status == 'ON-LINE' :
            result_site = site_profile # รับค่า return มาจาก linebot/connect_db_profile/get_site_profile ใน index ที่ 0
            day_loss = line_data[0] # รับค่า return มาจาก linebot/calculate_function/different_time_calculate โดย return มาทั้งหมด 5 index 0
            hours_loss = line_data[1] # รับค่า return มาจาก linebot/calculate_function/different_time_calculate โดย return มาทั้งหมด 5 index 1
            minutes_loss = line_data[2] # รับค่า return มาจาก linebot/calculate_function/different_time_calculate โดย return มาทั้งหมด 5 index 2
            datetime_now = line_data[3] # รับค่า return มาจาก linebot/calculate_function/different_time_calculate โดย return มาทั้งหมด 5 index 3
            Error_start = line_data[4] # รับค่า return มาจาก linebot/calculate_function/different_time_calculate โดย return มาทั้งหมด 5 index 4
            dt_save = datetime.datetime.now().strftime("%d-%m-%y-%H:%M")
            file_path = 'line_folder/picture_store/VIS-FORM.jpg'  # Window Server
            path_font_check = 'line_folder/font/THSarabunNew.ttf'
            path_save_check = 'line_folder/picture_for_send/'+ 'VIS-OFFLINE-' +dt_save+'.jpg'
            module_dir = os.path.dirname(__file__)  # get current directory
            path = os.path.join(module_dir, file_path)# Window Server
            path_font = os.path.join(module_dir, path_font_check)# Window Server
            patch_save = os.path.join(module_dir, path_save_check)# Window Server
            image = Image.open(path)
            imageSizeW, imageSizeH = image.size
            draw = ImageDraw.Draw(image)
            color = 'rgb(0, 0, 0)'  # black color
            fnt_hardder = ImageFont.truetype(path_font, 120)
            fnt_report_name = ImageFont.truetype(path_font, 70)
            fnt_report_detail = ImageFont.truetype(path_font, 80)
            fnt_report_sub_detail = ImageFont.truetype(path_font, 50)
            draw.text((450, 300), datetime_now, fill=color, font=fnt_hardder)
            draw.text((490,430), Header_type, fill=color_status, font=fnt_hardder)
            draw.text((140, 620), 'สถานี : ' + result_site.site.station_name, fill=color, font=fnt_report_name)
            draw.text((140,700), Header_IP_TYPE  + str(result_site.site.mwgt_ip), fill=color, font=fnt_report_name)
            draw.text((140,780), 'สถานะ ' , fill=color, font=fnt_report_name)
            draw.text((1080,780), Status, fill=color_status, font=fnt_report_name)
            draw.text((140,880), 'ติดต่อไม่ได้เมื่อ ' , fill=color, font=fnt_report_name)
            draw.text((980, 880), str(Error_start), fill=color, font=fnt_report_name)
            draw.text((140,980), 'ติดต่อได้แล้วเมื่อ ' , fill=color, font=fnt_report_name)
            draw.text((980, 980), str(datetime_now), fill=color, font=fnt_report_name)
            draw.text((140,1080), 'ขาดการติดต่อรวม ' , fill=color, font=fnt_report_name)
            draw.text((890, 1080), str(day_loss)+' วัน '+str(hours_loss)+' ชม. '+ str(minutes_loss)+' นาที', fill=color, font=fnt_report_name)
            draw.text((140, 1180), str('ทีมงาน : '), fill=color, font=fnt_report_name)
            draw.text((890, 1180), str('คุณ : '+result_site.site.team_support.team_name), fill=color, font=fnt_report_name)
            dt_save = datetime.datetime.now().strftime("%d-%m-%y-%H:%M")
            # path_save = 'line_folder/picture_for_send/'+ 'MWGT-ONLINE-' +dt_save+'.jpg'
            image.save(patch_save, optimize=True, quality=20)
            return (patch_save)
    def CreatingPictureForNOZZLE(device,line_data,site_profile,Status):
        print ('driver is',device)
        if device == 'NOZZLE' :
            if Status == 'OFF-LINE':
                Header_type = 'NOZZLE : OFFLINE'
                Header_IP_TYPE = 'MWGT : IP '
                Status = 'OFF-LINE'
                color_status = 'rgb(255,0,0)'
            elif Status == 'ON-LINE':
                Header_type = 'NOZZLE : ONLINE'
                Header_IP_TYPE = 'MWGT : IP '
                Status = 'ON-LINE'
                color_status = 'rgb(124,252,0)'
        if Status == 'OFF-LINE' :
            result_site = site_profile # รับค่า return มาจาก linebot/connect_db_profile/get_site_profile ใน index ที่ 0
            day_loss = line_data[0] # รับค่า return มาจาก linebot/calculate_function/different_time_calculate โดย return มาทั้งหมด 5 index 0
            hours_loss = line_data[1] # รับค่า return มาจาก linebot/calculate_function/different_time_calculate โดย return มาทั้งหมด 5 index 1
            minutes_loss = line_data[2] # รับค่า return มาจาก linebot/calculate_function/different_time_calculate โดย return มาทั้งหมด 5 index 2
            datetime_now = line_data[3] # รับค่า return มาจาก linebot/calculate_function/different_time_calculate โดย return มาทั้งหมด 5 index 3
            Error_start = line_data[4] # รับค่า return มาจาก linebot/calculate_function/different_time_calculate โดย return มาทั้งหมด 5 index 4
            dt_save = datetime.datetime.now().strftime("%d-%m-%y-%H:%M")
            file_path = 'line_folder/picture_store/VIS-FORM.jpg'  # Window Server
            path_font_check = 'line_folder/font/THSarabunNew.ttf'
            path_save_check = 'line_folder/picture_for_send/'+ 'VIS-OFFLINE-' +dt_save+'.jpg'
            module_dir = os.path.dirname(__file__)  # get current directory
            path = os.path.join(module_dir, file_path)# Window Server
            path_font = os.path.join(module_dir, path_font_check)# Window Server
            patch_save = os.path.join(module_dir, path_save_check)# Window Server
            image = Image.open(path)
            imageSizeW, imageSizeH = image.size
            draw = ImageDraw.Draw(image)
            color = 'rgb(0, 0, 0)'  # black color
            fnt_hardder = ImageFont.truetype(path_font, 120)
            fnt_report_name = ImageFont.truetype(path_font, 70)
            fnt_report_detail = ImageFont.truetype(path_font, 80)
            fnt_report_sub_detail = ImageFont.truetype(path_font, 50)
            draw.text((450, 300), datetime_now, fill=color, font=fnt_hardder)
            draw.text((430,430), Header_type, fill=color_status, font=fnt_hardder)
            draw.text((140, 620), 'สถานี : ' + result_site.site.station_name, fill=color, font=fnt_report_name)
            draw.text((140,700), Header_IP_TYPE  + str(result_site.site.mwgt_ip), fill=color, font=fnt_report_name)
            draw.text((140,760), 'สถานะ ' , fill=color, font=fnt_report_name)
            draw.text((1080,760), Status, fill=color_status, font=fnt_report_name)
            draw.text((140,830), 'หน้าจ่าย : ' , fill=color, font=fnt_report_name)
            draw.text((1230, 830), str(result_site.NOZZLE_pump_log_address), fill=color, font=fnt_report_name)
            draw.text((140,900), 'มือจ่าย :' , fill=color, font=fnt_report_name)
            draw.text((1230, 900), str(result_site.NOZZLE_num), fill=color, font=fnt_report_name)
            draw.text((140,975), 'BatteryVolt. ' , fill=color, font=fnt_report_name)
            draw.text((1170, 975), str(result_site.NOZZLE_Battery_Status_Volts), fill=color, font=fnt_report_name)
            draw.text((140, 1050), str('SerialNo : '), fill=color, font=fnt_report_name)
            draw.text((1080, 1050), str(result_site.NOZZLE_SN), fill=color, font=fnt_report_name)
            draw.text((140, 1120), str('LastCon : '), fill=color, font=fnt_report_name)
            draw.text((930, 1120), str(result_site.NOZZLE_Last_conn), fill=color, font=fnt_report_name)
            draw.text((140, 1200), str('ติิดต่อไม่ได้เมื่อ : '), fill=color, font=fnt_report_name)
            draw.text((960, 1200), str(Error_start), fill=color, font=fnt_report_name)
            draw.text((140, 1280), str('ขาดการติดต่อเมื่อ : '), fill=color, font=fnt_report_name)
            draw.text((960, 1280), str(datetime_now), fill=color, font=fnt_report_name)
            draw.text((140, 1350), str('ขาดการติดต่อนาน : '), fill=color, font=fnt_report_name)
            draw.text((890, 1350), str(day_loss)+' วัน '+str(hours_loss)+' ชม. '+ str(minutes_loss)+' นาที', fill=color, font=fnt_report_name)
            draw.text((140, 1420), str('ทีมงาน : '), fill=color, font=fnt_report_name)
            draw.text((920, 1420), 'คุณ : '+result_site.site.team_support.team_name, fill=color, font=fnt_report_name)
            dt_save = datetime.datetime.now().strftime("%d-%m-%y-%H:%M")
            # path_save = 'line_folder/picture_for_send/'+ 'MWGT-OFFLINE-' +dt_save+'.jpg'
            image.save(patch_save, optimize=True, quality=20)
            return (patch_save)
        elif Status == 'ON-LINE' :
            result_site = site_profile # รับค่า return มาจาก linebot/connect_db_profile/get_site_profile ใน index ที่ 0
            day_loss = line_data[0] # รับค่า return มาจาก linebot/calculate_function/different_time_calculate โดย return มาทั้งหมด 5 index 0
            hours_loss = line_data[1] # รับค่า return มาจาก linebot/calculate_function/different_time_calculate โดย return มาทั้งหมด 5 index 1
            minutes_loss = line_data[2] # รับค่า return มาจาก linebot/calculate_function/different_time_calculate โดย return มาทั้งหมด 5 index 2
            datetime_now = line_data[3] # รับค่า return มาจาก linebot/calculate_function/different_time_calculate โดย return มาทั้งหมด 5 index 3
            Error_start = line_data[4] # รับค่า return มาจาก linebot/calculate_function/different_time_calculate โดย return มาทั้งหมด 5 index 4
            dt_save = datetime.datetime.now().strftime("%d-%m-%y-%H:%M")
            file_path = 'line_folder/picture_store/VIS-FORM.jpg'  # Window Server
            path_font_check = 'line_folder/font/THSarabunNew.ttf'
            path_save_check = 'line_folder/picture_for_send/'+ 'VIS-OFFLINE-' +dt_save+'.jpg'
            module_dir = os.path.dirname(__file__)  # get current directory
            path = os.path.join(module_dir, file_path)# Window Server
            path_font = os.path.join(module_dir, path_font_check)# Window Server
            patch_save = os.path.join(module_dir, path_save_check)# Window Server
            image = Image.open(path)
            imageSizeW, imageSizeH = image.size
            draw = ImageDraw.Draw(image)
            color = 'rgb(0, 0, 0)'  # black color
            fnt_hardder = ImageFont.truetype(path_font, 120)
            fnt_report_name = ImageFont.truetype(path_font, 70)
            fnt_report_detail = ImageFont.truetype(path_font, 80)
            fnt_report_sub_detail = ImageFont.truetype(path_font, 50)
            draw.text((450, 300), datetime_now, fill=color, font=fnt_hardder)
            draw.text((430,430), Header_type, fill=color_status, font=fnt_hardder)
            draw.text((140, 620), 'สถานี : ' + result_site.site.station_name, fill=color, font=fnt_report_name)
            draw.text((140,700), Header_IP_TYPE  + str(result_site.site.mwgt_ip), fill=color, font=fnt_report_name)
            draw.text((140,760), 'สถานะ ' , fill=color, font=fnt_report_name)
            draw.text((1080,760), Status, fill=color_status, font=fnt_report_name)
            draw.text((140,830), 'หน้าจ่าย : ' , fill=color, font=fnt_report_name)
            draw.text((1230, 830), str(result_site.NOZZLE_pump_log_address), fill=color, font=fnt_report_name)
            draw.text((140,900), 'มือจ่าย :' , fill=color, font=fnt_report_name)
            draw.text((1230, 900), str(result_site.NOZZLE_num), fill=color, font=fnt_report_name)
            draw.text((140,975), 'BatteryVolt. ' , fill=color, font=fnt_report_name)
            draw.text((1170, 975), str(result_site.NOZZLE_Battery_Status_Volts), fill=color, font=fnt_report_name)
            draw.text((140, 1050), str('SerialNo : '), fill=color, font=fnt_report_name)
            draw.text((1080, 1050), str(result_site.NOZZLE_SN), fill=color, font=fnt_report_name)
            draw.text((140, 1120), str('LastCon : '), fill=color, font=fnt_report_name)
            draw.text((930, 1120), str(result_site.NOZZLE_Last_conn), fill=color, font=fnt_report_name)
            draw.text((140, 1200), str('ติิดต่อไม่ได้เมื่อ : '), fill=color, font=fnt_report_name)
            draw.text((960, 1200), str(Error_start), fill=color, font=fnt_report_name)
            draw.text((140, 1280), str('ติดต่อได้แล้วเมื่อ : '), fill=color, font=fnt_report_name)
            draw.text((960, 1280), str(datetime_now), fill=color, font=fnt_report_name)
            draw.text((140, 1350), str('ขาดการติดต่อนาน : '), fill=color, font=fnt_report_name)
            draw.text((890, 1350), str(day_loss)+' วัน '+str(hours_loss)+' ชม. '+ str(minutes_loss)+' นาที', fill=color, font=fnt_report_name)
            draw.text((140, 1420), str('ทีมงาน : '), fill=color, font=fnt_report_name)
            draw.text((920, 1420), 'คุณ : '+result_site.site.team_support.team_name, fill=color, font=fnt_report_name)
            dt_save = datetime.datetime.now().strftime("%d-%m-%y-%H:%M")
            image.save(patch_save, optimize=True, quality=20)
            return (patch_save)  
    def CreatingPictureForBATTERY(Status_in,site_profile):
        if Status_in == 'NORMAL':
            Header_type = 'BATTERY : NORMAL'
            Header_IP_TYPE = 'MWGT : IP '
            Status = 'NORMAL'
            color_status = 'rgb(0,255,0)'
        elif Status_in == 'LOW':
            Header_type = 'BATTERY : LOW'
            Header_IP_TYPE = 'MWGT : IP '
            Status = 'LOW'
            color_status = 'rgb(255,128,0)'
        elif Status_in == 'ALARM':
            Header_type = 'BATTERY : ALARM'
            Header_IP_TYPE = 'MWGT : IP '
            Status = 'ALARM'
            color_status = 'rgb(220,20,60)'
      
        result_site = site_profile # รับค่า return มาจาก linebot/connect_db_profile/get_site_profile ใน index ที่ 0
        # day_loss = line_data[0] # รับค่า return มาจาก linebot/calculate_function/different_time_calculate โดย return มาทั้งหมด 5 index 0
        # hours_loss = line_data[1] # รับค่า return มาจาก linebot/calculate_function/different_time_calculate โดย return มาทั้งหมด 5 index 1
        # minutes_loss = line_data[2] # รับค่า return มาจาก linebot/calculate_function/different_time_calculate โดย return มาทั้งหมด 5 index 2
        # datetime_now = line_data[3] # รับค่า return มาจาก linebot/calculate_function/different_time_calculate โดย return มาทั้งหมด 5 index 3
        # Error_start = line_data[4] # รับค่า return มาจาก linebot/calculate_function/different_time_calculate โดย return มาทั้งหมด 5 index 4
        datetime_now = datetime.datetime.now().strftime("%d-%m-%y-%H:%M")
        dt_save = datetime.datetime.now().strftime("%d-%m-%y-%H:%M")
        file_path = 'line_folder/picture_store/VIS-FORM.jpg'  # Window Server
        path_font_check = 'line_folder/font/THSarabunNew.ttf'
        path_save_check = 'line_folder/picture_for_send/'+ 'BATTERY' +dt_save+'.jpg'
        module_dir = os.path.dirname(__file__)  # get current directory
        path = os.path.join(module_dir, file_path)# Window Server
        path_font = os.path.join(module_dir, path_font_check)# Window Server
        patch_save = os.path.join(module_dir, path_save_check)# Window Server
        image = Image.open(path)
        imageSizeW, imageSizeH = image.size
        draw = ImageDraw.Draw(image)
        color = 'rgb(0, 0, 0)'  # black color
        fnt_hardder = ImageFont.truetype(path_font, 120)
        fnt_report_name = ImageFont.truetype(path_font, 70)
        fnt_report_detail = ImageFont.truetype(path_font, 80)
        fnt_report_sub_detail = ImageFont.truetype(path_font, 50)
        draw.text((450, 300), datetime_now, fill=color, font=fnt_hardder)
        draw.text((430,430), Header_type, fill=color_status, font=fnt_hardder)
        draw.text((140, 620), 'สถานี : ' + result_site.site.station_name, fill=color, font=fnt_report_name)
        draw.text((140,700), Header_IP_TYPE  + str(result_site.site.mwgt_ip), fill=color, font=fnt_report_name)
        draw.text((140,760), 'สถานะ ' , fill=color, font=fnt_report_name)
        draw.text((1110,760), Status, fill=color_status, font=fnt_report_name)
        draw.text((140,830), 'หน้าจ่าย : ' , fill=color, font=fnt_report_name)
        draw.text((1230, 830), str(result_site.NOZZLE_pump_log_address), fill=color, font=fnt_report_name)
        draw.text((140,900), 'มือจ่าย :' , fill=color, font=fnt_report_name)
        draw.text((1230, 900), str(result_site.NOZZLE_num), fill=color, font=fnt_report_name)
        draw.text((140,975), 'BatteryVolt. ' , fill=color, font=fnt_report_name)
        draw.text((1170, 975), str(result_site.NOZZLE_Battery_Status_Volts), fill=color, font=fnt_report_name)
        draw.text((140, 1050), str('SerialNo : '), fill=color, font=fnt_report_name)
        draw.text((1080, 1050), str(result_site.NOZZLE_SN), fill=color, font=fnt_report_name)
        draw.text((140, 1120), str('LastCon : '), fill=color, font=fnt_report_name)
        draw.text((930, 1120), str(result_site.NOZZLE_Last_conn), fill=color, font=fnt_report_name)
        # draw.text((140, 1200), str('ติิดต่อไม่ได้เมื่อ : '), fill=color, font=fnt_report_name)
        # draw.text((960, 1200), str(Error_start), fill=color, font=fnt_report_name)
        # draw.text((140, 1280), str('ขาดการติดต่อเมื่อ : '), fill=color, font=fnt_report_name)
        # draw.text((960, 1280), str(datetime_now), fill=color, font=fnt_report_name)
        # draw.text((140, 1350), str('ขาดการติดต่อนาน : '), fill=color, font=fnt_report_name)
        # draw.text((890, 1350), str(day_loss)+' วัน '+str(hours_loss)+' ชม. '+ str(minutes_loss)+' นาที', fill=color, font=fnt_report_name)
        draw.text((140, 1420), str('ทีมงาน : '), fill=color, font=fnt_report_name)
        draw.text((920, 1420), 'คุณ : '+result_site.site.team_support.team_name, fill=color, font=fnt_report_name)
        dt_save = datetime.datetime.now().strftime("%d-%m-%y-%H:%M")
        # path_save = 'line_folder/picture_for_send/'+ 'MWGT-OFFLINE-' +dt_save+'.jpg'
        image.save(patch_save, optimize=True, quality=20)
        return (patch_save)
    