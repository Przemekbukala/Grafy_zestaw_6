import math
import random

D = 0.2           # prawdopodobieństwo teleportacji
STEPS = 1_000_000  # liczba kroków błądzenia przypadkowego
EPS = 1e-9         # próg zbieżności metody potęgowej


def pagerank_random_walk(g, steps=STEPS, d=D, start=None):
    """ Błądzenie przypadkowe z teleportacją."""
    vertices = list(g.adj_list)
    v = start if start is not None else random.choice(vertices)
    visits = {u: 0 for u in vertices}
    for _ in range(steps):
        if random.random() < d:
            v = random.choice(vertices)        # teleportacja
        else:
            v = random.choice(g.adj_list[v])   # przejście do sąsiedniego wierzchołka
        visits[v] += 1
    return {u: c / steps for u, c in visits.items()}


def google_matrix(g, d=D):
    """Macierz stochastyczna P[i][j] = (1 - d) * A[i][j] / d_i + d / n."""
    n = g.n
    a = g.adjacency_matrix()  # macierz sąsiedztwa
    p = []
    for i in range(n):
        out_deg = sum(a[i])   # stopień wyjściowy d_i czyli liczba krawędzi
        p.append([(1 - d) * a[i][j] / out_deg + d / n for j in range(n)])
    return p


def pagerank_power(g, d=D, eps=EPS, max_iter=10_000):
    """ metoda potęgowa
    Koniec => długość różnicy wektorów |p_{t+1} - p_t| < eps 
    """
    n = g.n
    pm = google_matrix(g, d)
    p = [1 / n] * n
    for t in range(1, max_iter + 1):
        q = [sum(p[i] * pm[i][j] for i in range(n)) for j in range(n)]
        diff = math.sqrt(sum((x - y) ** 2 for x, y in zip(q, p)))  # |p_{t+1} - p_t|
        p = q
        if diff < eps:
            break
    return {v: p[v - 1] for v in range(1, n + 1)}, t


def ranking(pr):
    """Wierzchołki posortowane od najważniejszego."""
    return sorted(pr, key=lambda v: (-pr[v], v))


def format_ranking(pr, labels):
    """I ==> PageRank = WARTOSC"""
    return "\n".join(f"{labels[v - 1]} ==> PageRank = {pr[v]:.6f}" for v in ranking(pr))
