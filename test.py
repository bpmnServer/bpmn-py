#from example_package_RH import example

from bpmnClient import client

cl = client.Client('http://localhost:3000','12345')
#cl.model.list()
      
from src.bpmnClient.bpmn2 import BPMNClient2 as client2

b=client2('bpmn.omniworkflow.com',443,'12345')

print(b.model.list_models())
#res=b.data.find_instances({},'').print_instances(['name','id'])
#print('find instances',res.dump())


