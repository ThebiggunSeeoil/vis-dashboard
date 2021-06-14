
import datetime # Library สำหรับ วัน เดือน ปี time
datetime_now = datetime.datetime.now().strftime("%d.%m.%Y %H:%M")


def convert_xml_json(data_xml_type_check): #ใช้สำหรับจัดรูปแปบข้อมูลให้อยู่ในรูปแบบ Json
    request_type = 'MRGetMapping'
    data_xml_type = data_xml_type_check['events'][0]['data']
    site_id = data_xml_type_check['events'][0]['name_id']
    print('site_id is',site_id)
    print('data_xml_type is',data_xml_type)
    if request_type == 'DeviceList':
        Device_rtc = data_xml_type['soap:Envelope']['soap:Body']['MRGetDeviceListResponse']['MRGetDeviceListResult']['rc']
        Device_rc_desc = data_xml_type['soap:Envelope']['soap:Body']['MRGetDeviceListResponse']['MRGetDeviceListResult']['rc_desc']
        Device_DataUnit = data_xml_type['soap:Envelope']['soap:Body']['MRGetDeviceListResponse']['MRGetDeviceListResult']['DataUnits']['DataUnit']
        Device_DataUnit_status = data_xml_type['soap:Envelope']['soap:Body']['MRGetDeviceListResponse']['MRGetDeviceListResult']['DataUnits']['DataUnit']['Status']
        Device_DataUnit_StatusDesc = data_xml_type['soap:Envelope']['soap:Body']['MRGetDeviceListResponse']['MRGetDeviceListResult']['DataUnits']['DataUnit']['StatusDesc']
        Device_DataUnit_CountChild = data_xml_type['soap:Envelope']['soap:Body']['MRGetDeviceListResponse']['MRGetDeviceListResult']['DataUnits']['DataUnit']['CountChild']
        Device_DataUnit_IP = data_xml_type['soap:Envelope']['soap:Body']['MRGetDeviceListResponse']['MRGetDeviceListResult']['DataUnits']['DataUnit']['IP']
        Device_DataUnit_LgAddr = data_xml_type['soap:Envelope']['soap:Body']['MRGetDeviceListResponse']['MRGetDeviceListResult']['DataUnits']['DataUnit']['LgAddr']
        Device_DataUnit_address = data_xml_type['soap:Envelope']['soap:Body']['MRGetDeviceListResponse']['MRGetDeviceListResult']['DataUnits']['DataUnit']['address']['addres']
        return Device_rtc, Device_rc_desc, Device_DataUnit, Device_DataUnit_status, \
                    Device_DataUnit_StatusDesc,Device_DataUnit_CountChild, Device_DataUnit_IP, \
                        Device_DataUnit_LgAddr, Device_DataUnit_address
    elif request_type == 'DeviceErrors':
        Error_rtc = data_xml_type['soap:Envelope']['soap:Body']['MRGetErrorsResponse']['MRGetErrorsResult']['rc']
        Error_rc_desc = data_xml_type['soap:Envelope']['soap:Body']['MRGetErrorsResponse']['MRGetErrorsResult']['rc_desc']
        Error_DataUnit = data_xml_type['soap:Envelope']['soap:Body']['MRGetErrorsResponse']['MRGetErrorsResult']['DataUnits']['DataUnitError']
        Error_DataUnit_status = data_xml_type['soap:Envelope']['soap:Body']['MRGetErrorsResponse']['MRGetErrorsResult']['DataUnits']['DataUnitError']['Status']
        Error_DataUnit_StatusDesc = data_xml_type['soap:Envelope']['soap:Body']['MRGetErrorsResponse']['MRGetErrorsResult']['DataUnits']['DataUnitError']['StatusDesc']
        Error_DataUnit_IP = data_xml_type['soap:Envelope']['soap:Body']['MRGetErrorsResponse']['MRGetErrorsResult']['DataUnits']['DataUnitError']['IP']
        Error_DataUnit_LgAddr = data_xml_type['soap:Envelope']['soap:Body']['MRGetErrorsResponse']['MRGetErrorsResult']['DataUnits']['DataUnitError']['LgAddr']
        Error_DataUnit_Errors = data_xml_type['soap:Envelope']['soap:Body']['MRGetErrorsResponse']['MRGetErrorsResult']['DataUnits']['DataUnitError']['Errors']
        return Error_rtc, Error_rc_desc, Error_DataUnit, Error_DataUnit_status, \
                    Error_DataUnit_StatusDesc,Error_DataUnit_IP, Error_DataUnit_LgAddr, \
                        Error_DataUnit_Errors
    elif request_type == 'MRGetMapping':
        data_nozzle_post = []
        Mapping_DataUnit_Units_Nozzles = data_xml_type['soap:Envelope']['soap:Body']['MRGetMappingResponse']['MRGetMappingResult']['DataUnits']['DataUnitMap']['Units']['Unit']['Nozzles']['Nozzle']
        Mapping_rtc = data_xml_type['soap:Envelope']['soap:Body']['MRGetMappingResponse']['MRGetMappingResult']['rc']
        Mapping_rc_desc = data_xml_type['soap:Envelope']['soap:Body']['MRGetMappingResponse']['MRGetMappingResult']['rc_desc']
        Mapping_DataUnit_status = data_xml_type['soap:Envelope']['soap:Body']['MRGetMappingResponse']['MRGetMappingResult']['DataUnits']['DataUnitMap']['Status']
        Mapping_DataUnit_StatusDesc = data_xml_type['soap:Envelope']['soap:Body']['MRGetMappingResponse']['MRGetMappingResult']['DataUnits']['DataUnitMap']['StatusDesc']
        Mapping_DataUnit_IP = data_xml_type['soap:Envelope']['soap:Body']['MRGetMappingResponse']['MRGetMappingResult']['DataUnits']['DataUnitMap']['IP']
        Mapping_DataUnit_LgAddr = data_xml_type['soap:Envelope']['soap:Body']['MRGetMappingResponse']['MRGetMappingResult']['DataUnits']['DataUnitMap']['LgAddr']
        Mapping_DataUnit_Units_log_address = data_xml_type['soap:Envelope']['soap:Body']['MRGetMappingResponse']['MRGetMappingResult']['DataUnits']['DataUnitMap']['Units']['Unit']['log_address']
        Mapping_DataUnit_Units_GWTypS = data_xml_type['soap:Envelope']['soap:Body']['MRGetMappingResponse']['MRGetMappingResult']['DataUnits']['DataUnitMap']['Units']['Unit']['GWTypS']
        Mapping_DataUnit_Units_location = data_xml_type['soap:Envelope']['soap:Body']['MRGetMappingResponse']['MRGetMappingResult']['DataUnits']['DataUnitMap']['Units']['Unit']['location']
        Mapping_DataUnit_Units_sw_version = data_xml_type['soap:Envelope']['soap:Body']['MRGetMappingResponse']['MRGetMappingResult']['DataUnits']['DataUnitMap']['Units']['Unit']['sw_version']
        Mapping_DataUnit_Units_hw_version = data_xml_type['soap:Envelope']['soap:Body']['MRGetMappingResponse']['MRGetMappingResult']['DataUnits']['DataUnitMap']['Units']['Unit']['hw_version']
        Mapping_DataUnit_Units_status_code = data_xml_type['soap:Envelope']['soap:Body']['MRGetMappingResponse']['MRGetMappingResult']['DataUnits']['DataUnitMap']['Units']['Unit']['status_code']
        Mapping_DataUnit_Units_status_desc = data_xml_type['soap:Envelope']['soap:Body']['MRGetMappingResponse']['MRGetMappingResult']['DataUnits']['DataUnitMap']['Units']['Unit']['status_desc']
        try :
            for I in Mapping_DataUnit_Units_Nozzles:
                print('data nozzle is',I)
                data_main = {"name_id":site_id ,
                                "MWGT_last_time": datetime_now,
                                    "VIS_last_time": datetime_now,
                                        "MWGT_status": 'online',
                                             "VIS_status": 'online',
                                                "RTC": Mapping_rtc,
                                                    "DESC": Mapping_rc_desc,
                                                        "DataUnitMap_Status": Mapping_DataUnit_status,
                                                            "DataUnitMap_StatusDesc": Mapping_DataUnit_StatusDesc,
                                                                "DataUnitMap_IP": Mapping_DataUnit_IP,
                                                                    "Unit_log_LgAddr": Mapping_DataUnit_LgAddr,
                                                                        "Unit_log_address": Mapping_DataUnit_Units_log_address,
                                                                            "Unit_GWTypS": Mapping_DataUnit_Units_GWTypS,
                                                                                "Unit_sw_location": Mapping_DataUnit_Units_location,
                                                                                    "Unit_sw_version": Mapping_DataUnit_Units_sw_version,
                                                                                        "Unit_hw_version": Mapping_DataUnit_Units_hw_version,
                                                                                            "Unit_status_code": Mapping_DataUnit_Units_status_code,
                                                                                                "Unit_status_desc": Mapping_DataUnit_Units_status_desc,
                                                                                                    "site_id":site_id,}
                pump_log_address = {"pump_log_address": I['pump_log_address']}
                nozzle_num = {"nozzle_num": I['nozzle_num']}
                nozzle_status = {"nozzle_status": I['nozzle_status']}
                sw_version = {"sw_version": I['sw_version']}
                hw_version = {"hw_version": I['hw_version']}
                SN = {"SN": I['SN']}
                last_conn = {"last_conn": I['last_conn']}
                battery_status = {"battery_status": I['battery_status']}
                BatPrcnt = {"BatPrcnt": I['BatPrcnt']}
                nozzle_dist = [pump_log_address, nozzle_num, nozzle_status, sw_version, hw_version, SN, last_conn,battery_status, BatPrcnt]
                for zozzle_loop in nozzle_dist:
                    data_main.update(zozzle_loop)
                data_nozzle_post.append(data_main)
            print('data_nozzle_post is',data_nozzle_post)
            return data_nozzle_post

        except :
            return False
