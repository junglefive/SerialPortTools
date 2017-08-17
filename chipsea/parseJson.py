import json
try:
    print('parsing file: sfr.json')
    with open('sfr.json','r') as json_file:
        print('content of file is：')
        data = json.load(json_file)
        json_file.close()
        print(type(data))
        print('\nname:',data['sfr_name'],'\nadress:',data['adress'],'\nvalue:',data['write_value'])
        
except e:
    print('erro', str(e))
finally:
    input()


