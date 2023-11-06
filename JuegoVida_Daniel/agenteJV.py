from mesa import Agent

REGLAS = {("Alive", "Alive", "Alive"): "Alive", 
          ("Alive", "Alive", "Dead"): "Dead", 
          ("Alive", "Dead", "Alive"): "Alive", 
          ("Alive", "Dead", "Dead"): "Dead", 
          ("Dead", "Alive", "Alive"): "Dead", 
          ("Dead", "Alive", "Dead"): "Alive", 
          ("Dead", "Dead", "Alive"): "Dead", 
          ("Dead", "Dead", "Dead"): "Alive"}


class TreeCell(Agent):
    """
        A tree cell.
        
        Attributes:
            x, y: Grid coordinates
            condition: Can be "Fine", "On Fire", or "Burned Out"
            unique_id: (x,y) tuple.

            unique_id isn't strictly necessary here, but it's good practice to give one to each agent anyway.
    """

    def __init__(self, pos, model):
        """
        Create a new tree.

        Args:
            pos: The tree's coordinates on the grid.
            model: standard model reference for agent.
        """
        super().__init__(pos, model)
        self.pos = pos
        self.condition = "Dead"
        self._next_condition = None
        self.model = model

    #def step(self):
        """
        If the tree is on fire, spread it to fine trees nearby.
        """
        # if self.condition == "Alive":
        #     for neighbor in self.model.grid.iter_neighbors(self.pos, True):
        #         if neighbor.condition == "Dead":
        #             neighbor._next_condition = "Alive"
        #     self._next_condition = "Alive"
        
        lista = []
        #if self.condition == "Alive":
        for neighbor in self.model.grid.iter_neighbors(self.pos, True):
            if neighbor.pos[1] == self.pos[1] + 1:
                lista.append(neighbor.condition)

        tupla = tuple(lista)
        if tupla in REGLAS:
            self.condition = REGLAS[tupla]


    
    def advance(self):
        """
        Advance the model by one step.
        """
        if self._next_condition is not None:
            self.condition = self._next_condition
