from mesa.visualization.modules import CanvasGrid, ChartModule, PieChartModule      
from mesa.visualization.ModularVisualization import ModularServer                 
#from mesa.visualization.UserParam import UserSettableParameter
# from mesa.visualization.UserParam import UserSettableParameter
from mesa.visualization.UserParam import UserSettableParameter
                   
from modelo import RoombaModel
from agentes import Roomba, Tile

colors = {"Dirty": "brown", "Clean": "grey"}
colorsPieChart = {"Dirty": "brown", "Clean": "grey", "Empty": "#a2ff00"}

def portrayal(agent):
    if agent is None:
        return
    
    portrayal = {
        "Shape": "circle",
        "Filled": "true"
    }

    if (isinstance(agent,Roomba)):
        portrayal["Color"] = "red"
        portrayal["Layer"] = 1
        portrayal["r"] = 0.5
    
    if (isinstance(agent, Tile)):
        portrayal["Color"] = colors[agent.status]
        portrayal["Layer"] = 0
        portrayal["r"] = 1

    return portrayal

dirtyChart = ChartModule(
    [
        {"Label": label, "Color": color} for (label, color) in colors.items()
    ]
)

pieChart = PieChartModule(
    [{"Label": label, "Color": color, "Outline": "black"} for (label, color) in colorsPieChart.items()]
)

roombas = UserSettableParameter("slider", "Numero de Roombas", 10, 1, 225, 1)
width =  UserSettableParameter("slider", "Ancho del Grid", 10, 5, 15, 1)
height = UserSettableParameter("slider", "Alto del Grid", 10, 5, 15, 1)
numObs = UserSettableParameter("slider", "Porcentaje de Area Sucia", 0.3, 0, 0.9, 0.05)
maxSteps = UserSettableParameter("number", "Pasos Maximos", 1000, 1, 2000, 1)

modelParam = {
    "N": roombas,
    "width": width,
    "height": height,
    "numObs": numObs,
    "maxSteps": maxSteps
}

grid = CanvasGrid(portrayal, 15, 15, 500, 500)

server = ModularServer(RoombaModel, [grid, dirtyChart, pieChart], "Roomba_Activity", modelParam)
server.launch()