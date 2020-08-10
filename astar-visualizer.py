'''

Noah Park - A* pathfinding visualizer with major credit to 'Tech With Tim', as his explanation of the
algorithm and how to use pygame and such was phenomenal.

This was a super interesting way to delve into the A* algorithm and how it works.
I quite enjoyed working on this!

'''

# Need to import pygame for the 'gui' and priority queue for the A* algorithm
import pygame
from queue import PriorityQueue


# Setting up the screen
SCREEN_SIZE = 800
WINDOW = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
pygame.display.set_caption("A* Pathfinding Visualizer")


# Color variables
OPEN = (255, 255, 255)         # Open space - white
VISITED = (255, 0, 0)          # Visited - red
AVAILABLE = (0, 255, 0)        # Available - green
PATH = (255, 255, 0)           # Shortest path the algorithm found - yellow
BARRIER = (0, 0, 0)            # Border - black
START = (0, 0, 255)            # Start node - blue
GRIDLINES = (128, 128, 128)    # Line for the grid - gray
END = (128, 0, 128)            # End node - purple


# Node class for each 'node', or cell, in the window/visualizer
# Need to keep track of location, size, all neighbors, color, and number of rows
class Node:
    def __init__(self, row, col, size, num_rows):
        self.row = row
        self.col = col
        self.y = row * size
        self.x = col * size
        self.color = OPEN
        self.neighbors = []
        self.size = size
        self.num_rows = num_rows

    # Returns the current (row, col) of the node
    def getPos(self):
        return self.row, self.col

    # Return if the node is already been visited and is marked as red
    def isVisited(self):
        return self.color == VISITED

    # Return if the node is available to visit and is marked as green
    def isAvailable(self):
        return self.color == AVAILABLE

    # Return if the node is a barrier and marked as black
    def isBarrier(self):
        return self.color == BARRIER

    # Return if the node is the starting node and marked as blue
    def isStart(self):
        return self.color == START

    # Return if the node is the ending node and marked as purple
    def isEnd(self):
        return self.color == END

    # Sets the node's color to white
    def reset(self):
        self.color = OPEN

    # Sets the node's color to red
    def visit(self):
        self.color = VISITED

    # Sets the node's color to green
    def makeAvailable(self):
        self.color = AVAILABLE

    # Sets the node's color to black
    def makeBarrier(self):
        self.color = BARRIER

    # Sets the node's color to blue
    def makeStart(self):
        self.color = START

    # Sets the node's color to purple
    def makeEnd(self):
        self.color = END

    # Sets the node's color to yellow
    def makePath(self):
        self.color = PATH

    # Draws the window using pygame
    def draw(self, WINDOW):
        pygame.draw.rect(WINDOW, self.color, (self.y, self.x, self.size, self.size))

    # Updates the neighbors of the node
    def updateNeighbors(self, grid):
        # Check up, down, left, and right to see if there are any barriers
        # If there aren't, add them to the neighbors list
        self.neighbors = []
        # Neighbor below
        if self.row < self.num_rows - 1 and not grid[self.row + 1][self.col].isBarrier():
            self.neighbors.append(grid[self.row + 1][self.col])
        # Neighbor right
        if self.col < self.num_rows - 1 and not grid[self.row][self.col + 1].isBarrier():
            self.neighbors.append(grid[self.row][self.col + 1])
        # Neighbor Above
        if self.row >= 0 and not grid[self.row - 1][self.col].isBarrier():
            self.neighbors.append(grid[self.row - 1][self.col])
        # Neighbor Below
        if self.col >= 0 and not grid[self.row][self.col - 1].isBarrier():
            self.neighbors.append(grid[self.row][self.col - 1])




# Heuristics function
# Calculates the 'Manhattan' distance between the two points
def h(point1, point2):
    y1, x1 = point1 # (row, col) y is row and x is col
    y2, x2 = point2 # (row, col) y is row and x is col
    return abs(y2 - y1) + abs(x2 - x1) # Return the positive difference added together


# Create the grid
def makeGrid(numRowsAndCols, sizeOfGrid):
    grid = []                               # Empty grid
    nodeSize = sizeOfGrid // numRowsAndCols # Find the size of each node
    for i in range(numRowsAndCols):         # Iterate through the rows
        grid.append([])                     # Append a list for each row
        for j in range(numRowsAndCols):     # Iterate through the cols
            # Create a new Node ( at a particular (row, col))
            # Append it to the grid in this row
            node = Node(i, j, nodeSize, numRowsAndCols)
            grid[i].append(node)
    return grid


# Draw the grid lines so that the grid looks like a visible grid
def drawGridLines(WINDOW, numRowsAndCols, sizeOfGrid):
    nodeSize = sizeOfGrid // numRowsAndCols
    for i in range(numRowsAndCols):
        pygame.draw.line(WINDOW, GRIDLINES, (0, i * nodeSize), (sizeOfGrid, i * nodeSize))
        for j in range(numRowsAndCols):
            pygame.draw.line(WINDOW, GRIDLINES, (j * nodeSize, 0), (j * nodeSize, sizeOfGrid))


# Redraw everything each frame
def draw(WINDOW, grid, numRowsAndCols, sizeOfGrid):
    WINDOW.fill(OPEN)

    # Draws each node
    for row in grid:
        for node in row:
            node.draw(WINDOW)

    # Draws the grid lines
    drawGridLines(WINDOW, numRowsAndCols, sizeOfGrid)
    # Update pygame's display
    pygame.display.update()


# Get the row and col index from the mouse position when choosing nodes
def getMousePos(mousePos, numRowsAndCols, sizeOfGrid):
    # Calculate the size of each node and get the raw mouse input to store into y and x
    nodeSize = sizeOfGrid // numRowsAndCols
    y, x = mousePos

    # Use the raw mouse input divided by the nodeSize to get our actual row and column
    row = y // nodeSize
    col = x // nodeSize

    return row, col


# Draws the shortest path found by the A* algorithm
def make_path(parentNode, currentNode, draw):
    # Iterate through all of parentNode
    while currentNode in parentNode:
        currentNode = parentNode[currentNode] # Set currentNode to its parent node
        currentNode.makePath()                # Update the current node's color for the visualizer
        draw()                                # Call draw to reflect these changes


# Function to run the A* algorithm
# Draw is our draw function being passed in as an anonymous function
def algorithm(draw, grid, startNode, endNode):
    order = 0                          # order keeps track of the order we put in the set
    openset = PriorityQueue()          # Priority queue for the nodes
    openset.put((0, order, startNode)) # Push the startNode into the queue
    parentNode = {}                    # Dictionary for the node we came from

    # Keeps track of the current shortest distance from the start node to the current node
    # Initialized all to infinity since we have yet to check those nodes except for startNode which is set to 0
    gValue = {node: float("inf") for row in grid for node in row}
    gValue[startNode] = 0

    # Keeps track of the predicted distance of this node to the end node
    # Initialized all to infinity except for startNode which is initialized using the heuristics function
    fValue = {node: float("inf") for row in grid for node in row}
    fValue[startNode] = h(startNode.getPos(), endNode.getPos())

    # Keeps track of all items in the priority queue and out of the priority queue
    # Tells us if something is in the open set
    set_hash = {startNode}

    # While the queue is not empty, we have more reachable nodes we an visit
    while not openset.empty():
        for event in pygame.event.get():
            # If we want to quit the game prior to finishing
            if event.type == pygame.QUIT:
                pygame.quit()

        # Get our current node by indexing the open set
        # Remove it from the set hash
        currentNode = openset.get()[2]
        set_hash.remove(currentNode)

        # We found the ending node, YAY!
        if currentNode == endNode:
            # Call the make path function to draw the path
            make_path(parentNode, endNode, draw)

            # Redraw the start and end nodes so we can see them
            startNode.makeStart()
            endNode.makeEnd()
            draw()

            return True

        # Otherwise, consider all reachable neighbors
        for neighbor in currentNode.neighbors:
            # Check a temporary g value to compare to the current g value to maybe have found a better path
            tempgValue = gValue[currentNode] + 1

            # There is a better way to reach this neighbor
            if tempgValue < gValue[neighbor]:
                # Update the neighbor's parent node to the currentNode
                # Update the neighbor's g value to the temporary g value
                # Update the neighbor's f value using the temporary g value and a new heuristics based on the neighbor's position and the endNode's position
                parentNode[neighbor] = currentNode
                gValue[neighbor] = tempgValue
                fValue[neighbor] = tempgValue + h(neighbor.getPos(), endNode.getPos())

                # If the neighbor is not in the set hash, we will add it to it
                if neighbor not in set_hash:
                    order += 1 # Increment order
                    # Add the neighbor to the openset using the proper arguments
                    # Add the neighbor to the set hash
                    # Make the neighbor open
                    openset.put((fValue[neighbor], order, neighbor))
                    set_hash.add(neighbor)
                    neighbor.makeAvailable()
        draw()

        # If there is no path
        if currentNode != startNode:
            currentNode.visit()

    # No path exists
    return False


# main loop to do collision checking, starting the algorithm, changing barriers, etc.
def main(WINDOW, sizeOfGrid):
    TOTAL_ROWS_AND_COLS = 50
    grid = makeGrid(TOTAL_ROWS_AND_COLS, sizeOfGrid)

    # Maintain start and end nodes/positions
    start = None
    end = None

    # Maintain starting and running variables
    run = True
    started = False

    # While the 'activity' is running
    while run:
        draw(WINDOW, grid, TOTAL_ROWS_AND_COLS, sizeOfGrid)
        # Go through all events occurring in pygame
        for event in pygame.event.get():
            # If the X button is pressed, stop running the game
            if event.type == pygame.QUIT:
                run = False

            # Once the algorithm is running, nothing should be able to be modified during the run
            if started:
                continue

            # Check the mouse click
            # 0 is left, 1 is middle, 2 is right
            if pygame.mouse.get_pressed()[0]: # Left mouse button
                pos = pygame.mouse.get_pos() # Gets x,y coordinate of mouse click
                row, col = getMousePos(pos, TOTAL_ROWS_AND_COLS, sizeOfGrid)
                node = grid[row][col]
                # If there is no start node, place a starting node
                # Ensure that node is not currently the start node; no overriding!
                if not start and node != end:
                    start = node
                    start.makeStart()

                # Else if there is no end node, place an ending node
                # Ensure that node is not currently the start node; no overriding!
                elif not end and node != start:
                    end = node
                    end.makeEnd()

                # Else we draw a barrier as long as the node is not the start or end node
                # No overriding!
                elif node != start and node != end:
                    node.makeBarrier()

            elif pygame.mouse.get_pressed()[2]: # Right mouse button
                pos = pygame.mouse.get_pos()  # Gets x,y coordinate of mouse click
                row, col = getMousePos(pos, TOTAL_ROWS_AND_COLS, sizeOfGrid)
                node = grid[row][col]
                node.reset()
                if node == start:
                    start = None

                elif node == end:
                    end = None

            # Check if a key was pressed
            if event.type == pygame.KEYDOWN:
                # If the key pressed is the spacebar and the algorithm has not been started...
                # Make sure start and end are defined before beginning
                if event.key == pygame.K_SPACE and not started and start and end:
                    for row in grid:
                        for node in row:
                            node.updateNeighbors(grid)

                    algorithm(lambda: draw(WINDOW, grid, TOTAL_ROWS_AND_COLS, sizeOfGrid), grid, start, end)

                # Reset the visualizer to go again
                if event.key == pygame.K_r:
                    start = None
                    end = None
                    grid = makeGrid(TOTAL_ROWS_AND_COLS, sizeOfGrid)

    # End the game completely
    pygame.quit()

# Run the main with the WINDOW and SCREEN_SIZE as defined at the top of the file
main(WINDOW, SCREEN_SIZE)