
class creating_line_data ():
        def Line_Creating_MWGT_OFFLINE (line_data,site_profile):
            result_site = site_profile[0] # รับค่า return มาจาก linebot/connect_db_profile/get_site_profile ใน index ที่ 0
            day_loss = line_data[0] # รับค่า return มาจาก linebot/calculate_function/different_time_calculate โดย return มาทั้งหมด 5 index 0
            hours_loss = line_data[1] # รับค่า return มาจาก linebot/calculate_function/different_time_calculate โดย return มาทั้งหมด 5 index 1
            minutes_loss = line_data[2] # รับค่า return มาจาก linebot/calculate_function/different_time_calculate โดย return มาทั้งหมด 5 index 2
            datetime_now = line_data[3] # รับค่า return มาจาก linebot/calculate_function/different_time_calculate โดย return มาทั้งหมด 5 index 3
            MWGT_last_time = line_data[4] # รับค่า return มาจาก linebot/calculate_function/different_time_calculate โดย return มาทั้งหมด 5 index 4
            messages = 'MWGT Status ' + '\n' + \
                            'Type : ' + ' การติดต่อ : ไม่ปกติ ' + '\n' \
                                'สถานี : ' + result_site.station_name + '\n' + \
                                    'IP : ' + result_site.station_ip + '\n' + \
                                        'ติดต่อไม่ได้เมื่อ : ' + datetime_now + '\n' + \
                                            'ติดต่อครั้งล่าสุด : ' + MWGT_last_time + '\n' + \
                                                'ขาดการติดต่อนาน : ' + str(day_loss) + \
                                                    ' วัน ' + str(hours_loss) + \
                                                        ' ชม ' + str(minutes_loss) + \
                                                            ' นาที' + '\n' + 'ช่างเขต : ' + result_site.team_support.team_name
            return messages , result_site.team_support.line_notify_token #result_site.team_support.line_notify_token คือ อ้างอิงจาก site_profile --> อ้างไปที่ ตาราง Site -- > team_support --> อ้างไปที่ ตาราง Team --> line_notify_token

        def Line_Creating_MWGT_ONLINE (line_data,site_profile):
            result_site = site_profile[0] # รับค่า return มาจาก linebot/connect_db_profile/get_site_profile ใน index ที่ 0
            day_loss = line_data[0] # รับค่า return มาจาก linebot/calculate_function/different_time_calculate โดย return มาทั้งหมด 5 index 0
            hours_loss = line_data[1] # รับค่า return มาจาก linebot/calculate_function/different_time_calculate โดย return มาทั้งหมด 5 index 1
            minutes_loss = line_data[2] # รับค่า return มาจาก linebot/calculate_function/different_time_calculate โดย return มาทั้งหมด 5 index 2
            datetime_now = line_data[3] # รับค่า return มาจาก linebot/calculate_function/different_time_calculate โดย return มาทั้งหมด 5 index 3
            Error_start = line_data[4] # รับค่า return มาจาก linebot/calculate_function/different_time_calculate โดย return มาทั้งหมด 5 index 4
            messages = 'MWGT Status ' + '\n' + \
                            'Type : ' + ' การติดต่อ : ปกติ' + '\n'\
                                'สถานี : ' + result_site.station_name + '\n' + \
                                    'IP : ' + result_site.station_ip + '\n' + \
                                        'ติดต่อไม่ได้เมื่อ : ' + Error_start + '\n' + \
                                            'ติดต่อได้ล่าสุด : ' + datetime_now + '\n' + \
                                                'ขาดการติดต่อรวม : ' + str(day_loss) + \
                                                    ' วัน ' + str(hours_loss) + \
                                                        ' ชม ' + str(minutes_loss) + \
                                                            ' นาที' + '\n' + 'ช่างเขต : ' + result_site.team_support.team_name
            return messages , result_site.team_support.line_notify_token #result_site.team_support.line_notify_token คือ อ้างอิงจาก site_profile --> อ้างไปที่ ตาราง Site -- > team_support --> อ้างไปที่ ตาราง Team --> line_notify_token

        def Line_Creating_VIS_OFFLINE (line_data,site_profile):
            result_site = site_profile[0] # รับค่า return มาจาก linebot/connect_db_profile/get_site_profile ใน index ที่ 0
            day_loss = line_data[0] # รับค่า return มาจาก linebot/calculate_function/different_time_calculate โดย return มาทั้งหมด 5 index 0
            hours_loss = line_data[1] # รับค่า return มาจาก linebot/calculate_function/different_time_calculate โดย return มาทั้งหมด 5 index 1
            minutes_loss = line_data[2] # รับค่า return มาจาก linebot/calculate_function/different_time_calculate โดย return มาทั้งหมด 5 index 2
            datetime_now = line_data[3] # รับค่า return มาจาก linebot/calculate_function/different_time_calculate โดย return มาทั้งหมด 5 index 3
            MWGT_last_time = line_data[4] # รับค่า return มาจาก linebot/calculate_function/different_time_calculate โดย return มาทั้งหมด 5 index 4
            messages = 'MWGT Status ' + '\n' + \
                            'Type : ' + ' การติดต่อ : ไม่ปกติ ' + '\n' \
                                'สถานี : ' + result_site.station_name + '\n' + \
                                    'IP : ' + result_site.station_ip + '\n' + \
                                        'ติดต่อไม่ได้เมื่อ : ' + datetime_now + '\n' + \
                                            'ติดต่อครั้งล่าสุด : ' + MWGT_last_time + '\n' + \
                                                'ขาดการติดต่อนาน : ' + str(day_loss) + \
                                                    ' วัน ' + str(hours_loss) + \
                                                        ' ชม ' + str(minutes_loss) + \
                                                            ' นาที' + '\n' + 'ช่างเขต : ' + result_site.team_support.team_name
            return messages , result_site.team_support.line_notify_token #result_site.team_support.line_notify_token คือ อ้างอิงจาก site_profile --> อ้างไปที่ ตาราง Site -- > team_support --> อ้างไปที่ ตาราง Team --> line_notify_token

        def Line_Creating_VIS_ONLINE (line_data,site_profile):
            result_site = site_profile[0] # รับค่า return มาจาก linebot/connect_db_profile/get_site_profile ใน index ที่ 0
            day_loss = line_data[0] # รับค่า return มาจาก linebot/calculate_function/different_time_calculate โดย return มาทั้งหมด 5 index 0
            hours_loss = line_data[1] # รับค่า return มาจาก linebot/calculate_function/different_time_calculate โดย return มาทั้งหมด 5 index 1
            minutes_loss = line_data[2] # รับค่า return มาจาก linebot/calculate_function/different_time_calculate โดย return มาทั้งหมด 5 index 2
            datetime_now = line_data[3] # รับค่า return มาจาก linebot/calculate_function/different_time_calculate โดย return มาทั้งหมด 5 index 3
            Error_start = line_data[4] # รับค่า return มาจาก linebot/calculate_function/different_time_calculate โดย return มาทั้งหมด 5 index 4
            messages = 'MWGT Status ' + '\n' + \
                            'Type : ' + ' การติดต่อ : ปกติ' + '\n'\
                                'สถานี : ' + result_site.station_name + '\n' + \
                                    'IP : ' + result_site.station_ip + '\n' + \
                                        'ติดต่อไม่ได้เมื่อ : ' + Error_start + '\n' + \
                                            'ติดต่อได้ล่าสุด : ' + datetime_now + '\n' + \
                                                'ขาดการติดต่อรวม : ' + str(day_loss) + \
                                                    ' วัน ' + str(hours_loss) + \
                                                        ' ชม ' + str(minutes_loss) + \
                                                            ' นาที' + '\n' + 'ช่างเขต : ' + result_site.team_support.team_name
            return messages , result_site.team_support.line_notify_token #result_site.team_support.line_notify_token คือ อ้างอิงจาก site_profile --> อ้างไปที่ ตาราง Site -- > team_support --> อ้างไปที่ ตาราง Team --> line_notify_token