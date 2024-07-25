import networkx as nx
import numpy as np
import pandas as pd
from tqdm.auto import tqdm
from data_loading import load_graph_and_data, load_accident_data


class Intersection:
    def __init__(self, osmid: int, x: float, y: float):
        self.osmid = osmid
        self.x = x
        self.y = y
        self.accident_number = 0


def preprocess_data(G: nx.MultiDiGraph, df_accidents: pd.DataFrame, threshold: int = 0.1) -> nx.MultiDiGraph:
    intersections = []
    inter_x = [attribute['x'] for osmid, attribute in G.nodes(data=True)]
    inter_y = [attribute['y'] for osmid, attribute in G.nodes(data=True)]
    osmid = [osmid for osmid, attribute in G.nodes(data=True)]

    for tmp_osmid, tmp_x, tmp_y in zip(osmid, inter_x, inter_y):
        intersections.append(Intersection(tmp_osmid, tmp_x, tmp_y))

    accident_x, accident_y = [], []
    for data in tqdm(df_accidents.itertuples(), total=df_accidents.shape[0], desc="実行状況"):
        accident_x.append(data[3])
        accident_y.append(data[2])

    accident_x = np.array(accident_x)
    accident_y = np.array(accident_y)

    for i in tqdm(range(len(accident_x)), desc="発生した交差点判定"):
        x_check = np.abs(inter_x - accident_x[i]) < threshold
        y_check = np.abs(inter_y - accident_y[i]) < threshold
        xy_check = x_check * y_check  # 論理値の積でand処理

        if any(xy_check):
            match = np.where(xy_check == True)[0][0]  # タプル中のndarray中の値を取り出している
            intersections[match].accident_number += 1

    for num, inter in enumerate(intersections):
        if inter.accident_number != 0:
            G.nodes(data = True)[inter.osmid]['number_of_accident'] = inter.accident_number

    return G


if __name__ == "__main__":
    place = 'Miyazaki,Miyazaki,Japan'
    G = load_graph_and_data(place)
    file_paths = [
        'data/2019_miyazaki_latlot.csv',
        'data/2020_miyazaki_latlot.csv',
        'data/2021_miyazaki_latlot.csv'
    ]
    df_accidents = load_accident_data(file_paths)
    G = preprocess_data(G, df_accidents)
