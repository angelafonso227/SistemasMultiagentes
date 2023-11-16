from model import RandomModel, ObstacleAgent, TrashAgent, BatteryAgent
from mesa.visualization import CanvasGrid, BarChartModule
from mesa.visualization import ModularServer

def agent_portrayal(agent):
    if agent is None: return
    
    portrayal = {"Shape": "circle",
                 "Filled": "true",
                 "Layer": 1,
                 "Color": "red",
                 "r": 0.5}

    if (isinstance(agent, ObstacleAgent)):
        portrayal["Color"] = "grey"
        portrayal["Layer"] = 1
        portrayal["r"] = 0.7
        
    if (isinstance(agent, TrashAgent)):
        portrayal["Color"] = "black"
        portrayal["Layer"] = 1
        portrayal["r"] = 0.3
        
    if (isinstance(agent, BatteryAgent)):
        portrayal["Color"] = "green"
        portrayal["Layer"] = 0
        portrayal["r"] = 1


    return portrayal

model_params = {"N":1, "width":15, "height":15}

grid = CanvasGrid(agent_portrayal, 15, 15, 500, 500)

bar_chart = BarChartModule(
    [{"Label":"Steps", "Color":"#AA0000"}], 
    scope="agent", sorting="ascending", sort_by="Steps")

server = ModularServer(RandomModel, [grid, bar_chart], "Random Agents", model_params)
                       
server.port = 8521 # The default
server.launch()