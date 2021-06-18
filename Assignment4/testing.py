import numpy as np

from domain.Map import Map
from domain.Sensor import Sensor

mapM = Map()
mapM.loadMap('test1.map')
sensor = Sensor(mapM, 0, 5)

list = [1,2,3,4,5,6]
list.reverse()
print(list)

