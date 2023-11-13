from random import randint
from mesa import Agent

class Roomba(Agent):

    def _init_(self, unique_id, model):
        super()._init_(unique_id, model)
        self.direction = 4
        self.status = "Roomba"
    
    def move(self):
        randomRange = 8
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=False
        )
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)
        
    def clean_agent(self):
        trash = self.model.grid.get_cell_list_contents([self.pos])
        for obj in trash:
            if(obj.status == 'Dirty'):
                obj.status = 'Clean'
                return 1

        
    
    def step(self):
        if(self.clean_agent()!=1):
            self.move()

class Tile(Agent):
    """ Modelo para un Obstaculo """
    def _init_(self, unique_id, model):
        super()._init_(unique_id, model)
        self.status = "Dirty"

    def step(self):
        pass