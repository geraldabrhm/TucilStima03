from puzzleSolver import *

print("Pilihan input")
print("\t1. User-defined")
print("\t2. Already in program")

pilihan = input("Masukan pilihanmu: (1 atau 2): ")
# * Testing user-defined
if pilihan == "1":
    fileName = input("Masukan nama file: ")
    with open('input/' + fileName) as f:
        ls = [int(x) for x in f.read().split()]

    ls = np.reshape(ls, (4,4))
    puzzleX = Puzzle.fromMatrix(ls, 0)
    print(puzzleX.matrix)
    print(">>> Puzzlemu <<<")
    if(puzzleX.isReachable()):
        a = generateTree(puzzleX, [], [])
        a = makeUnique(a)
        a = getSolution(a)
        showSolution(a)
    else:
        print("15 puzzle tidak dapat diselesaikan")
# * Testing manual
elif pilihan == "2": 
    print("Pilihan puzzle")
    print("\t1. Puzzle1")
    print("\t2. Puzzle2")

    puzzle = input("Masukkan pilihanmu: (1 atau 2): ")

    if puzzle == "1":
        puzzle1 = Puzzle.fromMatrix([[1,2,3,4],[5,6,16,8],[9,10,7,11],[13,14,15,12]], 0)
        print(puzzle1.matrix)
        print(">>> Puzzle 1 <<<")
        if(puzzle1.isReachable()):
            a = generateTree(puzzle1, [], [])
            a = makeUnique(a)
            a = getSolution(a)
            showSolution(a)
        else:
            print("15 puzzle tidak dapat diselesaikan")
    elif puzzle == "2":
        puzzle2 = Puzzle.fromSeed(13, 0)
        print(puzzle2.matrix)
        print(">>> Puzzle 2 <<<")
        if(puzzle2.isReachable()):
            a = generateTree(puzzle2, [], [])
            a = makeUnique(a)
            a = getSolution(a)
            showSolution(a)
        else:
            print("15 puzzle tidak dapat diselesaikan")

    # ! Known bugs: Maximum recursion depth exceeded
    # puzzle3 = Puzzle.fromMatrix([[15,6,12,10],[13,11,1,16],[7,8,2,5],[4,9,3,14]], 0)
    # print(">>> Puzzle 3 <<<")
    # if(puzzle3.isReachable()):
    #     a = generateTree(puzzle3, [], [])
    #     a = makeUnique(a)
    #     a = getSolution(a)
    #     showSolution(a)
    # else:
    #     print("15 puzzle tidak dapat diselesaikan")