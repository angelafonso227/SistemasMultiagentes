from mesa import Agent
import random

class Car(Agent):
    """
    Agent that moves randomly.
    Attributes:
        unique_id: Agent's ID 
        direction: Randomly chosen direction chosen from one of eight directions
    """
    def __init__(self, unique_id, model):
        """
        Creates a new random agent.
        Args:
            unique_id: The agent's ID
            model: Model reference for the agent
        """
        super().__init__(unique_id, model)
        self.direction = 4
        self.steps_taken = 0

    def move(self):
        """
        Mueve el agente en la dirección indicada por el agente en la misma celda.
        """
        x, y = self.pos  # Obtener la posición actual del agente

        # Obtener todos los agentes en la misma celda que el agente Car
        agents_in_same_cell = self.model.grid.get_cell_list_contents([(x, y)])

        # Obtener la dirección del primer agente en la misma celda (puede ser Road, Traffic_Light u otro)
        direction_below = getattr(agents_in_same_cell[0], "direction", None) if agents_in_same_cell else None

        # Mapa de direcciones a desplazamientos en la cuadrícula
        direction_mapping = {
            "Up": (0, 1),
            "Down": (0, -1),
            "Left": (-1, 0),
            "Right": (1, 0),
        }

        # Obtener el desplazamiento correspondiente a la dirección en la misma celda que el agente Car
        displacement = direction_mapping.get(direction_below, (0, 0))

        # Calcular la nueva posición sumando el desplazamiento
        new_pos = ((x + displacement[0]) % self.model.grid.width, (y + displacement[1]) % self.model.grid.height)

        # Mover el agente a la nueva posición en la cuadrícula
        self.model.grid.move_agent(self, new_pos)

    def step(self):
        """ 
        Determines the new direction it will take, and then moves
        """
        self.move()

class Traffic_Light(Agent):
    """
    Traffic light. Where the traffic lights are in the grid.
    """
    def __init__(self, unique_id, model, state = False, timeToChange = 10):
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
        self.timeToChange = timeToChange

    def step(self):
        """ 
        To change the state (green or red) of the traffic light in case you consider the time to change of each traffic light.
        """
        if self.model.schedule.steps % self.timeToChange == 0:
            self.state = not self.state

class Destination(Agent):
    """
    Destination agent. Where each car should go.
    """
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        pass

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
