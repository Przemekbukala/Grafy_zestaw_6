#!/usr/bin/env python3
"""Zestaw 6, zad. 2: problem komiwojażera – symulowane wyżarzanie z ruchem 2-opt."""

import argparse
import random
import time

from tsp import (COOLING, cycle_length, distance_matrix, read_cycle, read_points,
                 simulated_annealing, write_cycle)
from visualize import plot_cycles


def parse_args():
    ap = argparse.ArgumentParser(
        description="Najkrótszy cykl Hamiltona (TSP) metodą symulowanego wyżarzania (2-opt)"
    )
    ap.add_argument("--input", metavar="PLIK", default="xqf131.dat",
                    help="plik ze współrzędnymi `x y`")
    ap.add_argument("--max-it", type=int, default=100_000,
                    help="MAX_IT – liczba iteracji dla jednej temperatury (domyślnie: 100000)")
    ap.add_argument("--cooling", choices=sorted(COOLING), default="quadratic",
                    help="schemat chłodzenia (domyślnie: T = 0.001 i^2 )")
    ap.add_argument("--runs", type=int, default=5,
                    help="ile razy powtórzyć wyżarzanie; każde kolejne startuje "
                         "od najlepszego dotąd cyklu (domyślnie: 5)")
    ap.add_argument("--start-cycle", metavar="PLIK",
                    help="cykl startowy z pliku (domyślnie: kolejność z pliku wejściowego)")
    ap.add_argument("--save-cycle", metavar="PLIK", default="najlepszy_cykl.txt",
                    help="gdzie zapisać najlepszy cykl (domyślnie: najlepszy_cykl.txt)")
    ap.add_argument("--output", metavar="PLIK.png", default="tsp_cykl.png",
                    help="plik z wykresem (domyślnie: tsp_cykl.png)")
    ap.add_argument("--show", action="store_true", help="pokaż wykres w oknie")
    ap.add_argument("--seed", type=int, help="ziarno generatora liczb losowych")
    return ap.parse_args()


def main():
    args = parse_args()
    try:
        import matplotlib 
    except ImportError:
        raise SystemExit("Brak biblioteki matplotlib: sudo apt install python3-matplotlib")
    if args.seed is not None:
        random.seed(args.seed)

    points = read_points(args.input)
    dist = distance_matrix(points)
    start = read_cycle(args.start_cycle) if args.start_cycle else list(range(len(points)))
    if sorted(start) != list(range(len(points))):
        raise SystemExit("Błąd: cykl startowy musi zawierać każdy punkt dokładnie raz")
    start_len = cycle_length(start, dist)

    print(f"Wczytano n = {len(points)} punktów z {args.input}")
    print(f"Chłodzenie: {args.cooling}, MAX_IT = {args.max_it}, powtórzeń: {args.runs}\n")
    print(f"Cykl początkowy o długości: {start_len:.3f}")

    best, best_len = start, start_len
    for run in range(1, args.runs + 1):
        t0 = time.perf_counter()
        cycle, length = simulated_annealing(dist, best, args.max_it, args.cooling)
        mark = ""
        if length < best_len:
            best, best_len = cycle, length
            mark = "  <- nowy najlepszy"
        print(f"  przebieg {run}/{args.runs}: długość = {length:.3f}"
              f"  ({time.perf_counter() - t0:.1f} s){mark}")

    print(f"\nCykl wyjściowy. Długość cyklu: {best_len:.3f}")
    write_cycle(args.save_cycle, best)
    print(f"Zapisano cykl: {args.save_cycle}")
    print(f"Zapisano wykres: {plot_cycles(points, start, start_len, best, best_len, args.output, args.show)}")


if __name__ == "__main__":
    main()
