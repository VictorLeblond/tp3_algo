import sys
import random
from collections import defaultdict

cell_size = 10 #mm
wall_height = 10 #mm
wall_thickness = 1 #mm
cell_amount = 10 #number of cells going both sides of the square
passages = [] #use a dictionnary to map the source to...

strategy_choice = 2

class Strategy :
    def __init__(self):
        pass

    def Apply(self):
        print("Applying Abstract Strategy")

    def DoSomething(self):
        print("Do Something")

class Coords:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

class Wall:
    def __init__(self, coords1, coords2, side) -> None:
        self.source = coords1
        self.dest = coords2
        self.side = side

class Cell:
    def __init__(self, coords, up, down, left, right) -> None:
        self.coords = coords
        self.up = up
        self.down = down
        self.left = left
        self.right = right

class Algorithm1(Strategy) :
    def Apply(self):
        #super().Apply()
        print("Applying Algorithm1")
        #Iterative randomized Prim's algorithm
        cells = [[0] * cell_amount for _ in range(cell_amount)]
        walls = []
        #Start with a grid full of walls. or no passages
        #Pick a cell, mark it as part of the maze.
        startCoords = Coords(random.randrange(0, cell_amount - 1), random.randrange(0, cell_amount - 1))
        cells[startCoords.x][startCoords.y] = 1
        #Add the walls of the cell to the wall list
        walls.extend(self.getWallsOfCell(startCoords))
        #While there are walls in the list
        while(walls):
            #Pick a random wall from the list.
            rand_index, wall = random.choice(list(enumerate(walls)))
            #Remove the wall from the list.
            walls.pop(rand_index)
            #If only one of the cells that the wall divides is visited, then:
            if (cells[wall.dest.x][wall.dest.y] == 0):
                #Make the wall a passage and mark the unvisited cell as part of the maze.
                passages.append(wall)
                cells[wall.dest.x][wall.dest.y] = 1
                #Add the neighboring walls of the cell to the wall list.
                walls.extend(self.getWallsOfCell(wall.dest))
        #now we have passages
        return passages
    
    def getWallsOfCell(self, coords):
        walls = []
        if coords.x - 1 >= 0:
            walls.append(Wall(coords, Coords(coords.x - 1, coords.y), "l"))
        if coords.x + 1 <= cell_amount - 1:
            walls.append(Wall(coords, Coords(coords.x + 1, coords.y), "r"))
        if coords.y - 1 >= 0:
            walls.append(Wall(coords, Coords(coords.x, coords.y - 1), "u"))
        if coords.y + 1 <= cell_amount - 1:
            walls.append(Wall(coords, Coords(coords.x, coords.y + 1), "d"))
        return walls

class Algorithm2(Strategy) :

    def Apply(self):
        super().Apply()
        print("Applying Algorithm2")
        #randomized DFS Iterative implementation (with stack)
        cells = [[0] * cell_amount for _ in range(cell_amount)]
        stack = []
        #Choose the initial cell, mark it as visited and push it to the stack
        curCell = Coords(random.randrange(0, cell_amount), random.randrange(0, cell_amount))
        cells[curCell.x][curCell.y] = 1
        stack.append(curCell)
        #While the stack is not empty
        while (stack):
            #Pop a cell from the stack and make it a current cell
            curCell = stack.pop()
            #If the current cell has any neighbours which have not been visited
            unvisited = self.hasUnvisitedNeighbours(cells, curCell)
            if (unvisited):
                #Push the current cell to the stack
                stack.append(curCell)
                #Choose one of the unvisited neighbours
                #Remove the wall between the current cell and the chosen cell
                passages.append(Wall(curCell, unvisited))
                #Mark the chosen cell as visited and push it to the stack
                cells[unvisited.x][unvisited.y] = 1
                stack.append(unvisited)
        for passage in passages:
            print(str(passage.source.x) + "," + str(passage.source.y) + "-->" + str(passage.dest.x) + "," + str(passage.dest.y) + "" + str(passage.side))
        return passages
    
    def hasUnvisitedNeighbours(self, cells, coords):
        x , y = coords.x, coords.y
        deltas = [(0, 1), (0, -1), (-1, 0), (1, 0)]
        for dx, dy in deltas:
            nx, ny = x + dx, y + dy
            if 0 <= nx < cell_amount and 0 <= ny < cell_amount and cells[nx][ny] == 0:
                return Coords(nx, ny)
        return False        
    

class Generator() :
    strategy = None

    def __init__(self):
        pass

    def SetStrategy(self, new_strategy):
        self.strategy = new_strategy

    def Generate(self):
        self.strategy.Apply()
        self.strategy.DoSomething()

class Creator() :
    def __init__(self):
        pass
    
    #cleanup passages into usable cells
    def cleanupCells(self):
        #map from source -> dest cell
        directionMap = {'l': 'r', 'r': 'l', 'u': 'd', 'd': 'u'}
        passageDict = defaultdict(set)
        for passage in passages:
            passageDict[(passage.source.x, passage.source.y)].add(passage.side)
            passageDict[(passage.dest.x, passage.dest.y)].add(directionMap.get(passage.side))
        #construct cells
        cells = []
        for j in range(cell_amount):
            for i in range(cell_amount):
                #row per row
                walls = passageDict[(i, j)]
                cells.append(Cell((i, j), 'u' not in walls, 'd' not in walls, 'l' not in walls, 'r' not in walls))
        return cells

    def PrintLabyrinth(self): 
        pass

    #generate .scad file
    def OutputScad(self):
        cells = self.cleanupCells()
        filename = "./labytinthe_algo" + str(strategy_choice) + ".scad"
        #initialize
        content = "difference () {\nunion() {\n"
        width = str(cell_amount * cell_size)
        content += "translate([-0.5,-0.5,-1])\n{cube([" + width + "," + width + ",1], center=false);\n}"
        for cell in cells:
            #cells only take care of up and left
            if cell.up: content += self.writeWall(cell.coords, 'u')
            if cell.left: content += self.writeWall(cell.coords, 'l')
            #special cases for first last indices x and y
            if (cell.coords[0] == cell_amount - 1): content += self.writeWall(cell.coords, "r")
            if (cell.coords[1] == cell_amount - 1): content += self.writeWall(cell.coords, "d")
        content += "}\n}"
        self.write(filename, content)

    def writeWall(self, cellCoords, direction):
        directionMap = {
            "l": 0,
            "u": 90,
            "r": 90,
            "d": 0,
        }
        offsetX = (cellCoords[0] + (1 if direction == 'r' else 0)) * cell_size + (1 if direction == 'u' or direction == "r" else 0)
        offsetY = (cellCoords[1] + (1 if direction == 'd' else 0)) * cell_size
        rotation = "[0,0," + str(directionMap[direction]) + "]"
        cube = "cube([" + (str(cell_size + 1)) + "," + str(wall_thickness) + "," + str(cell_size) + "], center=false);\n"
        coords = "[" + str(offsetX) + "," + str(offsetY) + "," +",0]"
        return "translate(" + coords + "){\nrotate (" + rotation + "){\n" + cube + "}\n}"
    
    def write(self, fileName, content):
        file = open(fileName, "w")
        file.write(content)
        file.close()

# main call
def main():
    global strategy_choice
    args = sys.argv[:]
    if len(args) >= 2 :
        strategy_choice = int(args[1])

    # Generator
    my_generator = Generator()
    if strategy_choice == 1:
        my_generator.SetStrategy(Algorithm1())
    elif strategy_choice == 2:
        my_generator.SetStrategy(Algorithm2())
    else :
        print("error strategy choice")
    my_generator.Generate()

    #Creator
    my_creator = Creator()
    my_creator.PrintLabyrinth()
    my_creator.OutputScad()

if __name__ == "__main__":
    main()
