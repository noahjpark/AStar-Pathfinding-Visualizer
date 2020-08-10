# A* Pathfinding Visualizer

*Run Instructions:*
* Execute astar.py
* Place a starting node
* Place an ending node
* Draw any barriers you would like
* Press space to start the algorithm
  * Once the algorithm has started, the only way to stop it is to quit the program by pressing the *x* for the window
* Once the algorithm has ended, the path will be visible to view. To run the algorithm again, simply click the *'r'* key to reset the window back to step 2

*Colors:*
* Red: Represents visited cells/nodes
* Green: Represents available cells/nodes
* White: Represents an open/blank cell/node
* Yellow: Represents the shortest path found - Drawn after the algorithm finishes
* Black: Represents a barrier that the algorithm cannot go through
* Gray: Represents the gridlines so each cell is visible
* Purple: Represents the ending cell/node
* Blue: Represents the starting cell/node

*Other Notes:*
* The first *left* click will place the starting node (*blue*)
* The second *left* click will place the ending node (*purple*)
* Any other *left* clicks will place barriers - Click can be dragged (*black*)
* Any *right* clicks will undo wherever the mouse cursor is pointing to i.e.
  * If the starting node is *right* clicked, then the starting node is removed and will be the next item to be placed
  * This applies also to the ending node
  * Priority is: Starting node, ending node, then barriers
  
# Example Runs

![Visualizer 1](https://github.com/noahjpark/AStar-Pathfinding-Visualizer/blob/master/images/pathfinding1.JPG?raw=true)

![Visualizer 2](https://github.com/noahjpark/AStar-Pathfinding-Visualizer/blob/master/images/pathfinding2.JPG?raw=true)

![Visualizer 3](https://github.com/noahjpark/AStar-Pathfinding-Visualizer/blob/master/images/pathfinding3.JPG?raw=true)
