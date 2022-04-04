import numpy as np
from extended_int import int_inf
from typing import List

class Puzzle:
    def __init__ (self, data, lenRoot, dirGenerated): # lenRoot = 0 (?), cek lagi nanti
        self.lenRoot = lenRoot
        self.matrix = data
        self.dirGenerated = dirGenerated
        self.pos16Row, self.pos16Col = self.getPosition16()
        self.cost = self.getCost()
        self.target = self.isTarget()

    def __eq__(self, other):
        oneDimMatrix = self.matrix.reshape(16)
        otherMatrix = other.matrix.reshape(16)
        for i in range(16):
            if oneDimMatrix[i] != otherMatrix[i]:
                return False
        return True
    
    @classmethod
    def fromMatrix(cls, array, lenRoot, dirGenerated = None):
        array_ = np.array(array)
        return cls(array_, lenRoot, dirGenerated)

    @classmethod
    def fromSeed(cls, seedInput, lenRoot, dirGenerated = None):
        np.random.seed(seedInput)
        return cls(np.random.choice(range(1,17), size=16, replace=False).reshape((4,4)), lenRoot, dirGenerated)
    
    # @classmethod
    # def dummyPuzzle(cls, lenRoot):
    #     return cls(np.empty([4,4]), lenRoot)

    def measureKurang(self):
        count = 0
        oneDimMatrix = self.matrix.reshape(16)
        for i in range(15):
            valueI = oneDimMatrix[i]
            for j in range(i + 1, 16):
                if(oneDimMatrix[j] < valueI):
                    count += 1
        return count + (x := (0 if (self.pos16Row + self.pos16Col) % 2 == 0 else 1))

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
                if(self.matrix[i][j] == 16):
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
        i, j = self.pos16Row, self.pos16Col
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
                newPuzzle = Puzzle.fromMatrix(val1, self.lenRoot + 1, direction)
                list.append(newPuzzle)
        return list

    def getCost(self):
        return self.lenRoot + self.countImproper()

    def sortNodes(self, nodes):
        sortedNodes = sorted(nodes, key=lambda x: x.cost)
        return sortedNodes
i = 0
def generateTree(puzzle, simpulHidup, haveGenerated):
    # !
    # time.sleep(1)
    global i
    # print(f"Iterasi ke {i}, banyak simpulHidup: {len(simpulHidup)}")
    # for simpul in simpulHidup:
    #     print(simpul.matrix)
    i += 1
    # print("\n")
    # ! 
    if puzzle.dirGenerated is None:
        simpulHidup.append(puzzle)
        haveGenerated.append(puzzle)
    simpulHidup = makeUnique(simpulHidup)
    haveGenerated = makeUnique(haveGenerated)

    if puzzle.target == False:
        childNode = simpulHidup[0].getChild()
        for child in childNode:
            if child not in haveGenerated:
                simpulHidup.append(child)
                haveGenerated.append(child)
        del simpulHidup[0]
        simpulHidup = puzzle.sortNodes(simpulHidup)
        temp = simpulHidup[0]
        if temp.target:
            pass
        else:
            simpulHidup.append(generateTree(simpulHidup[0], simpulHidup, haveGenerated)[0])
    return simpulHidup, haveGenerated

def makeUnique(ls):
    if(len(ls) != 0):
        flat_list = []
        for sublist in ls:
            if type(sublist) == list:
                temp = makeUnique(sublist)
                for tem in temp:
                    if tem not in flat_list:
                        flat_list.append(tem)
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
        for elmt in tree:
            if elmt.lenRoot == i and elmt.cost < valSolution[i]:
                solution[i] = elmt
                valSolution[i] = elmt.cost
    return solution
            
def showSolution(solution):
    a = solution.values()
    i = 1
    for temp in a:
        print(f"Move {i}")
        print(temp.matrix)
        i += 1

def deepest_list(l: List) -> List:
    last_item = l[-1]
    if isinstance(last_item, list):
        return deepest_list(last_item)
    return l

'''Test Case'''
puzzle1 = Puzzle.fromMatrix([[1,2,3,4],[5,6,16,8],[9,10,7,11],[13,14,15,12]], 0)
print(puzzle1.matrix)
print(">>> Puzzle 1 <<<")

if(puzzle1.isReachable()):
    a = generateTree(puzzle1, [],[])[0]
    test = deepest_list(a)
    for i in range(len(test)):
        print(test[i].matrix)
        print(test[i].lenRoot)
        print(test[i].cost)
else:
    print("15 puzzle tidak dapat diselesaikan")