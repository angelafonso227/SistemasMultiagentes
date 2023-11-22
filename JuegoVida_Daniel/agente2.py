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
        self.condition = "Alive"
        self._next_condition = None


        def step(self):
            # if self.pos[1] == 49:
            #     return
            
            # Recolectar los estados de los vecinos superiores
            lista = []
            for neighbor in self.model.grid.iter_neighbors(self.pos, True):
                if neighbor.pos[1] == self.pos[1] + 1 and abs(neighbor.pos[0] - self.pos[0]) == 1:
                    lista.append(neighbor.condition)
            
            # Definir las reglas de transición de estados
            tupla = tuple(lista)
            if tupla in REGLAS:
                self._next_condition = REGLAS[tupla]#REGLAS.get(tupla, "Alive")
            
            print(f"Next condition for cell at {self.pos[0]}, {self.pos[1]}: {self._next_condition}")

    
    def advance(self):
        """
        Advance the model by one step.
        """
        if self._next_condition is not None:
            self.condition = self._next_condition