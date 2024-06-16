# bpmn-py
Python implementation to connect to bpmnServer

To Install:

```os
pip install bpmnclient
```

To Run:
```python

# version 1: from bpmnClient import client as bpmn

from src.bpmnClient.bpmn2 import client2 as bpmn

b=BPMNClient2('localhost',3000,'12345')

print(b.model.list_models())
```
