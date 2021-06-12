class line_templates :
    def Gressing_msg():

                                                    data = {
                                                    "type": "flex",
                                                    "altText": "Flex Message",
                                                    "contents": {
                                            "type": "bubble",
                                            "hero": {
                                                "type": "image",
                                                "url": "https://seeoil-web.com/cbre/Picture/CBRE-Logo.jpg",
                                                "align": "center",
                                                "gravity": "bottom",
                                                "size": "full",
                                                "aspectRatio": "20:7",
                                                "aspectMode": "cover",
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
                                                    "text": "EXXON:CBRE",
                                                    "weight": "bold",
                                                    "size": "xl",
                                                    "color": "#225508FF",
                                                    "align": "center",
                                                    "contents": []
                                                },
                                                {
                                                    "type": "text",
                                                    "text": "ขอบคุณที่เพิ่มเราเป็นเพื่อน",
                                                    "align": "center",
                                                    "contents": []
                                                },
                                                {
                                                    "type": "separator",
                                                    "margin": "lg",
                                                    "color": "#E42424FF"
                                                },
                                                {
                                                    "type": "text",
                                                    "text": "เราคือบริการ BOT ของ EXXON-CBRE M&R WORK สำหรับใช้งานซ่อมบำรุงของ CBRE เองเท่านั้น",
                                                    "weight": "bold",
                                                    "color": "#293CCDFF",
                                                    "align": "center",
                                                    "margin": "lg",
                                                    "wrap": True,
                                                    "contents": []
                                                },
                                                {
                                                    "type": "separator",
                                                    "margin": "lg",
                                                    "color": "#E42424FF"
                                                },
                                                {
                                                    "type": "text",
                                                    "text": "สำหรับท่านที่เข้ามาครั้งแรก กรุณาเตรียมระหัสลงทะเบียน เพื่อใช้ในการยืนยันตัวตนก่อนเข้าใช้งาน หากท่านไม่ทราบกรุณาติดต่อไปยัง ส่วนงานของท่านเพื่อขอรับระหัส เพื่อเข้าใช้งาน",
                                                    "weight": "bold",
                                                    "color": "#293CCDFF",
                                                    "align": "center",
                                                    "gravity": "center",
                                                    "margin": "xl",
                                                    "wrap": True,
                                                    "contents": []
                                                },
                                                {
                                                    "type": "separator",
                                                    "margin": "xl",
                                                    "color": "#E42424FF"
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
                                                    "type": "postback",
                                                    "label": "กด - ลงทะเบียนใช้งาน",
                                                    "text": "รอสักครู่ กำลังเช็คระบบลงทะเบียน",
                                                    "data": "register"
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
                                            }
                                                }

                                                    return data
    def register_code ():
        data = {
                                "type": "flex",
                                "altText": "Flex Message",
                                "contents": {
                                "type": "bubble",
                                "body": {
                                  "type": "box",
                                  "layout": "vertical",
                                  "contents": [
                                    {
                                      "type": "text",
                                      "text": "EXXON:CBRE",
                                      "weight": "bold",
                                      "size": "xl",
                                      "color": "#225508FF",
                                      "align": "center",
                                      "contents": []
                                    },
                                    {
                                      "type": "separator",
                                      "margin": "lg",
                                      "color": "#E42424FF"
                                    },
                                    {
                                      "type": "text",
                                      "text": "กรุณาพิมพ์ CBRE และ ตามด้วยระหัสยืนยันตัวตน  6 ตัว เพื่อยืนยันตัวตน",
                                      "weight": "bold",
                                      "color": "#293CCDFF",
                                      "align": "center",
                                      "margin": "lg",
                                      "wrap": True,
                                      "contents": []
                                    },
                                    {
                                      "type": "text",
                                      "text": "ตัวอย่าง CBREXO6875",
                                      "weight": "bold",
                                      "color": "#D01111FF",
                                      "align": "center",
                                      "margin": "lg",
                                      "contents": []
                                    },
                                    {
                                      "type": "separator",
                                      "margin": "lg",
                                      "color": "#E42424FF"
                                    },
                                    {
                                      "type": "text",
                                      "text": "หากหน้าจอไม่แสดงแป้นพิมพ์ ให้กดที่รูปแป้นพิมพ์ตรงด้านล่างมุมซ้ายของหน้าจอ",
                                      "color": "#293CCDFF",
                                      "align": "center",
                                      "margin": "xl",
                                      "wrap": True,
                                      "contents": []
                                    }
                                  ]
                                }
                              }
                                                                              }

        return data
    def re่ject_code ():
        data = {
                                "type": "flex",
                                "altText": "Flex Message",
                                "contents": {
                          "type": "bubble",
                          "body": {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                              {
                                "type": "text",
                                "text": "EXXON:CBRE",
                                "weight": "bold",
                                "size": "xl",
                                "color": "#225508FF",
                                "align": "center",
                                "contents": []
                              },
                              {
                                "type": "separator",
                                "margin": "lg",
                                "color": "#E42424FF"
                              },
                              {
                                "type": "text",
                                "text": "ไม่พบระหัสยืนยันตัวตน กรุณาป้อนอีกครั้ง หรือ ติดต่อ CBRE",
                                "weight": "bold",
                                "color": "#293CCDFF",
                                "align": "center",
                                "margin": "lg",
                                "wrap": True,
                                "contents": []
                              },
                              {
                                "type": "text",
                                "text": "ตัวอย่างการป้อนระห้ัส  ",
                                "weight": "bold",
                                "color": "#D01111FF",
                                "align": "center",
                                "margin": "lg",
                                "contents": []
                              },
                              {
                                "type": "text",
                                "text": "CBREXO6875",
                                "weight": "bold",
                                "color": "#D01111FF",
                                "align": "center",
                                "margin": "lg",
                                "contents": []
                              },
                              {
                                "type": "separator",
                                "margin": "lg",
                                "color": "#E42424FF"
                              }
                            ]
                          }
                        }
                                                                                                      }

        return data
    def alreadySubmit_code (is_user):
        name = is_user.name
        company = is_user.company
        data = {
                                "type": "flex",
                                "altText": "Flex Message",
                                "contents": {
                          "type": "bubble",
                          "body": {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                              {
                                "type": "text",
                                "text": "EXXON:CBRE",
                                "weight": "bold",
                                "size": "xl",
                                "color": "#225508FF",
                                "align": "center",
                                "contents": []
                              },
                              {
                                "type": "separator",
                                "margin": "lg",
                                "color": "#E42424FF"
                              },
                              {
                                "type": "text",
                                "text": "คุณได้ทำการลงทะเบียนเรียบร้อยแล้ว",
                                "weight": "bold",
                                "color": "#293CCDFF",
                                "align": "center",
                                "margin": "lg",
                                "wrap": True,
                                "contents": []
                              },
                              {
                                "type": "text",
                                "text": name,
                                "weight": "bold",
                                "color": "#D01111FF",
                                "align": "center",
                                "margin": "lg",
                                "contents": []
                              },
                              {
                                "type": "text",
                                "text": company,
                                "weight": "bold",
                                "color": "#D01111FF",
                                "align": "center",
                                "margin": "lg",
                                "contents": []
                              },
                              {
                                "type": "text",
                                "text": "ลงทะเบียนสำเร็จแล้ว",
                                "weight": "bold",
                                "color": "#D01111FF",
                                "align": "center",
                                "margin": "lg",
                                "contents": []
                              },
                              {
                                "type": "separator",
                                "margin": "lg",
                                "color": "#E42424FF"
                              }
                            ]
                          }
                        }
                                                                                                      }

        return data
    def ensure_submit (is_user):
      name = is_user.name
      company = is_user.company
      data = {
                                "type": "flex",
                                "altText": "Flex Message",
                                "contents": {
                  "type": "bubble",
                  "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                      {
                        "type": "text",
                        "text": "EXXON:CBRE",
                        "weight": "bold",
                        "size": "xl",
                        "color": "#225508FF",
                        "align": "center",
                        "contents": []
                      },
                      {
                        "type": "separator",
                        "margin": "lg",
                        "color": "#E42424FF"
                      },
                      {
                        "type": "text",
                        "text": "กรุณายืนยันตัวตนตามรายละเอียดนี้",
                        "weight": "bold",
                        "color": "#293CCDFF",
                        "align": "center",
                        "margin": "lg",
                        "wrap": True,
                        "contents": []
                      },
                      {
                        "type": "text",
                        "text": name,
                        "weight": "bold",
                        "color": "#D01111FF",
                        "align": "center",
                        "margin": "lg",
                        "contents": []
                      },
                      {
                        "type": "text",
                        "text": company,
                        "weight": "bold",
                        "color": "#D01111FF",
                        "align": "center",
                        "margin": "lg",
                        "contents": []
                      },
                      {
                        "type": "separator",
                        "margin": "lg",
                        "color": "#E42424FF"
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
                          "type": "postback",
                          "label": "ยืนยันใช่ฉัน",
                          "text": "รอสักครู่ กำลังทำการลงทะเบียน",
                          "data": "REGISTER-OK"
                        },
                        "color": "#078025FF",
                        "margin": "none",
                        "height": "sm",
                        "style": "secondary"
                      },
                      {
                        "type": "button",
                        "action": {
                          "type": "postback",
                          "label": "ไม่ใช่ ฉัน",
                          "text": "กรุณาติดต่อ CBRE เพื่อยืนยันอีกครั้ง",
                          "data": "REGISTER-NOK"
                        },
                        "color": "#706C6CFF",
                        "height": "sm",
                        "style": "primary"
                      },
                      {
                        "type": "spacer",
                        "size": "sm"
                      }
                    ]
                  }
                }
                                                                                                      }

      return data
    def registed ():
        data = {
                                "type": "flex",
                                "altText": "Flex Message",
                                "contents": {
                "type": "bubble",
                "body": {
                  "type": "box",
                  "layout": "vertical",
                  "contents": [
                    {
                      "type": "text",
                      "text": "EXXON:CBRE",
                      "weight": "bold",
                      "size": "xl",
                      "color": "#225508FF",
                      "align": "center",
                      "contents": []
                    },
                    {
                      "type": "separator",
                      "margin": "lg",
                      "color": "#E42424FF"
                    },
                    {
                      "type": "text",
                      "text": "ลงทะเบียนสำเร็จ",
                      "weight": "bold",
                      "color": "#293CCDFF",
                      "align": "center",
                      "margin": "lg",
                      "wrap": True,
                      "contents": []
                    },
                    {
                      "type": "text",
                      "text": "เลือกแถบ CBRE - MENU แล้วเลือก",
                      "weight": "bold",
                      "color": "#D01111FF",
                      "align": "center",
                      "margin": "lg",
                      "contents": []
                    },
                    {
                      "type": "text",
                      "text": "LOGIN",
                      "weight": "bold",
                      "color": "#D01111FF",
                      "align": "center",
                      "margin": "lg",
                      "contents": []
                    },
                    {
                      "type": "separator",
                      "margin": "lg",
                      "color": "#E42424FF"
                    },
                    {
                      "type": "text",
                      "text": "หากหน้าจอไม่แสดงแถบเมนู ให้กดที่รูปเครื่องหมายขีดๆ ตรงด้านล่างมุมซ้ายของหน้าจอ",
                      "weight": "bold",
                      "color": "#293CCDFF",
                      "align": "center",
                      "margin": "lg",
                      "wrap": True,
                      "contents": []
                    }
                  ]
                }
              }
                                                                                                      }

        return data
    def logout ():
        data = {
                                "type": "flex",
                                "altText": "Flex Message",
                                "contents": {
                          "type": "bubble",
                          "body": {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                              {
                                "type": "text",
                                "text": "EXXON:CBRE",
                                "weight": "bold",
                                "size": "xl",
                                "color": "#225508FF",
                                "align": "center",
                                "contents": []
                              },
                              {
                                "type": "separator",
                                "margin": "lg",
                                "color": "#E42424FF"
                              },
                              {
                                "type": "text",
                                "text": "LOGOUT SUCCCESS",
                                "weight": "bold",
                                "color": "#293CCDFF",
                                "align": "center",
                                "margin": "lg",
                                "wrap": True,
                                "contents": []
                              },
                              
                              {
                                "type": "separator",
                                "margin": "lg",
                                "color": "#E42424FF"
                              }
                            ]
                          }
                        }
                                                                                                      }

        return data
    def login ():
        data = {
                                "type": "flex",
                                "altText": "Flex Message",
                                "contents": {
                          "type": "bubble",
                          "body": {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                              {
                                "type": "text",
                                "text": "EXXON:CBRE",
                                "weight": "bold",
                                "size": "xl",
                                "color": "#225508FF",
                                "align": "center",
                                "contents": []
                              },
                              {
                                "type": "separator",
                                "margin": "lg",
                                "color": "#E42424FF"
                              },
                              {
                                "type": "text",
                                "text": "LOGIN SUCCCESS",
                                "weight": "bold",
                                "color": "#293CCDFF",
                                "align": "center",
                                "margin": "lg",
                                "wrap": True,
                                "contents": []
                              },
                              
                              {
                                "type": "separator",
                                "margin": "lg",
                                "color": "#E42424FF"
                              }
                            ]
                          }
                        }
                                                                                                      }

        return data
    
    def re่ject_not_register ():
        data = {
                                "type": "flex",
                                "altText": "Flex Message",
                                "contents": {
                          "type": "bubble",
                          "body": {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                              {
                                "type": "text",
                                "text": "EXXON:CBRE",
                                "weight": "bold",
                                "size": "xl",
                                "color": "#225508FF",
                                "align": "center",
                                "contents": []
                              },
                              {
                                "type": "separator",
                                "margin": "lg",
                                "color": "#E42424FF"
                              },
                              {
                                "type": "text",
                                "text": "กรุณายืนยันตัวตนก่อนเข้าใช้งาน หรือ ติดต่อ CBRE",
                                "weight": "bold",
                                "color": "#293CCDFF",
                                "align": "center",
                                "margin": "lg",
                                "wrap": True,
                                "contents": []
                              },
                              
                              {
                                "type": "separator",
                                "margin": "lg",
                                "color": "#E42424FF"
                              }
                            ]
                          }
                        }
                                                                                                      }

        return data
    
    