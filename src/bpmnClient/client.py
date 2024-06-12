import requests 

class Engine:
    def __init__(self,client) -> None:
        self.client=client

    def start(self,name,data):
        print('start:',self,name)
        body={"name": name,"data": data}
        url = self.client.site+'/api/engine/start'

        r=requests.post(url,json=body,headers=self.client.headers)

        return Response(r.json())
    
   
    def invoke(self,query,data):
        
        body={"query": query,"data": data}
        url = self.client.site+'/api/engine/invoke'

        r=requests.put(url,json=body,headers=self.client.headers)

        res=r.json()
        for key in res['instance']: {
            print(' key',key)
        }
            
        return r.json()

class Data:
    def __init__(self,client) -> None:
        self.client=client

    def findInstnaces(self,query):
        body={"query": query}
        url = self.client.site+'/api/datastore/findInstances'
        print(body)

        r=requests.get(url,json=body,headers=self.client.headers)

        print('findInstances.... results')
        print(r.json)
        res=r.json()

        for key in res['instances']: {
            print(' instance',key['name'],key['id'])
        }
            
        return r.json()

  
class Model:
    def __init__(self,client) -> None:
        self.client=client

    def list(self):
        res=self.client.get('definitions/list',{})

        data=res.json()

        for key in data:{ 
            print(key['name']) 
        }

class Client:
    def __init__(self,site,apiKey) -> None:
        self.site=site
        self.apiKey=apiKey
        self.headers = {'x-api-key': apiKey}
        self.engine=Engine(self)
        self.data=Data(self)
        self.model=Model(self)

        print('self:',self)

    def __str__(self):

        return 'self:'+self.site+' '+self.apiKey
        
    def get(self,url,body):
        url = self.site+'/api/'+url
        r=requests.get(url,json=body,headers=self.headers)
        return r



    def status(self):
        
        r=self.get('status',{})
        res=r.json()
        for key in res: {
            print(' key',key)
        }

        return r.json()
        
    def listItems(self,response):

        res=response
        for key in res: {
            print(' res key:',key)
        }

        for item in res['items']: {
            print(' item:',item['seq'],item['elementId'],item['status'])
        }

class Response:
    def __init__(self,res) -> None:
        self.res=res
    def hasErrors(self):
        pass
        return self

    def listItems(self):
        for key in self.res: {
            print(' res key:',key)
        }

        for item in self.res['items']: {
            print(' item:',item['seq'],item['elementId'],item['status'])
        }
        return self

    def dump(self):
        for key in self.res: {
            print(' key',key)
        }
        return self

