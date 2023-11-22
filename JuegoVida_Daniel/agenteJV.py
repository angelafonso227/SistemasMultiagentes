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
            condition: Can be "Alive", "On Fire", or "Dead"
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

    # def step(self):
        
    #     lista=[]
    #     for neighbor in self.model.grid.iter_neighbors(self.pos, True):
    #         if neighbor.pos[1] == self.pos[1] + 1:
    #             lista.append(neighbor.condition)
    #             tupla= tuple(lista)
    #             if tupla in REGLAS:
    #                 self.condition = REGLAS[tupla]



    def step(self):
    # Recolectar las condiciones de los vecinos encima de la celda actual
        lista = []
        for neighbor in self.model.grid.iter_neighbors(self.pos, True):
            if neighbor.pos[1] == self.pos[1] + 1:  # Vecinos directamente encima (arriba)
                lista.append(neighbor.condition)
        
        # Construir la tupla una vez se han recolectado todas las condiciones de los vecinos
        tupla = tuple(lista)
        
        # Verificar si la tupla está en las reglas y actualizar la condición
        if tupla in REGLAS:
            self.condition = REGLAS[tupla]
    
    def advance(self):
        """
        Advance the model by one step.
        """
        if self._next_condition is not None:
            self.condition = self._next_condition