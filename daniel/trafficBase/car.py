from mesa import Agent, Model
from mesa.time import BaseScheduler
import random
from trafficLight import Traffic_Light

class Car(Agent):
    """
    Agent that moves randomly.
    Attributes:
        unique_id: Agent's ID 
        direction: Randomly chosen direction chosen from one of eight directions
    """
    def _init_(self, unique_id, model, direction):
        """
        Creates a new random agent.
        Args:
            unique_id: The agent's ID
            model: Model reference for the agent
        """
        super()._init_(unique_id, model)
        self.direction = direction
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
        if Traffic_Light == True:
            if direction_below == "Up":
                direction_below = "Down"
            elif direction_below == "Down":
                direction_below = "Up"
            elif direction_below == "Left":
                direction_below = "Right"
            elif direction_below == "Right":
                direction_below = "Left"
            elif direction_below == "Up-Right":
                direction_below = "Down-Left"
            elif direction_below == "Up-Left":
                direction_below = "Down-Right"
            elif direction_below == "Down-Right":
                direction_below = "Up-Left"
            elif direction_below == "Down-Left":
                direction_below = "Up-Right"
            else:
                direction_below = None

        # Mapa de direcciones a desplazamientos en la cuadrícula
        direction_mapping = {
            "Up": (0, 1),
            "Down": (0, -1),
            "Left": (-1, 0),
            "Right": (1, 0),
            "Up-Right" : [(0, 1), (1, 0)],
            "Up-Left" : [(0, 1), (-1, 0)],
            "Down-Right" : [(0, -1), (1, 0)],
            "Down-Left" : [(0, -1), (-1, 0)],
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
        
