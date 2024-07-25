import torch
import torch_geometric.data
import torch.optim as optim
from data_preprocessing import preprocess_data
from data_loading import load_graph_and_data, load_accident_data
from models import GCN
from create_dataset import create_dataset
from torch.nn import Module
from torch.optim import Optimizer


def train(model: Module, train_loader: torch_geometric.data.DataLoader,
          optimizer: Optimizer, criterion: torch.nn.Module) -> float:
    model.train()
    total_loss = 0.0
    for data in train_loader:
        out = model(data.x, data.edge_index, data.batch)
        loss = criterion(out, data.y)
        loss.backward()
        optimizer.step()
        optimizer.zero_grad()
        total_loss += loss.item()
    return total_loss / len(train_loader)


def test(model: Module, loader: torch_geometric.data.DataLoader) -> float:
    model.eval()
    correct = 0
    for data in loader:
        out = model(data.x, data.edge_index, data.batch)
        pred = out.argmax(dim=1)
        correct += int((pred == data.y).sum())
    return correct / len(loader.dataset)


if __name__ == "__main__":
    place = 'Miyazaki,Miyazaki,Japan'
    G = load_graph_and_data(place)
    file_paths = [
        '../data/2019_miyazaki_latlot.csv',
        '../data/2020_miyazaki_latlot.csv',
        '../data/2021_miyazaki_latlot.csv'
    ]
    df_accidents = load_accident_data(file_paths)
    G = preprocess_data(G, df_accidents)

    # データの作成とデータローダーの準備
    dataset = create_dataset(G)
    train_loader = torch_geometric.data.DataLoader(dataset, batch_size=32, shuffle=True)
    test_loader = torch_geometric.data.DataLoader(dataset, batch_size=32, shuffle=True)

    # モデル、損失関数、オプティマイザの定義
    model = GCN(hidden_channels=64)
    criterion = torch.nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    # トレーニングとテストの実行
    for epoch in range(1, 201):
        loss = train(model, train_loader, optimizer, criterion)
        train_acc = test(model, train_loader)
        test_acc = test(model, test_loader)
        print(f'Epoch: {epoch}, Loss: {loss:.4f}, Train Acc: {train_acc:.4f}, Test Acc: {test_acc:.4f}')
