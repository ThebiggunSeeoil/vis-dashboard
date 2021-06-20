import io
import urllib.parse
import sys
import time
import datetime
import os
from PIL import Image, ImageDraw, ImageFont

class creating_picture_for_line_notify():
    def CreatingPictureForVisGoOffline(line_data,site_profile):
        result_site = site_profile # รับค่า return มาจาก linebot/connect_db_profile/get_site_profile ใน index ที่ 0
        day_loss = line_data[0] # รับค่า return มาจาก linebot/calculate_function/different_time_calculate โดย return มาทั้งหมด 5 index 0
        hours_loss = line_data[1] # รับค่า return มาจาก linebot/calculate_function/different_time_calculate โดย return มาทั้งหมด 5 index 1
        minutes_loss = line_data[2] # รับค่า return มาจาก linebot/calculate_function/different_time_calculate โดย return มาทั้งหมด 5 index 2
        datetime_now = line_data[3] # รับค่า return มาจาก linebot/calculate_function/different_time_calculate โดย return มาทั้งหมด 5 index 3
        VIS_last_time = line_data[4] # รับค่า return มาจาก linebot/calculate_function/different_time_calculate โดย return มาทั้งหมด 5 index 4
        # print ('team support is',result_site.site.team_support.team_name)
        # messages = 'VIS Status ' + '\n' + \
        #                 'Type : ' + ' การติดต่อ : ไม่ปกติ ' + '\n' \
        #                     'สถานี : ' + result_site.site.station_name + '\n' + \
        #                         'IP : ' + result_site.site.station_ip + '\n' + \
        #                             'ติดต่อไม่ได้เมื่อ : ' + datetime_now + '\n' + \
        #                                 'ติดต่อครั้งล่าสุด : ' + MWGT_last_time + '\n' + \
        #                                     'ขาดการติดต่อนาน : ' + str(day_loss) + \
        #                                         ' วัน ' + str(hours_loss) + \
        #                                             ' ชม ' + str(minutes_loss) + \
        #                                                 ' นาที' + '\n' + 'ช่างเขต : ' + result_site.site.team_support.team_name
        file_path = 'line_folder/picture_store/VIS-OFFLINE.jpg'  # Window Server
        path_font_check = 'line_folder/font/THSarabunNew.ttf'
        path_save_check = 'line_folder/picture_for_send/'+ 'VIS-OFFLINE-' +'dt_save'+'.jpg'
        module_dir = os.path.dirname(__file__)  # get current directory
        path = os.path.join(module_dir, file_path)# Window Server
        path_font = os.path.join(module_dir, path_font_check)# Window Server
        patch_save = os.path.join(module_dir, path_save_check)# Window Server
        image = Image.open(path)
        imageSizeW, imageSizeH = image.size
        draw = ImageDraw.Draw(image)
        color = 'rgb(0, 0, 0)'  # black color
        # fnt_hardder = ImageFont.truetype(path_font, 70)
        # fnt_report_name = ImageFont.truetype(path_font, 60)
        # fnt_report_detail = ImageFont.truetype(path_font, 80)
        # fnt_report_sub_detail = ImageFont.truetype(path_font, 50)
        # draw.text((220, 180), datetime_now, fill=color, font=fnt_hardder)
        # draw.text(((imageSizeW - (len(result_site.site.station_name))) / 4, 265), result_site.site.station_name, fill=color, font=fnt_report_name)
        # draw.text((220,340), 'VIS:IP : ' + str(result_site.site.station_ip), fill=color, font=fnt_report_name)
        # draw.text((500, 576), str(datetime_now), fill=color, font=fnt_report_sub_detail)
        # draw.text((500, 636), str(VIS_last_time), fill=color, font=fnt_report_sub_detail)
        # draw.text((446, 710), str(day_loss)+' วัน '+ str(hours_loss)+' ชม. '+ str(minutes_loss)+' นาที', fill=color, font=fnt_report_sub_detail)
        # draw.text((500, 775), str('คุณ : '+result_site.site.team_support.team_name), fill=color, font=fnt_report_sub_detail)
        fnt_hardder = ImageFont.truetype(path_font, 120)
        fnt_report_name = ImageFont.truetype(path_font, 100)
        fnt_report_detail = ImageFont.truetype(path_font, 80)
        fnt_report_sub_detail = ImageFont.truetype(path_font, 50)
        draw.text((400, 390), datetime_now, fill=color, font=fnt_hardder)
        
        
        # draw.text(((imageSizeW - (len(result_site.site.station_name))) / 4, 530), result_site.site.station_name, fill=color, font=fnt_report_name)
        # draw.text((350,650), 'VIS : IP '  + str(result_site.site.station_ip), fill=color, font=fnt_report_name)
        # draw.text((450,750), 'VIS : OFFLINE ', fill='rgb(255,0,0)', font=fnt_report_name)
        # draw.text((400, 390), datetime_now, fill=color, font=fnt_hardder)
        
        draw.text((450,530), 'VIS : OFFLINE ', fill='rgb(255,0,0)', font=fnt_report_name)
        draw.text((100,650), 'VIS : IP '  + str(result_site.site.station_ip), fill=color, font=fnt_report_name)
        draw.text((100, 760), 'สถานี : ' + result_site.site.station_name, fill=color, font=fnt_report_name)
        draw.text((1020,910), 'OFFLINE ', fill='rgb(255,0,0)', font=fnt_report_detail)
        draw.text((870, 1030), str(datetime_now), fill=color, font=fnt_report_detail)
        draw.text((870, 1130), str(VIS_last_time), fill=color, font=fnt_report_detail)
        draw.text((780, 1250), str(day_loss)+' วัน '+str(hours_loss)+' ชม. '+ str(minutes_loss)+' นาที', fill=color, font=fnt_report_detail)
        draw.text((820, 1370), str('คุณ : '+result_site.site.team_support.team_name), fill=color, font=fnt_report_detail)
        dt_save = datetime.datetime.now().strftime("%d-%m-%y-%H:%M")
        # path_save = 'line_folder/picture_for_send/'+ 'VIS-OFFLINE-' +'dt_save'+'.jpg'
        print ('path_save is',patch_save)
        image.save(patch_save, optimize=True, quality=20)
        return (patch_save)
        