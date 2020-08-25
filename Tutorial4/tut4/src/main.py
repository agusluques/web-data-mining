import numpy as np

number_nodes = 0

def createH(inputFile):
    global number_nodes

    text = None
    with open(inputFile, 'r') as f:
        text = f.read()
    lines = text.splitlines()

    number_nodes = int(lines[0])

    H = np.zeros((number_nodes,number_nodes))

    for node in range(number_nodes):
        number_edges = lines[node + 1].count(':')
        if (number_edges > 0):
            neighbours = list(map(lambda x: int(x[:1]),lines[node + 1].split(' ')))

            row = [0] * number_nodes

            for index in neighbours:
                row[index] = 1 / number_edges

            H[node] = row
        else:
            H[node] = [0] * number_nodes
    
    return H

def createS(H):
    S = H

    zero_rows = list(np.where(~H.any(axis=1))[0])
    
    for i in zero_rows:
        S[i] = [1/number_nodes] * number_nodes

    return S

def createG(S,alpha):
    G = S*alpha

    aux = np.zeros((number_nodes,number_nodes))
    aux.fill((1-alpha)/number_nodes)

    G = G + aux

    return G


def computePR(M, iterations):
    pi = np.zeros(number_nodes)

    pi.fill(1/number_nodes)
    print('\nInitialize PR:\n')
    print(pi)
    for i in range(iterations):
        pi = np.dot(pi, M)
        print('\nPR in iteration number ' + str(i)+ ':\n')
        print(pi)

inputFile = "./data/test3.txt"
alpha = 0.9
iterations = 16

H = createH(inputFile)
print("\nH matrix:\n")
print(H)
computePR(H, iterations)

S = createS(H)
print("\nS matrix:\n")
print(S)
computePR(S, iterations)

G = createG(S,alpha)
print("\nG matrix:\n")
print(G)
computePR(G, iterations)