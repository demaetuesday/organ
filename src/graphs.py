from priorityqueue import *

def getShortestPath(startFS, goalFS, allFSs):

    dist = dict()
    prev = dict()
    for fs in allFSs:
        dist[fs] = float('inf')
        prev[fs] = None
    dist[startFS] = 0.0

    pq = PriorityQueue()
    pq.insert(startFS, dist[startFS])
    inPQ = []
    inPQ.append(startFS)

    settled = set()

    found = False

    while len(inPQ) > 0 and not found:
        u = pq.pop()[1]
        inPQ.remove(u)
        if u is goalFS:
            found = True
        else:
            settled.add(u)
            for child in u.children:
                v = child[0]
                if v not in settled:
                    transitionCost = v.vertCost + child[1]
                    if v not in inPQ:
                        dist[v] = dist[u] + transitionCost
                        prev[v] = u
                        pq.insert(v, dist[v])
                        inPQ.append(v)
                    elif dist[v] > dist[u] + transitionCost:
                        dist[v] = dist[u] + transitionCost
                        prev[v] = u
                        pq.insert(v, dist[v])

    path = []
    currentFS = goalFS
    while currentFS is not None:
        path.append(currentFS)
        currentFS = prev[currentFS]

    path.reverse()
    return path
