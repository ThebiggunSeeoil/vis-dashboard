# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from app.models import Team,Site,Nozzle,Status,Status_Error_logger,VIS_ip_address,Setup_Config,LinegroupId,PersanalDetaillogin
from admin_auto_filters.filters import AutocompleteFilter

@admin.register(Site)
class SiteListAdmin(ImportExportModelAdmin):
    search_fields = ('station_name', 'station_ip') # สร้าง tab ในการค้นหาข้อมูลต่างที่ต้องการ
    list_filter = ['station_name']
    list_display = ("station_name","station_ip","station_active")

    list_per_page = 30
    pass

@admin.register(Team)
class TeamListAdmin(ImportExportModelAdmin):
    list_display = ("team","team_name","line_notify_token")
    list_per_page = 30
    pass

# @admin.register(VIS_ip_address)
# class VisAddressListAdmin(ImportExportModelAdmin):
#     list_display = ("ip_address","last_update")
#     list_per_page = 30
#     pass

# ส่วนของการสร้าง Filter ในหน้า Admin เพื่อสร้างการค้นหาจากรายชื่อสถานี
class NozzleFilter(AutocompleteFilter): #ขั้นตอนที่ 1
    title = 'เลือกสถานีที่ต้องการ' # กำหนดชื่อที่ต้องการให้แสดงในส่วนหัว
    field_name = 'site' # อ้างไปที่ตารางที่ได้มีการทำ foreign key field เอาไว้ กรณีนี้อ้างไปที่ตาราง Site เพื่อเอาชื่อสถานีมาแสดง

class ArtistAdmin(admin.ModelAdmin): #ขั้นตอนที่ 2
    search_fields = ['site__station_name'] # อ้างอิงไปที่ตาราง Site และเลือกฟิวที่ต้องการทำการ Filter กรณีนี้ให้เอาชื่อสถานีมาแสดง

@admin.register(Nozzle)
class NozzleListAdmin(ImportExportModelAdmin):
    search_fields = ('site__station_name','station_ip','pump_log_address') # สร้าง tab ในการค้นหาข้อมูลต่างที่ต้องการ
    list_filter = [NozzleFilter] #สร้าง list_filter แล้วอ้างอิงไปที่ Classs ที่ทำไว้ในข้้นตอนที่ 1
    # search_filter =['site',]
    list_display = ("site","station_ip","log_address","pump_log_address","nozzle_num","active_nozzle")
    list_per_page = 30
    def detail(self,obj):
        return u'%s %s' % (obj.site, obj.station_ip)
    # pass


# ส่วนของการสร้าง Filter ในหน้า Admin เพื่อสร้างการค้นหาจากรายชื่อสถานี
class StatusFilter(AutocompleteFilter): #ขั้นตอนที่ 1
    title = 'เลือกสถานีที่ต้องการ' # กำหนดชื่อที่ต้องการให้แสดงในส่วนหัว
    field_name = 'site' # อ้างไปที่ตารางที่ได้มีการทำ foreign key field เอาไว้ กรณีนี้อ้างไปที่ตาราง Site เพื่อเอาชื่อสถานีมาแสดง


class StatusAdmin(admin.ModelAdmin): #ขั้นตอนที่ 2
    search_fields = ['site__station_name'] # อ้างอิงไปที่ตาราง Site และเลือกฟิวที่ต้องการทำการ Filter กรณีนี้ให้เอาชื่อสถานีมาแสดง

@admin.register(Status)
class StatusListAdmin(ImportExportModelAdmin):
    # search_fields = ('site', 'station_ip') # สร้าง tab ในการค้นหาข้อมูลต่างที่ต้องการ
    list_filter = [StatusFilter]  # สร้าง list_filter แล้วอ้างอิงไปที่ Classs ที่ทำไว้ในข้้นตอนที่ 1
    list_display = ("site","VIS_status","MWGT_status","NOZZLE_pump_log_address","NOZZLE_num","NOZZLE_Last_conn","VIS_last_time","MWGT_last_time")
    list_per_page = 30
    pass

@admin.register(Status_Error_logger)
class StatusErrorListAdmin(ImportExportModelAdmin):
    # search_fields = ('site', 'station_ip') # สร้าง tab ในการค้นหาข้อมูลต่างที่ต้องการ
    list_display = ("site","name_id","Error_type","Error_start","Timestramp")
    list_per_page = 30
    pass


@admin.register(Setup_Config)
class SetupListAdmin(ImportExportModelAdmin):
    # search_fields = ('time_alert_alarm_day', 'time_alert_warning_day','battery_level_alarm_hours','battery_level_low_hours','battery_level_failed_hours') # สร้าง tab ในการค้นหาข้อมูลต่างที่ต้องการ
    # list_filter = ['station_name']
    list_display = ('time_alert_alarm_hours', 'time_alert_warning_hours','battery_level_alarm_volt','battery_level_low_volt','battery_level_failed_volt')

    list_per_page = 30
    # This will help you to disbale add functionality
    def has_add_permission(self, request):
        return False

    # This will help you to disable delete functionaliyt
    def has_delete_permission(self, request, obj=None):
        return False
    pass

@admin.register(LinegroupId)
class LinegroupIdListAdmin(ImportExportModelAdmin):
    # search_fields = ('time_alert_alarm_day', 'time_alert_warning_day','battery_level_alarm_hours','battery_level_low_hours','battery_level_failed_hours') # สร้าง tab ในการค้นหาข้อมูลต่างที่ต้องการ
    # list_filter = ['station_name']
    list_display = ('group_name', 'group_id')

    list_per_page = 30
    # This will help you to disbale add functionality
    # def has_add_permission(self, request):
    #     return False

    # # This will help you to disable delete functionaliyt
    # def has_delete_permission(self, request, obj=None):
    #     return False
    pass

@admin.register(PersanalDetaillogin)
class PersanalDetailloginListAdmin(ImportExportModelAdmin):
    # search_fields = ('time_alert_alarm_day', 'time_alert_warning_day','battery_level_alarm_hours','battery_level_low_hours','battery_level_failed_hours') # สร้าง tab ในการค้นหาข้อมูลต่างที่ต้องการ
    # list_filter = ['station_name']
    list_display = ('company', 'user_type','name','need_to_notify')
    exclude = ('richmenu_id','line_id','line_id_name','member_status') # ซ่อนในหน้า Admain หากไม่ต้องการให้แสดง
    list_per_page = 30
    # This will help you to disbale add functionality
    # def has_add_permission(self, request):
    #     return False

    # # This will help you to disable delete functionaliyt
    # def has_delete_permission(self, request, obj=None):
    #     return False
    pass
# Register your models here.
