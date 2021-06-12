from itertools import groupby
INFO = [{'name_id': 1224, 'Unit_log_address': '11', 'NOZZLE_pump_log_address': '11', 'NOZZLE_num': '1', 'dcount': 1}, {'name_id': 1224, 'Unit_log_address': '11', 'NOZZLE_pump_log_address': '11', 'NOZZLE_num': '2', 'dcount': 1}, {'name_id': 1224, 'Unit_log_address': '11', 'NOZZLE_pump_log_address': '11', 'NOZZLE_num': '3', 'dcount': 1}, {'name_id': 1224, 'Unit_log_address': '11', 'NOZZLE_pump_log_address': '12', 'NOZZLE_num': '1', 'dcount': 1}, {'name_id': 1224, 'Unit_log_address': '11', 'NOZZLE_pump_log_address': '12', 'NOZZLE_num': '2', 'dcount': 1}, {'name_id': 1224, 'Unit_log_address': '11', 'NOZZLE_pump_log_address': '12', 'NOZZLE_num': '3', 'dcount': 1}, {'name_id': 1224, 'Unit_log_address': '11', 'NOZZLE_pump_log_address': '13', 'NOZZLE_num': '1', 'dcount': 1}, {'name_id': 1224, 'Unit_log_address': '11', 'NOZZLE_pump_log_address': '13', 'NOZZLE_num': '2', 'dcount': 1}, {'name_id': 1224, 'Unit_log_address': '11', 'NOZZLE_pump_log_address': '13', 'NOZZLE_num': '3', 'dcount': 1}, {'name_id': 1224, 'Unit_log_address': '11', 'NOZZLE_pump_log_address': '14', 'NOZZLE_num': '1', 'dcount': 1}, {'name_id': 1224, 'Unit_log_address': '11', 'NOZZLE_pump_log_address': '14', 'NOZZLE_num': '2', 'dcount': 1}, {'name_id': 1224, 'Unit_log_address': '11', 'NOZZLE_pump_log_address': '14', 'NOZZLE_num': '3', 'dcount': 1}, {'name_id': 1224, 'Unit_log_address': '11', 'NOZZLE_pump_log_address': '15', 'NOZZLE_num': '1', 'dcount': 1}, {'name_id': 1224, 'Unit_log_address': '11', 'NOZZLE_pump_log_address': '15', 'NOZZLE_num': '2', 'dcount': 1}, {'name_id': 1224, 'Unit_log_address': '11', 'NOZZLE_pump_log_address': '15', 'NOZZLE_num': '3', 'dcount': 1}, {'name_id': 1224, 'Unit_log_address': '12', 'NOZZLE_pump_log_address': '16', 'NOZZLE_num': '1', 'dcount': 1}, {'name_id': 1224, 'Unit_log_address': '12', 'NOZZLE_pump_log_address': '16', 'NOZZLE_num': '2', 'dcount': 1}, {'name_id': 1224, 'Unit_log_address': '12', 'NOZZLE_pump_log_address': '16', 'NOZZLE_num': '3', 'dcount': 1}, {'name_id': 1224, 'Unit_log_address': '12', 'NOZZLE_pump_log_address': '17', 'NOZZLE_num': '1', 'dcount': 1}, {'name_id': 1224, 'Unit_log_address': '12', 'NOZZLE_pump_log_address': '17', 'NOZZLE_num': '2', 'dcount': 1}, {'name_id': 1224, 'Unit_log_address': '12', 'NOZZLE_pump_log_address': '17', 'NOZZLE_num': '3', 'dcount': 1}, {'name_id': 1224, 'Unit_log_address': '12', 'NOZZLE_pump_log_address': '18', 'NOZZLE_num': '1', 'dcount': 1}, {'name_id': 1224, 'Unit_log_address': '12', 'NOZZLE_pump_log_address': '18', 'NOZZLE_num': '2', 'dcount': 1}, {'name_id': 1224, 'Unit_log_address': '12', 'NOZZLE_pump_log_address': '18', 'NOZZLE_num': '3', 'dcount': 1}, {'name_id': 1224, 'Unit_log_address': '12', 'NOZZLE_pump_log_address': '19', 'NOZZLE_num': '1', 'dcount': 1}, {'name_id': 1224, 'Unit_log_address': '12', 'NOZZLE_pump_log_address': '19', 'NOZZLE_num': '2', 'dcount': 1}, {'name_id': 1224, 'Unit_log_address': '12', 'NOZZLE_pump_log_address': '19', 'NOZZLE_num': '3', 'dcount': 1}, {'name_id': 1224, 'Unit_log_address': '12', 'NOZZLE_pump_log_address': '20', 'NOZZLE_num': '1', 'dcount': 1}, {'name_id': 1224, 'Unit_log_address': '12', 'NOZZLE_pump_log_address': '20', 'NOZZLE_num': '2', 'dcount': 1}, {'name_id': 1224, 'Unit_log_address': '12', 'NOZZLE_pump_log_address': '20', 'NOZZLE_num': '3', 'dcount': 1}, {'name_id': 1224, 'Unit_log_address': '12', 'NOZZLE_pump_log_address': '23', 'NOZZLE_num': '1', 'dcount': 1}]
# dictionary
# INFO = [
#     {'employee': 'XYZ_1', 'company': 'ABC_1'},
#     {'employee': 'XYZ_2', 'company': 'ABC_2'},
#     {'employee': 'XYZ_3', 'company': 'ABC_3'},
#     {'employee': 'XYZ_4', 'company': 'ABC_3'},
#     {'employee': 'XYZ_5', 'company': 'ABC_2'},
#     {'employee': 'XYZ_6', 'company': 'ABC_3'},
#     {'employee': 'XYZ_7', 'company': 'ABC_1'},
#     {'employee': 'XYZ_8', 'company': 'ABC_2'},
#     {'employee': 'XYZ_9', 'company': 'ABC_1'}
# ]


# define a fuction for key
def key_func(k):
    return k['name_id']


# sort INFO data by 'company' key.
INFO = sorted(INFO, key=key_func)

for key, value in groupby(INFO, key_func):
    print(key)
    print(list(value))