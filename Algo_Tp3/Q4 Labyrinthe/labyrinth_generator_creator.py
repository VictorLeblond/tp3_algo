import sys
import random

cell_size = 10 #mm
wall_height = 10 #mm
wall_thickness = 1 #mm
cell_amount = 20 #number of cells going both sides of the square

strategy_choice = 1

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
    def __init__(self, coords1, coords2) -> None:
        self.source = coords1
        self.dest = coords2

class Algorithm1(Strategy) :

    def Apply(self):
        super().Apply()
        print("Applying Algorithm1")
        #Iterative randomized Prim's algorithm
        cells = [[0] * cell_amount for _ in range(cell_amount)]
        walls = []
        #Start with a grid full of walls. or no passages
        passages = []
        #Pick a cell, mark it as part of the maze.
        startCoords = Coords(random(cell_size), random(cell_size))
        cells[startCoords.x][startCoords.y] = 1
        #Add the walls of the cell to the wall list
        walls.append(self.getWallsOfCell(cells, startCoords))
        #While there are walls in the list
        while(walls):
            #Pick a random wall from the list.
            wall = walls[0]
            #If only one of the cells that the wall divides is visited, then:
            if (cells[wall.dest.x][wall.dest.y] == 0):
                #Make the wall a passage and mark the unvisited cell as part of the maze.
                passages.append(wall)
                cells[wall.dest.x][wall.dest.y] == 1
                #Add the neighboring walls of the cell to the wall list.
                walls.append(self.getWallsOfCell(cells, wall.dest))
            #Remove the wall from the list.
            walls.pop()
        #now we have passages
        return passages
    
    def getWallsOfCell(cells, coords):
        l = Wall(coords, Coords(coords.x - 1, coords.y)) if (coords.x - 1 >= 0) else None
        r = Wall(coords, Coords(coords.x + 1, coords.y)) if (coords.x + 1 <= cell_amount - 1) else None
        u = Wall(coords, Coords(coords.x, coords.y + 1)) if (coords.y - 1 >= 0) else None
        d = Wall(coords, Coords(coords.x, coords.y - 1)) if (coords.y + 1 <= cell_amount - 1) else None
        return l, r, u, d

class Algorithm2(Strategy) :

    def Apply(self):
        super().Apply()
        print("Applying Algorithm2")
        #Aldous-Broder algorithm
        cells = [[0] * cell_amount for _ in range(cell_amount)]
        visitedCount = 0
        passages = []
        #Pick a random cell as the current cell and mark it as visited.
        curCoords = Coords(random(cell_amount), random(cell_amount))
        cells[curCoords.x][curCoords.y] = 1
        visitedCount += 1
        #While there are unvisited cells:
        while (visitedCount < cell_amount*cell_amount):
            #Pick a random neighbour.
            neighbor = self.pickRandomNode(cells, curCoords)
            #If the chosen neighbour has not been visited
            if (cells[neighbor.x][neighbor.y] != 1):
                #Remove the wall between the current cell and the chosen neighbour.
                passages.append(Wall(curCoords, neighbor))
                #Mark the chosen neighbour as visited.
                cells[neighbor.x][neighbor.y] = 1
            #Make the chosen neighbour the current cell.
            curCoords = neighbor
            visitedCount += 1
    
    def pickRandomNode(cells, coords):
        upDown = random(1,-1)
        leftRight = random(1,-1)
        newCoords = Coords(coords.x + leftRight, coords.y + upDown)
        return newCoords



class Generator() :
    strategy = None

    def __init__(self):
        pass

    def SetStrategy(self, new_strategy):
        self.strategy = new_strategy

    def Generate(self):
        print(self.strategy.Apply())
        self.strategy.DoSomething()

class Creator() :
    #generate .scad file
    def __init__(self):
        pass

    def PrintLabyrinth(self):
        pass


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


if __name__ == "__main__":
    main()
