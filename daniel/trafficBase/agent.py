from mesa import Agent
import random
import heapq
from queue import PriorityQueue


class Car(Agent):
    """
    Agent that moves randomly.
    Attributes:
        unique_id: Agent's ID 
        direction: Randomly chosen direction chosen from one of eight directions
    """
    def __init__(self, unique_id, model, destination_pos):
        """
        Creates a new random agent.
        Args:
            unique_id: The agent's ID
            model: Model reference for the agent
        """
        super().__init__(unique_id, model)
        self.direction = 4
        self.steps_taken = 0
        self.type = "car"
        self.destination_pos = destination_pos
        self.path = None

    def move(self):
        """
        Mueve el agente en la dirección indicada por el agente en la misma celda.
        """
        x, y = self.pos  # Obtener la posición actual del agente

        # Obtener todos los agentes en la misma celda que el agente Car
        agents_in_same_cell = self.model.grid.get_cell_list_contents([(x, y)])

        # Obtener la dirección del primer agente en la misma celda (puede ser Road, Traffic_Light u otro)
        if agents_in_same_cell:
            direction_below = getattr(agents_in_same_cell[0], "direction", None)
        else:
            direction_below = None

        
        traffic_light = next((agent for agent in agents_in_same_cell if isinstance(agent, Traffic_Light)), None)
        if traffic_light and not traffic_light.state:  # If there is a red traffic light, do not move
            return
        

        # Mapa de direcciones a desplazamientos en la cuadrícula
        direction_mapping = {
            "Up": (0, 1),
            "Down": (0, -1),
            "Left": (-1, 0),
            "Right": (1, 0),
        }

        # Obtener el desplazamiento correspondiente a la dirección en la misma celda que el agente Car
        displacement = direction_mapping.get(direction_below, (0, 0))
        
        if direction_below == "Up-Left":
            displacement = random.choice([(0, 1), (-1, 0)])
            new_pos = ((x + displacement[0]) % self.model.grid.width, (y + displacement[1]) % self.model.grid.height)
            
        if direction_below == "Up-Right":
            displacement = random.choice([(0, 1), (1, 0)])
            new_pos = ((x + displacement[0]) % self.model.grid.width, (y + displacement[1]) % self.model.grid.height)
            
        if direction_below == "Down-Right":
            displacement = random.choice([(0, -1), (1, 0)])
            new_pos = ((x + displacement[0]) % self.model.grid.width, (y + displacement[1]) % self.model.grid.height)
            
        if direction_below == "Down-Left":
            displacement = random.choice([(0, -1), (-1, 0)])
            new_pos = ((x + displacement[0]) % self.model.grid.width, (y + displacement[1]) % self.model.grid.height)
            

        # Calcular la nueva posición sumando el desplazamiento
        new_pos = ((x + displacement[0]) % self.model.grid.width, (y + displacement[1]) % self.model.grid.height)

        if any(isinstance(agent, Car) for agent in self.model.grid.get_cell_list_contents([new_pos])):
            print("Atorado")  # Puedes poner aquí el código que deseas ejecutar cuando la nueva posición está ocupada por otro agente Car
        else:
            # Mover el agente a la nueva posición en la cuadrícula
            self.model.grid.move_agent(self, new_pos)

        # # Mover el agente a la nueva posición en la cuadrícula
        # self.model.grid.move_agent(self, new_pos)

        # # Mover el agente a la nueva posición en la cuadrícula
        # self.model.grid.move_agent(self, new_pos)
        if self.path is not None and len(self.path) > 0:
            new_pos = self.path.pop(0)
            self.model.grid.move_agent(self, new_pos)
    
    
    def calculate_path(self):
        start = self.pos
        #goal = self.destination_pos
        goal = self.find_goal_on_map()
        #destinations = [agent for agent in self.model.schedule.agents if isinstance(agent, Destination)]
        #if destinations:
        # Implementación del algoritmo A*
        def heuristic(a, b):
            return abs(a[0] - b[0]) + abs(a[1] - b[1])
            
        def a_star_search(graph, start, goal):
            frontier = PriorityQueue()
            frontier.put((0, start))
            came_from = {}
            cost_so_far = {}
            came_from[start] = None
            cost_so_far[start] = 0

            while not frontier.empty():
                current = frontier.get()[1]

                if current == goal:
                    break

                for next in graph.neighbors(current):
                    new_cost = cost_so_far[current] + graph.cost(current, next)
                    if next not in cost_so_far or new_cost < cost_so_far[next]:
                        cost_so_far[next] = new_cost
                        priority = new_cost + heuristic(goal, next)
                        frontier.put((priority, next))
                        came_from[next] = current

            return reconstruct_path(came_from, start, goal)
        self.path = a_star_search(self.model.grid, start, goal)
        def find_goal_on_map(self):
            # Busca el destino "F" en el mapa y devuelve su posición
            for y, row in enumerate(self.model.mapa):
                for x, cell in enumerate(row):
                    if cell == "F":
                        return (x, y)
            return None  # Devuelve None si no se encuentra el destino



        #self.path = a_star_search(self.model.grid, start, goal)

    def step(self):
        """ 
        Determines the new direction it will take, and then moves
        """
        if self.path is None or len(self.path) == 0:
            self.calculate_path()
        self.move()
        

class Traffic_Light(Agent):
    """
    Traffic light. Where the traffic lights are in the grid.
    """
    def __init__(self, unique_id, model, state = False, direction= "Left", time_to_change=5):
        super().__init__(unique_id, model)
        """
        Creates a new Traffic light.
        Args:
            unique_id: The agent's ID
            model: Model reference for the agent
            state: Whether the traffic light is green or red
            timeToChange: After how many step should the traffic light change color 
        """
        self.state = state
        self.direction = direction
        self.time_to_change= time_to_change

    def step(self):
        """ 
        To change the state (green or red) of the traffic light every time_to_change steps.
        """
        if self.model.schedule.steps % self.time_to_change == 0:
            self.state = not self.state  # Cambiar el estado del semáforo cada time_to_change pasos

class Destination(Agent):
    """
    Destination agent. Where each car should go.
    """
    def __init__(self, unique_id, model): 
        super().__init__(unique_id, model)
        self.type = "destination"

    def step(self):
        # Obtener todos los agentes en la misma celda que la entidad Destination
        agents_in_same_cell = self.model.grid.get_cell_list_contents([self.pos])

        # Verificar si hay algún agente de tipo Car en la misma celda
        car_agents = [agent for agent in agents_in_same_cell if isinstance(agent, Car)]

        # Eliminar los agentes de tipo Car
        for car_agent in car_agents:
            self.model.grid.remove_agent(car_agent)
            self.model.schedule.remove(car_agent)

class Obstacle(Agent):
    """
    Obstacle agent. Just to add obstacles to the grid.
    """
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        pass

class Road(Agent):
    """
    Road agent. Determines where the cars can move, and in which direction.
    """
    def __init__(self, unique_id, model, direction= "Left"):
        """
        Creates a new road.
        Args:
            unique_id: The agent's ID
            model: Model reference for the agent
            direction: Direction where the cars can move
        """
        super().__init__(unique_id, model)
        self.direction = direction

    def step(self):
        pass