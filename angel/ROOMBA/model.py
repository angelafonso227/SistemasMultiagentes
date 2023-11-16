from mesa import Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
from agent import RandomAgent, ObstacleAgent, TrashAgent, BatteryAgent

class RandomModel(Model):
    """ 
    Creates a new model with random agents.
    Args:
        N: Number of agents in the simulation
        height, width: The size of the grid to model
    """
    def __init__(self, N, width, height):
        self.num_agents = N
        # Multigrid is a special type of grid where each cell can contain multiple agents.
        self.grid = MultiGrid(width, height, torus=False) 

        # RandomActivation is a scheduler that activates each agent once per step, in random order.
        self.schedule = RandomActivation(self)
        
        self.running = True 

        self.datacollector = DataCollector( 
            agent_reporters={"Steps": lambda a: a.steps_taken if isinstance(a, RandomAgent) else 0})


        
        # Function to generate random positions
        pos_gen = lambda w, h: (self.random.randrange(w), self.random.randrange(h))

        # Add the agent to a random empty grid cell
        for i in range(self.num_agents):
            a = RandomAgent(i + 1000, self) 
            self.schedule.add(a)
            pos = pos_gen(1,1)
            self.grid.place_agent(a, pos)
            
            
        # Add obstacles to the grid at random positions
        num_obstacles = 20  # You can adjust the number of obstacles as needed
        for _ in range(num_obstacles):
            pos = self.random_position()
            while not self.grid.is_cell_empty(pos):
                pos = self.random_position()
            obs = ObstacleAgent(pos, self)
            self.grid.place_agent(obs, pos)
            
        num_trash = 40  # You can adjust the number of obstacles as needed
        for _ in range(num_trash):
            pos = self.random_position()
            while not self.grid.is_cell_empty(pos):
                pos = self.random_position()
            tra = TrashAgent(pos, self)
            self.grid.place_agent(tra, pos)
            
        num_bat = 1  # You can adjust the number of obstacles as needed
        for _ in range(num_bat):
            pos = pos_gen(1,1)
            bat = BatteryAgent(pos, self)
            self.grid.place_agent(bat, pos)        
        
        
        self.datacollector.collect(self)

    def random_position(self):
        x = self.random.randint(0, self.grid.width - 1)
        y = self.random.randint(0, self.grid.height - 1)
        return x, y

    def step(self):
        """Advance the model by one step."""
        self.schedule.step()
        self.datacollector.collect(self)
