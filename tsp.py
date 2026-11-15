"""Problem komiwojażera"""

import math
import random


def read_points(path):
    """w każdym wierszu `x y`"""
    points = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            if line.strip():
                x, y = line.split()[:2]
                points.append((float(x), float(y)))
    return points


def distance_matrix(points):
    """Graf pełny nieskierowany, gdzie  waga krawędzi = odległość euklidesowa"""
    return [[math.dist(p, q) for q in points] for p in points]


def cycle_length(cycle, dist):
    """d(P) = suma długości krawędzi cyklu (razem z krawędzią zamykającą)."""
    return sum(dist[cycle[k - 1]][cycle[k]] for k in range(len(cycle)))


def random_edge_pair(n):
    """Losuje krawędzie (a, b) = (P[i], P[i+1]) i (c, d) = (P[j], P[j+1]), i < j.
    """
    while True:
        i, j = random.randrange(n), random.randrange(n)
        if i > j:
            i, j = j, i
        if j - i >= 2 and not (i == 0 and j == n - 1):
            return i, j


def two_opt(cycle, i, j):
    """Zamiana (a, b), (c, d) na (a, c), (b, d)"""
    cycle[i + 1:j + 1] = cycle[i + 1:j + 1][::-1]


def two_opt_delta(cycle, i, j, dist):
    """d(P_new) - d(P) dla ruchu 2-opt  zmieniają się tylko dwie krawędzie."""
    n = len(cycle)
    a, b = cycle[i], cycle[i + 1]
    c, d = cycle[j], cycle[(j + 1) % n]
    return dist[a][c] + dist[b][d] - dist[a][b] - dist[c][d]



def cooling_quadratic():
    for i in range(100, 0, -1):
        yield 0.001 * i * i


def cooling_linear():
    for t in range(50, 0, -1):
        yield float(t)


def cooling_exponential(t0=10.0, alpha=0.95, t_min=1e-3):
    t = t0
    while t >= t_min:
        yield t
        t *= alpha


COOLING = {
    "quadratic": cooling_quadratic,
    "linear": cooling_linear,
    "exponential": cooling_exponential,
}


def simulated_annealing(dist, start_cycle, max_it, cooling="quadratic"):
    """
    Zwraca (P, d(P)).
    """
    p = list(start_cycle)
    n = len(p)
    for t in COOLING[cooling]():                    
        for _ in range(max_it):                     
            i, j = random_edge_pair(n)              # (a, b) oraz (c, d)
            delta = two_opt_delta(p, i, j, dist)    # d(P_new) - d(P)
            if delta < 0:                           # krótszy cykl => akceptujemy
                two_opt(p, i, j)
            elif random.random() < math.exp(-delta / t):  # dłuższy => z prawd. exp(-Δ/T)
                two_opt(p, i, j)
    return p, cycle_length(p, dist)


def read_cycle(path):
    """Cykl zapisany przez `write_cycle`."""
    with open(path, encoding="utf-8") as f:
        return [int(line) for line in f if line.strip()]


def write_cycle(path, cycle):
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(map(str, cycle)) + "\n")
