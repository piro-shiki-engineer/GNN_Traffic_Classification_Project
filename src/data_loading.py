import pandas as pd
import osmnx as ox
import networkx as nx


def load_graph_and_data(place):
    G = ox.graph_from_place(place, network_type="drive")

    for node in G.nodes(data=True):
        node[1]['number_of_accident'] = 0

    return G


def load_accident_data(file_paths):
    dfs = [pd.read_csv(file_path, encoding='utf-8') for file_path in file_paths]
    df_accidents = pd.concat(dfs)

    return df_accidents


if __name__ == "__main__":
    place = 'Miyazaki,Miyazaki,Japan'
    G = load_graph_and_data(place)
    file_paths = [
        'data/2019_miyazaki_latlot.csv',
        'data/2020_miyazaki_latlot.csv',
        'data/2021_miyazaki_latlot.csv'
    ]
    df_accidents = load_accident_data(file_paths)
    print(G)
    print(df_accidents.head())