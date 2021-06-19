from app.models import Site, Status , Status_Error_logger,Store_data_send_line_failed

class connect_db_profile ():
    def get_site_profile (payload,type):
        try :
            result_site = Site.objects.select_related().get(id=payload['events'][0]['data'])
            result_status = Status.objects.all().filter(name_id=payload['events'][0]['data']).first()
            if type == 'notify_MWGT_ONLINE' :
                result_status_error_logger = Status_Error_logger.objects.all().filter(id=payload['events'][0]['Logger_id']).first()
                return result_site, result_status, result_status_error_logger
            elif type == 'notify_MWGT_OFFLINE' :
                return result_site , result_status
            elif type == 'notify_VIS_ONLINE' :
                result_status_error_logger = Status_Error_logger.objects.all().filter(name_id=payload['events'][0]['data'],Error_type='VIS-OFFLINE').order_by('-Timestramp').first()
                # print ('notify_VIS_ONLINE is',result_status_error_logger)
                return result_site , result_status ,result_status_error_logger
        except Exception as e: 
            print(e) 
            print('Cannot get site profile in linebot.connect_db_profile')