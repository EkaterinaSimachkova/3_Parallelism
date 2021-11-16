from multiprocessing import Process, freeze_support, Manager
import random


def element(index, A, B):
    i, j = index
    res = 0
    # get a middle dimension
    N = len(A[0]) or len(B)
    for k in range(N):
        res += A[i][k] * B[k][j]

    with open("log", "a") as log:
        log.write(f"{i} {j} {res}\n")


def CreateNewMatrix(matrix_size, Var = None):
    matrix = []
    for i in range(matrix_size):
        matrix.append([])
        for j in range(matrix_size):
            matrix[i].append(random.randint(0, 10))
    if Var:
        Var = matrix
    else:
        return matrix


def Multiply(matrix1, matrix2, Var):
    log = open("log", "w").close()

    matrix = []
    for i in range(len(matrix1)):
        matrix.append([])
        for j in range(len(matrix2[0])):
            matrix[i].append(0)
            if i == len(matrix1) - 1 and j == len(matrix2[0]) - 1:
                p = Process(target=element, args=((i, j), matrix1, matrix2))
                p.start()
                p.join()
            else:
                Process(target=element, args=((i, j), matrix1, matrix2)).start()

    with open("log", "r") as log:
        for value in log.readlines():
            line, column, var = value.split()
            matrix[int(line)][int(column)] = str(var)


    with open("result", "w") as file:
        for line in matrix:
            file.write(" ".join(line) + "\n")

    for i in range(len(matrix)):
        for j in range(len((matrix[0]))):
            matrix[i][j] = int(matrix[i][j])
    Var.matrix = matrix


def MainCycle(matrix_size, Var):
    freeze_support()
    matrix_size = int(matrix_size)
    Var.matrix1 = CreateNewMatrix(matrix_size)
    Var.matrix2 = CreateNewMatrix(matrix_size)

    Mult = Process(target=Multiply, args=(Var.matrix1, Var.matrix2, Var))
    Mult.start()

    while not Var.StopFlag:
        CreateMatrix = Process(target=CreateNewMatrix, args=(matrix_size, Var))
        CreateMatrix.start()
        Mult.join()
        Var.matrix1 = Var.matrix

        Mult = Process(target=Multiply, args=(Var.matrix1, Var.matrix2, Var))
        Mult.start()


if __name__ == '__main__':
    manager = Manager()
    Var = manager.Namespace()
    Var.matrix = []
    Var.StopFlag = False
    matrix_size = int(input("Введите размер матрицы: "))

    Process(target=MainCycle, args=(matrix_size,Var)).start()

    while True:
        command = input("Введите команду: ")
        if command == "stop":
            Var.StopFlag = True
            break
        else:
            print("Неизвестная команда")

