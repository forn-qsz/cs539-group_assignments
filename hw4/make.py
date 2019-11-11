from sys import stdin

#epron = ['W', 'AY', 'N']
#jpron = ['W', 'A', 'I', 'N']

#epron = ['AY', 'N']
#jpron = ['I', 'N']

#epron = ['T','O']
#jpron = ['O', 'T', 'O']

#epron = ['B', 'OW', 'T']
#jpron = ['B', 'O', 'O', 'T', 'O']

epron = ['T', 'EH', 'S', 'T']
jpron = ['T', 'E', 'S','U', 'T', 'O']

start = [0.333, 0.333, 0.333]
def enum(epron, jpron, path):
    if(len(epron) == 1):
        k = []
        for i in range(len(jpron)):
            k.append(jpron[i])
        path.append([epron, k])
        #print(prev, 'haha')
        print (path)
    else:
        #print()
        for i in range(len(jpron) - len(epron) + 1):
            k = []
            test = []
            for j in range(i + 1):
                k.append(jpron[j])
            #print(epron[0], k)
            test.append([epron[0], k])
            enum(epron[1:], jpron[i+1:], test)
path = []
enum(epron, jpron, path)

#dic = {'W': {'W' : 0.0, 'WA' : 0.0}, 'AY': {'A' : 0.0, 'AI', 'I':0.0}, 'N':
