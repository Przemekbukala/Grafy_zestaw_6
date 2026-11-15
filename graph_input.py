"""Wczytywanie / losowanie digrafu dla PageRank."""

import random

from digraph import Digraph, random_digraph


def from_labeled_adjacency_list(text):
    """Format: `A: E, F, I`.

    Zwraca (g, labels): g to Digraph (wierzchołki 1..n),
    labels[v - 1] to nazwa wierzchołka v. 
    """
    rows = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        head, sep, rest = line.partition(":")
        if not sep:
            raise ValueError(f"brak ':' w wierszu {line!r}")
        rows.append((head.strip(), [x.strip() for x in rest.split(",") if x.strip()]))

    labels, index = [], {}

    def number(name):
        if name not in index:
            labels.append(name)
            index[name] = len(labels)
        return index[name]

    for head, _ in rows:
        number(head)
    for _, nbrs in rows:
        for name in nbrs:
            number(name)

    g = Digraph(len(labels))
    for head, nbrs in rows:
        for name in nbrs:
            g.add_edge(index[head], index[name])
    return g, labels


def read_graph(text):
    """Obsługuje format (`A: E, F`) i format (`1. 2 3`)."""
    if ":" in text:
        return from_labeled_adjacency_list(text)
    g = Digraph.from_adjacency_list(text)
    return g, [str(v) for v in range(1, g.n + 1)]


def dangling_nodes(g):
    """Wierzchołki bez krawędzi wychodzących"""
    return [v for v in g.adj_list if not g.adj_list[v]]


def random_digraph_without_dangling(n, p):
    if n < 2:
        raise ValueError("n musi być >= 2 (wierzchołek musi mieć dokąd wyjść)")
    g = random_digraph(n, p)
    for v in dangling_nodes(g):
        g.add_edge(v, random.choice([u for u in range(1, n + 1) if u != v]))
    return g


def format_labeled_adjacency_list(g, labels):
    """Lista sąsiedztwa w formacie: `A: E, F, I`."""
    return "\n".join(
        f"{labels[v - 1]}: " + ", ".join(labels[u - 1] for u in nbrs)
        for v, nbrs in g.adjacency_list()
    )
