import json

class JsonParse(object):
    def __init__(self, msg = 'nothing'):
        self.msg = msg
    def load(self, path):
        with open(path,'r') as jf:
            data = json.load(jf)
            jf.close()
            return data
if __name__ == "__main__":
    js = JsonParse()
    try:
        data = js.load('sfr_test.json')
        print(data)
    except Exception as e:
        print(str(e))
    finally:
        print('exit')
        input()





