
from collections import deque

class node:
    def __init__(self,x,y,camefrom):
        self.x = x
        self.y = y
        self.cf = camefrom

    def __str__(self):
        return str((self.x,self.y))

class Queue:
    def __init__(self):
        self.el = deque()

    def empty(self):
        return len(self.el) == 0

    def put(self, a):
        self.el.append(a)

    def get(self):
        return self.el.popleft()

found = False

def neighbours(nod,tov,xm,ym):
    ret = []
    for i in tov:
        tx = nod.x+i[0]
        ty = nod.y+i[1]
        if tx>=0 and tx<xm and ty>=0 and ty<ym:
            tmpnd = node(tx,ty,nod)
            ret.append(tmpnd)
    return ret

def find(x,y,xm,ym,b,c):
    visited = []
    nodes = []
    q = Queue()
    start = node(x,y,None)
    q.put(start)
    nodes.append(start)
    tov = [(0,-1),(-1,0),(0,1),(1,0)]
    final = None
    topr = []
    while not q.empty():
        print('cycle')
        next = q.get()
        nb = neighbours(next,tov,xm,ym)
        mod = 0
        for i in range(len(nb)):
            print(nb[i-mod].x)
            if str(nb[i-mod]) in visited:
                print('ifvisited')
                del nb[i-mod]
                mod+=1
            elif str(b.structure[nb[i-mod].y][nb[i-mod].x]) == 'robot':
                print('robot')
                del nb[i-mod]
                mod+=1
            elif str(b.structure[nb[i-mod].y][nb[i-mod].x]) == 'box':
                print('box')
                final = nb[i-mod]
                break
            else:
                print('else')
                visited.append(str(nb[i-mod]))
                q.put(nb[i-mod])
                topr.append((nb[i-mod].x,nb[i-mod].y))
        if final != None:
            break
    if final == None:
        return False
    else:
        toret = []
        while final.cf != None:
            toret.append((final.x,final.y))
            final = final.cf
        return toret
