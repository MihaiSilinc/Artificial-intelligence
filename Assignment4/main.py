from random import randint

from Console import Console
from Repo import Repo
from Service import Service
from domain.Drone import Drone
from domain.Map import Map


def main():
    # we create the map
    m = Map()
    # m.randomMap()
    # m.saveMap("test2.map")
    m.loadMap("test1.map")

    # we position the drone somewhere in the area
    x = randint(0, 19)
    y = randint(0, 19)

    # create drone
    d = Drone(x, y)

    repo = Repo(d, m)
    service = Service(repo)
    console = Console(service)

    console.run()


main()

