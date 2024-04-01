#Kelvin Chen, 20238788
#Victor Leblond, matricule

#N : Force maximale
#k : Nombre de fenêtres disponibles
#Valeur de retour : le nombre minimal de tests qu'il faut faire 
#                   en pire cas pour déterminer le seuil de solidité 
#                   d'une fenêtre
#Doit retourner la réponse comme un int.
def vitre(N, k):
    #axes: colonne: force maximale, rangee: nombre de vitres restantes(k)
    #valeur represente le nombre d'essais minimales
    tests = [[float('inf')] * (k + 1) for _ in range(N + 1)]

    for s in range (1, N + 1):
        tests[s][1] = s - 1

    for s in range(1, N + 1):
        for j in range(2, k + 1):
            for i in range(1, s):
                tests[s][j] = min(tests[s][j], 1 + max(tests[i][j-1], tests[s-1][j]))

    return tests[N][k]

def main(args):
    N = int(args[0])
    k = int(args[1])

    answer = vitre(N,k)
    print(answer)

if __name__ == '__main__':
    main(sys.argv[1:])