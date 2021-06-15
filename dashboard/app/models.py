# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

# python manage.py migrate --fake 'appname' zero ใช้สำหรับ fake ตัวข้อมูลกรณีระบบไม่ยอม migrate ให้
from django.utils import timezone
from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User


class Team(models.Model):
    team = models.CharField(max_length=255, unique=True, blank=True, null=True)
    team_name = models.CharField(max_length=255, blank=True, null=True)
    line_notify_token = models.CharField(max_length=255, blank=True, null=True)
    line_offical_token = models.CharField(max_length=255, blank=True, null=True)
    remark = models.CharField(max_length=255, blank=True, null=True)
    last_update = models.DateTimeField(auto_now_add=True, auto_now=False, blank=True)

    def __str__(self):
        return self.team_name

    class Meta:
        ordering = ('team',)  # ทำหน้าที่เรียงลำดับการแสดงผลที่หน้าเวบ
        verbose_name = 'ทีมงาน'  # แปลงให้ข้อมูลหน้าเวบเป็นภาษาไทย
        verbose_name_plural = 'ข้อมูลทีมงาน'  # แปลงให้ข้อมูลหน้าเวบเป็นภาษาไทย


class VIS_ip_address(models.Model):
    # nozzle_vis = models.O('Nozzle',on_delete=models.SET_NULL,related_name='nozzle_vis')
    nozzle_vis = models.CharField(max_length=255, blank=True, null=True)
    ip_address = models.CharField(max_length=255, blank=True, null=True)
    last_update = models.DateTimeField(auto_now_add=True, auto_now=False, blank=True)

    def __str__(self):
        # return 'Memo={0}, Tag={1}'.format(self.memo, self.tags)
        return self.ip_address

    class Meta:
        ordering = ('ip_address',)  # ทำหน้าที่เรียงลำดับการแสดงผลที่หน้าเวบ
        verbose_name = 'ข้อมูล IP Address'  # แปลงให้ข้อมูลหน้าเวบเป็นภาษาไทย
        verbose_name_plural = 'รายละเอียด IP Address'  # แปลงให้ข้อมูลหน้าเวบเป็นภาษาไทย


class Nozzle(models.Model):
    site = models.ForeignKey('Site', on_delete=models.CASCADE, blank=True, null=True)
    pump_log_address = models.CharField(max_length=255, blank=True, null=True)
    nozzle_num = models.CharField(max_length=255, blank=True, null=True)
    nozzle_status = models.CharField(max_length=255, blank=True, null=True)
    log_address = models.CharField(max_length=255, blank=True, null=True)
    station_ip = models.CharField(max_length=255, blank=True, null=True)
    data_unit_ip = models.CharField(max_length=255, blank=True, null=True)
    active_nozzle = models.BooleanField(default=False)
    last_update = models.DateTimeField(auto_now_add=True, auto_now=False, blank=True)

    def __str__(self):
        return str(self.pump_log_address)

    class Meta:
        ordering = ('log_address', 'pump_log_address',)  # ทำหน้าที่เรียงลำดับการแสดงผลที่หน้าเวบ
        verbose_name = 'มือจ่าย'  # แปลงให้ข้อมูลหน้าเวบเป็นภาษาไทย
        verbose_name_plural = 'ข้อมูลมือจ่าย'  # แปลงให้ข้อมูลหน้าเวบเป็นภาษาไทย


class Site(models.Model):
    station_ip = models.CharField(max_length=255, blank=True, null=True)
    mwgt_ip = models.CharField(max_length=255, blank=True, null=True)
    station_active = models.BooleanField(default=False)
    station_name = models.CharField(max_length=255, blank=True, null=True)
    station_name_eng = models.CharField(max_length=255, blank=True, null=True)
    team_support = models.ForeignKey(Team, on_delete=models.CASCADE, blank=True, null=True)
    nozzle_mapping = models.ForeignKey(VIS_ip_address, on_delete=models.CASCADE, blank=True, null=True)
    province = models.CharField(max_length=255, blank=True, null=True)
    pbl = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=255, blank=True, null=True)
    station_port = models.IntegerField(blank=True, null=True)
    station_status = models.IntegerField(default=0)
    station_password = models.IntegerField(default=123456)
    station_monitor_device = models.IntegerField(default=1)
    alert_via_email = models.IntegerField(default=0)
    alert_via_line = models.IntegerField(default=1)
    masterfield = models.IntegerField(default=1)
    station_enable = models.IntegerField(default=1)
    station_open_time = models.TimeField(default='05:00:00.0000000', blank=True, null=True)
    station_close_time = models.TimeField(default='23:59:00.0000000', blank=True, null=True)
    station_team_manage = models.CharField(max_length=10, blank=True, null=True)
    remark_1 = models.CharField(max_length=255, blank=True, null=True)
    remark_ring = models.CharField(max_length=255, blank=True, null=True)
    timestramp = models.DateTimeField(auto_now_add=True, auto_now=False, blank=True)

    def __str__(self):
        return self.station_name

    class Meta:
        ordering = ('station_name',)  # ทำหน้าที่เรียงลำดับการแสดงผลที่หน้าเวบ
        verbose_name = 'สถานี'  # แปลงให้ข้อมูลหน้าเวบเป็นภาษาไทย
        verbose_name_plural = 'ข้อมูลสถานี'  # แปลงให้ข้อมูลหน้าเวบเป็นภาษาไทย


class Status(models.Model):
    site = models.ForeignKey(Site, on_delete=models.CASCADE, blank=True, null=True)
    name_id = models.IntegerField(blank=True, null=True)
    MWGT_last_time = models.DateTimeField(default=now)
    MWGT_status = models.CharField(max_length=255, blank=True, null=True)
    NOZZLE_status_check = models.CharField(max_length=255, default='online')
    BATTERY_status_check = models.CharField(max_length=255, default='normal')
    VIS_last_time = models.DateTimeField(default=now)
    VIS_status = models.CharField(max_length=255, blank=True, null=True)
    RTC = models.CharField(max_length=255, blank=True, null=True)
    DESC = models.CharField(max_length=255, blank=True, null=True)
    DataUnitMap_Status = models.CharField(max_length=255, default='None')
    DataUnitMap_StatusDesc = models.CharField(max_length=255, default='None')
    DataUnitMap_IP = models.CharField(max_length=255, default='None')
    Unit_log_LgAddr = models.CharField(max_length=255, blank=True, null=True)
    Unit_log_address = models.CharField(max_length=255, default='None')
    Unit_GWTypS = models.CharField(max_length=255, blank=True, null=True)
    Unit_sw_location = models.CharField(max_length=255, blank=True, null=True)
    Unit_sw_version = models.CharField(max_length=255, default='None')
    Unit_hw_version = models.CharField(max_length=255, default='None')
    Unit_status_code = models.CharField(max_length=255, default='None')
    Unit_status_desc = models.CharField(max_length=255, default='None')
    NOZZLE_pump_log_address = models.CharField(max_length=255, default='None', blank=True, null=True)
    NOZZLE_num = models.CharField(max_length=255, default='None', blank=True, null=True)
    NOZZLE_status = models.CharField(max_length=255, default='None', blank=True, null=True)
    NOZZLE_SW_Version = models.CharField(max_length=20, default='None', blank=True, null=True)
    NOZZLE_HW_Version = models.CharField(max_length=20, default='None', blank=True, null=True)
    NOZZLE_SN = models.CharField(max_length=255, default='None')
    NOZZLE_Last_conn = models.CharField(max_length=255, default='None')
    NOZZLE_Battery_Status = models.CharField(max_length=255, default='None')
    NOZZLE_Battery_Status_Volts = models.CharField(max_length=255, default='3.50')
    NOZZLE_Battery_BatPrcnt = models.CharField(max_length=255, default='None')
    Timestramp = models.DateTimeField(auto_now_add=True, auto_now=False, blank=True)

    def __str__(self):
        return str(self.name_id)

    class Meta:
        ordering = ('name_id',)  # ทำหน้าที่เรียงลำดับการแสดงผลที่หน้าเวบ
        verbose_name = 'สถานะ'  # แปลงให้ข้อมูลหน้าเวบเป็นภาษาไทย
        verbose_name_plural = 'ข้อมูลสถานะ'  # แปลงให้ข้อมูลหน้าเวบเป็นภาษาไทย

class battery_status (models.Model):
    site = models.ForeignKey(Site, on_delete=models.CASCADE, null=True)
    name_id = models.IntegerField(blank=True, null=True)
    date_stamp = models.DateTimeField(null=True, blank=True)
    mac = models.CharField(max_length=255, blank=True, null=True)
    sn = models.CharField(max_length=255, blank=True, null=True)
    fwtype = models.CharField(max_length=255, blank=True, null=True)
    version = models.CharField(max_length=255, blank=True, null=True)
    devtype = models.CharField(max_length=255, blank=True, null=True)
    din = models.CharField(max_length=255, blank=True, null=True)
    battery_vcclevel = models.CharField(max_length=255, blank=True, null=True)
    battery_level = models.CharField(max_length=255, blank=True, null=True)
    temp = models.CharField(max_length=255, blank=True, null=True)
    fwu = models.CharField(max_length=255, blank=True, null=True)
    
    def __str__(self):
        return str(self.sn)

    class Meta:
        ordering = ('date_stamp',)  # ทำหน้าที่เรียงลำดับการแสดงผลที่หน้าเวบ
        verbose_name = 'แบตเตอร์รี่'  # แปลงให้ข้อมูลหน้าเวบเป็นภาษาไทย
        verbose_name_plural = 'สถานะแบตเตอร์รี่'  # แปลงให้ข้อมูลหน้าเวบเป็นภาษาไทย
    
    
    

class Status_Error_logger(models.Model):
    site = models.ForeignKey(Site, on_delete=models.CASCADE, null=True)
    name_id = models.CharField(max_length=255, blank=True, null=True)
    Error_type = models.CharField(max_length=255, blank=True, null=True)
    Error_start = models.DateTimeField(default=now)
    Error_stop = models.DateTimeField(null=True, blank=True)
    Timestramp = models.DateTimeField(auto_now_add=True, auto_now=False, blank=True)

    def __str__(self):
        return self.name_id

    class Meta:
        ordering = ('name_id',)  # ทำหน้าที่เรียงลำดับการแสดงผลที่หน้าเวบ
        verbose_name = 'ประวัติ'  # แปลงให้ข้อมูลหน้าเวบเป็นภาษาไทย
        verbose_name_plural = 'รายละเอียดประวัติ'  # แปลงให้ข้อมูลหน้าเวบเป็นภาษาไทย


class Store_data_send_line_failed(models.Model):
    site = models.ForeignKey(Site, on_delete=models.CASCADE, null=True)
    name_id = models.CharField(max_length=255, blank=True, null=True)
    team_name = models.ForeignKey(Team, on_delete=models.CASCADE, null=True)
    date_failed = models.DateTimeField(default=now)
    date_pass = models.DateTimeField(null=True, blank=True)
    messages = models.TextField(null=True, blank=True)
    status_send = models.CharField(max_length=255, blank=True, null=True)
    last_update = models.DateTimeField(auto_now_add=True, auto_now=False, blank=True)

    def __str__(self):
        return self.name_id

    class Meta:
        ordering = ('name_id',)  # ทำหน้าที่เรียงลำดับการแสดงผลที่หน้าเวบ
        verbose_name = 'สถานะการส่งแจ้งเตือน'  # แปลงให้ข้อมูลหน้าเวบเป็นภาษาไทย
        verbose_name_plural = 'ข้อมูลการส่งข้อมูลไม่ผ่านสถานะ'  # แปลงให้ข้อมูลหน้าเวบเป็นภาษาไทย











