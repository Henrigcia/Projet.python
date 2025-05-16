from abc import ABC, abstractmethod

# ConnectedCells implements an abstract class that in the given 2D grid of points detects the groups of connected cells ("islands") using the (to-be-defined-later) get_neighbors() absract method.
# The connected cells are being identified using Depth First Search algorithm (https://brilliant.org/wiki/depth-first-search-dfs/).
 
# Platforms, HSeries and VSeries are then derived from ConnectedCells for the particluar implementations, each implementing its own get_neighbors():

# For Platforms the connected cells (neighbors) are left, right, up and down cells
# For HSeries the connected cells (neighbors) are left ands right cells
# For VSeries the connected cells (neighbors) are up and down cells

class ConnectedCells:

    Cells: set[tuple[int,int]]  = set()                                  # The full set of cells defined by tuples of (x,y) coordinates
    Visited: set[tuple[int,int]] = set()                                 # We will track visited cells here
    
    def __init__(self, Cells: set[tuple[int, int]]) -> None:
        self.Cells = Cells
        self.Visited = set()

# We will define this function as needed to return the set of the cells around the given cell (aka set of "neighbors")
    @abstractmethod
    def get_neighbors(self, cell: tuple[int,int]) -> set[tuple[int, int]]:                         
        pass


# This is Depth First Search from the given cell. 
# It will build a new "island" of the connected cells using get_neighbors() call
    def DFS(self, cell: tuple[int, int]) -> list[tuple[int, int]]:                                        
        stack = [cell]                                       # Initialize to-do list with the first cell
        island: list[tuple[int,int]] = []                    # Initialize new island
        while stack:                                         # While still smth on to-do list...
            p = stack.pop()                                  # ... pop this cell from the stack (to-do list)
            if p in self.Visited:                            # if cell already visited then skip to the next one on to-do list
                continue
            self.Visited.add(p)                              # add the cell to the visited
            island.append(p)                                 # add the cell to the island
            for neighbor in self.get_neighbors(p):           # Now let's look for the neighbors. For each neigboring cell...
                if neighbor in self.Cells and neighbor not in self.Visited :
                                                                                          # ...if it's in the Cells and not visited yet...
                    stack.append(neighbor)                   # ...write the neighbor into to-do list
        return island


# This method will build the list of all connected "islands of cells" by calling DFS for each cell that has not been visited yet
# If a cell is in visited set this means it has already been assigned to some island so we skip it
    def get_islands(self) -> list[list[tuple[int, int]]]:
        self.Visited = set()                                                          # Reset visits list
        islands: list[list[tuple[int, int]]] = []                                     # Reset islands list

        for cell in self.Cells:                        # Go through each cell in the grid
            if cell not in self.Visited:               # If it has not been visited yet...
                island = self.DFS(cell)                # ...build a new island from this cell using DFS 
                islands.append(island)                 # Add it to the list of islands

        return islands


class Platforms(ConnectedCells):

    def get_neighbors(self, cell: tuple[int,int]) -> set[tuple[int, int]]:                         
        x, y = cell
        return {(x+1, y), (x-1, y), (x, y+1), (x, y-1)}    # Return left, right, up and down cells as neighbors - for platform blocks

class HSeries(ConnectedCells):

    def get_neighbors(self, cell: tuple[int,int]) -> set[tuple[int, int]]:                         
        x, y = cell
        return {(x+1, y), (x-1, y)}                       # Return left and right cells as neighbors - for horizontal arrows

class VSeries(ConnectedCells):

    def get_neighbors(self, cell: tuple[int,int]) -> set[tuple[int, int]]:                         
        x, y = cell
        return {(x, y+1), (x, y-1)}                       # Return up and down cells as neighbors - for vertical arrows