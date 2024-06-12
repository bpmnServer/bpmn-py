import json
import requests
import asyncio

class BPMNClient:
    def __init__(self, host, port, api_key):
        self.host = host
        self.port = port
        self.api_key = api_key
        self.engine = ClientEngine(self)
        self.datastore = ClientDatastore(self)
        self.definitions = ClientDefinitions(self)

    def get(self, url, data=None):
        if data is None:
            data = {}
        return  self.request(url, 'GET', data)

    def post(self, url, data=None):
        if data is None:
            data = {}
        return  self.request(url, 'POST', data)

    def put(self, url, data=None):
        if data is None:
            data = {}
        return  self.request(url, 'PUT', data)

    def delete(self, url, data=None):
        if data is None:
            data = {}
        return  self.request(url, 'DELETE', data)

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

        options = {
            'url': f'http://{self.host}:{self.port}/api/{url}',
            'method': method,
            'headers': headers,
            'data': body
        }

        with requests.Session() as session:
            with session.request(**options) as response:
                response.raise_for_status()
                return response.json()

class ClientEngine:
    def __init__(self, client):
        self.client = client

    def start(self, name, data=None, start_node_id=None, user_id=None, options=None):
        if data is None:
            data = {}
        if options is None:
            options = {}
        ret =  self.client.post('engine/start', {"name": name, "data": data, "startNodeId": start_node_id, "userId": user_id, "options": options})
        if 'errors' in ret:
            raise Exception(ret['errors'])
        return ret

    def invoke(self, query, data, user_id=None, options=None):
        if options is None:
            options = {}
        ret =  self.client.put('engine/invoke', {"query": query, "data": data, "userId": user_id, "options": options})
        if 'errors' in ret:
            raise Exception(ret['errors'])
        return ret['instance']

    def assign(self, query, data, user_id=None, assignment=None):
        ret =  self.client.put('engine/assign', {"query": query, "data": data, "userId": user_id, "assignment": assignment})
        if 'errors' in ret:
            raise Exception(ret['errors'])
        return ret['instance']

    def restart(self, query, data, user_id=None, options=None):
        if options is None:
            options = {}
        ret =  self.client.put('engine/restart', {"query": query, "data": data, "userId": user_id, "options": options})
        if 'errors' in ret:
            raise Exception(ret['errors'])
        return ret['instance']

    def throw_message(self, message_id, data=None, message_matching_key=None):
        if data is None:
            data = {}
        if message_matching_key is None:
            message_matching_key = {}
        ret =  self.client.post('engine/throwMessage', {"messageId": message_id, "data": data, "messageMatchingKey": message_matching_key})
        if 'errors' in ret:
            raise Exception(ret['errors'])
        return ret

    def throw_signal(self, signal_id, data=None, message_matching_key=None):
        if data is None:
            data = {}
        if message_matching_key is None:
            message_matching_key = {}
        ret =  self.client.post('engine/throwSignal', {"signalId": signal_id, "data": data, "messageMatchingKey": message_matching_key})
        if 'errors' in ret:
            raise Exception(ret['errors'])
        return ret

    def start_event(self, instance_id, start_node_id, data=None, user_id=None, options=None):
        if data is None:
            data = {}
        if options is None:
            options = {}
        ret =  self.client.put('engine/startEvent', {"instanceId": instance_id, "startNodeId": start_node_id, "data": data, "userName": user_id, "options": options})
        if 'errors' in ret:
            raise Exception(ret['errors'])
        return ret

    def get(self, query):
        ret =  self.client.get('engine/get', query)
        if 'errors' in ret:
            raise Exception(ret['errors'])
        return ret['instance']

    def status(self):
        ret =  self.client.get('engine/status', {})
        if 'errors' in ret:
            raise Exception(ret['errors'])
        return ret

class ClientDatastore:
    def __init__(self, client):
        self.client = client

    def find_items(self, query):
        res =  self.client.get('datastore/findItems', query)
        if 'errors' in res:
            raise Exception(res['errors'])
        return res['items']

    def find_instances(self, query, projection=None):
        if projection is None:
            projection = {}
        res =  self.client.get('datastore/findInstances', {"query": query, "projection": projection})
        if 'errors' in res:
            raise Exception(res['errors'])
        return res['instances']

    def delete_instances(self, query):
        return  self.client.delete('datastore/deleteInstances', query)

class ClientDefinitions:
    def __init__(self, client):
        self.client = client

    def import_definition(self, name, path_to_bpmn, path_to_svg=None):
        options = {
            'method': 'POST',
            'url': f'http://{self.client.host}:{self.client.port}/api/definitions/import/{name}',
            'headers': {
                'x-api-key': self.client.api_key
            }
        }
        res =  self.client.upload(name, path_to_bpmn, path_to_svg, options)
        self.check_errors(res)
        return res

    def list(self):
        res = self.client.get('definitions/list', [])
        if 'errors' in res:
            raise Exception(res['errors'])
        return res

    def delete(self, name):
        res =  self.client.post('definitions/delete/', {"name": name})
        if 'errors' in res:
            raise Exception(res['errors'])
        return res

    def rename(self, name, new_name):
        res =  self.client.post('definitions/rename/', {"name": name, "newName": new_name})
        if 'errors' in res:
            raise Exception(res['errors'])
        return res

    def load(self, name):
        res =  self.client.get(f'definitions/load/{name}', {"name": name})
        if 'errors' in res:
            raise Exception(res['errors'])
        return res

    def check_errors(self, res):
        if 'errors' in res:
            raise Exception(res['errors'])

