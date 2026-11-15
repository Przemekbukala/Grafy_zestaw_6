#!/usr/bin/env python3
"""Zestaw 6, zad. 1: PageRank – błądzenie przypadkowe oraz metoda potęgowa."""

import argparse
import sys

from graph_input import (dangling_nodes, format_labeled_adjacency_list,
                         random_digraph_without_dangling, read_graph)
from kosaraju import components, kosaraju
from pagerank import D, EPS, STEPS, format_ranking, pagerank_power, pagerank_random_walk, ranking
from visualize import draw_digraph


def parse_args():
    ap = argparse.ArgumentParser(
        description="Ranking PageRank digrafu: błądzenie przypadkowe i metoda potęgowa"
    )
    ap.add_argument("-n", type=int, help="liczba wierzchołków losowego digrafu")
    ap.add_argument("-p", type=float, help="prawdopodobieństwo istnienia łuku, 0..1")
    ap.add_argument("--input", metavar="PLIK",
                    help="wczytaj digraf z pliku (format `A: E, F, I` lub `1. 2 3`)")
    ap.add_argument("--draw", metavar="PLIK.png",
                    help="zapisz rysunek digrafu (Graphviz)")
    args = ap.parse_args()
    if args.input is None and (args.n is None or args.p is None):
        ap.error("podaj -n i -p albo --input (sprawdz metode parse_args)")
    return args


def print_comparison(walk, power, labels):
    print("Porównanie metod (kolejność wg metody potęgowej):")
    print(f"  {'v':>3}  {'błądzenie':>10}  {'potęgowa':>10}  {'różnica':>10}")
    for v in ranking(power):
        print(f"  {labels[v - 1]:>3}  {walk[v]:10.6f}  {power[v]:10.6f}  {walk[v] - power[v]:+10.6f}")
    max_diff = max(abs(walk[v] - power[v]) for v in power)
    same = ranking(walk) == ranking(power)
    print(f"\nMaks. różnica: {max_diff:.6f}; kolejność rankingu "
          + ("identyczna" if same else "różni się!"))


def main():
    args = parse_args()

    if args.input is not None:
        text = sys.stdin.read() if args.input == "-" else open(args.input, encoding="utf-8").read()
        g, labels = read_graph(text)
    else:
        g = random_digraph_without_dangling(args.n, args.p)
        labels = [str(v) for v in range(1, g.n + 1)]

    dangling = dangling_nodes(g)
    if dangling:
        sys.exit("Błąd: wierzchołki bez krawędzi wychodzących (dangling nodes): "
                 + ", ".join(labels[v - 1] for v in dangling))

    print(f"Digraf: n = {g.n}, liczba łuków = {len(g.edges())}\n")
    print("Lista sąsiedztwa:")
    print(format_labeled_adjacency_list(g, labels))
    groups = components(kosaraju(g)[0])
    print("\nGraf jest silnie spójny" if len(groups) == 1
          else f"\nGraf nie jest silnie spójny ({len(groups)} silnie spójne składowe)")
    print()

    if args.draw:
        print(f"Zapisano rysunek: {draw_digraph(g, labels, args.draw)}\n")

    walk = pagerank_random_walk(g, STEPS, D)
    print(f"(a) Błądzenie przypadkowe z teleportacją, N = {STEPS} kroków:")
    print(format_ranking(walk, labels))
    print()

    power, iterations = pagerank_power(g, D, EPS)
    print(f"(b) Metoda potęgowa (iteracja wektora obsadzeń), zbieżność po {iterations} iteracjach:")
    print(format_ranking(power, labels))
    print()

    print_comparison(walk, power, labels)


if __name__ == "__main__":
    main()
