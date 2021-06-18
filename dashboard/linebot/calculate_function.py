
import datetime
from dateutil.relativedelta import relativedelta, SA, TH

class different_time_calculate ():
    def different_time_calculate(TimeZone,TimeCalculate):
        print(TimeCalculate)
        # TimeCalculateDetail = TimeCalculate[1].MWGT_last_time
        print('TimeCalculateDetail',TimeCalculate)
        different_time = relativedelta(TimeZone,TimeCalculate)  # คำนวณหาผลต่างระหว่างวันที่ Now กับ MWGT_last_time
        day_loss = different_time.days  # แสดงผลลัพท์เป็นจำนวนวัน จาก different_time
        hours_loss = different_time.hours  # แสดงผลลัพท์เป็นจำนวน ชั่วโมง จาก different_time
        minutes_loss = different_time.minutes  # แสดงผลลัพท์เป็นจำนวนวัน นาที different_time
        datetime_now = datetime.datetime.now().strftime("%d-%m-%y %H:%M")
        MWGT_last_time = TimeCalculate.strftime("%d-%m-%y %H:%M")    # แปลง datetime
        print('TimeCalculateDetail',TimeCalculate)
        print('different_time',different_time)
        print('day_loss',day_loss)
        print('hours_loss',hours_loss)
        print('minutes_loss',minutes_loss)
        print('datetime_now',datetime_now)
        print('MWGT_last_time',MWGT_last_time)
        return day_loss , hours_loss , minutes_loss , datetime_now , MWGT_last_time