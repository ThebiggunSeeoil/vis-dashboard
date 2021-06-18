# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path, include
from app import views
from django.contrib import admin
admin.site.site_header = 'VIS-MONITOR PAGE ADMIN'
admin.site.site_title = 'VIS-MONITOR PAGE ADMIN'

urlpatterns = [
    re_path(r'^.*\.html', views.pages, name='pages'),
    path('', views.index, name='home'),
    path('linebot/', include('linebot.urls')),
    path('updatedatabase/', include('linebot.urls')), #send data to update into database
    path('permission_check/', include('linebot.urls')),#send request to check permistion
    path('vis-status/',views.visstatus,name='vis-status'),
    path('vis-status-test/',views.visstatus_test,name='vis-status-test'),
    path('search/',views.search,name='search'),
    path('update_battery/', include('linebot.urls')),
    path('task_jobs/', include('linebot.urls')),

    # path('get_more_tables',views.get_more_tables,name='get_more_tables'),

]
