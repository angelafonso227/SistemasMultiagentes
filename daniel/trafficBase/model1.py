from mesa import Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from agent import *
import json

class CityModel(Model):
    """ 
        Creates a model based on a city map.

        Args:
            N: Number of agents in the simulation
    """
    def __init__(self, N):

        # Load the map dictionary. The dictionary maps the characters in the map file to the corresponding agent.
        dataDictionary = json.load(open("city_files/mapDictionary.json"))

        self.num_agents = N
        self.traffic_lights = []

        # Load the map file. The map file is a text file where each character represents an agent.
        with open('city_files/2022_base.txt') as baseFile:
            lines = baseFile.readlines()
            self.width = len(lines[0])-1
            self.height = len(lines)

            self.grid = MultiGrid(self.width, self.height, torus=False) 
            self.schedule = RandomActivation(self)
            self.mapa = baseFile
            
            # for i in range(self.num_agents):
            #     # a = Car(i + 1000, self)
            #     a = Car(i + 1000, self, destination=self.grid.coord_to_agent((10, 10)))
            #     self.schedule.add(a)
            #     pos = (0, 0)
            #     self.grid.place_agent(a, pos)

            # Goes through each character in the map file and creates the corresponding agent.
            for r, row in enumerate(lines):
                for c, col in enumerate(row):
                    if col in ["v", "^", ">", "<", "1", "2", "3", "4"]:
                        agent = Road(f"r_{r*self.width+c}", self, dataDictionary[col])
                        self.grid.place_agent(agent, (c, self.height - r - 1))

                    elif col in ["R", "r", "L", "l", "U", "u", "D", "d"]:
                        change_frequency = 15 if col in ["R", "L", "U", "D"] else 7
                        agent = Traffic_Light(f"tl_{r*self.width+c}", self, False if col in ["R", "L", "U", "D"] else True, dataDictionary[col], change_frequency)
                        self.grid.place_agent(agent, (c, self.height - r - 1))
                        self.schedule.add(agent)
                        self.traffic_lights.append(agent)

                    elif col == "#":
                        agent = Obstacle(f"ob_{r*self.width+c}", self)
                        self.grid.place_agent(agent, (c, self.height - r - 1))

                    elif col == "F":
                        agent = Destination(f"d_{r*self.width+c}", self)
                        self.grid.place_agent(agent, (c, self.height - r - 1))
        
        self.running = True

    def add_car(self):
        # new_agent = Car(self.num_agents + 1000, self)
        # self.num_agents += 1
        # #pos = (0, 0)
        # corner_options = [(0, 0), (0, self.grid.height-1), (self.grid.width-1, 0), (self.grid.width-1, self.grid.height-1)]
        # pos = random.choice(corner_options)
        # self.grid.place_agent(new_agent, pos)
        # self.schedule.add(new_agent)
        for _ in range(4):
            destination_pos = (10,10)
            new_agent = Car(self.num_agents + 1000, self, destination_pos)
            self.num_agents += 1

            # Coordinates of the four corners
            corners = [(0, 0), (0, self.grid.height-1), (self.grid.width-1, 0), (self.grid.width-1, self.grid.height-1)]

            # Use the current corner for the new agent
            pos = random.choice(corners)
            while self.grid.is_cell_empty(pos):
                pos = (random.randint(0, self.grid.width-1), random.randint(0, self.grid.height-1))
            # while self.grid.is_cell_empty(pos) or any(isinstance(agent, Car) for agent in self.grid.get_cell_list_contents(pos)):
            #     pos = (random.randint(0, self.grid.width-1), random.randint(0, self.grid.height-1))

            self.grid.place_agent(new_agent, pos)
            self.schedule.add(new_agent)

    def add_destination(self):
        new_destination = Destination(self.num_agents + 2000, self)
        self.num_agents += 1

        pos = (random.randint(0, self.grid.width - 1), random.randint(0, self.grid.height - 1))
        while not self.grid.is_cell_empty(pos):
            pos = (random.randint(0, self.grid.width - 1), random.randint(0, self.grid.height - 1))

        self.grid.place_agent(new_destination, pos)


    def step(self):
        '''Advance the model by one step.'''
        # Añade un nuevo carro cada 4 pasos
        if self.schedule.steps % 10 == 0:
            if self.num_agents <= 10:
                self.add_car()
            else:
                pass

        self.schedule.step()
