import numpy as np
from extended_int import int_inf
# import time

class Puzzle:
    def __init__ (self, data, lenRoot, dirGenerated = None): # lenRoot = 0 (?), cek lagi nanti
        self.lenRoot = lenRoot
        self.matrix = data
        self.dirGenerated = dirGenerated
    
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
            if oneDimMatrix[i] != (i + 1):
                count += 1
        return count - 1


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

    def moveEmptyBox(self, direction):
        i, j = self.getPosition16()
        tempMatrix = np.copy(self.matrix)
        if direction == "up" and i != 0:
            temp = tempMatrix[i - 1][j]
            tempMatrix[i][j] = temp
            tempMatrix[i - 1][j] = 16
            return tempMatrix, True
        elif direction == "down" and i != 3:
            temp = tempMatrix[i + 1][j]
            tempMatrix[i][j] = temp
            tempMatrix[i + 1][j] = 16
            return tempMatrix, True
        elif direction == "right" and j != 3:
            temp = tempMatrix[i][j + 1]
            tempMatrix[i][j] = temp
            tempMatrix[i][j + 1] = 16
            return tempMatrix, True
        elif direction == "left" and j != 0:
            temp = tempMatrix[i][j - 1]
            tempMatrix[i][j] = temp
            tempMatrix[i][j - 1] = 16
            return tempMatrix, True
        return tempMatrix, False
        
    def isTarget(self):
        oneDimMatrix = self.matrix.reshape(16)
        for i in range(16):
            if oneDimMatrix[i] != (i + 1):
                return False
        return True

    def getChild(self):
        directions = ["up", "down", "right", "left"]
        if self.dirGenerated == "up":
            directions.remove("down")
        elif self.dirGenerated == "down":
            directions.remove("up")
        elif self.dirGenerated == "right":
            directions.remove("left")
        elif self.dirGenerated == "left":
            directions.remove("right")
            
        list = []
        for direction in directions:
            val1, val2 = self.moveEmptyBox(direction)
            if(val2):
                dummyPuzzle = Puzzle.dummyPuzzle(self.lenRoot + 1)
                dummyPuzzle.matrix = val1
                dummyPuzzle.dirGenerated = direction
                list.append(dummyPuzzle)
        return list 

    def getCost(self):
        return self.lenRoot + self.countImproper()

    def sortNodes(self, nodes):
        sortedNodes = sorted(nodes, key=lambda x: x.getCost())
        return sortedNodes
i = 0
def generateTree(puzzle, simpulHidup, haveGenerated):
    # !
    # time.sleep(1)
    # global i
    # print(f"Iterasi ke {i}, banyak simpulHidup: {len(simpulHidup)}")
    # for simpul in simpulHidup:
    #     print(simpul.matrix)
    # i += 1
    # print("\n")
    # ! 
    simpulHidup.append(puzzle)
    haveGenerated.append(puzzle)

    if puzzle.isTarget() == False:
        childNode = simpulHidup[0].getChild()
        for child in childNode:
            if child not in haveGenerated:
                simpulHidup.append(child)
                haveGenerated.append(child)
        del simpulHidup[0]
        simpulHidup = puzzle.sortNodes(simpulHidup)
        temp = simpulHidup[0]
        if temp.isTarget():
            pass
        else:
            simpulHidup.append(generateTree(simpulHidup[0], simpulHidup, haveGenerated)[0])
    return simpulHidup, haveGenerated

def makeUnique(ls):
    if(len(ls) != 0):
        flat_list = []
        for sublist in ls:
            if type(sublist) == list:
                for item in sublist:
                    if type(item) == list:
                        temp = makeUnique(item)
                        for tem in temp:
                            if tem not in flat_list:
                                flat_list.append(tem)
                    else: 
                        if item not in flat_list:
                            flat_list.append(item)
            else:
                if sublist not in flat_list:
                    flat_list.append(sublist)
        return flat_list
    return ls

def getMaxLenRoot(tree):
    max = tree[0].lenRoot
    for elmt in tree:
        if elmt.lenRoot > max:
            max = elmt.lenRoot
    return max

def getSolution(tree):
    solution = {}
    valSolution = {}
    for i in range(getMaxLenRoot(tree)):
        valSolution[i] = int_inf
    for i in range(getMaxLenRoot(tree)):
        for elmt in tree:
            if elmt.lenRoot == i and elmt.getCost() < valSolution[i]:
                solution[i] = elmt
                valSolution[i] = elmt.getCost()
    return solution
            
def showSolution(solution):
    for i in range(len(solution)):
        print(f"Move: {i + 1}")
        print(f"{solution[i].matrix}\n")