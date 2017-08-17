import json 
import sys
try:
    print('parsing file: sfr.json')
    with open('./sfr.json','r') as json_file:
        print('content of file is：')
        data = json.load(json_file)
        json_file.close()
        print(type(data))
        print('name',data['sfr_name'],'adress',data['adress'],'value',data['write_value'])
except e:
    print('erro', str(e))
finally:
    input()


