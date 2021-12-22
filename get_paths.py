from sysconfig import get_paths

import os
import json
d=get_paths()
d['libs']=os.path.join(os.environ['pythonLocation'],'libs')
for k,v in d.items():
  print('::set-output '+k+'=paths::'+v)
