
from bpmn2 import *

#cl=BPMNClient2('localhost','3000','12345')             
cl=BPMNClient2('bpmn.omniworkflow.com','443','12345')             

cl.model.listModels().dump()

print(list)
#cl.model.list();


#print(cl.status())

#cl.data.findInstnaces({"name":'Buy Used Car'})

#cl.engine.start('Buy Used Car',{}).listItems().dump()
#Report.dump(res)
#cl.listItems(res)
