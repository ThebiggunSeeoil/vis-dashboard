# -*- coding: utf-8 -*-
# !/usr/bin/env python
from app.models import Site, Status, Status_Error_logger, Store_data_send_line_failed, PersanalDetaillogin
import datetime
import requests
import json
from django.conf import settings
Channel_access_token = settings.LINE_CHANNEL_ACCESS_TOKEN


class creating_flex_messages():
    def PushMessage(messages, user_id):
        print('Nozzle 2')
        Token = Channel_access_token
        LINE_API = 'https://api.line.me/v2/bot/message/push'
        # print('line API {}'.format(push_new_messasge))

        Authorization = 'Bearer {}'.format(Token)
        headers = {
            'Content-Type': 'application/json; charset=UTF-8',
            'Authorization': Authorization
        }

        data = {
            "to": user_id,
            "messages": [messages], }

        # print('data to line {}'.format(data))
        data = json.dumps(data)
        r = requests.post(LINE_API, headers=headers, data=data)
        print(r)
        return 200

    def CheckPermissionBeforeSendLine(technician_team_name, messages):
        # start to check permission before send
        technician_detail = PersanalDetaillogin.objects.select_related().filter(
            need_to_notify=True, if_technician__team=technician_team_name)
        if technician_detail.exists():
            for detail in technician_detail:
                user_id = detail.line_id
                name = detail.name
                creating_flex_messages.PushMessage(messages, user_id)
            print('SUCCESS TO SEND LINE TO Technician need to send line flex_message for team_name {} line_id{}'.format(
                name, user_id))
        else:
            print('DO NOT FOUND Technician need to send line flex_message for team_name {}'.format(
                technician_team_name))

        supervisor_detail = PersanalDetaillogin.objects.select_related().filter(
            need_to_notify=True, user_type__id__in=[2])
        if supervisor_detail.exists():
            for detail in technician_detail:
                user_id = detail.line_id
                name = detail.name
                creating_flex_messages.PushMessage(messages, user_id)
            print('SUCCESS TO SEND LINE TO Supervisor need to send line flex_message for Supervisor Name {} line_id{}'.format(
                name, user_id))
        else:
            print('DO NOT FOUND LINE TO Supervisor need to send line flex_message for Team Name {}'.format(
                technician_team_name))

    def CreateFormDetailByIpAddress(results):
        for site_detail in results:
            print(site_detail['site_name'])
            if site_detail['VIS_status'] == 'offline':
                coler_1 = '#EE2424FF'
            else:
                coler_1 = '#000000'

            if site_detail['MWGT_status'] == 'offline':
                coler_2 = '#EE2424FF'
            else:
                coler_2 = '#000000'

            if site_detail['NOZZLE_status_check'] == 'offline':
                coler_3 = '#EE2424FF'
            else:
                coler_3 = '#000000'

            if site_detail['BATTERY_status_check'] == 'low':
                coler_4 = '#EE2424FF'
            else:
                coler_4 = '#000000'

            data = {"type": "flex",
                    "altText": "Flex Message",
                    "contents": {
                        "type": "carousel",
                        "contents": [
                            {
                                "type": "bubble",
                                "hero": {
                                    "type": "image",
                                    "url": "https://seeoil-web.com/picture_logo/VIS-MONITOR/vis.png",
                                    "align": "center",
                                    "gravity": "bottom",
                                    "size": "full",
                                    "aspectRatio": "35:8",
                                    "aspectMode": "fit",
                                    "action": {
                                        "type": "uri",
                                        "label": "Line",
                                        "uri": "https://linecorp.com/"
                                    },
                                    "position": "relative"
                                },
                                "body": {
                                    "type": "box",
                                    "layout": "vertical",
                                    "contents": [
                                        {
                                            "type": "text",
                                            "text": str(datetime.datetime.now().strftime("%d.%m.%y %H:%M")),
                                            "weight": "bold",
                                            "size": "sm",
                                            "color": "#225508FF",
                                            "align": "center",
                                            "gravity": "bottom",
                                            "contents": []
                                        },
                                        {
                                            "type": "text",
                                            "text": str(site_detail['site_name']),
                                            "weight": "bold",
                                            "size": "sm",
                                            "color": "#225508FF",
                                            "align": "center",
                                            "gravity": "bottom",
                                            "contents": []
                                        },
                                        {
                                            "type": "text",
                                            "text": "VIS : IP " + str(site_detail['station_ip']),
                                            "weight": "bold",
                                            "size": "sm",
                                            "color": "#225508FF",
                                            "align": "center",
                                            "margin": "xs",
                                            "wrap": True,
                                            "contents": []
                                        },
                                        {
                                            "type": "text",
                                            "text": "MWGT " + str(site_detail['log_address_count']) + " Device",
                                            "weight": "bold",
                                            "size": "sm",
                                            "color": "#225508FF",
                                            "align": "center",
                                            "margin": "xs",
                                            "wrap": True,
                                            "contents": []
                                        },
                                        {
                                            "type": "separator",
                                            "margin": "sm",
                                            "color": "#165C3CFF"
                                        },
                                        {
                                            "type": "box",
                                            "layout": "vertical",
                                            "spacing": "sm",
                                            "margin": "lg",
                                            "contents": [
                                                {
                                                    "type": "text",
                                                    "text": "??????????????????????????????",
                                                    "weight": "bold",
                                                    "size": "xs",
                                                    "align": "center",
                                                    "contents": []
                                                }
                                            ]
                                        },
                                        {
                                            "type": "box",
                                            "layout": "baseline",
                                            "spacing": "sm",
                                            "margin": "xs",
                                            "contents": [
                                                {
                                                    "type": "text",
                                                    "text": "VisStatus",
                                                    "size": "xs",
                                                    "align": "start",
                                                    "contents": []
                                                },
                                                {
                                                    "type": "text",
                                                    "text": str(site_detail['VIS_status']),
                                                    "size": "xs",
                                                    "color": coler_1,
                                                    "align": "end",
                                                    "contents": []
                                                }
                                            ]
                                        },
                                        {
                                            "type": "box",
                                            "layout": "baseline",
                                            "spacing": "sm",
                                            "margin": "sm",
                                            "contents": [
                                                {
                                                    "type": "text",
                                                    "text": "LastConnect",
                                                    "size": "xs",
                                                    "align": "start",
                                                    "contents": []
                                                },
                                                {
                                                    "type": "text",
                                                    "text": str(site_detail['VIS_last_time'].strftime("%d.%m.%y %H:%M")),
                                                    "size": "xs",
                                                    "align": "end",
                                                    "contents": []
                                                }
                                            ]
                                        },
                                        {
                                            "type": "box",
                                            "layout": "baseline",
                                            "spacing": "sm",
                                            "margin": "sm",
                                            "contents": [
                                                {
                                                    "type": "text",
                                                    "text": "LogAdds",
                                                    "size": "xs",
                                                    "align": "start",
                                                    "contents": []
                                                },
                                                {
                                                    "type": "text",
                                                    "text": str(site_detail['log_address_count']),
                                                    "size": "xs",
                                                    "align": "end",
                                                    "contents": []
                                                }
                                            ]
                                        },
                                        {
                                            "type": "box",
                                            "layout": "baseline",
                                            "spacing": "sm",
                                            "margin": "sm",
                                            "contents": [
                                                {
                                                    "type": "text",
                                                    "text": "NozzleActive",
                                                    "size": "xs",
                                                    "align": "start",
                                                    "contents": []
                                                },
                                                {
                                                    "type": "text",
                                                    "text": str('[' + str(site_detail['pump_log_address_count']) + ' ???????????? | ' + str(site_detail['nozzle_data_count']) + ' ?????????????????????]'),
                                                    "size": "xs",
                                                    "align": "end",
                                                    "contents": []
                                                }
                                            ]
                                        },
                                        {
                                            "type": "box",
                                            "layout": "baseline",
                                            "spacing": "sm",
                                            "margin": "sm",
                                            "contents": [
                                                {
                                                    "type": "text",
                                                    "text": "MwgtStatus",
                                                    "size": "xs",
                                                    "align": "start",
                                                    "contents": []
                                                },
                                                {
                                                    "type": "text",
                                                    "text": str(site_detail['MWGT_status']),
                                                    "size": "xs",
                                                    "color": coler_2,
                                                    "align": "end",
                                                    "contents": []
                                                }
                                            ]
                                        },
                                        {
                                            "type": "box",
                                            "layout": "baseline",
                                            "spacing": "sm",
                                            "margin": "sm",
                                            "contents": [
                                                {
                                                    "type": "text",
                                                    "text": "NozzleStatus",
                                                    "size": "xs",
                                                    "align": "start",
                                                    "contents": []
                                                },
                                                {
                                                    "type": "text",
                                                    "text": str(site_detail['NOZZLE_status_check']),
                                                    "size": "xs",
                                                    "color": coler_3,
                                                    "align": "end",
                                                    "contents": []
                                                }
                                            ]
                                        },
                                        {
                                            "type": "box",
                                            "layout": "baseline",
                                            "spacing": "sm",
                                            "margin": "sm",
                                            "contents": [
                                                {
                                                    "type": "text",
                                                    "text": "BatteryStatus",
                                                    "size": "xs",
                                                    "align": "start",
                                                    "contents": []
                                                },
                                                {
                                                    "type": "text",
                                                    "text": str(site_detail['BATTERY_status_check']),
                                                    "size": "xs",
                                                    "color": coler_4,
                                                    "align": "end",
                                                    "contents": []
                                                }
                                            ]
                                        },
                                        {
                                            "type": "separator",
                                            "margin": "md",
                                            "color": "#165C3CFF"
                                        }
                                    ]
                                },
                                "footer": {
                                    "type": "box",
                                    "layout": "vertical",
                                    "flex": 0,
                                    "spacing": "sm",
                                    "contents": [
                                        {
                                            "type": "button",
                                            "action": {
                                                "type": "uri",
                                                "label": "www.orpak.com",
                                                "uri": "https://www.orpak.com/"
                                            },
                                            "color": "#078025FF",
                                            "margin": "none",
                                            "height": "sm",
                                            "style": "primary"
                                        },
                                        {
                                            "type": "spacer",
                                            "size": "sm"
                                        }
                                    ]
                                }
                            },
                            # Body next

                            # ?????? ???????????? Body
                        ]
                    }}

            for log_address in site_detail['Unit_log_address']:
                print('log_address is ', log_address)
                content_log_address = {
                    "type": "bubble",
                    "hero": {
                        "type": "image",
                        "url": "https://seeoil-web.com/picture_logo/VIS-MONITOR/vis.png",
                        "align": "center",
                        "gravity": "bottom",
                        "size": "full",
                        "aspectRatio": "35:8",
                        "aspectMode": "fit",
                        "action": {
                            "type": "uri",
                            "label": "Line",
                            "uri": "https://linecorp.com/"
                        },
                        "position": "relative"
                    },
                    "body": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": 'MWGT Device' + str(log_address['Unit_log_address']),
                                "weight": "bold",
                                "size": "sm",
                                "color": "#225508FF",
                                "align": "center",
                                "gravity": "bottom",
                                "contents": []
                            },
                            {
                                "type": "text",
                                "text": 'IP ' + str(log_address['DataUnitMap_IP']),
                                "weight": "bold",
                                "size": "sm",
                                "color": "#225508FF",
                                "align": "center",
                                "margin": "xs",
                                "wrap": True,
                                "contents": []
                            },
                            {
                                "type": "separator",
                                "margin": "sm",
                                "color": "#165C3CFF"
                            },
                            {
                                "type": "box",
                                "layout": "vertical",
                                "spacing": "sm",
                                "margin": "lg",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "??????????????????????????????",
                                        "weight": "bold",
                                        "size": "md",
                                        "align": "center",
                                        "contents": []
                                    }
                                ]
                            },
                            {
                                "type": "box",
                                "layout": "baseline",
                                "spacing": "sm",
                                "margin": "xs",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "Pump",
                                        "weight": "bold",
                                        "size": "xs",
                                        "align": "center",
                                        "contents": []
                                    },
                                    {
                                        "type": "text",
                                        "text": "Nozzle",
                                        "weight": "bold",
                                        "size": "xs",
                                        "align": "center",
                                        "contents": []
                                    },
                                    {
                                        "type": "text",
                                        "text": "BatV.",
                                        "weight": "bold",
                                        "size": "xs",
                                        "align": "center",
                                        "contents": []
                                    },
                                    {
                                        "type": "text",
                                        "text": "LastCon",
                                        "weight": "bold",
                                        "size": "xs",
                                        "flex": 2,
                                        "align": "end",
                                        "contents": []
                                    }
                                ]
                            },
                            # ???????????????????????????????????????????????????????????????????????????


                            # ?????? ???????????????????????????????????????????????????????????????????????????

                            {
                                "type": "separator",
                                "margin": "md",
                                "color": "#165C3CFF"
                            }
                        ]
                    },
                    "footer": {
                        "type": "box",
                        "layout": "vertical",
                        "flex": 0,
                        "spacing": "sm",
                        "contents": [
                            {
                                "type": "button",
                                "action": {
                                    "type": "uri",
                                    "label": "www.orpak.com",
                                    "uri": "https://www.orpak.com/"
                                },
                                "color": "#078025FF",
                                "margin": "none",
                                "height": "sm",
                                "style": "primary"
                            },
                            {
                                "type": "separator"
                            }
                        ]
                    }
                }
                for nozzle_detail in log_address['nozzle']:
                    if nozzle_detail['NOZZLE_status_check'] == 'offline':
                        coler = '#EE2424FF'
                    else:
                        coler = '#000000'

                    content_nozzle = {
                        "type": "box",
                        "layout": "baseline",
                        "spacing": "sm",
                        "margin": "xs",
                        "contents": [
                            {
                                "type": "text",
                                "text": str(nozzle_detail['NOZZLE_pump_log_address']),
                                "size": "xs",
                                "color": coler,
                                "align": "center",
                                "contents": []
                            },
                            {
                                "type": "text",
                                "text": str(nozzle_detail['NOZZLE_num']),
                                "size": "xs",
                                "color": coler,
                                "align": "center",
                                "contents": []
                            },
                            {
                                "type": "text",
                                "text": str(nozzle_detail['NOZZLE_Battery_Status_Volts']),
                                "size": "xxs",
                                "color": coler,
                                "align": "center",
                                "contents": []
                            },
                            {
                                "type": "text",
                                "text": str(nozzle_detail['NOZZLE_Last_conn']),
                                "size": "xxs",
                                "color": coler,
                                "flex": 2,
                                "align": "end",
                                "style": "normal",
                                "contents": []
                            }
                        ]
                    }
                    content_log_address['body']['contents'].insert(
                        -1, content_nozzle)
                data['contents']['contents'].insert(1, content_log_address)
        return (data)

    def CreateFormAllStatusForMGR(dt, VIS_SUM_OFFLINE, MWGT_SUM_OFFLINE, NOZZLE_OFFLINE, BATTERY_OFFLINE, TOTAL_SITE_ACTIVE):
        data = {"type": "flex",
                "altText": "Flex Message",
                "contents":
                {
                    "type": "carousel",
                    "contents": [{
                        "type": "bubble",
                        "size": "mega",
                        "hero": {
                            "type": "image",
                            "url": "https://seeoil-web.com/picture_logo/VIS-MONITOR/vis.png",
                            "align": "center",
                            "gravity": "bottom",
                            "size": "full",
                            "aspectRatio": "35:8",
                            "aspectMode": "fit",
                            "action": {
                                "type": "uri",
                                "label": "Line",
                                "uri": "https://linecorp.com/"
                            },
                            "position": "relative"
                        },
                        "body": {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "VIS MONITOR STATUS",
                                    "weight": "bold",
                                    "size": "sm",
                                    "color": "#225508FF",
                                    "align": "center",
                                    "contents": []
                                },
                                {
                                    "type": "text",
                                    "text": str(dt),
                                    "weight": "bold",
                                    "size": "sm",
                                    "color": "#225508FF",
                                    "align": "center",
                                    "contents": []
                                },
                                {
                                    "type": "separator",
                                    "margin": "sm",
                                    "color": "#165C3CFF"
                                },
                                {
                                    "type": "box",
                                    "layout": "baseline",
                                    "spacing": "sm",
                                    "margin": "lg",
                                    "contents": [
                                        {
                                            "type": "text",
                                            "text": "Status",
                                            "weight": "bold",
                                            "size": "xs",
                                            "contents": []
                                        },
                                        {
                                            "type": "text",
                                            "text": "VIS",
                                            "weight": "bold",
                                            "size": "xs",
                                            "align": "center",
                                            "position": "relative",
                                            "contents": []
                                        },
                                        {
                                            "type": "text",
                                            "text": "MWGT",
                                            "weight": "bold",
                                            "size": "xs",
                                            "align": "center",
                                            "contents": []
                                        },
                                        {
                                            "type": "text",
                                            "text": "Nozzle",
                                            "weight": "bold",
                                            "size": "xs",
                                            "align": "center",
                                            "contents": []
                                        },
                                        {
                                            "type": "text",
                                            "text": "Battery",
                                            "weight": "bold",
                                            "size": "xs",
                                            "align": "center",
                                            "contents": []
                                        }
                                    ]
                                },
                                {
                                    "type": "box",
                                    "layout": "baseline",
                                    "margin": "md",
                                    "contents": [
                                        {
                                            "type": "text",
                                            "text": "Offline",
                                            "size": "xs",
                                            "align": "start",
                                            "contents": []
                                        },
                                        {
                                            "type": "text",
                                            "text": str(VIS_SUM_OFFLINE),
                                            "size": "xs",
                                            "align": "center",
                                            "position": "relative",
                                            "contents": []
                                        },
                                        {
                                            "type": "text",
                                            "text": str(MWGT_SUM_OFFLINE),
                                            "size": "xs",
                                            "align": "center",
                                            "contents": []
                                        },
                                        {
                                            "type": "text",
                                            "text": str(NOZZLE_OFFLINE),
                                            "size": "xs",
                                            "align": "center",
                                            "contents": []
                                        },
                                        {
                                            "type": "text",
                                            "text": '-',
                                            "size": "xs",
                                            "align": "center",
                                            "contents": []
                                        }
                                    ]
                                },
                                {
                                    "type": "box",
                                    "layout": "baseline",
                                    "margin": "md",
                                    "contents": [
                                        {
                                            "type": "text",
                                            "text": "Low:Volt",
                                            "size": "xs",
                                            "align": "start",
                                            "contents": []
                                        },
                                        {
                                            "type": "text",
                                            "text": "-",
                                            "size": "xs",
                                            "align": "center",
                                            "position": "relative",
                                            "contents": []
                                        },
                                        {
                                            "type": "text",
                                            "text": "-",
                                            "size": "xs",
                                            "align": "center",
                                            "contents": []
                                        },
                                        {
                                            "type": "text",
                                            "text": "-",
                                            "size": "xs",
                                            "align": "center",
                                            "contents": []
                                        },
                                        {
                                            "type": "text",
                                            "text": str(BATTERY_OFFLINE),
                                            "size": "xs",
                                            "align": "center",
                                            "contents": []
                                        }
                                    ]
                                },
                                {
                                    "type": "separator",
                                    "margin": "md",
                                    "color": "#165C3CFF"
                                },
                                {
                                    "type": "text",
                                    "text": "Total Online " + str(TOTAL_SITE_ACTIVE) + " Station",
                                    "weight": "bold",
                                    "size": "sm",
                                    "color": "#225508FF",
                                    "align": "center",
                                    "margin": "xxl",
                                    "contents": []
                                }
                            ]
                        }
                    }

                    ]

                }}
        return data

    def CreateFormAllStatusForFirstLevel(dt, VIS_SUM_OFFLINE, MWGT_SUM_OFFLINE, NOZZLE_OFFLINE, BATTERY_OFFLINE, TOTAL_SITE_ACTIVE, user_type):
        if user_type.user_type.id == 6:
            content_tech = {
                "type": "text",
                "text": '?????????????????? : ' + str(user_type.if_technician.team) + ' ????????? : ' + str(user_type.if_technician.team_name),
                "weight": "bold",
                "align": "center",
                "margin": "xs",
                "contents": []
            }
        if user_type.user_type.id != 6:
            content_tech = {
                "type": "text",
                "text": '-',
                "weight": "bold",
                "align": "center",
                "margin": "xs",
                "contents": []
            }

        data = {"type": "flex",
                "altText": "Flex Message",
                "contents":
                {
                    "type": "carousel",
                    "contents": [{
                        "type": "bubble",
                        "size": "mega",
                        "hero": {
                            "type": "image",
                            "url": "https://seeoil-web.com/picture_logo/VIS-MONITOR/vis.png",
                            "align": "center",
                            "gravity": "bottom",
                            "size": "full",
                            "aspectRatio": "35:8",
                            "aspectMode": "fit",
                            "action": {
                                "type": "uri",
                                "label": "Line",
                                "uri": "https://linecorp.com/"
                            },
                            "position": "relative"
                        },
                        "body": {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "VIS MONITOR STATUS",
                                    "weight": "bold",
                                    "size": "sm",
                                    "color": "#225508FF",
                                    "align": "center",
                                    "contents": []
                                },
                                {
                                    "type": "text",
                                    "text": str(dt),
                                    "weight": "bold",
                                    "size": "sm",
                                    "color": "#225508FF",
                                    "align": "center",
                                    "contents": []
                                },
                                content_tech,
                                {
                                    "type": "separator",
                                    "margin": "sm",
                                    "color": "#165C3CFF"
                                },
                                {
                                    "type": "box",
                                    "layout": "baseline",
                                    "spacing": "sm",
                                    "margin": "lg",
                                    "contents": [
                                        {
                                            "type": "text",
                                            "text": "Status",
                                            "weight": "bold",
                                            "size": "xs",
                                            "contents": []
                                        },
                                        {
                                            "type": "text",
                                            "text": "VIS",
                                            "weight": "bold",
                                            "size": "xs",
                                            "align": "center",
                                            "position": "relative",
                                            "contents": []
                                        },
                                        {
                                            "type": "text",
                                            "text": "MWGT",
                                            "weight": "bold",
                                            "size": "xs",
                                            "align": "center",
                                            "contents": []
                                        },
                                        {
                                            "type": "text",
                                            "text": "Nozzle",
                                            "weight": "bold",
                                            "size": "xs",
                                            "align": "center",
                                            "contents": []
                                        },
                                        {
                                            "type": "text",
                                            "text": "Battery",
                                            "weight": "bold",
                                            "size": "xs",
                                            "align": "center",
                                            "contents": []
                                        }
                                    ]
                                },
                                {
                                    "type": "box",
                                    "layout": "baseline",
                                    "margin": "md",
                                    "contents": [
                                        {
                                            "type": "text",
                                            "text": "Offline",
                                            "size": "xs",
                                            "align": "start",
                                            "contents": []
                                        },
                                        {
                                            "type": "text",
                                            "text": str(VIS_SUM_OFFLINE),
                                            "size": "xs",
                                            "align": "center",
                                            "position": "relative",
                                            "contents": []
                                        },
                                        {
                                            "type": "text",
                                            "text": str(MWGT_SUM_OFFLINE),
                                            "size": "xs",
                                            "align": "center",
                                            "contents": []
                                        },
                                        {
                                            "type": "text",
                                            "text": str(NOZZLE_OFFLINE),
                                            "size": "xs",
                                            "align": "center",
                                            "contents": []
                                        },
                                        {
                                            "type": "text",
                                            "text": '-',
                                            "size": "xs",
                                            "align": "center",
                                            "contents": []
                                        }
                                    ]
                                },
                                {
                                    "type": "box",
                                    "layout": "baseline",
                                    "margin": "md",
                                    "contents": [
                                        {
                                            "type": "text",
                                            "text": "Low:Volt",
                                            "size": "xs",
                                            "align": "start",
                                            "contents": []
                                        },
                                        {
                                            "type": "text",
                                            "text": "-",
                                            "size": "xs",
                                            "align": "center",
                                            "position": "relative",
                                            "contents": []
                                        },
                                        {
                                            "type": "text",
                                            "text": "-",
                                            "size": "xs",
                                            "align": "center",
                                            "contents": []
                                        },
                                        {
                                            "type": "text",
                                            "text": "-",
                                            "size": "xs",
                                            "align": "center",
                                            "contents": []
                                        },
                                        {
                                            "type": "text",
                                            "text": str(BATTERY_OFFLINE),
                                            "size": "xs",
                                            "align": "center",
                                            "contents": []
                                        }
                                    ]
                                },
                                {
                                    "type": "separator",
                                    "margin": "md",
                                    "color": "#165C3CFF"
                                },
                                {
                                    "type": "text",
                                    "text": "Total Online " + str(TOTAL_SITE_ACTIVE) + " Station",
                                    "weight": "bold",
                                    "size": "sm",
                                    "color": "#225508FF",
                                    "align": "center",
                                    "margin": "xxl",
                                    "contents": []
                                }
                            ]
                        }
                    }

                    ]

                }}
        return data

    def CreateFormVisFlexMessageDetail(data, user_type):
        if user_type.user_type.id == 6:
            content_tech = {
                "type": "text",
                "text": '?????????????????? : ' + str(data['user_type'].if_technician.team) + ' ????????? : ' + str(data['user_type'].if_technician.team_name),
                "weight": "bold",
                "align": "center",
                "margin": "xs",
                "contents": []
            }
        if user_type.user_type.id != 6:
            content_tech = {
                "type": "text",
                "text": '-',
                "weight": "bold",
                "align": "center",
                "margin": "xs",
                "contents": []
            }

        content = {
            "type": "carousel",
            "contents": [
                # ?????????????????? 1
                {
                    "type": "bubble",
                    "hero": {
                        "type": "image",
                        "url": "https://seeoil-web.com/picture_logo/VIS-MONITOR/vis.png",
                        "align": "center",
                        "gravity": "bottom",
                        "size": "full",
                        "aspectRatio": "35:8",
                        "aspectMode": "fit",
                        "action": {
                            "type": "uri",
                            "label": "Line",
                            "uri": "https://linecorp.com/"
                        },
                        "position": "relative"
                    },
                    "body": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": "VIS : STATUS",
                                "weight": "bold",
                                "size": "xl",
                                "color": "#225508FF",
                                "align": "center",
                                "gravity": "center",
                                "contents": []
                            },
                            {
                                "type": "text",
                                "text": str(data['TIME_UPDATE'].strftime("%d.%m.%Y %H:%M")),
                                "weight": "bold",
                                "size": "lg",
                                "color": "#225508FF",
                                "align": "center",
                                "gravity": "center",
                                "contents": []
                            },
                            {
                                "type": "separator",
                                "margin": "sm",
                                "color": "#165C3CFF"
                            },
                            {
                                "type": "box",
                                "layout": "vertical",
                                "spacing": "sm",
                                "margin": "lg",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "?????????????????????????????????????????????",
                                        "weight": "bold",
                                        "size": "lg",
                                        "align": "center",
                                        "gravity": "center",
                                        "contents": []
                                    },
                                    content_tech,
                                ]
                            },
                            {
                                "type": "box",
                                "layout": "baseline",
                                "spacing": "sm",
                                "margin": "xs",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "Deive",
                                        "weight": "bold",
                                        "size": "md",
                                        "align": "center",
                                        "gravity": "center",
                                        "contents": []
                                    },
                                    {
                                        "type": "text",
                                        "text": "OnLine",
                                        "weight": "bold",
                                        "size": "md",
                                        "align": "center",
                                        "contents": []
                                    },
                                    {
                                        "type": "text",
                                        "text": "OffLine",
                                        "weight": "bold",
                                        "size": "md",
                                        "align": "center",
                                        "contents": []
                                    }
                                ]
                            },
                            {
                                "type": "box",
                                "layout": "baseline",
                                "spacing": "sm",
                                "margin": "xs",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "VIS",
                                        "weight": "bold",
                                        "size": "md",
                                        "align": "center",
                                        "contents": []
                                    },
                                    {
                                        "type": "text",
                                        "text": str(int(data['TOTAL_SITE_ACTIVE']) - int(data['VIS_SUM_OFFLINE'])),
                                        "weight": "bold",
                                        "size": "md",
                                        "align": "center",
                                        "contents": []
                                    },
                                    {
                                        "type": "text",
                                        "text": str(data['VIS_SUM_OFFLINE']),
                                        "weight": "bold",
                                        "size": "md",
                                        "align": "center",
                                        "contents": []
                                    }
                                ]
                            },
                            {
                                "type": "separator",
                                "margin": "md",
                                "color": "#165C3CFF"
                            },
                            {
                                "type": "text",
                                "text": "Total Online " + str(data['TOTAL_SITE_ACTIVE']) + ' ' + " Station",
                                "weight": "bold",
                                "size": "lg",
                                "color": "#225508FF",
                                "align": "center",
                                "gravity": "bottom",
                                "margin": "xxl",
                                "contents": []
                            }
                        ]
                    },
                    "footer": {
                        "type": "box",
                        "layout": "vertical",
                        "flex": 0,
                        "spacing": "sm",
                        "contents": [
                            {
                                "type": "button",
                                "action": {
                                    "type": "uri",
                                    "label": "www.orpak.com",
                                    "uri": "https://www.orpak.com/"
                                },
                                "color": "#078025FF",
                                "margin": "none",
                                "height": "sm",
                                "style": "secondary"
                            },
                            {
                                "type": "spacer",
                                "size": "sm"
                            }
                        ]
                    }
                },
                # ?????????????????? 2
                {
                    "type": "bubble",
                    "hero": {
                        "type": "image",
                        "url": "https://seeoil-web.com/picture_logo/VIS-MONITOR/vis.png",
                        "align": "center",
                        "gravity": "bottom",
                        "size": "full",
                        "aspectRatio": "35:8",
                        "aspectMode": "fit",
                        "action": {
                            "type": "uri",
                            "label": "Line",
                            "uri": "https://linecorp.com/"
                        },
                        "position": "relative"
                    },
                    "body": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": "VIS : STATUS",
                                "weight": "bold",
                                "size": "xl",
                                "color": "#225508FF",
                                "align": "center",
                                "gravity": "bottom",
                                "contents": []
                            },
                            {
                                "type": "text",
                                "text": str(data['TIME_UPDATE'].strftime("%d.%m.%Y %H:%M")),
                                "weight": "bold",
                                "size": "lg",
                                "color": "#225508FF",
                                "align": "center",
                                "gravity": "bottom",
                                "contents": []
                            },
                            {
                                "type": "separator",
                                "margin": "sm",
                                "color": "#165C3CFF"
                            },
                            {
                                "type": "box",
                                "layout": "vertical",
                                "spacing": "sm",
                                "margin": "lg",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "??????????????????????????????????????????????????? VIS Offline",
                                        "weight": "bold",
                                        "size": "md",
                                        "align": "center",
                                        "contents": []
                                    }
                                ]
                            },
                            {
                                "type": "box",
                                "layout": "baseline",
                                "spacing": "sm",
                                "margin": "xs",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "???????????????",
                                        "weight": "bold",
                                        "size": "md",
                                        "align": "start",
                                        "contents": []
                                    },
                                    {
                                        "type": "text",
                                        "text": "IP-Address",
                                        "weight": "bold",
                                        "size": "md",
                                        "align": "end",
                                        "contents": []
                                    }
                                ]
                            },
                            # ?????????????????????????????????????????????????????????????????????
                            {
                                "type": "separator",
                                "margin": "md",
                                "color": "#165C3CFF"
                            },
                            {
                                "type": "text",
                                "text": "?????????????????????????????????????????? ????????????????????????????????? ip address ????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????",
                                "weight": "bold",
                                "size": "sm",
                                "color": "#225508FF",
                                "align": "center",
                                "margin": "xxl",
                                "wrap": True,
                                "contents": []
                            }
                        ]
                    }
                },
                # ?????????????????? 3
                {
                    "type": "bubble",
                    "hero": {
                        "type": "image",
                        "url": "https://seeoil-web.com/picture_logo/VIS-MONITOR/vis.png",
                        "align": "center",
                        "gravity": "bottom",
                        "size": "full",
                        "aspectRatio": "35:8",
                        "aspectMode": "fit",
                        "action": {
                            "type": "uri",
                            "label": "Line",
                            "uri": "https://linecorp.com/"
                        },
                        "position": "relative"
                    },
                    "body": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": "VIS : STATUS",
                                "weight": "bold",
                                "size": "xl",
                                "color": "#225508FF",
                                "align": "center",
                                "gravity": "bottom",
                                "contents": []
                            },
                            {
                                "type": "text",
                                "text": str(data['TIME_UPDATE'].strftime("%d.%m.%Y %H:%M")),
                                "weight": "bold",
                                "size": "lg",
                                "color": "#225508FF",
                                "align": "center",
                                "gravity": "bottom",
                                "contents": []
                            },
                            {
                                "type": "separator",
                                "margin": "sm",
                                "color": "#165C3CFF"
                            },
                            {
                                "type": "box",
                                "layout": "vertical",
                                "spacing": "sm",
                                "margin": "lg",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "??????????????????????????????????????????????????? VIS Offline",
                                        "weight": "bold",
                                        "size": "md",
                                        "align": "center",
                                        "contents": []
                                    }
                                ]
                            },
                            {
                                "type": "box",
                                "layout": "baseline",
                                "spacing": "sm",
                                "margin": "xs",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "???????????????",
                                        "weight": "bold",
                                        "size": "md",
                                        "align": "start",
                                        "contents": []
                                    },
                                    {
                                        "type": "text",
                                        "text": "LastConnect",
                                        "weight": "bold",
                                        "size": "md",
                                        "align": "end",
                                        "contents": []
                                    }
                                ]
                            },
                            # ?????????????????????????????????????????????????????????


                            {
                                "type": "separator",
                                "margin": "md",
                                "color": "#165C3CFF"
                            },
                            {
                                "type": "text",
                                "text": "?????????????????????????????????????????? ????????????????????????????????? ip address ????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????",
                                "weight": "bold",
                                "size": "sm",
                                "color": "#225508FF",
                                "align": "center",
                                "margin": "xxl",
                                "wrap": True,
                                "contents": []
                            }
                        ]
                    }
                },
                # ?????????????????? 4
                {
                    "type": "bubble",
                    "hero": {
                        "type": "image",
                        "url": "https://seeoil-web.com/picture_logo/VIS-MONITOR/vis.png",
                        "align": "center",
                        "gravity": "bottom",
                        "size": "full",
                        "aspectRatio": "35:8",
                        "aspectMode": "fit",
                        "action": {
                            "type": "uri",
                            "label": "Line",
                            "uri": "https://linecorp.com/"
                        },
                        "position": "relative"
                    },
                    "body": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": "VIS : STATUS",
                                "weight": "bold",
                                "size": "xl",
                                "color": "#225508FF",
                                "align": "center",
                                "gravity": "bottom",
                                "contents": []
                            },
                            {
                                "type": "text",
                                "text": "27-12-2020 20:18",
                                "weight": "bold",
                                "size": "lg",
                                "color": "#225508FF",
                                "align": "center",
                                "gravity": "bottom",
                                "contents": []
                            },
                            {
                                "type": "separator",
                                "margin": "sm",
                                "color": "#165C3CFF"
                            },
                            {
                                "type": "box",
                                "layout": "vertical",
                                "spacing": "sm",
                                "margin": "lg",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "??????????????????????????????????????????????????? VIS Offline",
                                        "weight": "bold",
                                        "size": "md",
                                        "align": "center",
                                        "contents": []
                                    }
                                ]
                            },
                            {
                                "type": "box",
                                "layout": "baseline",
                                "spacing": "sm",
                                "margin": "xs",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "???????????????",
                                        "weight": "bold",
                                        "size": "md",
                                        "align": "start",
                                        "contents": []
                                    },
                                    {
                                        "type": "text",
                                        "text": "LostTime",
                                        "weight": "bold",
                                        "size": "md",
                                        "align": "end",
                                        "contents": []
                                    }
                                ]
                            },
                            # ??????????????????????????????????????????

                            {
                                "type": "separator",
                                "margin": "md",
                                "color": "#165C3CFF"
                            },
                            {
                                "type": "text",
                                "text": "?????????????????????????????????????????? ????????????????????????????????? ip address ????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????",
                                "weight": "bold",
                                "size": "sm",
                                "color": "#225508FF",
                                "align": "center",
                                "margin": "xxl",
                                "wrap": True,
                                "contents": []
                            }
                        ]
                    }
                }
            ]
        }
        # ????????????????????????????????? loop 1
        if len(data['VIS_DETAIL']) <= 0:
            content_1 = {
                "type": "box",
                "layout": "baseline",
                "spacing": "sm",
                "margin": "md",
                "contents": [
                    {
                        "type": "text",
                        "text": '-',
                        "weight": "bold",
                        "size": "xs",
                        "align": "start",
                        "contents": []
                    },
                    {
                        "type": "text",
                        "text": '-',
                        "weight": "bold",
                        "size": "xs",
                        "color": "#EC1019FF",
                        "align": "end",
                        "action": {
                            "type": "postback",
                            "text": "?????????????????????????????????",
                            "data": '?????????????????????????????????'
                        },
                        "contents": []
                    }
                ]
            }
            content['contents'][1]['body']['contents'].insert(-2, content_1)
        elif len(data['VIS_DETAIL']) > 0:
            for ip_address in data['VIS_DETAIL']:
                content_1 = {
                    "type": "box",
                    "layout": "baseline",
                    "spacing": "sm",
                    "margin": "md",
                    "contents": [
                        {
                            "type": "text",
                            "text": str(ip_address['name']),
                            "weight": "bold",
                            "size": "xs",
                            "align": "start",
                            "contents": []
                        },
                        {
                            "type": "text",
                            "text": str(ip_address['ip_address']),
                            "weight": "bold",
                            "size": "xs",
                            "color": "#EC1019FF",
                            "align": "end",
                            "action": {
                                "type": "message",
                                "text": "check"+str(ip_address['ip_address'])

                            },
                            "contents": []
                        }
                    ]
                }
                content['contents'][1]['body']['contents'].insert(
                    -2, content_1)

        # ????????????????????????????????? loop 2
        if len(data['VIS_DETAIL']) <= 0:
            content_2 = {
                "type": "box",
                "layout": "baseline",
                "spacing": "sm",
                "margin": "md",
                "contents": [
                    {
                        "type": "text",
                        "text": '-',
                        "weight": "bold",
                        "size": "xs",
                        "align": "start",
                        "contents": []
                    },
                    {
                        "type": "text",
                        "text": '-',
                        "weight": "bold",
                        "size": "xs",
                        "color": "#EC1019FF",
                        "align": "end",
                        "action": {
                            "type": "postback",
                            "text": "?????????????????????????????????",
                            "data": '?????????????????????????????????'
                        },
                        "contents": []
                    }
                ]
            }
            content['contents'][2]['body']['contents'].insert(-2, content_2)
        elif len(data['VIS_DETAIL']) > 0:
            for ip_address in data['VIS_DETAIL']:
                content_2 = {
                    "type": "box",
                    "layout": "baseline",
                    "spacing": "sm",
                    "margin": "md",
                    "contents": [
                        {
                            "type": "text",
                            "text": str(ip_address['name']),
                            "weight": "bold",
                            "size": "xs",
                            "align": "start",
                            "contents": []
                        },
                        {
                            "type": "text",
                            "text": str(ip_address['VIS_last_time'].strftime("%d.%m.%y %H:%M")),
                            "weight": "bold",
                            "size": "xs",
                            "color": "#EC1019FF",
                            "align": "end",
                            "action": {
                                "type": "message",
                                "text": "check"+str(ip_address['ip_address'])

                            },
                            "contents": []
                        }
                    ]
                }
                content['contents'][2]['body']['contents'].insert(
                    -2, content_2)

        # ????????????????????????????????? loop 3
        if len(data['VIS_DETAIL']) <= 0:
            content_3 = {
                "type": "box",
                "layout": "baseline",
                "spacing": "sm",
                "margin": "md",
                "contents": [
                    {
                        "type": "text",
                        "text": '-',
                        "weight": "bold",
                        "size": "xs",
                        "align": "start",
                        "contents": []
                    },
                    {
                        "type": "text",
                        "text": '-',
                        "weight": "bold",
                        "size": "xs",
                        "color": "#EC1019FF",
                        "align": "end",
                        "action": {
                            "type": "postback",
                            "text": "?????????????????????????????????",
                            "data": '?????????????????????????????????'
                        },
                        "contents": []
                    }
                ]
            }
            content['contents'][3]['body']['contents'].insert(-2, content_3)
        elif len(data['VIS_DETAIL']) > 0:
            for ip_address in data['VIS_DETAIL']:
                content_3 = {
                    "type": "box",
                    "layout": "baseline",
                    "spacing": "sm",
                    "margin": "md",
                    "contents": [
                        {
                            "type": "text",
                            "text": str(ip_address['name']),
                            "weight": "bold",
                            "size": "xs",
                            "align": "start",
                            "contents": []
                        },
                        {
                            "type": "text",
                            "text": str(ip_address['time_dif']['day']) + '?????????' + str(ip_address['time_dif']['hour'])+'??????.' + str(ip_address['time_dif']['minutes'])+'????????????',
                            "weight": "bold",
                            "size": "xs",
                            "color": "#EC1019FF",
                            "align": "end",
                            "action": {
                                "type": "message",
                                "text": "check"+str(ip_address['ip_address'])

                            },
                            "contents": []
                        }
                    ]
                }
                content['contents'][3]['body']['contents'].insert(
                    -2, content_3)

        data = {"type": "flex",
                "altText": "Flex Message",
                "contents": content}
        return data

    def CreateFormMwgtFlexMessageDetail(data, user_type):
        if user_type.user_type.id == 6:
            content_tech = {
                "type": "text",
                "text": '?????????????????? : ' + str(data['user_type'].if_technician.team) + ' ????????? : ' + str(data['user_type'].if_technician.team_name),
                "weight": "bold",
                "align": "center",
                "margin": "xs",
                "contents": []
            }
        if user_type.user_type.id != 6:
            content_tech = {
                "type": "text",
                "text": '-',
                "weight": "bold",
                "align": "center",
                "margin": "xs",
                "contents": []
            }
        content = {
            "type": "carousel",
            "contents": [
                # ?????????????????? 1
                {
                    "type": "bubble",
                    "hero": {
                        "type": "image",
                        "url": "https://seeoil-web.com/picture_logo/VIS-MONITOR/vis.png",
                        "align": "center",
                        "gravity": "bottom",
                        "size": "full",
                        "aspectRatio": "35:8",
                        "aspectMode": "fit",
                        "action": {
                            "type": "uri",
                            "label": "Line",
                            "uri": "https://linecorp.com/"
                        },
                        "position": "relative"
                    },
                    "body": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": "MWGT : STATUS",
                                "weight": "bold",
                                "size": "xl",
                                "color": "#225508FF",
                                "align": "center",
                                "gravity": "center",
                                "contents": []
                            },
                            {
                                "type": "text",
                                "text": str(data['TIME_UPDATE'].strftime("%d.%m.%Y %H:%M")),
                                "weight": "bold",
                                "size": "lg",
                                "color": "#225508FF",
                                "align": "center",
                                "gravity": "center",
                                "contents": []
                            },
                            {
                                "type": "separator",
                                "margin": "sm",
                                "color": "#165C3CFF"
                            },
                            {
                                "type": "box",
                                "layout": "vertical",
                                "spacing": "sm",
                                "margin": "lg",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "?????????????????????????????????????????????",
                                        "weight": "bold",
                                        "size": "lg",
                                        "align": "center",
                                        "gravity": "center",
                                        "contents": []
                                    },
                                    content_tech,
                                ]
                            },
                            {
                                "type": "box",
                                "layout": "baseline",
                                "spacing": "sm",
                                "margin": "xs",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "Deive",
                                        "weight": "bold",
                                        "size": "md",
                                        "align": "center",
                                        "gravity": "center",
                                        "contents": []
                                    },
                                    {
                                        "type": "text",
                                        "text": "OnLine",
                                        "weight": "bold",
                                        "size": "md",
                                        "align": "center",
                                        "contents": []
                                    },
                                    {
                                        "type": "text",
                                        "text": "OffLine",
                                        "weight": "bold",
                                        "size": "md",
                                        "align": "center",
                                        "contents": []
                                    }
                                ]
                            },
                            {
                                "type": "box",
                                "layout": "baseline",
                                "spacing": "sm",
                                "margin": "xs",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "MWGT",
                                        "weight": "bold",
                                        "size": "md",
                                        "align": "center",
                                        "contents": []
                                    },
                                    {
                                        "type": "text",
                                        "text": str(int(data['TOTAL_SITE_ACTIVE']) - int(data['MWGT_SUM_OFFLINE'])),
                                        "weight": "bold",
                                        "size": "md",
                                        "align": "center",
                                        "contents": []
                                    },
                                    {
                                        "type": "text",
                                        "text": str(data['MWGT_SUM_OFFLINE']),
                                        "weight": "bold",
                                        "size": "md",
                                        "align": "center",
                                        "contents": []
                                    }
                                ]
                            },
                            {
                                "type": "separator",
                                "margin": "md",
                                "color": "#165C3CFF"
                            },
                            {
                                "type": "text",
                                "text": "Total Online " + str(data['TOTAL_SITE_ACTIVE']) + ' ' + " Station",
                                "weight": "bold",
                                "size": "lg",
                                "color": "#225508FF",
                                "align": "center",
                                "gravity": "bottom",
                                "margin": "xxl",
                                "contents": []
                            }
                        ]
                    },
                    "footer": {
                        "type": "box",
                        "layout": "vertical",
                        "flex": 0,
                        "spacing": "sm",
                        "contents": [
                            {
                                "type": "button",
                                "action": {
                                    "type": "uri",
                                    "label": "www.orpak.com",
                                    "uri": "https://www.orpak.com/"
                                },
                                "color": "#078025FF",
                                "margin": "none",
                                "height": "sm",
                                "style": "secondary"
                            },
                            {
                                "type": "spacer",
                                "size": "sm"
                            }
                        ]
                    }
                },
                # ?????????????????? 2
                {
                    "type": "bubble",
                    "hero": {
                        "type": "image",
                        "url": "https://seeoil-web.com/picture_logo/VIS-MONITOR/vis.png",
                        "align": "center",
                        "gravity": "bottom",
                        "size": "full",
                        "aspectRatio": "35:8",
                        "aspectMode": "fit",
                        "action": {
                            "type": "uri",
                            "label": "Line",
                            "uri": "https://linecorp.com/"
                        },
                        "position": "relative"
                    },
                    "body": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": "VIS : STATUS",
                                "weight": "bold",
                                "size": "xl",
                                "color": "#225508FF",
                                "align": "center",
                                "gravity": "bottom",
                                "contents": []
                            },
                            {
                                "type": "text",
                                "text": str(data['TIME_UPDATE'].strftime("%d.%m.%Y %H:%M")),
                                "weight": "bold",
                                "size": "lg",
                                "color": "#225508FF",
                                "align": "center",
                                "gravity": "bottom",
                                "contents": []
                            },
                            {
                                "type": "separator",
                                "margin": "sm",
                                "color": "#165C3CFF"
                            },
                            {
                                "type": "box",
                                "layout": "vertical",
                                "spacing": "sm",
                                "margin": "lg",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "??????????????????????????????????????????????????? MWGT Offline",
                                        "weight": "bold",
                                        "size": "md",
                                        "align": "center",
                                        "contents": []
                                    }
                                ]
                            },
                            {
                                "type": "box",
                                "layout": "baseline",
                                "spacing": "sm",
                                "margin": "xs",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "???????????????",
                                        "weight": "bold",
                                        "size": "md",
                                        "align": "start",
                                        "contents": []
                                    },
                                    {
                                        "type": "text",
                                        "text": "Unit-Address",
                                        "weight": "bold",
                                        "size": "md",
                                        "align": "end",
                                        "contents": []
                                    }
                                ]
                            },
                            # ?????????????????????????????????????????????????????????????????????
                            {
                                "type": "separator",
                                "margin": "md",
                                "color": "#165C3CFF"
                            },
                            {
                                "type": "text",
                                "text": "?????????????????????????????????????????? ????????????????????????????????? ip address ????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????",
                                "weight": "bold",
                                "size": "sm",
                                "color": "#225508FF",
                                "align": "center",
                                "margin": "xxl",
                                "wrap": True,
                                "contents": []
                            }
                        ]
                    }
                },
                # ?????????????????? 3
                {
                    "type": "bubble",
                    "hero": {
                        "type": "image",
                        "url": "https://seeoil-web.com/picture_logo/VIS-MONITOR/vis.png",
                        "align": "center",
                        "gravity": "bottom",
                        "size": "full",
                        "aspectRatio": "35:8",
                        "aspectMode": "fit",
                        "action": {
                            "type": "uri",
                            "label": "Line",
                            "uri": "https://linecorp.com/"
                        },
                        "position": "relative"
                    },
                    "body": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": "MWGT : STATUS",
                                "weight": "bold",
                                "size": "xl",
                                "color": "#225508FF",
                                "align": "center",
                                "gravity": "bottom",
                                "contents": []
                            },
                            {
                                "type": "text",
                                "text": str(data['TIME_UPDATE'].strftime("%d.%m.%Y %H:%M")),
                                "weight": "bold",
                                "size": "lg",
                                "color": "#225508FF",
                                "align": "center",
                                "gravity": "bottom",
                                "contents": []
                            },
                            {
                                "type": "separator",
                                "margin": "sm",
                                "color": "#165C3CFF"
                            },
                            {
                                "type": "box",
                                "layout": "vertical",
                                "spacing": "sm",
                                "margin": "lg",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "??????????????????????????????????????????????????? MWGT Offline",
                                        "weight": "bold",
                                        "size": "md",
                                        "align": "center",
                                        "contents": []
                                    }
                                ]
                            },
                            {
                                "type": "box",
                                "layout": "baseline",
                                "spacing": "sm",
                                "margin": "xs",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "???????????????",
                                        "weight": "bold",
                                        "size": "md",
                                        "align": "start",
                                        "contents": []
                                    },
                                    {
                                        "type": "text",
                                        "text": "LastConnect",
                                        "weight": "bold",
                                        "size": "md",
                                        "align": "end",
                                        "contents": []
                                    }
                                ]
                            },
                            # ?????????????????????????????????????????????????????????


                            {
                                "type": "separator",
                                "margin": "md",
                                "color": "#165C3CFF"
                            },
                            {
                                "type": "text",
                                "text": "?????????????????????????????????????????? ????????????????????????????????? ip address ????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????",
                                "weight": "bold",
                                "size": "sm",
                                "color": "#225508FF",
                                "align": "center",
                                "margin": "xxl",
                                "wrap": True,
                                "contents": []
                            }
                        ]
                    }
                },
                # ?????????????????? 4
                {
                    "type": "bubble",
                    "hero": {
                        "type": "image",
                        "url": "https://seeoil-web.com/picture_logo/VIS-MONITOR/vis.png",
                        "align": "center",
                        "gravity": "bottom",
                        "size": "full",
                        "aspectRatio": "35:8",
                        "aspectMode": "fit",
                        "action": {
                            "type": "uri",
                            "label": "Line",
                            "uri": "https://linecorp.com/"
                        },
                        "position": "relative"
                    },
                    "body": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": "MWGT : STATUS",
                                "weight": "bold",
                                "size": "xl",
                                "color": "#225508FF",
                                "align": "center",
                                "gravity": "bottom",
                                "contents": []
                            },
                            {
                                "type": "text",
                                "text": str(data['TIME_UPDATE'].strftime("%d.%m.%Y %H:%M")),
                                "weight": "bold",
                                "size": "lg",
                                "color": "#225508FF",
                                "align": "center",
                                "gravity": "bottom",
                                "contents": []
                            },
                            {
                                "type": "separator",
                                "margin": "sm",
                                "color": "#165C3CFF"
                            },
                            {
                                "type": "box",
                                "layout": "vertical",
                                "spacing": "sm",
                                "margin": "lg",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "??????????????????????????????????????????????????? MWGT Offline",
                                        "weight": "bold",
                                        "size": "md",
                                        "align": "center",
                                        "contents": []
                                    }
                                ]
                            },
                            {
                                "type": "box",
                                "layout": "baseline",
                                "spacing": "sm",
                                "margin": "xs",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "???????????????",
                                        "weight": "bold",
                                        "size": "md",
                                        "align": "start",
                                        "contents": []
                                    },
                                    {
                                        "type": "text",
                                        "text": "LostTime",
                                        "weight": "bold",
                                        "size": "md",
                                        "align": "end",
                                        "contents": []
                                    }
                                ]
                            },
                            # ??????????????????????????????????????????

                            {
                                "type": "separator",
                                "margin": "md",
                                "color": "#165C3CFF"
                            },
                            {
                                "type": "text",
                                "text": "?????????????????????????????????????????? ????????????????????????????????? ip address ????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????",
                                "weight": "bold",
                                "size": "sm",
                                "color": "#225508FF",
                                "align": "center",
                                "margin": "xxl",
                                "wrap": True,
                                "contents": []
                            }
                        ]
                    }
                }
            ]
        }
        # ????????????????????????????????? loop 1
        if len(data['MWTG_DETAIL']) <= 0:
            content_1 = {
                "type": "box",
                "layout": "baseline",
                "spacing": "sm",
                "margin": "md",
                "contents": [
                    {
                        "type": "text",
                        "text": '-',
                        "weight": "bold",
                        "size": "xs",
                        "align": "start",
                        "contents": []
                    },
                    {
                        "type": "text",
                        "text": '-',
                        "weight": "bold",
                        "size": "xs",
                        "color": "#EC1019FF",
                        "align": "end",
                        "action": {
                            "type": "postback",
                            "text": "?????????????????????????????????",
                            "data": '?????????????????????????????????'
                        },
                        "contents": []
                    }
                ]
            }
            content['contents'][1]['body']['contents'].insert(-2, content_1)
        elif len(data['MWTG_DETAIL']) > 0:
            for ip_address in data['MWTG_DETAIL']:
                print(ip_address)
                content_1 = {
                    "type": "box",
                    "layout": "baseline",
                    "spacing": "sm",
                    "margin": "md",
                    "contents": [
                        {
                            "type": "text",
                            "text": str(ip_address['name']),
                            "weight": "bold",
                            "size": "xs",
                            "align": "start",
                            "contents": []
                        },
                        {
                            "type": "text",
                            "text": str(ip_address['DataUnitMap_IP']),
                            "weight": "bold",
                            "size": "xs",
                            "color": "#EC1019FF",
                            "align": "end",
                            "action": {
                                "type": "message",
                                "text": "check"+str(ip_address['ip_address'])

                            },
                            "contents": []
                        }
                    ]
                }
                content['contents'][1]['body']['contents'].insert(
                    -2, content_1)

        # ????????????????????????????????? loop 2
        if len(data['MWTG_DETAIL']) <= 0:
            content_2 = {
                "type": "box",
                "layout": "baseline",
                "spacing": "sm",
                "margin": "md",
                "contents": [
                    {
                        "type": "text",
                        "text": '-',
                        "weight": "bold",
                        "size": "xs",
                        "align": "start",
                        "contents": []
                    },
                    {
                        "type": "text",
                        "text": '-',
                        "weight": "bold",
                        "size": "xs",
                        "color": "#EC1019FF",
                        "align": "end",
                        "action": {
                            "type": "postback",
                            "text": "?????????????????????????????????",
                            "data": '?????????????????????????????????'
                        },
                        "contents": []
                    }
                ]
            }
            content['contents'][2]['body']['contents'].insert(-2, content_2)
        elif len(data['MWTG_DETAIL']) > 0:
            for ip_address in data['MWTG_DETAIL']:
                content_2 = {
                    "type": "box",
                    "layout": "baseline",
                    "spacing": "sm",
                    "margin": "md",
                    "contents": [
                        {
                            "type": "text",
                            "text": str(ip_address['name']),
                            "weight": "bold",
                            "size": "xs",
                            "align": "start",
                            "contents": []
                        },
                        {
                            "type": "text",
                            "text": str(ip_address['MWGT_last_time'].strftime("%d.%m.%y %H:%M")),
                            "weight": "bold",
                            "size": "xs",
                            "color": "#EC1019FF",
                            "align": "end",
                            "action": {
                                "type": "message",
                                "text": "check"+str(ip_address['ip_address'])

                            },
                            "contents": []
                        }
                    ]
                }
                content['contents'][2]['body']['contents'].insert(
                    -2, content_2)

        # ????????????????????????????????? loop 3
        if len(data['MWTG_DETAIL']) <= 0:
            content_3 = {
                "type": "box",
                "layout": "baseline",
                "spacing": "sm",
                "margin": "md",
                "contents": [
                    {
                        "type": "text",
                        "text": '-',
                        "weight": "bold",
                        "size": "xs",
                        "align": "start",
                        "contents": []
                    },
                    {
                        "type": "text",
                        "text": '-',
                        "weight": "bold",
                        "size": "xs",
                        "color": "#EC1019FF",
                        "align": "end",
                        "action": {
                            "type": "postback",
                            "text": "?????????????????????????????????",
                            "data": '?????????????????????????????????'
                        },
                        "contents": []
                    }
                ]
            }
            content['contents'][3]['body']['contents'].insert(-2, content_3)
        elif len(data['MWTG_DETAIL']) > 0:
            for ip_address in data['MWTG_DETAIL']:
                content_3 = {
                    "type": "box",
                    "layout": "baseline",
                    "spacing": "sm",
                    "margin": "md",
                    "contents": [
                        {
                            "type": "text",
                            "text": str(ip_address['name']),
                            "weight": "bold",
                            "size": "xs",
                            "align": "start",
                            "contents": []
                        },
                        {
                            "type": "text",
                            "text": str(ip_address['time_dif']['day']) + '?????????' + str(ip_address['time_dif']['hour'])+'??????.' + str(ip_address['time_dif']['minutes'])+'????????????',
                            "weight": "bold",
                            "size": "xs",
                            "color": "#EC1019FF",
                            "align": "end",
                            "action": {
                                "type": "message",
                                "text": "check"+str(ip_address['ip_address'])

                            },
                            "contents": []
                        }
                    ]
                }
                content['contents'][3]['body']['contents'].insert(
                    -2, content_3)

        data = {"type": "flex",
                "altText": "Flex Message",
                "contents": content}
        return data

    def CreateFormNozzleFlexMessageDetail(data, user_type):
        if user_type.user_type.id == 6:
            content_tech = {
                "type": "text",
                "text": '?????????????????? : ' + str(data['user_type'].if_technician.team) + ' ????????? : ' + str(data['user_type'].if_technician.team_name),
                "weight": "bold",
                "align": "center",
                "margin": "xs",
                "contents": []
            }
        if user_type.user_type.id != 6:
            content_tech = {
                "type": "text",
                "text": '-',
                "weight": "bold",
                "align": "center",
                "margin": "xs",
                "contents": []
            }
        content = {
            "type": "carousel",
            "contents": [
                # ?????????????????? 1
                {
                    "type": "bubble",
                    "hero": {
                        "type": "image",
                        "url": "https://seeoil-web.com/picture_logo/VIS-MONITOR/vis.png",
                        "align": "center",
                        "gravity": "bottom",
                        "size": "full",
                        "aspectRatio": "35:8",
                        "aspectMode": "fit",
                        "action": {
                            "type": "uri",
                            "label": "Line",
                            "uri": "https://linecorp.com/"
                        },
                        "position": "relative"
                    },
                    "body": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": "NOZZLE : STATUS",
                                "weight": "bold",
                                "size": "xl",
                                "color": "#225508FF",
                                "align": "center",
                                "gravity": "center",
                                "contents": []
                            },
                            {
                                "type": "text",
                                "text": str(data['TIME_UPDATE'].strftime("%d.%m.%Y %H:%M")),
                                "weight": "bold",
                                "size": "lg",
                                "color": "#225508FF",
                                "align": "center",
                                "gravity": "center",
                                "contents": []
                            },
                            {
                                "type": "separator",
                                "margin": "sm",
                                "color": "#165C3CFF"
                            },
                            {
                                "type": "box",
                                "layout": "vertical",
                                "spacing": "sm",
                                "margin": "lg",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "?????????????????????????????????????????????",
                                        "weight": "bold",
                                        "size": "lg",
                                        "align": "center",
                                        "gravity": "center",
                                        "contents": []
                                    },
                                    content_tech,
                                ]
                            },
                            {
                                "type": "box",
                                "layout": "baseline",
                                "spacing": "sm",
                                "margin": "xs",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "Deive",
                                        "weight": "bold",
                                        "size": "md",
                                        "align": "center",
                                        "gravity": "center",
                                        "contents": []
                                    },
                                    {
                                        "type": "text",
                                        "text": "Normal",
                                        "weight": "bold",
                                        "size": "md",
                                        "align": "center",
                                        "contents": []
                                    },
                                    {
                                        "type": "text",
                                        "text": "Low",
                                        "weight": "bold",
                                        "size": "md",
                                        "align": "center",
                                        "contents": []
                                    }
                                ]
                            },
                            {
                                "type": "box",
                                "layout": "baseline",
                                "spacing": "sm",
                                "margin": "xs",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "NOZZLE",
                                        "weight": "bold",
                                        "size": "md",
                                        "align": "center",
                                        "contents": []
                                    },
                                    {
                                        "type": "text",
                                        "text": str(int(data['TOTAL_SITE_ACTIVE']) - int(data['NOZZLE_OFFLINE'])),
                                        "weight": "bold",
                                        "size": "md",
                                        "align": "center",
                                        "contents": []
                                    },
                                    {
                                        "type": "text",
                                        "text": str(data['NOZZLE_OFFLINE']),
                                        "weight": "bold",
                                        "size": "md",
                                        "align": "center",
                                        "contents": []
                                    }
                                ]
                            },
                            {
                                "type": "separator",
                                "margin": "md",
                                "color": "#165C3CFF"
                            },
                            {
                                "type": "text",
                                "text": "Total Online " + str(data['TOTAL_SITE_ACTIVE']) + ' ' + " Nozzle",
                                "weight": "bold",
                                "size": "lg",
                                "color": "#225508FF",
                                "align": "center",
                                "gravity": "bottom",
                                "margin": "xxl",
                                "contents": []
                            }
                        ]
                    },
                    "footer": {
                        "type": "box",
                        "layout": "vertical",
                        "flex": 0,
                        "spacing": "sm",
                        "contents": [
                            {
                                "type": "button",
                                "action": {
                                    "type": "uri",
                                    "label": "www.orpak.com",
                                    "uri": "https://www.orpak.com/"
                                },
                                "color": "#078025FF",
                                "margin": "none",
                                "height": "sm",
                                "style": "secondary"
                            },
                            {
                                "type": "spacer",
                                "size": "sm"
                            }
                        ]
                    }
                },
                # ?????????????????? 2
                {
                    "type": "bubble",
                    "hero": {
                        "type": "image",
                        "url": "https://seeoil-web.com/picture_logo/VIS-MONITOR/vis.png",
                        "align": "center",
                        "gravity": "bottom",
                        "size": "full",
                        "aspectRatio": "35:8",
                        "aspectMode": "fit",
                        "action": {
                            "type": "uri",
                            "label": "Line",
                            "uri": "https://linecorp.com/"
                        },
                        "position": "relative"
                    },
                    "body": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": "NOZZLE : STATUS",
                                "weight": "bold",
                                "size": "xl",
                                "color": "#225508FF",
                                "align": "center",
                                "gravity": "bottom",
                                "contents": []
                            },
                            {
                                "type": "text",
                                "text": str(data['TIME_UPDATE'].strftime("%d.%m.%Y %H:%M")),
                                "weight": "bold",
                                "size": "lg",
                                "color": "#225508FF",
                                "align": "center",
                                "gravity": "bottom",
                                "contents": []
                            },
                            {
                                "type": "separator",
                                "margin": "sm",
                                "color": "#165C3CFF"
                            },
                            {
                                "type": "box",
                                "layout": "vertical",
                                "spacing": "sm",
                                "margin": "lg",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "??????????????????????????????????????????????????? NOZZLE Offline",
                                        "weight": "bold",
                                        "size": "md",
                                        "align": "center",
                                        "contents": []
                                    }
                                ]
                            },
                            {
                                "type": "box",
                                "layout": "baseline",
                                "spacing": "sm",
                                "margin": "xs",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "???????????????",
                                        "weight": "bold",
                                        "size": "md",
                                        "align": "start",
                                        "contents": []
                                    },
                                    {
                                        "type": "text",
                                        "text": "NozzleDetail",
                                        "weight": "bold",
                                        "size": "md",
                                        "align": "end",
                                        "contents": []
                                    }
                                ]
                            },
                            # ?????????????????????????????????????????????????????????????????????
                            {
                                "type": "separator",
                                "margin": "md",
                                "color": "#165C3CFF"
                            },
                            {
                                "type": "text",
                                "text": "?????????????????????????????????????????? ????????????????????????????????? ip address ????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????",
                                "weight": "bold",
                                "size": "sm",
                                "color": "#225508FF",
                                "align": "center",
                                "margin": "xxl",
                                "wrap": True,
                                "contents": []
                            }
                        ]
                    }
                },
                # ?????????????????? 3
                {
                    "type": "bubble",
                    "hero": {
                        "type": "image",
                        "url": "https://seeoil-web.com/picture_logo/VIS-MONITOR/vis.png",
                        "align": "center",
                        "gravity": "bottom",
                        "size": "full",
                        "aspectRatio": "35:8",
                        "aspectMode": "fit",
                        "action": {
                            "type": "uri",
                            "label": "Line",
                            "uri": "https://linecorp.com/"
                        },
                        "position": "relative"
                    },
                    "body": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": "NOZZLE : STATUS",
                                "weight": "bold",
                                "size": "xl",
                                "color": "#225508FF",
                                "align": "center",
                                "gravity": "bottom",
                                "contents": []
                            },
                            {
                                "type": "text",
                                "text": str(data['TIME_UPDATE'].strftime("%d.%m.%Y %H:%M")),
                                "weight": "bold",
                                "size": "lg",
                                "color": "#225508FF",
                                "align": "center",
                                "gravity": "bottom",
                                "contents": []
                            },
                            {
                                "type": "separator",
                                "margin": "sm",
                                "color": "#165C3CFF"
                            },
                            {
                                "type": "box",
                                "layout": "vertical",
                                "spacing": "sm",
                                "margin": "lg",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "??????????????????????????????????????????????????? NOZZLE Offline",
                                        "weight": "bold",
                                        "size": "md",
                                        "align": "center",
                                        "contents": []
                                    }
                                ]
                            },
                            {
                                "type": "box",
                                "layout": "baseline",
                                "spacing": "sm",
                                "margin": "xs",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "???????????????",
                                        "weight": "bold",
                                        "size": "md",
                                        "align": "start",
                                        "contents": []
                                    },
                                    {
                                        "type": "text",
                                        "text": "LastConnect",
                                        "weight": "bold",
                                        "size": "md",
                                        "align": "end",
                                        "contents": []
                                    }
                                ]
                            },
                            # ?????????????????????????????????????????????????????????


                            {
                                "type": "separator",
                                "margin": "md",
                                "color": "#165C3CFF"
                            },
                            {
                                "type": "text",
                                "text": "?????????????????????????????????????????? ????????????????????????????????? ip address ????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????",
                                "weight": "bold",
                                "size": "sm",
                                "color": "#225508FF",
                                "align": "center",
                                "margin": "xxl",
                                "wrap": True,
                                "contents": []
                            }
                        ]
                    }
                },
                # ?????????????????? 4
                {
                    "type": "bubble",
                    "hero": {
                        "type": "image",
                        "url": "https://seeoil-web.com/picture_logo/VIS-MONITOR/vis.png",
                        "align": "center",
                        "gravity": "bottom",
                        "size": "full",
                        "aspectRatio": "35:8",
                        "aspectMode": "fit",
                        "action": {
                            "type": "uri",
                            "label": "Line",
                            "uri": "https://linecorp.com/"
                        },
                        "position": "relative"
                    },
                    "body": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": "NOZZLE : STATUS",
                                "weight": "bold",
                                "size": "xl",
                                "color": "#225508FF",
                                "align": "center",
                                "gravity": "bottom",
                                "contents": []
                            },
                            {
                                "type": "text",
                                "text": str(data['TIME_UPDATE'].strftime("%d.%m.%Y %H:%M")),
                                "weight": "bold",
                                "size": "lg",
                                "color": "#225508FF",
                                "align": "center",
                                "gravity": "bottom",
                                "contents": []
                            },
                            {
                                "type": "separator",
                                "margin": "sm",
                                "color": "#165C3CFF"
                            },
                            {
                                "type": "box",
                                "layout": "vertical",
                                "spacing": "sm",
                                "margin": "lg",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "??????????????????????????????????????????????????? NOZZLE Offline",
                                        "weight": "bold",
                                        "size": "md",
                                        "align": "center",
                                        "contents": []
                                    }
                                ]
                            },
                            {
                                "type": "box",
                                "layout": "baseline",
                                "spacing": "sm",
                                "margin": "xs",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "???????????????",
                                        "weight": "bold",
                                        "size": "md",
                                        "align": "start",
                                        "contents": []
                                    },
                                    {
                                        "type": "text",
                                        "text": "LostTime",
                                        "weight": "bold",
                                        "size": "md",
                                        "align": "end",
                                        "contents": []
                                    }
                                ]
                            },
                            # ??????????????????????????????????????????

                            {
                                "type": "separator",
                                "margin": "md",
                                "color": "#165C3CFF"
                            },
                            {
                                "type": "text",
                                "text": "?????????????????????????????????????????? ????????????????????????????????? ip address ????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????",
                                "weight": "bold",
                                "size": "sm",
                                "color": "#225508FF",
                                "align": "center",
                                "margin": "xxl",
                                "wrap": True,
                                "contents": []
                            }
                        ]
                    }
                }
            ]
        }
        # ????????????????????????????????? loop 1
        if len(data['NOZZLE_DETAIL']) <= 0:
            content_1 = {
                "type": "box",
                "layout": "baseline",
                "spacing": "sm",
                "margin": "md",
                "contents": [
                    {
                        "type": "text",
                        "text": '-',
                        "weight": "bold",
                        "size": "xs",
                        "align": "start",
                        "contents": []
                    },
                    {
                        "type": "text",
                        "text": '-',
                        "weight": "bold",
                        "size": "xs",
                        "color": "#EC1019FF",
                        "align": "end",
                        "action": {
                            "type": "postback",
                            "text": "?????????????????????????????????",
                            "data": '?????????????????????????????????'
                        },
                        "contents": []
                    }
                ]
            }
            content['contents'][1]['body']['contents'].insert(-2, content_1)
        elif len(data['NOZZLE_DETAIL']) > 0:
            for ip_address in data['NOZZLE_DETAIL']:
                print(ip_address)
                content_1 = {
                    "type": "box",
                    "layout": "baseline",
                    "spacing": "sm",
                    "margin": "md",
                    "contents": [
                        {
                            "type": "text",
                            "text": str(ip_address['name']),
                            "weight": "bold",
                            "size": "xs",
                            "align": "start",
                            "contents": []
                        },
                        {
                            "type": "text",
                            "text": str('Log : ' + ip_address['Unit_log_address'] + ' ???????????? ' + ip_address['NOZZLE_pump_log_address'] + '/'+ip_address['NOZZLE_num']),
                            "weight": "bold",
                            "size": "xs",
                            "color": "#EC1019FF",
                            "align": "end",
                            "action": {
                                "type": "message",
                                "text": "check"+str(ip_address['ip_address'])

                            },
                            "contents": []
                        }
                    ]
                }
                content['contents'][1]['body']['contents'].insert(
                    -2, content_1)

        # ????????????????????????????????? loop 2
        if len(data['NOZZLE_DETAIL']) <= 0:
            content_2 = {
                "type": "box",
                "layout": "baseline",
                "spacing": "sm",
                "margin": "md",
                "contents": [
                    {
                        "type": "text",
                        "text": '-',
                        "weight": "bold",
                        "size": "xs",
                        "align": "start",
                        "contents": []
                    },
                    {
                        "type": "text",
                        "text": '-',
                        "weight": "bold",
                        "size": "xs",
                        "color": "#EC1019FF",
                        "align": "end",
                        "action": {
                            "type": "postback",
                            "text": "?????????????????????????????????",
                            "data": '?????????????????????????????????'
                        },
                        "contents": []
                    }
                ]
            }
            content['contents'][2]['body']['contents'].insert(-2, content_2)
        elif len(data['NOZZLE_DETAIL']) > 0:
            for ip_address in data['NOZZLE_DETAIL']:
                content_2 = {
                    "type": "box",
                    "layout": "baseline",
                    "spacing": "sm",
                    "margin": "md",
                    "contents": [
                        {
                            "type": "text",
                            "text": str(ip_address['name']),
                            "weight": "bold",
                            "size": "xs",
                            "align": "start",
                            "contents": []
                        },
                        {
                            "type": "text",
                            "text": str(ip_address['VIS_last_time'].strftime("%d.%m.%y %H:%M")),
                            "weight": "bold",
                            "size": "xs",
                            "color": "#EC1019FF",
                            "align": "end",
                            "action": {
                                "type": "message",
                                "text": "check"+str(ip_address['ip_address'])

                            },
                            "contents": []
                        }
                    ]
                }
                content['contents'][2]['body']['contents'].insert(
                    -2, content_2)

        # ????????????????????????????????? loop 3
        if len(data['NOZZLE_DETAIL']) <= 0:
            content_3 = {
                "type": "box",
                "layout": "baseline",
                "spacing": "sm",
                "margin": "md",
                "contents": [
                    {
                        "type": "text",
                        "text": '-',
                        "weight": "bold",
                        "size": "xs",
                        "align": "start",
                        "contents": []
                    },
                    {
                        "type": "text",
                        "text": '-',
                        "weight": "bold",
                        "size": "xs",
                        "color": "#EC1019FF",
                        "align": "end",
                        "action": {
                            "type": "postback",
                            "text": "?????????????????????????????????",
                            "data": '?????????????????????????????????'
                        },
                        "contents": []
                    }
                ]
            }
            content['contents'][3]['body']['contents'].insert(-2, content_3)
        elif len(data['NOZZLE_DETAIL']) > 0:
            for ip_address in data['NOZZLE_DETAIL']:
                content_3 = {
                    "type": "box",
                    "layout": "baseline",
                    "spacing": "sm",
                    "margin": "md",
                    "contents": [
                        {
                            "type": "text",
                            "text": str(ip_address['name']),
                            "weight": "bold",
                            "size": "xs",
                            "align": "start",
                            "contents": []
                        },
                        {
                            "type": "text",
                            "text": str(ip_address['time_dif']['day']) + '?????????' + str(ip_address['time_dif']['hour'])+'??????.' + str(ip_address['time_dif']['minutes'])+'????????????',
                            "weight": "bold",
                            "size": "xs",
                            "color": "#EC1019FF",
                            "align": "end",
                            "action": {
                                "type": "message",
                                "text": "check"+str(ip_address['ip_address'])

                            },
                            "contents": []
                        }
                    ]
                }
                content['contents'][3]['body']['contents'].insert(
                    -2, content_3)

        data = {"type": "flex",
                "altText": "Flex Message",
                "contents": content}
        return data

    def CreateFormBatteryFlexMessageDetail(data, user_type):
        if user_type.user_type.id == 6:
            content_tech = {
                "type": "text",
                "text": '?????????????????? : ' + str(data['user_type'].if_technician.team) + ' ????????? : ' + str(data['user_type'].if_technician.team_name),
                "weight": "bold",
                "align": "center",
                "margin": "xs",
                "contents": []
            }
        if user_type.user_type.id != 6:
            content_tech = {
                "type": "text",
                "text": '-',
                "weight": "bold",
                "align": "center",
                "margin": "xs",
                "contents": []
            }
        content = {
            "type": "carousel",
            "contents": [
                # ?????????????????? 1
                {
                    "type": "bubble",
                    "hero": {
                        "type": "image",
                        "url": "https://seeoil-web.com/picture_logo/VIS-MONITOR/vis.png",
                        "align": "center",
                        "gravity": "bottom",
                        "size": "full",
                        "aspectRatio": "35:8",
                        "aspectMode": "fit",
                        "action": {
                            "type": "uri",
                            "label": "Line",
                            "uri": "https://linecorp.com/"
                        },
                        "position": "relative"
                    },
                    "body": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": "BATTERY : STATUS",
                                "weight": "bold",
                                "size": "xl",
                                "color": "#225508FF",
                                "align": "center",
                                "gravity": "center",
                                "contents": []
                            },
                            {
                                "type": "text",
                                "text": str(data['TIME_UPDATE'].strftime("%d.%m.%Y %H:%M")),
                                "weight": "bold",
                                "size": "lg",
                                "color": "#225508FF",
                                "align": "center",
                                "gravity": "center",
                                "contents": []
                            },
                            {
                                "type": "separator",
                                "margin": "sm",
                                "color": "#165C3CFF"
                            },
                            {
                                "type": "box",
                                "layout": "vertical",
                                "spacing": "sm",
                                "margin": "lg",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "?????????????????????????????????????????????",
                                        "weight": "bold",
                                        "size": "lg",
                                        "align": "center",
                                        "gravity": "center",
                                        "contents": []
                                    },
                                    content_tech,
                                ]
                            },
                            {
                                "type": "box",
                                "layout": "baseline",
                                "spacing": "sm",
                                "margin": "xs",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "Deive",
                                        "weight": "bold",
                                        "size": "md",
                                        "align": "center",
                                        "gravity": "center",
                                        "contents": []
                                    },
                                    {
                                        "type": "text",
                                        "text": "Normal",
                                        "weight": "bold",
                                        "size": "md",
                                        "align": "center",
                                        "contents": []
                                    },
                                    {
                                        "type": "text",
                                        "text": "Low",
                                        "weight": "bold",
                                        "size": "md",
                                        "align": "center",
                                        "contents": []
                                    }
                                ]
                            },
                            {
                                "type": "box",
                                "layout": "baseline",
                                "spacing": "sm",
                                "margin": "xs",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "BATTERY",
                                        "weight": "bold",
                                        "size": "md",
                                        "align": "center",
                                        "contents": []
                                    },
                                    {
                                        "type": "text",
                                        "text": str(int(data['TOTAL_SITE_ACTIVE']) - int(data['BATTERY_OFFLINE'])),
                                        "weight": "bold",
                                        "size": "md",
                                        "align": "center",
                                        "contents": []
                                    },
                                    {
                                        "type": "text",
                                        "text": str(data['BATTERY_OFFLINE']),
                                        "weight": "bold",
                                        "size": "md",
                                        "align": "center",
                                        "contents": []
                                    }
                                ]
                            },
                            {
                                "type": "separator",
                                "margin": "md",
                                "color": "#165C3CFF"
                            },
                            {
                                "type": "text",
                                "text": "Total Online " + str(data['TOTAL_SITE_ACTIVE']) + ' ' + " Battery",
                                "weight": "bold",
                                "size": "lg",
                                "color": "#225508FF",
                                "align": "center",
                                "gravity": "bottom",
                                "margin": "xxl",
                                "contents": []
                            }
                        ]
                    },
                    "footer": {
                        "type": "box",
                        "layout": "vertical",
                        "flex": 0,
                        "spacing": "sm",
                        "contents": [
                            {
                                "type": "button",
                                "action": {
                                    "type": "uri",
                                    "label": "www.orpak.com",
                                    "uri": "https://www.orpak.com/"
                                },
                                "color": "#078025FF",
                                "margin": "none",
                                "height": "sm",
                                "style": "secondary"
                            },
                            {
                                "type": "spacer",
                                "size": "sm"
                            }
                        ]
                    }
                },
                # ?????????????????? 2
                {
                    "type": "bubble",
                    "hero": {
                        "type": "image",
                        "url": "https://seeoil-web.com/picture_logo/VIS-MONITOR/vis.png",
                        "align": "center",
                        "gravity": "bottom",
                        "size": "full",
                        "aspectRatio": "35:8",
                        "aspectMode": "fit",
                        "action": {
                            "type": "uri",
                            "label": "Line",
                            "uri": "https://linecorp.com/"
                        },
                        "position": "relative"
                    },
                    "body": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": "BATTERY : STATUS",
                                "weight": "bold",
                                "size": "xl",
                                "color": "#225508FF",
                                "align": "center",
                                "gravity": "bottom",
                                "contents": []
                            },
                            {
                                "type": "text",
                                "text": str(data['TIME_UPDATE'].strftime("%d.%m.%Y %H:%M")),
                                "weight": "bold",
                                "size": "lg",
                                "color": "#225508FF",
                                "align": "center",
                                "gravity": "bottom",
                                "contents": []
                            },
                            {
                                "type": "separator",
                                "margin": "sm",
                                "color": "#165C3CFF"
                            },
                            {
                                "type": "box",
                                "layout": "vertical",
                                "spacing": "sm",
                                "margin": "lg",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "??????????????????????????????????????????????????? BATTERY",
                                        "weight": "bold",
                                        "size": "md",
                                        "align": "center",
                                        "contents": []
                                    }
                                ]
                            },
                            {
                                "type": "box",
                                "layout": "baseline",
                                "spacing": "sm",
                                "margin": "xs",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "???????????????",
                                        "weight": "bold",
                                        "size": "md",
                                        "align": "start",
                                        "contents": []
                                    },
                                    {
                                        "type": "text",
                                        "text": "BatterySts",
                                        "weight": "bold",
                                        "size": "md",
                                        "align": "end",
                                        "contents": []
                                    }
                                ]
                            },
                            # ?????????????????????????????????????????????????????????????????????
                            {
                                "type": "separator",
                                "margin": "md",
                                "color": "#165C3CFF"
                            },
                            {
                                "type": "text",
                                "text": "?????????????????????????????????????????? ????????????????????????????????? BatterySts ????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????",
                                "weight": "bold",
                                "size": "sm",
                                "color": "#225508FF",
                                "align": "center",
                                "margin": "xxl",
                                "wrap": True,
                                "contents": []
                            }
                        ]
                    }
                },
                # ?????????????????? 3
                {
                    "type": "bubble",
                    "hero": {
                        "type": "image",
                        "url": "https://seeoil-web.com/picture_logo/VIS-MONITOR/vis.png",
                        "align": "center",
                        "gravity": "bottom",
                        "size": "full",
                        "aspectRatio": "35:8",
                        "aspectMode": "fit",
                        "action": {
                            "type": "uri",
                            "label": "Line",
                            "uri": "https://linecorp.com/"
                        },
                        "position": "relative"
                    },
                    "body": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": "BATTERY : STATUS",
                                "weight": "bold",
                                "size": "xl",
                                "color": "#225508FF",
                                "align": "center",
                                "gravity": "bottom",
                                "contents": []
                            },
                            {
                                "type": "text",
                                "text": str(data['TIME_UPDATE'].strftime("%d.%m.%Y %H:%M")),
                                "weight": "bold",
                                "size": "lg",
                                "color": "#225508FF",
                                "align": "center",
                                "gravity": "bottom",
                                "contents": []
                            },
                            {
                                "type": "separator",
                                "margin": "sm",
                                "color": "#165C3CFF"
                            },
                            {
                                "type": "box",
                                "layout": "vertical",
                                "spacing": "sm",
                                "margin": "lg",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "??????????????????????????????????????????????????? BATTERY",
                                        "weight": "bold",
                                        "size": "md",
                                        "align": "center",
                                        "contents": []
                                    }
                                ]
                            },
                            {
                                "type": "box",
                                "layout": "baseline",
                                "spacing": "sm",
                                "margin": "xs",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "???????????????",
                                        "weight": "bold",
                                        "size": "md",
                                        "align": "start",
                                        "contents": []
                                    },
                                    {
                                        "type": "text",
                                        "text": "BatterySN",
                                        "weight": "bold",
                                        "size": "md",
                                        "align": "end",
                                        "contents": []
                                    }
                                ]
                            },
                            # ?????????????????????????????????????????????????????????


                            {
                                "type": "separator",
                                "margin": "md",
                                "color": "#165C3CFF"
                            },
                            {
                                "type": "text",
                                "text": "?????????????????????????????????????????? ????????????????????????????????? BatterySN ????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????",
                                "weight": "bold",
                                "size": "sm",
                                "color": "#225508FF",
                                "align": "center",
                                "margin": "xxl",
                                "wrap": True,
                                "contents": []
                            }
                        ]
                    }
                },
                # ?????????????????? 4
                {
                    "type": "bubble",
                    "hero": {
                        "type": "image",
                        "url": "https://seeoil-web.com/picture_logo/VIS-MONITOR/vis.png",
                        "align": "center",
                        "gravity": "bottom",
                        "size": "full",
                        "aspectRatio": "35:8",
                        "aspectMode": "fit",
                        "action": {
                            "type": "uri",
                            "label": "Line",
                            "uri": "https://linecorp.com/"
                        },
                        "position": "relative"
                    },
                    "body": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": "BATTERY : STATUS",
                                "weight": "bold",
                                "size": "xl",
                                "color": "#225508FF",
                                "align": "center",
                                "gravity": "bottom",
                                "contents": []
                            },
                            {
                                "type": "text",
                                "text": str(data['TIME_UPDATE'].strftime("%d.%m.%Y %H:%M")),
                                "weight": "bold",
                                "size": "lg",
                                "color": "#225508FF",
                                "align": "center",
                                "gravity": "bottom",
                                "contents": []
                            },
                            {
                                "type": "separator",
                                "margin": "sm",
                                "color": "#165C3CFF"
                            },
                            {
                                "type": "box",
                                "layout": "vertical",
                                "spacing": "sm",
                                "margin": "lg",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "??????????????????????????????????????????????????? NOZZLE",
                                        "weight": "bold",
                                        "size": "md",
                                        "align": "center",
                                        "contents": []
                                    }
                                ]
                            },
                            {
                                "type": "box",
                                "layout": "baseline",
                                "spacing": "sm",
                                "margin": "xs",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "???????????????",
                                        "weight": "bold",
                                        "size": "md",
                                        "align": "start",
                                        "contents": []
                                    },
                                    {
                                        "type": "text",
                                        "text": "BatteryVT",
                                        "weight": "bold",
                                        "size": "md",
                                        "align": "end",
                                        "contents": []
                                    }
                                ]
                            },
                            # ??????????????????????????????????????????

                            {
                                "type": "separator",
                                "margin": "md",
                                "color": "#165C3CFF"
                            },
                            {
                                "type": "text",
                                "text": "?????????????????????????????????????????? ????????????????????????????????? BatteryVT ????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????",
                                "weight": "bold",
                                "size": "sm",
                                "color": "#225508FF",
                                "align": "center",
                                "margin": "xxl",
                                "wrap": True,
                                "contents": []
                            }
                        ]
                    }
                }
            ]
        }
        # ????????????????????????????????? loop 1
        if len(data['BATTERY_DETAIL']) <= 0:
            content_1 = {
                "type": "box",
                "layout": "baseline",
                "spacing": "sm",
                "margin": "md",
                "contents": [
                    {
                        "type": "text",
                        "text": '-',
                        "weight": "bold",
                        "size": "xs",
                        "align": "start",
                        "contents": []
                    },
                    {
                        "type": "text",
                        "text": '-',
                        "weight": "bold",
                        "size": "xs",
                        "color": "#EC1019FF",
                        "align": "end",
                        "action": {
                            "type": "postback",
                            "text": "?????????????????????????????????",
                            "data": '?????????????????????????????????'
                        },
                        "contents": []
                    }
                ]
            }
            content['contents'][1]['body']['contents'].insert(-2, content_1)
        elif len(data['BATTERY_DETAIL']) > 0:
            for ip_address in data['BATTERY_DETAIL']:
                print(ip_address)
                content_1 = {
                    "type": "box",
                    "layout": "baseline",
                    "spacing": "sm",
                    "margin": "md",
                    "contents": [
                        {
                            "type": "text",
                            "text": str(ip_address['name']),
                            "weight": "bold",
                            "size": "xs",
                            "align": "start",
                            "contents": []
                        },
                        {
                            "type": "text",
                            "text": str(ip_address['BATTERY_status_check']),
                            "weight": "bold",
                            "size": "xs",
                            "color": "#EC1019FF",
                            "align": "end",
                            "action": {
                                "type": "message",
                                "text": "check"+str(ip_address['ip_address'])

                            },
                            "contents": []
                        }
                    ]
                }
                content['contents'][1]['body']['contents'].insert(
                    -2, content_1)

        # ????????????????????????????????? loop 2
        if len(data['BATTERY_DETAIL']) <= 0:
            content_2 = {
                "type": "box",
                "layout": "baseline",
                "spacing": "sm",
                "margin": "md",
                "contents": [
                    {
                        "type": "text",
                        "text": '-',
                        "weight": "bold",
                        "size": "xs",
                        "align": "start",
                        "contents": []
                    },
                    {
                        "type": "text",
                        "text": '-',
                        "weight": "bold",
                        "size": "xs",
                        "color": "#EC1019FF",
                        "align": "end",
                        "action": {
                            "type": "postback",
                            "text": "?????????????????????????????????",
                            "data": '?????????????????????????????????'
                        },
                        "contents": []
                    }
                ]
            }
            content['contents'][2]['body']['contents'].insert(-2, content_2)
        elif len(data['BATTERY_DETAIL']) > 0:
            for ip_address in data['BATTERY_DETAIL']:
                content_2 = {
                    "type": "box",
                    "layout": "baseline",
                    "spacing": "sm",
                    "margin": "md",
                    "contents": [
                        {
                            "type": "text",
                            "text": str(ip_address['name']),
                            "weight": "bold",
                            "size": "xs",
                            "align": "start",
                            "contents": []
                        },
                        {
                            "type": "text",
                            "text": str(ip_address['NOZZLE_SN']),
                            "weight": "bold",
                            "size": "xs",
                            "color": "#EC1019FF",
                            "align": "end",
                            "action": {
                                "type": "message",
                                "text": "check"+str(ip_address['ip_address'])

                            },
                            "contents": []
                        }
                    ]
                }
                content['contents'][2]['body']['contents'].insert(
                    -2, content_2)

        # ????????????????????????????????? loop 3
        if len(data['BATTERY_DETAIL']) <= 0:
            content_3 = {
                "type": "box",
                "layout": "baseline",
                "spacing": "sm",
                "margin": "md",
                "contents": [
                    {
                        "type": "text",
                        "text": '-',
                        "weight": "bold",
                        "size": "xs",
                        "align": "start",
                        "contents": []
                    },
                    {
                        "type": "text",
                        "text": '-',
                        "weight": "bold",
                        "size": "xs",
                        "color": "#EC1019FF",
                        "align": "end",
                        "action": {
                            "type": "postback",
                            "text": "?????????????????????????????????",
                            "data": '?????????????????????????????????'
                        },
                        "contents": []
                    }
                ]
            }
            content['contents'][3]['body']['contents'].insert(-2, content_3)
        elif len(data['BATTERY_DETAIL']) > 0:
            for ip_address in data['BATTERY_DETAIL']:
                content_3 = {
                    "type": "box",
                    "layout": "baseline",
                    "spacing": "sm",
                    "margin": "md",
                    "contents": [
                        {
                            "type": "text",
                            "text": str(ip_address['name']),
                            "weight": "bold",
                            "size": "xs",
                            "align": "start",
                            "contents": []
                        },
                        {
                            "type": "text",
                            "text": str(ip_address['NOZZLE_Battery_Status_Volts']),
                            "weight": "bold",
                            "size": "xs",
                            "color": "#EC1019FF",
                            "align": "end",
                            "action": {
                                "type": "message",
                                "text": "check"+str(ip_address['ip_address'])

                            },
                            "contents": []
                        }
                    ]
                }
                content['contents'][3]['body']['contents'].insert(
                    -2, content_3)

        data = {"type": "flex",
                "altText": "Flex Message",
                "contents": content}
        return data

    def CreateNotifyFormVisOffline(line_data, site_profile):
        print('site_profile', site_profile)
        print(type(site_profile))
        datetime_now = datetime.datetime.now().strftime("%d.%m.%y %H:%M")
        # ?????????????????? return ??????????????? linebot/connect_db_profile/get_site_profile ?????? index ????????? 0
        result_site = site_profile
        # ?????????????????? return ??????????????? linebot/calculate_function/different_time_calculate ????????? return ??????????????????????????? 5 index 0
        day_loss = line_data[0]
        # ?????????????????? return ??????????????? linebot/calculate_function/different_time_calculate ????????? return ??????????????????????????? 5 index 1
        hours_loss = line_data[1]
        # ?????????????????? return ??????????????? linebot/calculate_function/different_time_calculate ????????? return ??????????????????????????? 5 index 2
        minutes_loss = line_data[2]
        # ?????????????????? return ??????????????? linebot/calculate_function/different_time_calculate ????????? return ??????????????????????????? 5 index 3
        datetime_now = line_data[3]
        # ?????????????????? return ??????????????? linebot/calculate_function/different_time_calculate ????????? return ??????????????????????????? 5 index 4
        VIS_last_time = line_data[4]
        technician_team_name = result_site.site.team_support.team
        content = {"type": "flex",
                   "altText": "VIS OFFLINE",
                   "contents":
                   {
                       "type": "carousel",
                       "contents": [{
                           "type": "bubble",
                           "hero": {
                               "type": "image",
                               "url": "https://seeoil-web.com/picture_logo/VIS-MONITOR/vis.png",
                               "align": "center",
                               "gravity": "bottom",
                               "size": "full",
                               "aspectRatio": "35:8",
                               "aspectMode": "fit",
                               "action": {
                                   "type": "uri",
                                   "label": "Line",
                                   "uri": "https://linecorp.com/"
                               },
                               "position": "relative"
                           },
                           "body": {
                               "type": "box",
                               "layout": "vertical",
                               "contents": [
                                   {
                                       "type": "text",
                                       "text": str(datetime_now),
                                       "weight": "bold",
                                       "size": "lg",
                                       "color": "#225508FF",
                                       "align": "center",
                                       "gravity": "bottom",
                                       "contents": []
                                   },
                                   {
                                       "type": "text",
                                       "text": result_site.site.station_name,
                                       "weight": "bold",
                                       "size": "md",
                                       "color": "#225508FF",
                                       "align": "center",
                                       "gravity": "bottom",
                                       "contents": []
                                   },
                                   {
                                       "type": "text",
                                       "text": "VIS : IP " + result_site.site.station_ip,
                                       "weight": "bold",
                                       "size": "sm",
                                       "color": "#225508FF",
                                       "align": "center",
                                       "margin": "xs",
                                       "wrap": True,
                                       "contents": []
                                   },
                                   {
                                       "type": "text",
                                       "text": "VIS OFFLINE",
                                       "weight": "bold",
                                       "size": "lg",
                                       "color": "#DE3A13FF",
                                       "align": "center",
                                       "margin": "xs",
                                       "wrap": True,
                                       "contents": []
                                   },
                                   {
                                       "type": "separator",
                                       "margin": "sm",
                                       "color": "#165C3CFF"
                                   },
                                   {
                                       "type": "box",
                                       "layout": "baseline",
                                       "spacing": "sm",
                                       "margin": "xs",
                                       "contents": [
                                           {
                                               "type": "text",
                                               "text": "???????????????",
                                               "weight": "bold",
                                               "size": "md",
                                               "align": "start",
                                               "contents": []
                                           },
                                           {
                                               "type": "text",
                                               "text": "Offline",
                                               "weight": "bold",
                                               "size": "md",
                                               "align": "end",
                                               "contents": []
                                           }
                                       ]
                                   },
                                   {
                                       "type": "box",
                                       "layout": "baseline",
                                       "spacing": "sm",
                                       "margin": "sm",
                                       "contents": [
                                           {
                                               "type": "text",
                                               "text": "???????????????????????????????????????????????????",
                                               "weight": "bold",
                                               "size": "md",
                                               "align": "start",
                                               "contents": []
                                           },
                                           {
                                               "type": "text",
                                               "text": str(datetime_now),
                                               "weight": "bold",
                                               "size": "sm",
                                               "align": "end",

                                               "contents": []
                                           }
                                       ]
                                   },
                                   {
                                       "type": "box",
                                       "layout": "baseline",
                                       "spacing": "sm",
                                       "margin": "sm",
                                       "contents": [
                                           {
                                               "type": "text",
                                               "text": "???????????????????????????????????????????????????",
                                               "weight": "bold",
                                               "size": "md",
                                               "align": "start",
                                               "contents": []
                                           },
                                           {
                                               "type": "text",
                                               "text": str(VIS_last_time),
                                               "weight": "bold",
                                               "size": "sm",
                                               "align": "end",

                                               "contents": []
                                           }
                                       ]
                                   },
                                   {
                                       "type": "box",
                                       "layout": "baseline",
                                       "spacing": "sm",
                                       "margin": "sm",
                                       "contents": [
                                           {
                                               "type": "text",
                                               "text": "?????????????????????????????????????????????",
                                               "weight": "bold",
                                               "size": "md",
                                               "align": "start",
                                               "contents": []
                                           },
                                           {
                                               "type": "text",
                                               "text": str(day_loss) + " ????????? " + str(hours_loss) + " ?????? " + str(minutes_loss) + " ????????????",
                                               "weight": "bold",
                                               "size": "sm",
                                               "align": "end",

                                               "contents": []
                                           }
                                       ]
                                   },
                                   {
                                       "type": "box",
                                       "layout": "baseline",
                                       "spacing": "sm",
                                       "margin": "sm",
                                       "contents": [
                                           {
                                               "type": "text",
                                               "text": "?????????????????????",
                                               "weight": "bold",
                                               "size": "md",
                                               "align": "start",
                                               "contents": []
                                           },
                                           {
                                               "type": "text",
                                               "text": "????????? " + str(result_site.site.team_support.team_name),
                                               "weight": "bold",
                                               "size": "md",
                                               "align": "end",

                                               "contents": []
                                           }
                                       ]
                                   },
                                   {
                                       "type": "separator",
                                       "margin": "md",
                                       "color": "#165C3CFF"
                                   }
                               ]
                           },
                           "footer": {
                               "type": "box",
                               "layout": "vertical",
                               "flex": 0,
                               "spacing": "sm",
                               "contents": [
                                   {
                                       "type": "button",
                                       "action": {
                                           "type": "uri",
                                           "label": "www.orpak.co.th",
                                           "uri": "https://www.orpak.com/"
                                       },
                                       "color": "#078025FF",
                                       "margin": "none",
                                       "height": "sm",
                                       "style": "secondary"
                                   },
                                   {
                                       "type": "spacer",
                                       "size": "sm"
                                   }
                               ]
                           }
                       }]}}
        return creating_flex_messages.CheckPermissionBeforeSendLine(technician_team_name, content)

    def CreateNotifyFormVisOnline(line_data, site_profile):
        datetime_now = datetime.datetime.now().strftime("%d.%m.%y %H:%M")
        # ?????????????????? return ??????????????? linebot/connect_db_profile/get_site_profile ?????? index ????????? 0
        result_site = site_profile[1]
        # ?????????????????? return ??????????????? linebot/calculate_function/different_time_calculate ????????? return ??????????????????????????? 5 index 0
        day_loss = line_data[0]
        # ?????????????????? return ??????????????? linebot/calculate_function/different_time_calculate ????????? return ??????????????????????????? 5 index 1
        hours_loss = line_data[1]
        # ?????????????????? return ??????????????? linebot/calculate_function/different_time_calculate ????????? return ??????????????????????????? 5 index 2
        minutes_loss = line_data[2]
        # ?????????????????? return ??????????????? linebot/calculate_function/different_time_calculate ????????? return ??????????????????????????? 5 index 3
        datetime_now = line_data[3]
        # ?????????????????? return ??????????????? linebot/calculate_function/different_time_calculate ????????? return ??????????????????????????? 5 index 4
        VIS_last_time = line_data[4]
        Error_start = site_profile[2].Error_start.strftime("%d.%m.%y %H:%M")
        technician_team_name = result_site.site.team_support.team
        content = {"type": "flex",
                   "altText": "VIS OFFLINE",
                   "contents":
                   {
                       "type": "carousel",
                       "contents": [{
                           "type": "bubble",
                           "hero": {
                               "type": "image",
                               "url": "https://seeoil-web.com/picture_logo/VIS-MONITOR/vis.png",
                               "align": "center",
                               "gravity": "bottom",
                               "size": "full",
                               "aspectRatio": "35:8",
                               "aspectMode": "fit",
                               "action": {
                                   "type": "uri",
                                   "label": "Line",
                                   "uri": "https://linecorp.com/"
                               },
                               "position": "relative"
                           },
                           "body": {
                               "type": "box",
                               "layout": "vertical",
                               "contents": [
                                   {
                                       "type": "text",
                                       "text": str(datetime_now),
                                       "weight": "bold",
                                       "size": "lg",
                                       "color": "#225508FF",
                                       "align": "center",
                                       "gravity": "bottom",
                                       "contents": []
                                   },
                                   {
                                       "type": "text",
                                       "text": result_site.site.station_name,
                                       "weight": "bold",
                                       "size": "md",
                                       "color": "#225508FF",
                                       "align": "center",
                                       "gravity": "bottom",
                                       "contents": []
                                   },
                                   {
                                       "type": "text",
                                       "text": "VIS : IP " + result_site.site.station_ip,
                                       "weight": "bold",
                                       "size": "sm",
                                       "color": "#225508FF",
                                       "align": "center",
                                       "margin": "xs",
                                       "wrap": True,
                                       "contents": []
                                   },
                                   {
                                       "type": "text",
                                       "text": "VIS ONLINE",
                                       "weight": "bold",
                                       "size": "lg",
                                       "color": "#20970EFF",
                                       "align": "center",
                                       "margin": "xs",
                                       "wrap": True,
                                       "contents": []
                                   },
                                   {
                                       "type": "separator",
                                       "margin": "sm",
                                       "color": "#165C3CFF"
                                   },
                                   {
                                       "type": "box",
                                       "layout": "baseline",
                                       "spacing": "sm",
                                       "margin": "xs",
                                       "contents": [
                                           {
                                               "type": "text",
                                               "text": "???????????????",
                                               "weight": "bold",
                                               "size": "md",
                                               "align": "start",
                                               "contents": []
                                           },
                                           {
                                               "type": "text",
                                               "text": "Online",
                                               "weight": "bold",
                                               "size": "md",
                                               "align": "end",
                                               "contents": []
                                           }
                                       ]
                                   },
                                   {
                                       "type": "box",
                                       "layout": "baseline",
                                       "spacing": "sm",
                                       "margin": "sm",
                                       "contents": [
                                           {
                                               "type": "text",
                                               "text": "???????????????????????????????????????????????????",
                                               "weight": "bold",
                                               "size": "md",
                                               "align": "start",
                                               "contents": []
                                           },
                                           {
                                               "type": "text",
                                               "text": str(Error_start),
                                               "weight": "bold",
                                               "size": "sm",
                                               "align": "end",

                                               "contents": []
                                           }
                                       ]
                                   },
                                   {
                                       "type": "box",
                                       "layout": "baseline",
                                       "spacing": "sm",
                                       "margin": "sm",
                                       "contents": [
                                           {
                                               "type": "text",
                                               "text": "??????????????????????????????????????????????????????",
                                               "weight": "bold",
                                               "size": "md",
                                               "align": "start",
                                               "contents": []
                                           },
                                           {
                                               "type": "text",
                                               "text": str(datetime_now),
                                               "weight": "bold",
                                               "size": "sm",
                                               "align": "end",

                                               "contents": []
                                           }
                                       ]
                                   },
                                   {
                                       "type": "box",
                                       "layout": "baseline",
                                       "spacing": "sm",
                                       "margin": "sm",
                                       "contents": [
                                           {
                                               "type": "text",
                                               "text": "?????????????????????????????????????????????s",
                                               "weight": "bold",
                                               "size": "md",
                                               "align": "start",
                                               "contents": []
                                           },
                                           {
                                               "type": "text",
                                               "text": str(day_loss) + " ????????? " + str(hours_loss) + " ?????? " + str(minutes_loss) + " ????????????",
                                               "weight": "bold",
                                               "size": "sm",
                                               "align": "end",

                                               "contents": []
                                           }
                                       ]
                                   },
                                   {
                                       "type": "box",
                                       "layout": "baseline",
                                       "spacing": "sm",
                                       "margin": "sm",
                                       "contents": [
                                           {
                                               "type": "text",
                                               "text": "?????????????????????",
                                               "weight": "bold",
                                               "size": "md",
                                               "align": "start",
                                               "contents": []
                                           },
                                           {
                                               "type": "text",
                                               "text": "????????? " + str(result_site.site.team_support.team_name),
                                               "weight": "bold",
                                               "size": "md",
                                               "align": "end",

                                               "contents": []
                                           }
                                       ]
                                   },
                                   {
                                       "type": "separator",
                                       "margin": "md",
                                       "color": "#165C3CFF"
                                   }
                               ]
                           },
                           "footer": {
                               "type": "box",
                               "layout": "vertical",
                               "flex": 0,
                               "spacing": "sm",
                               "contents": [
                                   {
                                       "type": "button",
                                       "action": {
                                           "type": "uri",
                                           "label": "www.orpak.co.th",
                                           "uri": "https://www.orpak.com/"
                                       },
                                       "color": "#078025FF",
                                       "margin": "none",
                                       "height": "sm",
                                       "style": "secondary"
                                   },
                                   {
                                       "type": "spacer",
                                       "size": "sm"
                                   }
                               ]
                           }
                       }]}}
        return creating_flex_messages.CheckPermissionBeforeSendLine(technician_team_name, content)

    def CreateNotifyFormMwgtOffline(line_data, site_profile):
        datetime_now = datetime.datetime.now().strftime("%d.%m.%y %H:%M")
        # ?????????????????? return ??????????????? linebot/connect_db_profile/get_site_profile ?????? index ????????? 0
        result_site = site_profile[1]
        # ?????????????????? return ??????????????? linebot/calculate_function/different_time_calculate ????????? return ??????????????????????????? 5 index 0
        day_loss = line_data[0]
        # ?????????????????? return ??????????????? linebot/calculate_function/different_time_calculate ????????? return ??????????????????????????? 5 index 1
        hours_loss = line_data[1]
        # ?????????????????? return ??????????????? linebot/calculate_function/different_time_calculate ????????? return ??????????????????????????? 5 index 2
        minutes_loss = line_data[2]
        # ?????????????????? return ??????????????? linebot/calculate_function/different_time_calculate ????????? return ??????????????????????????? 5 index 3
        datetime_now = line_data[3]
        # ?????????????????? return ??????????????? linebot/calculate_function/different_time_calculate ????????? return ??????????????????????????? 5 index 4
        VIS_last_time = line_data[4]
        technician_team_name = result_site.site.team_support.team
        content = {"type": "flex",
                   "altText": "MWGT OFFLINE",
                   "contents":
                   {
                       "type": "carousel",
                       "contents": [{
                           "type": "bubble",
                           "hero": {
                               "type": "image",
                               "url": "https://seeoil-web.com/picture_logo/VIS-MONITOR/vis.png",
                               "align": "center",
                               "gravity": "bottom",
                               "size": "full",
                               "aspectRatio": "35:8",
                               "aspectMode": "fit",
                               "action": {
                                   "type": "uri",
                                   "label": "Line",
                                   "uri": "https://linecorp.com/"
                               },
                               "position": "relative"
                           },
                           "body": {
                               "type": "box",
                               "layout": "vertical",
                               "contents": [
                                   {
                                       "type": "text",
                                       "text": str(datetime_now),
                                       "weight": "bold",
                                       "size": "lg",
                                       "color": "#225508FF",
                                       "align": "center",
                                       "gravity": "bottom",
                                       "contents": []
                                   },
                                   {
                                       "type": "text",
                                       "text": result_site.site.station_name,
                                       "weight": "bold",
                                       "size": "md",
                                       "color": "#225508FF",
                                       "align": "center",
                                       "gravity": "bottom",
                                       "contents": []
                                   },
                                   {
                                       "type": "text",
                                       "text": "MWGT : IP " + result_site.site.mwgt_ip,
                                       "weight": "bold",
                                       "size": "sm",
                                       "color": "#225508FF",
                                       "align": "center",
                                       "margin": "xs",
                                       "wrap": True,
                                       "contents": []
                                   },
                                   {
                                       "type": "text",
                                       "text": "MWGT OFFLINE",
                                       "weight": "bold",
                                       "size": "lg",
                                       "color": "#DE3A13FF",
                                       "align": "center",
                                       "margin": "xs",
                                       "wrap": True,
                                       "contents": []
                                   },
                                   {
                                       "type": "separator",
                                       "margin": "sm",
                                       "color": "#165C3CFF"
                                   },
                                   {
                                       "type": "box",
                                       "layout": "baseline",
                                       "spacing": "sm",
                                       "margin": "xs",
                                       "contents": [
                                           {
                                               "type": "text",
                                               "text": "???????????????",
                                               "weight": "bold",
                                               "size": "md",
                                               "align": "start",
                                               "contents": []
                                           },
                                           {
                                               "type": "text",
                                               "text": "Offline",
                                               "weight": "bold",
                                               "size": "md",
                                               "align": "end",
                                               "contents": []
                                           }
                                       ]
                                   },
                                   {
                                       "type": "box",
                                       "layout": "baseline",
                                       "spacing": "sm",
                                       "margin": "sm",
                                       "contents": [
                                           {
                                               "type": "text",
                                               "text": "???????????????????????????????????????????????????",
                                               "weight": "bold",
                                               "size": "md",
                                               "align": "start",
                                               "contents": []
                                           },
                                           {
                                               "type": "text",
                                               "text": str(datetime_now),
                                               "weight": "bold",
                                               "size": "sm",
                                               "align": "end",

                                               "contents": []
                                           }
                                       ]
                                   },
                                   {
                                       "type": "box",
                                       "layout": "baseline",
                                       "spacing": "sm",
                                       "margin": "sm",
                                       "contents": [
                                           {
                                               "type": "text",
                                               "text": "???????????????????????????????????????????????????",
                                               "weight": "bold",
                                               "size": "md",
                                               "align": "start",
                                               "contents": []
                                           },
                                           {
                                               "type": "text",
                                               "text": str(VIS_last_time),
                                               "weight": "bold",
                                               "size": "sm",
                                               "align": "end",

                                               "contents": []
                                           }
                                       ]
                                   },
                                   {
                                       "type": "box",
                                       "layout": "baseline",
                                       "spacing": "sm",
                                       "margin": "sm",
                                       "contents": [
                                           {
                                               "type": "text",
                                               "text": "?????????????????????????????????????????????",
                                               "weight": "bold",
                                               "size": "md",
                                               "align": "start",
                                               "contents": []
                                           },
                                           {
                                               "type": "text",
                                               "text": str(day_loss) + " ????????? " + str(hours_loss) + " ?????? " + str(minutes_loss) + " ????????????",
                                               "weight": "bold",
                                               "size": "sm",
                                               "align": "end",

                                               "contents": []
                                           }
                                       ]
                                   },
                                   {
                                       "type": "box",
                                       "layout": "baseline",
                                       "spacing": "sm",
                                       "margin": "sm",
                                       "contents": [
                                           {
                                               "type": "text",
                                               "text": "?????????????????????",
                                               "weight": "bold",
                                               "size": "md",
                                               "align": "start",
                                               "contents": []
                                           },
                                           {
                                               "type": "text",
                                               "text": "????????? " + str(result_site.site.team_support.team_name),
                                               "weight": "bold",
                                               "size": "md",
                                               "align": "end",

                                               "contents": []
                                           }
                                       ]
                                   },
                                   {
                                       "type": "separator",
                                       "margin": "md",
                                       "color": "#165C3CFF"
                                   }
                               ]
                           },
                           "footer": {
                               "type": "box",
                               "layout": "vertical",
                               "flex": 0,
                               "spacing": "sm",
                               "contents": [
                                   {
                                       "type": "button",
                                       "action": {
                                           "type": "uri",
                                           "label": "www.orpak.co.th",
                                           "uri": "https://www.orpak.com/"
                                       },
                                       "color": "#078025FF",
                                       "margin": "none",
                                       "height": "sm",
                                       "style": "secondary"
                                   },
                                   {
                                       "type": "spacer",
                                       "size": "sm"
                                   }
                               ]
                           }
                       }]}}
        return creating_flex_messages.CheckPermissionBeforeSendLine(technician_team_name, content)

    def CreateNotifyFormMwgtOnline(line_data, site_profile):
        datetime_now = datetime.datetime.now().strftime("%d.%m.%y %H:%M")
        # ?????????????????? return ??????????????? linebot/connect_db_profile/get_site_profile ?????? index ????????? 0
        result_site = site_profile[1]
        # ?????????????????? return ??????????????? linebot/calculate_function/different_time_calculate ????????? return ??????????????????????????? 5 index 0
        day_loss = line_data[0]
        # ?????????????????? return ??????????????? linebot/calculate_function/different_time_calculate ????????? return ??????????????????????????? 5 index 1
        hours_loss = line_data[1]
        # ?????????????????? return ??????????????? linebot/calculate_function/different_time_calculate ????????? return ??????????????????????????? 5 index 2
        minutes_loss = line_data[2]
        # ?????????????????? return ??????????????? linebot/calculate_function/different_time_calculate ????????? return ??????????????????????????? 5 index 3
        datetime_now = line_data[3]
        # ?????????????????? return ??????????????? linebot/calculate_function/different_time_calculate ????????? return ??????????????????????????? 5 index 4
        VIS_last_time = line_data[4]
        Error_start = site_profile[2].Error_start.strftime("%d.%m.%y %H:%M")
        technician_team_name = result_site.site.team_support.team
        content = {"type": "flex",
                   "altText": "MWGT ONLINE",
                   "contents":
                   {
                       "type": "carousel",
                       "contents": [{
                           "type": "bubble",
                           "hero": {
                               "type": "image",
                               "url": "https://seeoil-web.com/picture_logo/VIS-MONITOR/vis.png",
                               "align": "center",
                               "gravity": "bottom",
                               "size": "full",
                               "aspectRatio": "35:8",
                               "aspectMode": "fit",
                               "action": {
                                   "type": "uri",
                                   "label": "Line",
                                   "uri": "https://linecorp.com/"
                               },
                               "position": "relative"
                           },
                           "body": {
                               "type": "box",
                               "layout": "vertical",
                               "contents": [
                                   {
                                       "type": "text",
                                       "text": str(datetime_now),
                                       "weight": "bold",
                                       "size": "lg",
                                       "color": "#225508FF",
                                       "align": "center",
                                       "gravity": "bottom",
                                       "contents": []
                                   },
                                   {
                                       "type": "text",
                                       "text": str(result_site.site.station_name),
                                       "weight": "bold",
                                       "size": "md",
                                       "color": "#225508FF",
                                       "align": "center",
                                       "gravity": "bottom",
                                       "contents": []
                                   },
                                   {
                                       "type": "text",
                                       "text": "MWGT : IP " + str(result_site.site.mwgt_ip),
                                       "weight": "bold",
                                       "size": "sm",
                                       "color": "#225508FF",
                                       "align": "center",
                                       "margin": "xs",
                                       "wrap": True,
                                       "contents": []
                                   },
                                   {
                                       "type": "text",
                                       "text": "MWGT ONLINE",
                                       "weight": "bold",
                                       "size": "lg",
                                       "color": "#20970EFF",
                                       "align": "center",
                                       "margin": "xs",
                                       "wrap": True,
                                       "contents": []
                                   },
                                   {
                                       "type": "separator",
                                       "margin": "sm",
                                       "color": "#165C3CFF"
                                   },
                                   {
                                       "type": "box",
                                       "layout": "baseline",
                                       "spacing": "sm",
                                       "margin": "xs",
                                       "contents": [
                                           {
                                               "type": "text",
                                               "text": "???????????????",
                                               "weight": "bold",
                                               "size": "md",
                                               "align": "start",
                                               "contents": []
                                           },
                                           {
                                               "type": "text",
                                               "text": "Online",
                                               "weight": "bold",
                                               "size": "md",
                                               "align": "end",
                                               "contents": []
                                           }
                                       ]
                                   },
                                   {
                                       "type": "box",
                                       "layout": "baseline",
                                       "spacing": "sm",
                                       "margin": "sm",
                                       "contents": [
                                           {
                                               "type": "text",
                                               "text": "???????????????????????????????????????????????????",
                                               "weight": "bold",
                                               "size": "md",
                                               "align": "start",
                                               "contents": []
                                           },
                                           {
                                               "type": "text",
                                               "text": str(Error_start),
                                               "weight": "bold",
                                               "size": "sm",
                                               "align": "end",

                                               "contents": []
                                           }
                                       ]
                                   },
                                   {
                                       "type": "box",
                                       "layout": "baseline",
                                       "spacing": "sm",
                                       "margin": "sm",
                                       "contents": [
                                           {
                                               "type": "text",
                                               "text": "??????????????????????????????????????????????????????",
                                               "weight": "bold",
                                               "size": "md",
                                               "align": "start",
                                               "contents": []
                                           },
                                           {
                                               "type": "text",
                                               "text": str(datetime_now),
                                               "weight": "bold",
                                               "size": "sm",
                                               "align": "end",

                                               "contents": []
                                           }
                                       ]
                                   },
                                   {
                                       "type": "box",
                                       "layout": "baseline",
                                       "spacing": "sm",
                                       "margin": "sm",
                                       "contents": [
                                           {
                                               "type": "text",
                                               "text": "?????????????????????????????????????????????",
                                               "weight": "bold",
                                               "size": "md",
                                               "align": "start",
                                               "contents": []
                                           },
                                           {
                                               "type": "text",
                                               "text": str(day_loss) + " ????????? " + str(hours_loss) + " ?????? " + str(minutes_loss) + " ????????????",
                                               "weight": "bold",
                                               "size": "sm",
                                               "align": "end",

                                               "contents": []
                                           }
                                       ]
                                   },
                                   {
                                       "type": "box",
                                       "layout": "baseline",
                                       "spacing": "sm",
                                       "margin": "sm",
                                       "contents": [
                                           {
                                               "type": "text",
                                               "text": "?????????????????????",
                                               "weight": "bold",
                                               "size": "md",
                                               "align": "start",
                                               "contents": []
                                           },
                                           {
                                               "type": "text",
                                               "text": "????????? " + str(result_site.site.team_support.team_name),
                                               "weight": "bold",
                                               "size": "md",
                                               "align": "end",

                                               "contents": []
                                           }
                                       ]
                                   },
                                   {
                                       "type": "separator",
                                       "margin": "md",
                                       "color": "#165C3CFF"
                                   }
                               ]
                           },
                           "footer": {
                               "type": "box",
                               "layout": "vertical",
                               "flex": 0,
                               "spacing": "sm",
                               "contents": [
                                   {
                                       "type": "button",
                                       "action": {
                                           "type": "uri",
                                           "label": "www.orpak.co.th",
                                           "uri": "https://www.orpak.com/"
                                       },
                                       "color": "#078025FF",
                                       "margin": "none",
                                       "height": "sm",
                                       "style": "secondary"
                                   },
                                   {
                                       "type": "spacer",
                                       "size": "sm"
                                   }
                               ]
                           }
                       }]}}
        return creating_flex_messages.CheckPermissionBeforeSendLine(technician_team_name, content)

    def CreateNotifyFormNozzleOnline(line_data, site_profile):
        # print('Nozzle')
        datetime_now = datetime.datetime.now().strftime("%d.%m.%y %H:%M")
        result_site = site_profile
        day_loss = line_data[0]
        hours_loss = line_data[1]
        # print ('Check')
        # ?????????????????? return ??????????????? linebot/calculate_function/different_time_calculate ????????? return ??????????????????????????? 5 index 2
        minutes_loss = line_data[2]
        # ?????????????????? return ??????????????? linebot/calculate_function/different_time_calculate ????????? return ??????????????????????????? 5 index 3
        datetime_now = line_data[3]
        # ?????????????????? return ??????????????? linebot/calculate_function/different_time_calculate ????????? return ??????????????????????????? 5 index 4
        VIS_last_time = line_data[4]

        technician_team_name = result_site.site.team_support.team_name
        station_name = result_site.site.station_name
        mwgt_ip = result_site.site.mwgt_ip
        Error_start = datetime_now
        Loss_times = str(day_loss) + " ????????? " + str(hours_loss) + \
            " ?????? " + str(minutes_loss) + " ????????????"
        team_name = result_site.site.team_support.team_name

        print(technician_team_name, station_name,
              mwgt_ip, Error_start, Loss_times, team_name)

        content = {"type": "flex",
                   "altText": "NOZZLE ONLINE",
                   "contents":
                   {
                       "type": "carousel",
                       "contents": [{
                           "type": "bubble",
                           "hero": {
                               "type": "image",
                               "url": "https://seeoil-web.com/picture_logo/VIS-MONITOR/vis.png",
                               "align": "center",
                               "gravity": "bottom",
                               "size": "full",
                               "aspectRatio": "35:8",
                               "aspectMode": "fit",
                               "action": {
                                   "type": "uri",
                                   "label": "Line",
                                   "uri": "https://linecorp.com/"
                               },
                               "position": "relative"
                           },
                           "body": {
                               "type": "box",
                               "layout": "vertical",
                               "contents": [
                                   {
                                       "type": "text",
                                       "text": datetime_now,
                                       "weight": "bold",
                                       "size": "lg",
                                       "color": "#225508FF",
                                       "align": "center",
                                       "gravity": "bottom",
                                       "contents": []
                                   },
                                   {
                                       "type": "text",
                                       "text": station_name,
                                       "weight": "bold",
                                       "size": "md",
                                       "color": "#225508FF",
                                       "align": "center",
                                       "gravity": "bottom",
                                       "contents": []
                                   },
                                   {
                                       "type": "text",
                                       "text": "VIS : IP " + mwgt_ip,
                                       "weight": "bold",
                                       "size": "sm",
                                       "color": "#225508FF",
                                       "align": "center",
                                       "margin": "xs",
                                       "wrap": True,
                                       "contents": []
                                   },
                                   {
                                       "type": "text",
                                       "text": "NOZZLE ONLINE",
                                       "weight": "bold",
                                       "size": "lg",
                                       "color": "#20970EFF",
                                       "align": "center",
                                       "margin": "xs",
                                       "wrap": True,
                                       "contents": []
                                   },
                                   {
                                       "type": "separator",
                                       "margin": "sm",
                                       "color": "#165C3CFF"
                                   },
                                   {
                                       "type": "box",
                                       "layout": "baseline",
                                       "spacing": "sm",
                                       "margin": "xs",
                                       "contents": [
                                           {
                                               "type": "text",
                                               "text": "???????????????",
                                               "weight": "bold",
                                               "size": "md",
                                               "align": "start",
                                               "contents": []
                                           },
                                           {
                                               "type": "text",
                                               "text": "Online",
                                               "weight": "bold",
                                               "size": "md",
                                               "align": "end",
                                               "contents": []
                                           }
                                       ]
                                   },
                                   {
                                       "type": "box",
                                       "layout": "baseline",
                                       "spacing": "sm",
                                       "margin": "sm",
                                       "contents": [
                                           {
                                               "type": "text",
                                               "text": "?????????????????????????????????????????????",
                                               "weight": "bold",
                                               "size": "md",
                                               "align": "start",
                                               "contents": []
                                           },
                                           {
                                               "type": "text",
                                               "text": site_profile.NOZZLE_pump_log_address,
                                               "weight": "bold",
                                               "size": "md",
                                               "align": "end",

                                               "contents": []
                                           }
                                       ]
                                   },
                                   {
                                       "type": "box",
                                       "layout": "baseline",
                                       "spacing": "sm",
                                       "margin": "sm",
                                       "contents": [
                                           {
                                               "type": "text",
                                               "text": "??????????????????????????????????????????",
                                               "weight": "bold",
                                               "size": "md",
                                               "align": "start",
                                               "contents": []
                                           },
                                           {
                                               "type": "text",
                                               "text": site_profile.NOZZLE_num,
                                               "weight": "bold",
                                               "size": "md",
                                               "align": "end",

                                               "contents": []
                                           }
                                       ]
                                   },
                                   {
                                       "type": "box",
                                       "layout": "baseline",
                                       "spacing": "sm",
                                       "margin": "sm",
                                       "contents": [
                                           {
                                               "type": "text",
                                               "text": "BatteryVolt",
                                               "weight": "bold",
                                               "size": "md",
                                               "align": "start",
                                               "contents": []
                                           },
                                           {
                                               "type": "text",
                                               "text": str(site_profile.NOZZLE_Battery_Status_Volts),
                                               "weight": "bold",
                                               "size": "md",
                                               "align": "end",

                                               "contents": []
                                           }
                                       ]
                                   },
                                   {
                                       "type": "box",
                                       "layout": "baseline",
                                       "spacing": "sm",
                                       "margin": "sm",
                                       "contents": [
                                           {
                                               "type": "text",
                                               "text": "SerialNo.",
                                               "weight": "bold",
                                               "size": "md",
                                               "align": "start",
                                               "contents": []
                                           },
                                           {
                                               "type": "text",
                                               "text": site_profile.NOZZLE_SN,
                                               "weight": "bold",
                                               "size": "md",
                                               "align": "end",

                                               "contents": []
                                           }
                                       ]
                                   },
                                   {
                                       "type": "box",
                                       "layout": "baseline",
                                       "spacing": "sm",
                                       "margin": "sm",
                                       "contents": [
                                           {
                                               "type": "text",
                                               "text": "LastCon.",
                                               "weight": "bold",
                                               "size": "md",
                                               "align": "start",
                                               "contents": []
                                           },
                                           {
                                               "type": "text",
                                               "text": site_profile.NOZZLE_Last_conn,
                                               "weight": "bold",
                                               "size": "md",
                                               "align": "end",

                                               "contents": []
                                           }
                                       ]
                                   },
                                   {
                                       "type": "box",
                                       "layout": "baseline",
                                       "spacing": "sm",
                                       "margin": "sm",
                                       "contents": [
                                           {
                                               "type": "text",
                                               "text": "???????????????????????????????????????????????????",
                                               "weight": "bold",
                                               "size": "md",
                                               "align": "start",
                                               "contents": []
                                           },
                                           {
                                               "type": "text",
                                               "text": str(site_profile.Timestramp.strftime("%d.%m.%y %H:%M")),
                                               "weight": "bold",
                                               "size": "md",
                                               "align": "end",

                                               "contents": []
                                           }
                                       ]
                                   },
                                   {
                                       "type": "box",
                                       "layout": "baseline",
                                       "spacing": "sm",
                                       "margin": "sm",
                                       "contents": [
                                           {
                                               "type": "text",
                                               "text": "?????????????????????????????????????????? ",
                                               "weight": "bold",
                                               "size": "md",
                                               "align": "start",
                                               "contents": []
                                           },
                                           {
                                               "type": "text",
                                               "text": datetime_now,
                                               "weight": "bold",
                                               "size": "md",
                                               "align": "end",

                                               "contents": []
                                           }
                                       ]
                                   },
                                   {
                                       "type": "box",
                                       "layout": "baseline",
                                       "spacing": "sm",
                                       "margin": "sm",
                                       "contents": [
                                           {
                                               "type": "text",
                                               "text": "?????????????????????????????????????????????",
                                               "weight": "bold",
                                               "size": "md",
                                               "align": "start",
                                               "contents": []
                                           },
                                           {
                                               "type": "text",
                                               "text": Loss_times,
                                               "weight": "bold",
                                               "size": "sm",
                                               "align": "end",

                                               "contents": []
                                           }
                                       ]
                                   },
                                   {
                                       "type": "box",
                                       "layout": "baseline",
                                       "spacing": "sm",
                                       "margin": "sm",
                                       "contents": [
                                           {
                                               "type": "text",
                                               "text": "?????????????????????",
                                               "weight": "bold",
                                               "size": "md",
                                               "align": "start",
                                               "contents": []
                                           },
                                           {
                                               "type": "text",
                                               "text": "????????? " + site_profile.site.team_support.team_name,
                                               "weight": "bold",
                                               "size": "md",
                                               "align": "end",

                                               "contents": []
                                           }
                                       ]
                                   },
                                   {
                                       "type": "separator",
                                       "margin": "md",
                                       "color": "#165C3CFF"
                                   }
                               ]
                           },
                           "footer": {
                               "type": "box",
                               "layout": "vertical",
                               "flex": 0,
                               "spacing": "sm",
                               "contents": [
                                   {
                                       "type": "button",
                                       "action": {
                                           "type": "uri",
                                           "label": "www.orpak.co.th",
                                           "uri": "https://www.orpak.com/"
                                       },
                                       "color": "#078025FF",
                                       "margin": "none",
                                       "height": "sm",
                                       "style": "secondary"
                                   },
                                   {
                                       "type": "spacer",
                                       "size": "sm"
                                   }
                               ]
                           }
                       }]}}
        print('content ', content)
        return creating_flex_messages.CheckPermissionBeforeSendLine(result_site.site.team_support.team, content)

    def CreateNotifyFormNozzleOffline(line_data, site_profile):
        # print('Nozzle')
        datetime_now = datetime.datetime.now().strftime("%d.%m.%y %H:%M")
        result_site = site_profile
        day_loss = line_data[0]
        hours_loss = line_data[1]
        # print ('Check')
        # ?????????????????? return ??????????????? linebot/calculate_function/different_time_calculate ????????? return ??????????????????????????? 5 index 2
        minutes_loss = line_data[2]
        # ?????????????????? return ??????????????? linebot/calculate_function/different_time_calculate ????????? return ??????????????????????????? 5 index 3
        datetime_now = line_data[3]
        # ?????????????????? return ??????????????? linebot/calculate_function/different_time_calculate ????????? return ??????????????????????????? 5 index 4
        VIS_last_time = line_data[4]

        technician_team_name = result_site.site.team_support.team_name
        station_name = result_site.site.station_name
        mwgt_ip = result_site.site.mwgt_ip
        Error_start = datetime_now
        Loss_times = str(day_loss) + " ????????? " + str(hours_loss) + \
            " ?????? " + str(minutes_loss) + " ????????????"
        team_name = result_site.site.team_support.team_name

        print(technician_team_name, station_name,
              mwgt_ip, Error_start, Loss_times, team_name)

        content = {"type": "flex",
                   "altText": "NOZZLE OFFLINE",
                   "contents":
                   {
                       "type": "carousel",
                       "contents": [{
                           "type": "bubble",
                           "hero": {
                               "type": "image",
                               "url": "https://seeoil-web.com/picture_logo/VIS-MONITOR/vis.png",
                               "align": "center",
                               "gravity": "bottom",
                               "size": "full",
                               "aspectRatio": "35:8",
                               "aspectMode": "fit",
                               "action": {
                                   "type": "uri",
                                   "label": "Line",
                                   "uri": "https://linecorp.com/"
                               },
                               "position": "relative"
                           },
                           "body": {
                               "type": "box",
                               "layout": "vertical",
                               "contents": [
                                   {
                                       "type": "text",
                                       "text": datetime_now,
                                       "weight": "bold",
                                       "size": "lg",
                                       "color": "#225508FF",
                                       "align": "center",
                                       "gravity": "bottom",
                                       "contents": []
                                   },
                                   {
                                       "type": "text",
                                       "text": station_name,
                                       "weight": "bold",
                                       "size": "md",
                                       "color": "#225508FF",
                                       "align": "center",
                                       "gravity": "bottom",
                                       "contents": []
                                   },
                                   {
                                       "type": "text",
                                       "text": "MWGT : IP " + mwgt_ip,
                                       "weight": "bold",
                                       "size": "sm",
                                       "color": "#225508FF",
                                       "align": "center",
                                       "margin": "xs",
                                       "wrap": True,
                                       "contents": []
                                   },
                                   {
                                       "type": "text",
                                       "text": "NOZZLE OFFLINE",
                                       "weight": "bold",
                                       "size": "lg",
                                       "color": "#FC2313FF",
                                       "align": "center",
                                       "margin": "xs",
                                       "wrap": True,
                                       "contents": []
                                   },
                                   {
                                       "type": "separator",
                                       "margin": "sm",
                                       "color": "#165C3CFF"
                                   },
                                   {
                                       "type": "box",
                                       "layout": "baseline",
                                       "spacing": "sm",
                                       "margin": "xs",
                                       "contents": [
                                           {
                                               "type": "text",
                                               "text": "???????????????",
                                               "weight": "bold",
                                               "size": "md",
                                               "align": "start",
                                               "contents": []
                                           },
                                           {
                                               "type": "text",
                                               "text": "Offline",
                                               "weight": "bold",
                                               "size": "md",
                                               "align": "end",
                                               "contents": []
                                           }
                                       ]
                                   },
                                   {
                                       "type": "box",
                                       "layout": "baseline",
                                       "spacing": "sm",
                                       "margin": "sm",
                                       "contents": [
                                           {
                                               "type": "text",
                                               "text": "?????????????????????????????????????????????",
                                               "weight": "bold",
                                               "size": "md",
                                               "align": "start",
                                               "contents": []
                                           },
                                           {
                                               "type": "text",
                                               "text": site_profile.NOZZLE_pump_log_address,
                                               "weight": "bold",
                                               "size": "md",
                                               "align": "end",

                                               "contents": []
                                           }
                                       ]
                                   },
                                   {
                                       "type": "box",
                                       "layout": "baseline",
                                       "spacing": "sm",
                                       "margin": "sm",
                                       "contents": [
                                           {
                                               "type": "text",
                                               "text": "??????????????????????????????????????????",
                                               "weight": "bold",
                                               "size": "md",
                                               "align": "start",
                                               "contents": []
                                           },
                                           {
                                               "type": "text",
                                               "text": site_profile.NOZZLE_num,
                                               "weight": "bold",
                                               "size": "md",
                                               "align": "end",

                                               "contents": []
                                           }
                                       ]
                                   },
                                   {
                                       "type": "box",
                                       "layout": "baseline",
                                       "spacing": "sm",
                                       "margin": "sm",
                                       "contents": [
                                           {
                                               "type": "text",
                                               "text": "BatteryVolt",
                                               "weight": "bold",
                                               "size": "md",
                                               "align": "start",
                                               "contents": []
                                           },
                                           {
                                               "type": "text",
                                               "text": str(site_profile.NOZZLE_Battery_Status_Volts),
                                               "weight": "bold",
                                               "size": "md",
                                               "align": "end",

                                               "contents": []
                                           }
                                       ]
                                   },
                                   {
                                       "type": "box",
                                       "layout": "baseline",
                                       "spacing": "sm",
                                       "margin": "sm",
                                       "contents": [
                                           {
                                               "type": "text",
                                               "text": "SerialNo.",
                                               "weight": "bold",
                                               "size": "md",
                                               "align": "start",
                                               "contents": []
                                           },
                                           {
                                               "type": "text",
                                               "text": site_profile.NOZZLE_SN,
                                               "weight": "bold",
                                               "size": "md",
                                               "align": "end",

                                               "contents": []
                                           }
                                       ]
                                   },
                                   {
                                       "type": "box",
                                       "layout": "baseline",
                                       "spacing": "sm",
                                       "margin": "sm",
                                       "contents": [
                                           {
                                               "type": "text",
                                               "text": "LastCon.",
                                               "weight": "bold",
                                               "size": "md",
                                               "align": "start",
                                               "contents": []
                                           },
                                           {
                                               "type": "text",
                                               "text": site_profile.NOZZLE_Last_conn,
                                               "weight": "bold",
                                               "size": "md",
                                               "align": "end",

                                               "contents": []
                                           }
                                       ]
                                   },
                                   {
                                       "type": "box",
                                       "layout": "baseline",
                                       "spacing": "sm",
                                       "margin": "sm",
                                       "contents": [
                                           {
                                               "type": "text",
                                               "text": "???????????????????????????????????????????????????",
                                               "weight": "bold",
                                               "size": "md",
                                               "align": "start",
                                               "contents": []
                                           },
                                           {
                                               "type": "text",
                                               "text": str(datetime_now),
                                               "weight": "bold",
                                               "size": "md",
                                               "align": "end",

                                               "contents": []
                                           }
                                       ]
                                   },
                                   {
                                       "type": "box",
                                       "layout": "baseline",
                                       "spacing": "sm",
                                       "margin": "sm",
                                       "contents": [
                                           {
                                               "type": "text",
                                               "text": "???????????????????????????????????????????????????????????? ",
                                               "weight": "bold",
                                               "size": "md",
                                               "align": "start",
                                               "contents": []
                                           },
                                           {
                                               "type": "text",
                                               "text": str(site_profile.Timestramp.strftime("%d.%m.%y %H:%M")),
                                               "weight": "bold",
                                               "size": "md",
                                               "align": "end",

                                               "contents": []
                                           }
                                       ]
                                   },
                                   {
                                       "type": "box",
                                       "layout": "baseline",
                                       "spacing": "sm",
                                       "margin": "sm",
                                       "contents": [
                                           {
                                               "type": "text",
                                               "text": "?????????????????????????????????????????????",
                                               "weight": "bold",
                                               "size": "md",
                                               "align": "start",
                                               "contents": []
                                           },
                                           {
                                               "type": "text",
                                               "text": Loss_times,
                                               "weight": "bold",
                                               "size": "sm",
                                               "align": "end",

                                               "contents": []
                                           }
                                       ]
                                   },
                                   {
                                       "type": "box",
                                       "layout": "baseline",
                                       "spacing": "sm",
                                       "margin": "sm",
                                       "contents": [
                                           {
                                               "type": "text",
                                               "text": "?????????????????????",
                                               "weight": "bold",
                                               "size": "md",
                                               "align": "start",
                                               "contents": []
                                           },
                                           {
                                               "type": "text",
                                               "text": "????????? " + site_profile.site.team_support.team_name,
                                               "weight": "bold",
                                               "size": "md",
                                               "align": "end",

                                               "contents": []
                                           }
                                       ]
                                   },
                                   {
                                       "type": "separator",
                                       "margin": "md",
                                       "color": "#165C3CFF"
                                   }
                               ]
                           },
                           "footer": {
                               "type": "box",
                               "layout": "vertical",
                               "flex": 0,
                               "spacing": "sm",
                               "contents": [
                                   {
                                       "type": "button",
                                       "action": {
                                           "type": "uri",
                                           "label": "www.orpak.co.th",
                                           "uri": "https://www.orpak.com/"
                                       },
                                       "color": "#078025FF",
                                       "margin": "none",
                                       "height": "sm",
                                       "style": "secondary"
                                   },
                                   {
                                       "type": "spacer",
                                       "size": "sm"
                                   }
                               ]
                           }
                       }]}}
        print('content ', content)
        return creating_flex_messages.CheckPermissionBeforeSendLine(result_site.site.team_support.team, content)

    def CreateNotifyFormBatteryStatus(type_alarm, site_profile):
        # ?????????????????? return ??????????????? linebot/connect_db_profile/get_site_profile ?????? index ????????? 0
        datetime_now = datetime.datetime.now().strftime("%d.%m.%y %H:%M")
        result_site = site_profile
        if type_alarm == 'NORMAL':
            Header_status = 'BATTERY NORMAL'
            Battery_status = 'Normal'
            color_status = '#279510FF'
        elif type_alarm == 'LOW':
            Header_status = 'BATTERY LOW'
            color_status = '#EAD447FF'
            Battery_status = 'Low'
        elif type_alarm == 'ALARM':
            Header_status = 'BATTERY ALARM'
            Battery_status = 'Alarm'
            color_status = '#E71913FF'

        messages = 'BATTERY Status ' + '\n' + \
            'Type : ' + ' Battery : NORMAL ' + '\n' \
            '??????????????? : ' + str(result_site.site.station_name) + '\n' + \
            'IP : ' + str(result_site.site.station_ip) + '\n' + \
            'Serial : ' + str(result_site.NOZZLE_SN) + '\n' + \
            '????????????????????? : ' + str(result_site.NOZZLE_pump_log_address) + '\n' + \
            '?????????????????????  : ' + str(result_site.NOZZLE_num) + '\n' + \
            '????????????????????????????????? : ' + str(result_site.NOZZLE_Battery_Status_Volts) + ' V.' + '\n' \
            + '????????????????????? : ' + result_site.site.team_support.team_name

        content = {"type": "flex",
                   "altText": Header_status,
                   "contents":
                   {
                       "type": "carousel",
                       "contents": [{
                           "type": "bubble",
                           "hero": {
                               "type": "image",
                               "url": "https://seeoil-web.com/picture_logo/VIS-MONITOR/vis.png",
                               "align": "center",
                               "gravity": "bottom",
                               "size": "full",
                               "aspectRatio": "35:8",
                               "aspectMode": "fit",
                               "action": {
                                   "type": "uri",
                                   "label": "Line",
                                   "uri": "https://linecorp.com/"
                               },
                               "position": "relative"
                           },
                           "body": {
                               "type": "box",
                               "layout": "vertical",
                               "contents": [
                                   {
                                       "type": "text",
                                       "text": datetime_now,
                                       "weight": "bold",
                                       "size": "lg",
                                       "color": "#225508FF",
                                       "align": "center",
                                       "gravity": "bottom",
                                       "contents": []
                                   },
                                   {
                                       "type": "text",
                                       "text": str(result_site.site.station_name),
                                       "weight": "bold",
                                       "size": "md",
                                       "color": "#225508FF",
                                       "align": "center",
                                       "gravity": "bottom",
                                       "contents": []
                                   },
                                   {
                                       "type": "text",
                                       "text": "MWGT : IP " + str(result_site.site.mwgt_ip),
                                       "weight": "bold",
                                       "size": "sm",
                                       "color": "#225508FF",
                                       "align": "center",
                                       "margin": "xs",
                                       "wrap": True,
                                       "contents": []
                                   },
                                   {
                                       "type": "text",
                                       "text": Header_status,
                                       "weight": "bold",
                                       "size": "lg",
                                       "color": color_status,
                                       "align": "center",
                                       "margin": "xs",
                                       "wrap": True,
                                       "contents": []
                                   },
                                   {
                                       "type": "separator",
                                       "margin": "sm",
                                       "color": "#165C3CFF"
                                   },
                                   {
                                       "type": "box",
                                       "layout": "baseline",
                                       "spacing": "sm",
                                       "margin": "xs",
                                       "contents": [
                                           {
                                               "type": "text",
                                               "text": "???????????????",
                                               "weight": "bold",
                                               "size": "md",
                                               "align": "start",
                                               "contents": []
                                           },
                                           {
                                               "type": "text",
                                               "text": Battery_status,
                                               "size": "sm",
                                               "align": "end",
                                               "contents": []
                                           }
                                       ]
                                   },
                                   {
                                       "type": "box",
                                       "layout": "baseline",
                                       "spacing": "sm",
                                       "margin": "sm",
                                       "contents": [
                                           {
                                               "type": "text",
                                               "text": "?????????????????????????????????????????????",
                                               "weight": "bold",
                                               "size": "md",
                                               "align": "start",
                                               "contents": []
                                           },
                                           {
                                               "type": "text",
                                               "text": str(result_site.NOZZLE_pump_log_address),
                                               "size": "sm",
                                               "align": "end",
                                               "contents": []
                                           }
                                       ]
                                   },
                                   {
                                       "type": "box",
                                       "layout": "baseline",
                                       "spacing": "sm",
                                       "margin": "sm",
                                       "contents": [
                                           {
                                               "type": "text",
                                               "text": "??????????????????????????????????????????",
                                               "weight": "bold",
                                               "size": "md",
                                               "align": "start",
                                               "contents": []
                                           },
                                           {
                                               "type": "text",
                                               "text": str(result_site.NOZZLE_num),
                                               "size": "sm",
                                               "align": "end",
                                               "contents": []
                                           }
                                       ]
                                   },
                                   {
                                       "type": "box",
                                       "layout": "baseline",
                                       "spacing": "sm",
                                       "margin": "sm",
                                       "contents": [
                                           {
                                               "type": "text",
                                               "text": "BatteryVolt",
                                               "weight": "bold",
                                               "size": "md",
                                               "align": "start",
                                               "contents": []
                                           },
                                           {
                                               "type": "text",
                                               "text": str(result_site.NOZZLE_Battery_Status_Volts),
                                               "size": "sm",
                                               "align": "end",
                                               "contents": []
                                           }
                                       ]
                                   },
                                   {
                                       "type": "box",
                                       "layout": "baseline",
                                       "spacing": "sm",
                                       "margin": "sm",
                                       "contents": [
                                           {
                                               "type": "text",
                                               "text": "SerialNo.",
                                               "weight": "bold",
                                               "size": "md",
                                               "align": "start",
                                               "contents": []
                                           },
                                           {
                                               "type": "text",
                                               "text": str(result_site.NOZZLE_SN),
                                               "size": "sm",
                                               "align": "end",
                                               "action": {
                                                   "type": "postback",
                                                   "text": "???????????????????????????????????????????????????????????????",
                                                   "data": "10.23.0.130"
                                               },
                                               "contents": []
                                           }
                                       ]
                                   },
                                   {
                                       "type": "box",
                                       "layout": "baseline",
                                       "spacing": "sm",
                                       "margin": "sm",
                                       "contents": [
                                           {
                                               "type": "text",
                                               "text": "LastCon.",
                                               "weight": "bold",
                                               "size": "md",
                                               "align": "start",
                                               "contents": []
                                           },
                                           {
                                               "type": "text",
                                               "text": str(result_site.NOZZLE_Last_conn),
                                               "size": "sm",
                                               "align": "end",
                                               "contents": []
                                           }
                                       ]
                                   },
                                   {
                                       "type": "box",
                                       "layout": "baseline",
                                       "spacing": "sm",
                                       "margin": "sm",
                                       "contents": [
                                           {
                                               "type": "text",
                                               "text": "?????????????????????????????????????????????",
                                               "weight": "bold",
                                               "size": "md",
                                               "align": "start",
                                               "contents": []
                                           },
                                           {
                                               "type": "text",
                                               "text": str(result_site.Timestramp.strftime("%d.%m.%y %H:%M")),
                                               "size": "sm",
                                               "align": "end",
                                               "contents": []
                                           }
                                       ]
                                   },
                                   {
                                       "type": "box",
                                       "layout": "baseline",
                                       "spacing": "sm",
                                       "margin": "sm",
                                       "contents": [
                                           {
                                               "type": "text",
                                               "text": "?????????????????????",
                                               "weight": "bold",
                                               "size": "md",
                                               "align": "start",
                                               "contents": []
                                           },
                                           {
                                               "type": "text",
                                               "text": "????????? " + str(result_site.site.team_support.team_name),
                                               "size": "sm",
                                               "align": "end",
                                               "contents": []
                                           }
                                       ]
                                   },
                                   {
                                       "type": "separator",
                                       "margin": "md",
                                       "color": "#165C3CFF"
                                   }
                               ]
                           },
                           "footer": {
                               "type": "box",
                               "layout": "vertical",
                               "flex": 0,
                               "spacing": "sm",
                               "contents": [
                                   {
                                       "type": "button",
                                       "action": {
                                           "type": "uri",
                                           "label": "www.orpak.co.th",
                                           "uri": "https://www.orpak.com/"
                                       },
                                       "color": "#078025FF",
                                       "margin": "none",
                                       "height": "sm",
                                       "style": "secondary"
                                   },
                                   {
                                       "type": "spacer",
                                       "size": "sm"
                                   }
                               ]
                           }
                       }]}}

        return creating_flex_messages.CheckPermissionBeforeSendLine(result_site.site.team_support.team, content)
