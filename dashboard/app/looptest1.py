GET_VIS_DATA_ALL = [{'name_id': 1224, 'Unit_log_address': '11', 'NOZZLE_pump_log_address': '11', 'NOZZLE_num': '1', 'dcount': 1},
                    {'name_id': 1224, 'Unit_log_address': '11', 'NOZZLE_pump_log_address': '11', 'NOZZLE_num': '2', 'dcount': 1},
                    {'name_id': 1224, 'Unit_log_address': '12', 'NOZZLE_pump_log_address': '16', 'NOZZLE_num': '1', 'dcount': 1},
                    {'name_id': 1225, 'Unit_log_address': '11', 'NOZZLE_pump_log_address': '11', 'NOZZLE_num': '1', 'dcount': 1},
                    {'name_id': 1225, 'Unit_log_address': '12', 'NOZZLE_pump_log_address': '16', 'NOZZLE_num': '1', 'dcount': 1},
                    ]

NOZZLE = [{'id': 10366, 'site_id': 1224, 'pump_log_address': '5', 'nozzle_num': '1', 'nozzle_status': '1', 'log_address': '1', 'station_ip': '10.23.0.114', 'data_unit_ip': '10.23.32.114'},
        {'id': 10385, 'site_id': 1224, 'pump_log_address': '5', 'nozzle_num': '2', 'nozzle_status': '1', 'log_address': '1', 'station_ip': '10.23.0.114', 'data_unit_ip': '10.23.32.114'},
        {'id': 10405, 'site_id': 1224, 'pump_log_address': '5', 'nozzle_num': '3', 'nozzle_status': '1', 'log_address': '1', 'station_ip': '10.23.0.114', 'data_unit_ip': '10.23.32.114'},
        {'id': 10432, 'site_id': 1224, 'pump_log_address': '6', 'nozzle_num': '1', 'nozzle_status': '1', 'log_address': '1', 'station_ip': '10.23.0.114', 'data_unit_ip': '10.23.32.114'},
        {'id': 10448, 'site_id': 1224, 'pump_log_address': '6', 'nozzle_num': '2', 'nozzle_status': '1', 'log_address': '1', 'station_ip': '10.23.0.114', 'data_unit_ip': '10.23.32.114'},
        {'id': 10455, 'site_id': 1224, 'pump_log_address': '6', 'nozzle_num': '3', 'nozzle_status': '1', 'log_address': '1', 'station_ip': '10.23.0.114', 'data_unit_ip': '10.23.32.114'},
          {'id': 10366, 'site_id': 1225, 'pump_log_address': '5', 'nozzle_num': '1', 'nozzle_status': '1',
           'log_address': '1', 'station_ip': '10.23.0.114', 'data_unit_ip': '10.23.32.114'},
          {'id': 10385, 'site_id': 1225, 'pump_log_address': '5', 'nozzle_num': '2', 'nozzle_status': '1',
           'log_address': '1', 'station_ip': '10.23.0.114', 'data_unit_ip': '10.23.32.114'},
          {'id': 10405, 'site_id': 1225, 'pump_log_address': '5', 'nozzle_num': '3', 'nozzle_status': '1',
           'log_address': '1', 'station_ip': '10.23.0.114', 'data_unit_ip': '10.23.32.114'},
          {'id': 10432, 'site_id': 1225, 'pump_log_address': '5', 'nozzle_num': '1', 'nozzle_status': '1',
           'log_address': '1', 'station_ip': '10.23.0.114', 'data_unit_ip': '10.23.32.114'},
          {'id': 10448, 'site_id': 1225, 'pump_log_address': '5', 'nozzle_num': '2', 'nozzle_status': '1',
           'log_address': '1', 'station_ip': '10.23.0.114', 'data_unit_ip': '10.23.32.114'},
          {'id': 10455, 'site_id': 1225, 'pump_log_address': '5', 'nozzle_num': '3', 'nozzle_status': '1',
           'log_address': '1', 'station_ip': '10.23.0.114', 'data_unit_ip': '10.23.32.114'}
          ]

name_site = [{'name_id':1021,'pump_log_address_check':[],'nozzle_data_check':[],'pump_log_address_count':[],'nozzle_data_count':[]}]

GET_VIS_DATA = [{'name_id': 1224, 'Unit_log_address': '11', 'dcount': 15 },{'name_id': 1225, 'Unit_log_address': '11', 'dcount': 15 }]


def prepare_nozzle (GET_VIS_DATA,GET_VIS_DATA_ALL,NOZZLE) :
    vis_check = [] #สำหรับเก็บค่า name_id เพื่อป้องกันไม่ให้มีการบันทึกซ้ำ
    vis_result = []
    #ส่วนสำหรับ นำค่าที่ได้จากตาราง site ที่เป็น name_id เอามาเพิ่มข้อมูล 'Unit_log_address':[] เข้าไปเพื่อใช้ในการเก็บข้อมูลของ nozzle
    for data in GET_VIS_DATA:
        # print(data)
        if data['name_id'] not in vis_check: #ทำการเช็คว่า name_id มีเก็บไว้ใน vis_check = [] หรือไม่ถ้ายังไม่มีก็จะทำข้างล่างจนเสร็จก่อน แล้วค่อยนำ name_id ไปบันทึกไว้เพื่อป้องกันการ loop รอบอื่นๆมาทำซ้ำอีก
            vis_check.append(data['name_id']) # ทำการนำ name_id ไปบันทึกไว้ที่ vis_check = []
            data = {'name_id': data['name_id'],
                    'log_address_check': [],
                    'pump_log_address_check': [],
                    'nozzle_data_check': [],
                    'log_address_count': [],
                    'pump_log_address_count': [],
                    'nozzle_data_count': [],
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
    for name_id in vis_result:
        for data in NOZZLE:
            if data['site_id'] == name_id['name_id']:
                name_id['nozzle_data_check'].append(data['nozzle_num'])
                if data['pump_log_address'] not in name_id['pump_log_address_check']:
                    name_id['pump_log_address_check'].append(data['pump_log_address'])


                if data['log_address'] not in name_id['log_address_check']:
                    name_id['log_address_check'].append(data['log_address'])
        for count in vis_result:

            count_log = len(count['pump_log_address_check'])
            count_num = len(count['nozzle_data_check'])
            count_log_main = len(count['log_address_check'])
            count['pump_log_address_count'] = count_log
            count['nozzle_data_count'] = count_num
            count['log_address_count'] = count_log_main

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




# for name_id in name_site :
#     for data in data :
#         if data['site_id'] == name_id['name_id']:
#             name_id['nozzle_data'].append(data['nozzle_num'])
#             if data['pump_log_address'] not in name_id['pump_log_address']:
#                 name_id['pump_log_address'].append(data['pump_log_address'])
#     for count in name_site :
#         count_log = len(count['pump_log_address'])
#         count_num = len(count['nozzle_data'])
#         count['pump_log_address_count'].append(count_log)
#         count['nozzle_data_count'].append(count_num)

# print(name_site)



result = prepare_nozzle(GET_VIS_DATA,GET_VIS_DATA_ALL,NOZZLE)
# print (result)
for i in result :
    print(i)




