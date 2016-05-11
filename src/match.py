import scipy.io as si
import random
from ImageClass import *
from itertools import groupby, product, permutations, combinations
from LimitedPriorityQueue import *
from imgtools import *


def fpoint_hash_func_norm(x, y, desc):
    return int(floor(nl.norm(desc)/100))


def parse_mat(path):
    try:
        temp = si.loadmat(path)
        mat = temp["b"][0][0].transpose(2, 0, 1)
        points = temp["a"][0][0].astype(np.int32)

        ret = []

        for i in range(len(points)):
            ret.append(fpoint(int(points[i][0]), int(points[i][1]), mat[i], 1000))
        print("Parse {0} points from {1}".format(len(ret), path))
        return ret

    except Exception as e:
        print(e)
        return None


def match(target, ref):
    ret = LimitedPriorityQueue(30)
    for x in product(target, ref):
        ret.push(fppair(x))

    q3 = voting_filter(ret.queue)

    # Method 1: Average #
    mat = np.identity(3)

    # Translation
    sx, sy = 0, 0
    for pp in q3:
        sx += (pp.fp1.x - pp.fp2.x)
        sy += (pp.fp1.y - pp.fp2.y)

    sx /= len(q3)
    sy /= len(q3)

    mat[0, 2] = sx
    mat[1, 2] = sy

    # Rotation (not working :(( )
    # r = 0
    # count = 0
    # for v in combinations(q3, 2):
    #     v1 = v[0].fp1 - v[1].fp1
    #     v2 = v[0].fp2 - v[1].fp2
    #     _cos = (v1.x * v2.x + v1.y * v2.y) / (v1.length() * v2.length())
    #     r += acos(_cos)
    #     count += 1
    # c = cos(r/count)
    # s = sin(r/count)
    #
    #
    # mat[0,0] = c
    # mat[0,1] = s
    # mat[1,0] = -s
    # mat[1,1] = c

    print("Matching with inlier cost = {0}".format(avg_distance(q3, mat)))

    return mat, q3


def distance_cost(fpp, mat):
    fp1 = fpp.fp1
    m = fpp.fp2.transform(mat)
    # return sqrt((m[0] - fp2.x) * (m[0] - fp2.x) + (m[1] - fp2.y) * (m[1] - fp2.y))
    return abs(m[0] - fp1.x) + abs(m[1] - fp1.y)


def avg_distance(queue, mat, thr=50):
    count = 0
    cost = 0
    q = []
    for pp in queue:
        count += 1
        cost += distance_cost(pp, mat)

    return cost/count


def voting_filter(q):
    key1x = lambda x: x.fp1.x
    key1y = lambda x: x.fp1.y
    key2x = lambda x: x.fp2.x
    key2y = lambda x: x.fp2.y

    q2 = []
    q3 = []
    for x, gx in groupby(sorted(q, key=key1x), key=key1x):
        for y, gy in groupby(sorted(gx, key=key1y), key=key1y):
            g = list(gy)
            if len(g) == 1:
                q2 = q2 + g
    for x, gx in groupby(sorted(q2, key=key2x), key=key2x):
        for y, gy in groupby(sorted(gx, key=key2y), key=key2y):
            g = list(gy)
            if len(g) == 1:
                q3 = q3 + g
    return q3