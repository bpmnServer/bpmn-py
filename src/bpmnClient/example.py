
from client import *

             

#cl.model.list();


#print(cl.status())

#cl.data.findInstnaces({"name":'Buy Used Car'})

cl.engine.start('Buy Used Car',{}).listItems().dump()
#Report.dump(res)
#cl.listItems(res)
