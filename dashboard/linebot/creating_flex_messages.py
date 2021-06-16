
def CreateAllStatusVIS(dt, VIS_SUM_OFFLINE, MWGT_SUM_OFFLINE, NOZZLE_OFFLINE, BATTERY_OFFLINE, TOTAL_SITE_ACTIVE):
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
