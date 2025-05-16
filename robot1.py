from random import choice
def digitalize(x, y, b, db, s=0):
    n = len(b)
    if x in range(n) and y in range(n) and b[x][y] == 0 and (db[x][y] == -1 or db[x][y] > s):
        db[x][y] = s
        digitalize(x + 1, y, b, db, s + 1)
        digitalize(x, y + 1, b, db, s + 1)
        digitalize(x - 1, y, b, db, s + 1)
        digitalize(x, y - 1, b, db, s + 1)
def makedecision(p1, p2, f1, f2, b, bricks, b2):
    prob = []
    n = len(b)
    db = [[-1 for i in range(n)] for j in range(n)]
    digitalize(f1[0], f1[1], b, db)
    np = p1.copy()
    nst = db[p1[0]][p1[1]]
    ist = nst
    if p1[0] - 1 in range(n):
        if 0 <= db[p1[0]-1][p1[1]] < nst:
            np = [p1[0]-1, p1[1]]
            nst = db[p1[0]-1][p1[1]]
            prob = [[False, np]]
        elif db[p1[0]-1][p1[1]] == nst:
            np = [p1[0] - 1, p1[1]]
            nst = db[p1[0] - 1][p1[1]]
            prob.append([False, np])
    if p1[0] + 1 in range(n):
        if 0 <= db[p1[0]+1][p1[1]] < nst:
            np = [p1[0]+1, p1[1]]
            nst = db[p1[0]+1][p1[1]]
            prob = [[False, np]]
        elif db[p1[0]+1][p1[1]] == nst:
            np = [p1[0]+1, p1[1]]
            nst = db[p1[0]+1][p1[1]]
            prob.append([False, np])
    if p1[1] - 1 in range(n):
        if 0 <= db[p1[0]][p1[1]-1]:
            np = [p1[0], p1[1] - 1]
            if db[p1[0]][p1[1]-1] < nst:
                nst = db[p1[0]][p1[1] - 1]
                prob = [[False, np]]
            elif db[p1[0]][p1[1] - 1] == nst:
                prob.append([False, np])
    if p1[1] + 1 in range(n):
        if 0 <= db[p1[0]][p1[1]+1]:
            np = [p1[0], p1[1]+1]
            if db[p1[0]][p1[1]+1] < nst:
                nst = db[p1[0]][p1[1] + 1]
                prob = [[False, np]]
            elif db[p1[0]][p1[1]+1] == nst:
                prob.append([False, np])
    db = [[-1 for i in range(n)] for j in range(n)]
    digitalize(f2[0], f2[1], b, db)
    oist = db[p2[0]][p2[1]]
    onst = db[p2[0]][p2[1]]
    nb = [[b[i][j] for j in range(n)] for i in range(n)]
    if bricks > 0:
       for i in range(n-1):
           for j in range(n-1):
               if b[i][j] == 0 and b[i][j+1] == 0 and p1 not in [[i, j], [i, j+1]] and p2 not in [[i, j], [i, j+1]]:
                   b1 = [[b[i][j] for j in range(n)] for i in range(n)]
                   b1[i][j] = 1
                   b1[i][j+1] = 1
                   db = [[-1 for i in range(n)] for j in range(n)]
                   digitalize(f2[0], f2[1], b1, db)
                   if nst > ist + oist - db[p2[0]][p2[1]]:
                       nst = ist + oist - db[p2[0]][p2[1]]
                       prob = [[True, b1]]
                   elif nst == ist + oist - db[p2[0]][p2[1]]:
                       prob .append([True, b1])
               if b[i][j] == 0 and b[i+1][j] == 0 and p1 not in [[i, j], [i+1, j]] and p2 not in [[i, j], [i+1, j]]:
                   b1 = [[b[i][j] for j in range(n)] for i in range(n)]
                   b1[i][j] = 1
                   b1[i+1][j] = 1
                   db = [[-1 for i in range(n)] for j in range(n)]
                   digitalize(f2[0], f2[1], b1, db)
                   if nst > ist + oist - db[p2[0]][p2[1]]:
                       nst = ist + oist - db[p2[0]][p2[1]]
                       prob = [[True, b1]]
                   elif nst == ist + oist - db[p2[0]][p2[1]]:
                       prob.append([True, b1])
    return choice(prob)