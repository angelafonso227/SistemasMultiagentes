from mesa import Agent

class RandomAgent(Agent):
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
        self.Life = 100
        self.initial_position = (0, 0)  # Guardar la posición inicial
        self.trash_collected = 0  # Contador de basura recogida
        self.collected_cells = set()  # Conjunto de celdas ya procesadas

    def move(self):
        """ 
        Determines if the agent can move in the direction that was chosen
        """
        # Si la vida es 21 o menos, regresar al punto inicial
        if self.Life <= 21:
            self.return_to_initial_position()
            return

        # Obtener las celdas vecinas (posiciones) alrededor del agente
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=False,
            radius=1
        )

        # Filtrar las celdas que no contienen ObstacleAgent
        possible_steps = [p for p in possible_steps if not any(isinstance(agent, ObstacleAgent) for agent in self.model.grid.get_cell_list_contents(p))]

        # Buscar celdas con TrashAgent que no han sido procesadas
        trash_cells = [p for p in possible_steps if any(isinstance(agent, TrashAgent) for agent in self.model.grid.get_cell_list_contents(p)) and p not in self.collected_cells]

        # Elegir aleatoriamente la próxima celda
        if trash_cells:
            # Si hay TrashAgent en alguna celda vecina no procesada, elegir una de ellas aleatoriamente
            next_move = self.random.choice(trash_cells)
            
            # Imprimir mensaje al remover basura y actualizar el contador y el conjunto de celdas procesadas
            self.trash_collected += 1
            self.collected_cells.add(next_move)
            print(f"Agent {self.unique_id}: Removed trash {self.trash_collected} at {next_move}")

        else:
            # Si no hay TrashAgent en las celdas vecinas, elegir aleatoriamente entre todas las celdas disponibles
            next_move = self.random.choice(possible_steps)

        # Moverse a la nueva celda
        if self.random.random() < 0.9:
            # Verificar si hay un TrashAgent en la nueva celda
            trash_agents_in_next_cell = [agent for agent in self.model.grid.get_cell_list_contents(next_move) if isinstance(agent, TrashAgent)]

            # Si hay al menos un TrashAgent en la nueva celda, eliminarlo
            if trash_agents_in_next_cell:
                trash_agent_to_remove = self.random.choice(trash_agents_in_next_cell)
                self.model.grid.remove_agent(trash_agent_to_remove)

            # Moverse a la nueva celda después de verificar y eliminar TrashAgent
            self.model.grid.move_agent(self, next_move)
            self.steps_taken += 1
            self.Life -= 1

    def return_to_initial_position(self):
        """
        Move back to the initial position (1, 1) step by step.
        """
        current_position = self.pos
        initial_position = self.initial_position

        # Calcular la dirección para llegar al punto inicial
        dx = initial_position[0] - current_position[0]
        dy = initial_position[1] - current_position[1]

        # Determinar la próxima posición para moverse un paso más cerca del punto inicial
        next_move = (current_position[0] + dx, current_position[1] + dy)

        # Realizar el movimiento
        self.model.grid.move_agent(self, next_move)
        self.steps_taken += 1

    def step(self):
        """ 
        Determines the new direction it will take, and then moves
        """
        self.move()

class ObstacleAgent(Agent):
    """
    Obstacle agent. Just to add obstacles to the grid.
    """
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        pass  
    
class TrashAgent(Agent):
    """
    Trash agent. Just to add obstacles to the grid.
    """
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        pass  
    
class BatteryAgent(Agent):
    """
    Trash agent. Just to add obstacles to the grid.
    """
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        pass
