import numpy as np
from pythonlangutil.overload import Overload, signature
from multipledispatch import dispatch

class Puzzle:
    # Attribute
    # Method
    
    # def __init__(self, matrix):
    #     self.matrix = np.array(matrix)

    # def __init__(self, seedInput):
    #     np.random.seed(seedInput)
    #     self.matrix = np.random.choice(range(1,17), size=16, replace=False).reshape((4,4))

    def __init__ (self, data, lenRoot): # lenRoot = 0 (?), cek lagi nanti
        self.lenRoot = lenRoot
        self.matrix = data
    
    @classmethod
    def fromMatrix(cls, array, lenRoot):
        array_ = np.array(array)
        return cls(array_, lenRoot)

    @classmethod
    def fromSeed(cls, seedInput, lenRoot):
        np.random.seed(seedInput)
        return cls(np.random.choice(range(1,17), size=16, replace=False).reshape((4,4)), lenRoot)
    
    @classmethod
    def dummyPuzzle(cls, lenRoot):
        return cls(np.empty([4,4]), lenRoot)

    # @classmethod
    # def producePuzzle(cls):
    #     return cls.dummyPuzzle()

    def getElmt(self, idxRow, idxCol):
        return self.matrix[idxRow][idxCol]

    def measureKurang(self):
        count = 0
        oneDimMatrix = self.matrix.reshape(16)
        for i in range(15):
            valueI = oneDimMatrix[i]
            for j in range(i + 1, 16):
                if(oneDimMatrix[j] < valueI):
                    count += 1
        return count + (x := (0 if (self.getPosition16()[0] + self.getPosition16()[1]) % 2 == 0 else 1))

    def countImproper(self):
        count = 0
        oneDimMatrix = self.matrix.reshape(16)
        for i in range(16):
            if (oneDimMatrix[i] != (i + 1)) and (oneDimMatrix[i] != 16):
                count += 1
        return count


    def getPosition16(self):
        for i in range(4):
            for j in range(4):
                if(self.getElmt(i,j) == 16):
                    break
            else:
                continue
            break
        return i, j
        
    def isReachable(self):
        if(self.measureKurang() % 2 == 0):
            return True
        return False

    def isValidDirection(self, direction):
        if direction == "up": # syntax error when trying to use match-case
            if self.getPosition16()[0] != 0:
                return True
        elif direction == "down":
            if self.getPosition16()[0] != 3:
                return True
        elif direction == "right":
            if self.getPosition16()[1] != 3:
                return True
        elif direction == "left":
            if self.getPosition16()[1] != 0:
                return True
        return False

    def moveEmptyBox(self, direction):
        i, j = self.getPosition16()
        tempMatrix = np.copy(self.matrix)
        if direction == "up" and self.isValidDirection("up"):
            temp = tempMatrix[i - 1][j]
            tempMatrix[i][j] = temp
            tempMatrix[i - 1][j] = 16
        elif direction == "down" and self.isValidDirection("down"):
            temp = tempMatrix[i + 1][j]
            tempMatrix[i][j] = temp
            tempMatrix[i + 1][j] = 16
        elif direction == "right" and self.isValidDirection("right"):
            temp = tempMatrix[i][j + 1]
            tempMatrix[i][j] = temp
            tempMatrix[i][j + 1] = 16
        elif direction == "left" and self.isValidDirection("left"):
            temp = tempMatrix[i][j - 1]
            tempMatrix[i][j] = temp
            tempMatrix[i][j - 1] = 16
        return tempMatrix, self.isValidDirection(direction)
        
    def isTarget(self):
        oneDimMatrix = self.matrix.reshape(16)
        for i in range(16):
            if oneDimMatrix[i] != (i + 1):
                return False
        return True

    def getChild(self):
        dummyPuzzle = Puzzle.dummyPuzzle(self.lenRoot + 1)
        directions = ["up", "down", "right", "left"]
        list = []
        for direction in directions:
            if(self.moveEmptyBox(direction)[1]):
                dummyPuzzle.matrix = self.moveEmptyBox(direction)[0]
                list.append(dummyPuzzle)
        return list

puzzle = Puzzle.fromSeed(4, 0)
# puzzle_ = Puzzle.producePuzzle()
# print(puzzle_.matrix)

puzzleChild = puzzle.getChild()
print(puzzle.matrix)
# print("===========")
for child in puzzleChild:
    print(f"{child.matrix}")
    print(f"{child.lenRoot}\n")
print("===============")
puzzleGrandChild = puzzleChild[0].getChild()
for child in puzzleGrandChild:
    print(f"{child.matrix}")
    print(f"{child.lenRoot}\n")