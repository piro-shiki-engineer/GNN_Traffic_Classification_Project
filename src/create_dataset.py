import torch
import torch_geometric.data
from torch_geometric.data import Data
import osmnx as ox
import networkx as nx
from typing import List


def create_dataset(G: nx.MultiDiGraph) -> List[torch_geometric.data.Data]:
    dataset = []

    for node in G.nodes():
        # 隣接ノードの取得
        neighbors = list(G.neighbors(node))
        neighbors.append(node)  # 自分自身を含む

        # サブグラフの作成
        subgraph = G.subgraph(neighbors)

        # ノード特徴量の取得
        x = []
        for n in subgraph.nodes(data=True):
            x.append([n[1]['x'], n[1]['y'], n[1]['number_of_accident']])
        x = torch.tensor(x, dtype=torch.float)

        # エッジの取得
        edge_index = []
        for edge in subgraph.edges():
            edge_index.append([neighbors.index(edge[0]), neighbors.index(edge[1])])
        edge_index = torch.tensor(edge_index, dtype=torch.long).t().contiguous()

        # ラベルの取得
        y = torch.tensor([G.nodes[node]['number_of_accident']], dtype=torch.long)

        # データオブジェクトの作成
        data = Data(x=x, edge_index=edge_index, y=y)
        dataset.append(data)

    return dataset
