import heapq

# Definition of a position in the maze
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

# Node in the search space
class Node:
    def __init__(self, pt, f, g, h):
        self.pt = pt
        self.f = f
        self.g = g
        self.h = h

    def __lt__(self, other):
        return self.f > other.f

# Check if a point is inside the maze
def is_valid(x, y, N):
    return 0 <= x < N and 0 <= y < N

# Check if a point is unblocked
def is_unblocked(maze, x, y):
    return maze[x][y] == 1

# Heuristic: Manhattan Distance from the start point to the end point
def calculate_h_value(x, y, dest):
    return abs(x - dest.x) + abs(y - dest.y)

# Implementation of the A* algorithm
def a_star_search(maze, src, dest, N):
    if not is_valid(src.x, src.y, N) or not is_valid(dest.x, dest.y, N) or not is_unblocked(maze, src.x, src.y) or not is_unblocked(maze, dest.x, dest.y):
        return "No hay camino posible."

    # Matrix to track visited nodes
    closed_list = [[False for _ in range(N)] for _ in range(N)]

    # Initialize all f, g, h values with infinity
    all_nodes = [[Node(Point(-1, -1), float('inf'), float('inf'), float('inf')) for _ in range(N)] for _ in range(N)]

    # Initialize the start node
    i, j = src.x, src.y
    all_nodes[i][j] = Node(Point(i, j), 0, 0, 0)

    # Create a priority queue (min heap)
    open_list = [all_nodes[i][j]]

    while open_list:
        # Get the node with the minimum f value
        current_node = heapq.heappop(open_list)

        i, j = current_node.pt.x, current_node.pt.y

        # Mark the current node as visited
        closed_list[i][j] = True

        # Generate possible movements
        row = [-1, 0, 0, 1]
        col = [0, -1, 1, 0]

        for k in range(4):
            new_row = i + row[k]
            new_col = j + col[k]

            # Check if the new point is valid
            if is_valid(new_row, new_col, N):
                # Check if the destination is reached
                if new_row == dest.x and new_col == dest.y:
                    # Build the path from the destination to the origin
                    path = ""
                    while not (i == src.x and j == src.y):
                        temp = i
                        temp2 = j
                        i = all_nodes[temp][temp2].pt.x
                        j = all_nodes[temp][temp2].pt.y
                        if i == temp - 1 and j == temp2:
                            path = 'D' + path
                        elif i == temp + 1 and j == temp2:
                            path = 'U' + path
                        elif i == temp and j == temp2 - 1:
                            path = 'R' + path
                        elif i == temp and j == temp2 + 1:
                            path = 'L' + path
                    return path

                # Check if the new point is valid and not blocked or visited
                if not closed_list[new_row][new_col] and is_unblocked(maze, new_row, new_col):
                    # Update g, h, and f values if necessary
                    g_new = all_nodes[i][j].g + 1
                    h_new = calculate_h_value(new_row, new_col, dest)
                    f_new = g_new + h_new

                    # If the new path is better, update the node information
                    if all_nodes[new_row][new_col].f == float('inf') or all_nodes[new_row][new_col].f > f_new:
                        heapq.heappush(open_list, Node(Point(new_row, new_col), f_new, g_new, h_new))
                        all_nodes[new_row][new_col] = Node(Point(i, j), f_new, g_new, h_new)

    # No path found
    return "No hay camino posible."

def main():
    N = 4

    # Create a dynamic matrix to represent the maze
    maze = [[0 for _ in range(N)] for _ in range(N)]

    # Initialize the maze matrix
    maze[0][0] = 1
    maze[0][1] = 0
    maze[0][2] = 0
    maze[0][3] = 0
    maze[1][0] = 1
    maze[1][1] = 1
    maze[1][2] = 0
    maze[1][3] = 1
    maze[2][0] = 1
    maze[2][1] = 1
    maze[2][2] = 0
    maze[2][3] = 0
    maze[3][0] = 0
    maze[3][1] = 1
    maze[3][2] = 1
    maze[3][3] = 1

    src = Point(0, 0)
    dest = Point(N - 1, N - 1)

    # Call the A* function and display the result
    result = a_star_search(maze, src, dest, N)
    print("Resultado:", result)

if __name__ == "__main__":
    main()
