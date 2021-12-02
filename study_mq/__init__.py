import sys
import os
from pprint import pprint

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
pprint(sys.path)