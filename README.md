## Wymagania

```bash
sudo apt install graphviz python3-graphviz python3-matplotlib
```


## Zadanie 1 – PageRank

```bash
python3 main_pagerank.py --input PLIK [--draw PLIK.png]
python3 main_pagerank.py -n N -p P [--draw PLIK.png]
```

| Opcje | Znaczenie |
|---|---|
| `--input PLIK` | wczytuje digraf z pliku: format `A: E, F, I`  albo `1. 2 3` |
| `-n`, `-p` | losowy digraf G(n, p); wierzchołkom bez łuków wychodzących dopisywany jest jeden łuk |
| `--draw PLIK.png` | rysunek digrafu|

Parametry algorytmów są stałymi w `pagerank.py`:
`D = 0.15` (prawdopodobieństwo teleportacji), `STEPS = 1_000_000` (liczba kroków błądzenia
przypadkowego), `EPS = 1e-9` (próg zbieżności metody potęgowej).

### Przykład

```bash
python3 main_pagerank.py --input example_graph.txt --draw pagerank_graf.png
```

## Zadanie 2 – Problem komiwojażera 


```bash
python3 main_tsp.py [--input xqf131.dat] [--max-it MAX_IT] [--cooling quadratic|linear|exponential]
                    [--runs R] [--start-cycle PLIK] [--save-cycle PLIK] [--output PLIK.png] [--show]
```

| Opcje | Znaczenie |
|---|---|
| `--max-it` | `MAX_IT`, liczba prób dla jednej temperatury (domyślnie 100000) |
| `--cooling` | `quadratic`: `T = 0.001·i²`, i = 100…1; `linear`: T = 50…1; `exponential`: T ← 0.95·T |
| `--runs` | liczba powtórzeń całej procedury; każde kolejne startuje od najlepszego dotąd cyklu |
| `--start-cycle` | cykl startowy z pliku |
| `--save-cycle` | zapis najlepszego cyklu |
| `--output`, `--show` | wykres (a) cykl początkowy, (b) cykl wyjściowy|

### Przykład

```bash
python3 main_tsp.py --runs 10 --max-it 200000
```

```
Cykl początkowy o długości: 4705.907
  przebieg 1/10: długość = 579.654  (16.8 s)  <- nowy najlepszy
  ...
  przebieg 6/10: długość = 567.292  (17.9 s)  <- nowy najlepszy
  ...
Cykl wyjściowy. Długość cyklu: 567.292
```

Gotowy wynik jest w plikach `tsp_cykl.png` i `najlepszy_cykl.txt` (567.292; w input_6.pdf: 567.203).

### Jak to działa (Algorytm 1 z alg_6.pdf)

1. Cykl startowy: kolejność punktów z pliku.
2. Pętla chłodzenia po T, a w niej `MAX_IT` razy:
   * losujemy krawędzie `(a, b) = (P[i], P[i+1])` i `(c, d) = (P[j], P[j+1])`, różne i niesąsiednie;
   * ruch 2-opt: zamiana na `(a, c)`, `(b, d)`, czyli odwrócenie fragmentu `b … c`;
   * jeśli `d(P_new) < d(P)`, akceptujemy; w przeciwnym razie akceptujemy z prawdopodobieństwem
     `exp(−(d(P_new) − d(P)) / T)` (Metropolis–Hastings).
3. `d(P_new) − d(P)` liczymy tylko z 4 zmienianych krawędzi, a 2-opt wykonujemy dopiero przy
   akceptacji. Wynik jest taki sam, jak przy budowaniu całego `P_new`, a działa znacznie szybciej.

