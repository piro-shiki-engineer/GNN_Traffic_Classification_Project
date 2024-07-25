import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import networkx as nx
import osmnx as ox
from typing import Dict, Any


def visualize_graph(G: nx.MultiDiGraph, heatmap_values: Dict[Any, int], filepath: str) -> None:
    min_value, max_value = min(heatmap_values.values()), max(heatmap_values.values())
    normalized_heatmap_values = {
        node: (value - min_value) / (max_value - min_value) for node, value in heatmap_values.items()
    }

    opts = {
        "node_color": (0, 0, 0, 0.01),
        "node_size": 2,
        "bgcolor": (0, 0, 0, 0.0)
    }

    fig, ax = ox.plot_graph(G, show=False, close=False, save=True, filepath=filepath, **opts)

    cmap = LinearSegmentedColormap.from_list("custom_cmap", [(1, 1, 1, 0.2), (0.9, 0.2, 0.2, 1)], N=1024)

    sc = ax.scatter(
        [G.nodes[node]["x"] for node in G.nodes],
        [G.nodes[node]["y"] for node in G.nodes],
        c=list(normalized_heatmap_values.values()),
        cmap=cmap,
        s=opts["node_size"],
    )

    plt.colorbar(sc, label="Accident Risk")
    plt.show()


if __name__ == "__main__":
    from data_loading import load_graph_and_data
    from data_preprocessing import preprocess_data
    from data_loading import load_accident_data

    place = 'Miyazaki,Miyazaki,Japan'
    G = load_graph_and_data(place)
    file_paths = [
        'data/2019_miyazaki_latlot.csv',
        'data/2020_miyazaki_latlot.csv',
        'data/2021_miyazaki_latlot.csv'
    ]
    df_accidents = load_accident_data(file_paths)
    G = preprocess_data(G, df_accidents)

    heatmap_values = {node: G.nodes[node]['number_of_accident'] for node in G.nodes}
    visualize_graph(G, heatmap_values, "results/road_net2.png")
