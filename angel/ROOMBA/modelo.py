from mesa.time import RandomActivation          
from mesa.space import MultiGrid                
from mesa.datacollection import DataCollector   
from mesa import Model                          
from agentes import Roomba, Tile  

class RoombaModel(Model):
    stepCount = 0
    def _init_(self, N, width, height,  numObs, maxSteps):

        self.numRoombas = N
        self.grid = MultiGrid(width, height, torus= False)
        self.schedule = RandomActivation(self)
        self.running = True
        self.steps = 0
        self.maxSteps = maxSteps

        self.datacollector = DataCollector(
            {
                "Dirty": lambda m: self.count_type(m, "Dirty"),
                "Clean": lambda m: self.count_type(m, "Clean"),
                "Empty": lambda m: self.count_empty(m)
            }
        )

        i = 0
        for (contents, x, y) in self.grid.coord_iter():
            if(self.random.random() <= numObs):
                a = Tile(i, self)
                self.schedule.add(a)
                x = self.random.randrange(self.grid.width)
                y = self.random.randrange(self.grid.height)
                while (not self.grid.is_cell_empty((x,y))):
                    x = self.random.randrange(self.grid.width)
                    y = self.random.randrange(self.grid.height)
                self.grid.place_agent(a, (x, y))
            i+=1

        for i in range(self.numRoombas):
            a = Roomba(i+1000, self)
            self.schedule.add(a)
            x = 1
            y =1
            self.grid.place_agent(a, (x, y))
        
        self.datacollector.collect(self)

    def step(self):

        self.steps+=1
        if self.steps == self.maxSteps:
            self.running = False
        self.schedule.step()

        self.datacollector.collect(self)

        if self.count_type(self, 'Dirty') == 0:
            self.running = False

    @staticmethod
    def count_type(model, status):
        count = 0
        for agent in model.schedule.agents:
            if agent.status == status:
                count += 1
        return count

    @staticmethod
    def count_empty(model):
        count = 0
        for (contents, x, y) in model.grid.coord_iter():
            if(model.grid.is_cell_empty((x, y))):
                count+=1
        return count