from mesa import Agent

REGLAS = {("Fine", "Fine", "Fine"): "Fine", ("Fine", "Fine", "Burned Out"): "Burned Out", ("Fine", "Burned Out", "Fine"): "Fine", ("Fine", "Burned Out", "Burned Out"): "Burned Out", ("Burned Out", "Fine", "Fine"): "Burned Out", ("Burned Out", "Fine", "Burned Out"): "Fine", ("Burned Out", "Burned Out", "Fine"): "Burned Out", ("Burned Out", "Burned Out", "Burned Out"): "Fine"}

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
        self.condition = "Fine"
        self._next_condition = None

    def step(self):
        
        lista=[]
        for neighbor in self.model.grid.iter_neighbors(self.pos, True):
            if self.pos[1] == 49 and (neighbor.pos[1] == self.pos[1] + 1):
                neighbor.pos[1]=self.pos[1]-49
                lista.append(neighbor.consition)
            elif neighbor.pos[1] == self.pos[1] + 1:
                    lista.append(neighbor.condition)
        
        tupla= tuple(lista)
        if tupla in REGLAS:
            self.condition = REGLAS[tupla]

    
    def advance(self):
        """
        Advance the model by one step.
        """
        if self._next_condition is not None:
            self.condition = self._next_condition