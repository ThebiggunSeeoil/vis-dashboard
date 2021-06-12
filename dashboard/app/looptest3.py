# from itertools import groupby
# from operator import itemgetter
# strings = [{'name_id': 1224, 'Unit_log_address': '11', 'NOZZLE_pump_log_address': '11', 'NOZZLE_num': '1', 'dcount': 1},
#            {'name_id': 1224, 'Unit_log_address': '11', 'NOZZLE_pump_log_address': '11', 'NOZZLE_num': '2', 'dcount': 1},
#            {'name_id': 1224, 'Unit_log_address': '11', 'NOZZLE_pump_log_address': '11', 'NOZZLE_num': '3', 'dcount': 1},
#            {'name_id': 1224, 'Unit_log_address': '11', 'NOZZLE_pump_log_address': '12', 'NOZZLE_num': '1', 'dcount': 1},
#            {'name_id': 1224, 'Unit_log_address': '11', 'NOZZLE_pump_log_address': '12', 'NOZZLE_num': '2', 'dcount': 1},
#            {'name_id': 1224, 'Unit_log_address': '11', 'NOZZLE_pump_log_address': '12', 'NOZZLE_num': '3', 'dcount': 1},
#            {'name_id': 1224, 'Unit_log_address': '11', 'NOZZLE_pump_log_address': '13', 'NOZZLE_num': '1', 'dcount': 1},
#            {'name_id': 1224, 'Unit_log_address': '11', 'NOZZLE_pump_log_address': '13', 'NOZZLE_num': '2', 'dcount': 1},
#            {'name_id': 1224, 'Unit_log_address': '11', 'NOZZLE_pump_log_address': '13', 'NOZZLE_num': '3', 'dcount': 1},
#            {'name_id': 1224, 'Unit_log_address': '11', 'NOZZLE_pump_log_address': '14', 'NOZZLE_num': '1', 'dcount': 1},
#            {'name_id': 1224, 'Unit_log_address': '11', 'NOZZLE_pump_log_address': '14', 'NOZZLE_num': '2', 'dcount': 1},
#            {'name_id': 1224, 'Unit_log_address': '11', 'NOZZLE_pump_log_address': '14', 'NOZZLE_num': '3', 'dcount': 1},
#            {'name_id': 1224, 'Unit_log_address': '11', 'NOZZLE_pump_log_address': '15', 'NOZZLE_num': '1', 'dcount': 1},
#            {'name_id': 1224, 'Unit_log_address': '11', 'NOZZLE_pump_log_address': '15', 'NOZZLE_num': '2', 'dcount': 1},
#            {'name_id': 1224, 'Unit_log_address': '11', 'NOZZLE_pump_log_address': '15', 'NOZZLE_num': '3', 'dcount': 1},
#            {'name_id': 1224, 'Unit_log_address': '12', 'NOZZLE_pump_log_address': '16', 'NOZZLE_num': '1', 'dcount': 1},
#            {'name_id': 1224, 'Unit_log_address': '12', 'NOZZLE_pump_log_address': '16', 'NOZZLE_num': '2', 'dcount': 1},
#            {'name_id': 1224, 'Unit_log_address': '12', 'NOZZLE_pump_log_address': '16', 'NOZZLE_num': '3', 'dcount': 1},
#            {'name_id': 1224, 'Unit_log_address': '12', 'NOZZLE_pump_log_address': '17', 'NOZZLE_num': '1', 'dcount': 1},
#            {'name_id': 1224, 'Unit_log_address': '12', 'NOZZLE_pump_log_address': '17', 'NOZZLE_num': '2', 'dcount': 1},
#            {'name_id': 1224, 'Unit_log_address': '12', 'NOZZLE_pump_log_address': '17', 'NOZZLE_num': '3', 'dcount': 1},
#            {'name_id': 1224, 'Unit_log_address': '12', 'NOZZLE_pump_log_address': '18', 'NOZZLE_num': '1', 'dcount': 1},
#            {'name_id': 1224, 'Unit_log_address': '12', 'NOZZLE_pump_log_address': '18', 'NOZZLE_num': '2', 'dcount': 1},
#            {'name_id': 1224, 'Unit_log_address': '12', 'NOZZLE_pump_log_address': '18', 'NOZZLE_num': '3', 'dcount': 1},
#            {'name_id': 1224, 'Unit_log_address': '12', 'NOZZLE_pump_log_address': '19', 'NOZZLE_num': '1', 'dcount': 1},
#            {'name_id': 1224, 'Unit_log_address': '12', 'NOZZLE_pump_log_address': '19', 'NOZZLE_num': '2', 'dcount': 1},
#            {'name_id': 1224, 'Unit_log_address': '12', 'NOZZLE_pump_log_address': '19', 'NOZZLE_num': '3', 'dcount': 1},
#            {'name_id': 1224, 'Unit_log_address': '12', 'NOZZLE_pump_log_address': '20', 'NOZZLE_num': '1', 'dcount': 1},
#            {'name_id': 1224, 'Unit_log_address': '12', 'NOZZLE_pump_log_address': '20', 'NOZZLE_num': '2', 'dcount': 1},
#            {'name_id': 1224, 'Unit_log_address': '12', 'NOZZLE_pump_log_address': '20', 'NOZZLE_num': '3', 'dcount': 1},
#            {'name_id': 1224, 'Unit_log_address': '12', 'NOZZLE_pump_log_address': '23', 'NOZZLE_num': '1', 'dcount': 1}]

records = [{'name': '1224', 'Unit_log_address': '11'},
           {'name': '1224', 'Unit_log_address': '12'},
          {'name': '1225', 'Unit_log_address': '12'},
           ]
#
# for k, v in groupby(sorted(d.items(), key=itemgetter(1)), itemgetter(1)):
#     print(k, list(map(itemgetter(0), v)))

from collections import ChainMap

# records = [{'name': 'charlie', 'Ready For Dev': 2.0},
#            {'name': 'charlie', 'Ready for Release': 12.0},
#            {'name': 'john', 'Ready to Test': 2.0},
#            {'name': 'henry', 'Open': 8.0},
#            {'name': 'henry', 'Ready for Release': 16.0}]

names = {row['name'] for row in records}  # set of unique names

new = []  # list to collect new dictionaries

for name in names:
    new.append(dict(ChainMap(*(row for row in records if row['name'] == name))))

for i in new :
    print(i)