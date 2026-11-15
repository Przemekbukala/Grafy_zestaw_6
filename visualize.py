"""

* digraf PageRank = Graphviz 
* cykl komiwojażera = matplotlib
"""

from pathlib import Path


def draw_digraph(g, labels, filename):
    """Rysowanie digrafu  do pliku PNG; zwraca ścieżkę pliku."""
    from graphviz import Digraph as GvDigraph

    path = Path(filename)
    gv = GvDigraph(format=path.suffix.lstrip(".") or "png")
    gv.attr(rankdir="LR")
    gv.attr("node", shape="ellipse", style="filled",
            fillcolor="#d8d8f8", color="blue", fontname="Helvetica")
    gv.attr("edge", arrowsize="0.7")
    for v in g.adj_list:
        gv.node(labels[v - 1])
    for u, v in g.edges():
        gv.edge(labels[u - 1], labels[v - 1])
    return gv.render(str(path.with_suffix("")), cleanup=True)


def _plot_cycle(ax, points, cycle, caption):
    xs = [points[v][0] for v in cycle] + [points[cycle[0]][0]]
    ys = [points[v][1] for v in cycle] + [points[cycle[0]][1]]
    ax.plot(xs, ys, "-o", color="red", linewidth=0.8, markersize=3)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_aspect("equal", adjustable="box")
    ax.set_title(caption, y=-0.3)


def plot_cycles(points, start_cycle, start_len, best_cycle, best_len, filename, show=False):
    """ cykl początkowy,  cykl wyjściowy."""
    import matplotlib
    if not show:
        matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, (ax_a, ax_b) = plt.subplots(1, 2, figsize=(13, 4))
    _plot_cycle(ax_a, points, start_cycle,
                f" Cykl początkowy o długości: {start_len:.3f}")
    _plot_cycle(ax_b, points, best_cycle,
                f" Cykl wyjściowy. Długość cyklu: {best_len:.3f}")
    fig.subplots_adjust(left=0.05, right=0.98, top=0.97, bottom=0.22, wspace=0.12)
    fig.savefig(filename, dpi=150)
    if show:
        plt.show()
    plt.close(fig)
    return filename
