GET_VIS_DATA_ALL = [{'name_id': 1224, 'Unit_log_address': '11', 'NOZZLE_pump_log_address': '11', 'NOZZLE_num': '1', 'dcount': 1},
                    {'name_id': 1224, 'Unit_log_address': '11', 'NOZZLE_pump_log_address': '11', 'NOZZLE_num': '2', 'dcount': 1},
                    {'name_id': 1224, 'Unit_log_address': '12', 'NOZZLE_pump_log_address': '16', 'NOZZLE_num': '1', 'dcount': 1},
                    {'name_id': 1225, 'Unit_log_address': '11', 'NOZZLE_pump_log_address': '11', 'NOZZLE_num': '1', 'dcount': 1},
                    {'name_id': 1225, 'Unit_log_address': '12', 'NOZZLE_pump_log_address': '16', 'NOZZLE_num': '1', 'dcount': 1},
                    ]

data1 = [{'name_id': 1224},{'Unit_log_address':'11'}]


# query เอามาเฉพาะ name_id จากตาราง Site
GET_VIS_DATA = [{'name_id': 1224, 'Unit_log_address': '11', 'dcount': 15 },{'name_id': 1225, 'Unit_log_address': '11', 'dcount': 15 }]
store = []

def prepare_nozzle (GET_VIS_DATA,GET_VIS_DATA_ALL) :
    vis_check = [] #สำหรับเก็บค่า name_id เพื่อป้องกันไม่ให้มีการบันทึกซ้ำ
    vis_result = []
    #ส่วนสำหรับ นำค่าที่ได้จากตาราง site ที่เป็น name_id เอามาเพิ่มข้อมูล 'Unit_log_address':[] เข้าไปเพื่อใช้ในการเก็บข้อมูลของ nozzle
    for data in GET_VIS_DATA:
        # print(data)
        if data['name_id'] not in vis_check: #ทำการเช็คว่า name_id มีเก็บไว้ใน vis_check = [] หรือไม่ถ้ายังไม่มีก็จะทำข้างล่างจนเสร็จก่อน แล้วค่อยนำ name_id ไปบันทึกไว้เพื่อป้องกันการ loop รอบอื่นๆมาทำซ้ำอีก
            vis_check.append(data['name_id']) # ทำการนำ name_id ไปบันทึกไว้ที่ vis_check = []
            data = {'name_id': data['name_id'],
                        # 'site_name':data['site__station_name'],
                        #     'station_ip':data['site__station_ip'],
                        #         'station_monitor_device': data['site__station_monitor_device'],
                        #                 'MWGT_status':data['MWGT_status'],
                        #                     'VIS_status':data['VIS_status'],
                        #                         'NOZZLE_status_check':data['NOZZLE_status_check'],
                        #                             'BATTERY_status_check':data['BATTERY_status_check'],
                        #                                 'VIS_last_time':data['VIS_last_time'],
                                                            'Unit_log_address':[]} #สร้างข้อมูลไว้ สำหรับโยนเข้าไปเก็บไว้ใน vis_result = []
            vis_result.append(data) # นำ data ไปเก็บไว้ใน vis_result = [] เพื่อเอาไปใช้ใน function อื่น
    # for vis_1 in vis_result :
    #     print('vis 1 ',vis_1)
    GET_VIS_DATA_ALL_CHECK_STORE = [] #สำหรับเก็บค่า Unit_log_address เพื่อป้องกันไม่ให้มีการบันทึกซ้ำ
    for Unit_check in vis_result :
        for GET_VIS_DATA_ALL_CHECK in GET_VIS_DATA_ALL :
            log_check = str(GET_VIS_DATA_ALL_CHECK['name_id']) + str(GET_VIS_DATA_ALL_CHECK['Unit_log_address'])
            if GET_VIS_DATA_ALL_CHECK['name_id'] == Unit_check['name_id']:
                if log_check not in GET_VIS_DATA_ALL_CHECK_STORE:
                    GET_VIS_DATA_ALL_CHECK_STORE.append(log_check)
                    value = {'Unit_log_address': GET_VIS_DATA_ALL_CHECK['Unit_log_address'] ,'nozzle':[]}
                    Unit_check['Unit_log_address'].append(value)




    GET_NOZZLE_CHECK_STORE = [] #สำหรับเก็บค่า Unit_log_address เพื่อป้องกันไม่ให้มีการบันทึกซ้ำ
    for nozzle_check in vis_result  :
        for GET_VIS_DATA_ALL_CHECK in GET_VIS_DATA_ALL:

            if GET_VIS_DATA_ALL_CHECK['name_id'] == nozzle_check['name_id']:
                log_check = str(GET_VIS_DATA_ALL_CHECK['name_id']) + str(GET_VIS_DATA_ALL_CHECK['Unit_log_address'])
                # for index , loop_check in enumerate(nozzle_check['Unit_log_address']) :
                #     if loop_check['Unit_log_address'] == GET_VIS_DATA_ALL_CHECK['Unit_log_address'] :
                #         nozzle_check['Unit_log_address'][index]['nozzle'].append(GET_VIS_DATA_ALL_CHECK)
                # if GET_VIS_DATA_ALL_CHECK['Unit_log_address'] == nozzle_check['Unit_log_address'][0]['Unit_log_address']:
                    # if log_check not in GET_NOZZLE_CHECK_STORE:
                    # GET_NOZZLE_CHECK_STORE.append(log_check)
                value = {'Unit_log_address': GET_VIS_DATA_ALL_CHECK['Unit_log_address'] ,'nozzle':[]}
                for nozzle_loop in nozzle_check['Unit_log_address'] :
                    if nozzle_loop['Unit_log_address'] == GET_VIS_DATA_ALL_CHECK['Unit_log_address']:
                        nozzle_loop['nozzle'].append(GET_VIS_DATA_ALL_CHECK)
    # print(vis_result)
    return (vis_result)
result = prepare_nozzle(GET_VIS_DATA,GET_VIS_DATA_ALL)
# print (result)
for i in result :
    print(i)