import json
import requests

class WebService:
    def __init__(self):
        pass
    
    def upload(self, name, path_to_bpmn, path_to_svg, options):
        # Implement the upload logic here
        pass

class BPMNClient2(WebService):
    def __init__(self, host, port, api_key):
        super().__init__()
        self.host = host
        self.port = port
        self.api_key = api_key
        self.engine = Engine(self)
        self.data = Data(self)
        self.model = Model(self)

    def get(self, url, params=None):
        return  self.request(url, 'GET', params)

    def post(self, url, params=None):
        return  self.request(url, 'POST', params)

    def put(self, url, params=None):
        return  self.request(url, 'PUT', params)

    def delete(self, url, params=None):
        return  self.request(url, 'DELETE', params)

    def request(self, url, method, params):
        body = json.dumps(params)
        content_type = "application/json"

        if method == 'UPLOAD':
            content_type = 'multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW'
            method = 'POST'

        headers = {
            "Content-Type": content_type,
            "x-api-key": self.api_key,
            "Accept": "*/*",
            "Connection": "keep-alive"
        }
        
        if (self.port=='443'):
            furl=f'https://{self.host}/api2/{url}'
        else:
            furl=f'http://{self.host}:{self.port}/api2/{url}'
        options = {
            'url': furl,
            'method': method,
            'headers': headers,
            'data': body
        }

        return  self.invoke(params, options)

    def invoke(self, params, options):
        response = requests.request(
            method=options['method'],
            url=options['url'],
            headers=options['headers'],
            data=options.get('data')
        )
        return response.json()
    
    def status(self):
        return self.get('status')        

class Engine:
    def __init__(self, client):
        self.client = client

    def start(self, name, data=None, user=None, options=None):
        if data is None:
            data = {}
        if options is None:
            options = {}
        ret =  self.client.post('engine/start', {'name': name, 'data': data, 'user': user, 'options': options})
        if 'errors' in ret:
            print(ret['errors'])
            raise Exception(ret['errors'])
        return ret['instance']

    def invoke(self, query, data, user, options=None):
        if options is None:
            options = {}
        ret =  self.client.put('engine/invoke', {'query': query, 'data': data, 'user': user, 'options': options})
        if 'errors' in ret:
            print(ret['errors'])
            raise Exception(ret['errors'])
        return ret['instance']

    def assign(self, query, data, assignment, user):
        ret =  self.client.put('engine/assign', {'query': query, 'data': data, 'assignment': assignment, 'user': user})
        if 'errors' in ret:
            print(ret['errors'])
            raise Exception(ret['errors'])
        return ret['instance']

    def throw_message(self, message_id, data=None, message_matching_key=None, user=None, options=None):
        if data is None:
            data = {}
        if message_matching_key is None:
            message_matching_key = {}
        ret =  self.client.post('engine/throwMessage', {'messageId': message_id, 'data': data, 'messageMatchingKey': message_matching_key, 'user': user, 'options': options})
        if 'errors' in ret:
            print(ret['errors'])
            raise Exception(ret['errors'])
        return ret

    def throw_signal(self, signal_id, data=None, message_matching_key=None, user=None, options=None):
        if data is None:
            data = {}
        if message_matching_key is None:
            message_matching_key = {}
        ret =  self.client.post('engine/throwSignal', {'signalId': signal_id, 'data': data, 'message_matching_key': message_matching_key, 'user': user, 'options': options})
        if 'errors' in ret:
            print(ret['errors'])
            raise Exception(ret['errors'])
        return ret

class Data:
    def __init__(self, client):
        self.client = client

    def find_items(self, query, user):
        res =  self.client.get('data/findItems', {'query': query, 'user': user})
        if 'errors' in res:
            print(res['errors'])
            raise Exception(res['errors'])
        return res['items']

    def find_instances(self, query, user):
        res =  self.client.get('data/findInstances', {'query': query, 'user': user})
        if 'errors' in res:
            print(res['errors'])
            raise Exception(res['errors'])
        
        return Response(res)
        return res['instances']

    def delete_instances(self, query, user):
        return  self.client.delete('data/deleteInstances', {'query': query, 'user': user})

class Model:
    def __init__(self, client):
        self.client = client

    def importModel(self, name, path_to_bpmn, path_to_svg=None, user=None):
        options = {
            'method': 'POST',
            'url': f'http://{self.client.host}:{self.client.port}/api/model/import/{name}',
            'headers': {
                'x-api-key': self.client.api_key
            },
            'maxRedirects': 20
        }
        print('import', name, path_to_bpmn, path_to_svg)
        res =  self.client.upload(name, path_to_bpmn, path_to_svg, options)
        print('import done', res)
        self.check_errors(res)
        return res

    def listModels(self):
        res =  self.client.get('model/list', [])
        if 'errors' in res:
            print(res['errors'])
            raise Exception(res['errors'])
        return res

    def deleteModel(self, name):
        res =  self.client.post('model/delete/', {'name': name})
        if 'errors' in res:
            print(res['errors'])
            raise Exception(res['errors'])
        return res

    def renameModel(self, name, new_name):
        res =  self.client.post('model/rename/', {'name': name, 'newName': new_name})
        if 'errors' in res:
            print(res['errors'])
            raise Exception(res['errors'])
        return res

    def loadModel(self, name):
        res =  self.client.get(f'model/load/{name}', {'name': name})
        return Response(res)

class Response:
    def __init__(self,res) -> None:
        self.res=res
    def hasErrors(self):
        if 'errors' in self.res:
            print(self.res['errors'])
            raise Exception(self.res['errors'])
        return self
    
    def status(self):
        return self;

    def listItems(self):
        self.hasErrors()


        for item in self.res['items']: {
            print(' item:',item['seq'],item['elementId'],item['status'])
        }
        return self

    def print_instances(self,fields=['id','name']):
        for inst in self.res['instances']: 
            vals=''
            for f in fields: 
                vals=vals+inst[f]
            
            print('instance:',vals)
        
    def dump(self):
        self.hasErrors()
        for key in self.res: {
            print(' key',key)
        }
        return self

class DisplayUtil:
    from IPython.display import HTML , IFrame
    
    def displayTable(self,data,cols):
        html = "<table>"
        for col in cols:
            html = f"{html}<th style='text-align:center;'>{col}</th>"
        for row in data:
            html = f"{html}<tr>"
            for col in cols:
                html = f"{html}<td style='text-align:left;'>{row[col]}</td>"
            html = f"{html}</tr>"
        html = f"{html}</table>"

 #       return display(HTML(html))

    def displayItems(self,res):
        return self.displayTable(res['items'],['seq','elementId', 'status'])

    def displayDiagram(self,name):
        url = f"https://bpmn.omniworkflow.com/model/getSVg/{name}"

#        return HTML(f"<img src='{url}' width='100%' height='100%'/>")

  #  def displayPage(self,url):
  #      display(IFrame(url,"100%","100%"))
        #return HTML(f"<iframe src='{url}' width='100%' height='100%'></iframe>")

    def describeModel(self,model):
        
   #     display(HTML('<h2>Elements</h2>'))

        els=[]
        for el in model.res['elements']:
            el["property"]=''
            el["value"]=''
            els.append(el)
            for des in el["description"]:
                el1={"id":'',"type":'',"property":des[0],"value":des[1]}
                els.append(el1)
                
        self.displayTable(els,['id','type','property','value'])

    #    display(HTML('<h2>Sequence Flows</h2>'))

        els=[]
        for el in model.res['flows']:
            el["property"]=''
            el["value"]=''
            els.append(el)
            for des in el["description"]:
                el1={"id":'',"type":'',"property":des[0],"value":des[1]}
                els.append(el1)
            
        self.displayTable(els,['id','type','property','value'])
