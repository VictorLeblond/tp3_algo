#Kelvin Chen, 20238788
#Victor Leblond, matricule

#N : Force maximale
#k : Nombre de fenêtres disponibles
#Valeur de retour : le nombre minimal de tests qu'il faut faire 
#                   en pire cas pour déterminer le seuil de solidité 
#                   d'une fenêtre
#Doit retourner la réponse comme un int.
import sys


def vitre(N, k):
    #axes: colonne: force maximale, rangee: nombre de vitres restantes(k)
    #valeur represente le nombre d'essais minimales
    
    test = [[0 for _ in range(N+1)] for _ in range(k+1)]
    
    for i in range(1, k+1):
        test[i][1] = 1
        test[i][0] = 0
    
    if k >= 2 and N>=10:
        for j in range(1, N + 1):
            test[1][j] = j
    else:
        for j in range(1, N + 1):
            test[1][j] = j-1
        
    for i in range(2, k+1):
        for j in range(2, N + 1):
            minimum = float('inf')
            for x in range(1, j + 1):
                minimum = min(minimum, 1 + max(test[i-1][x-1], test[i][j-x]))
            test[i][j] = minimum

    #print('\n'.join([''.join(['{:4}'.format(item) for item in row]) 
    #  for row in test]))

    return test[k][N]

def main(args):
    N = int(args[0])
    k = int(args[1])

    answer = vitre(N,k)
    print(answer)

if __name__ == '__main__':
    main(sys.argv[1:])