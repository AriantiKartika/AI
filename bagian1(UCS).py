import heapq
import networkx as nx
import matplotlib.pyplot as plt

class Node:
    def __init__(self, state, parent=None, cost=0):
        self.state = state
        self.parent = parent
        self.cost = cost

    def __lt__(self, other):
        return self.cost < other.cost  

# UCS: f(n) = g(n)
def uniform_cost_search(graph, start, goal):
    frontier = []
    heapq.heappush(frontier, Node(start, None, 0))
    explored = set()

    while frontier:
        node = heapq.heappop(frontier)
        if node.state == goal:
            path = []
            total_cost = node.cost
            while node:
                path.append(node.state)
                node = node.parent
            return path[::-1], total_cost
        explored.add(node.state)
        for neighbor, cost in graph.get(node.state, []):
            if neighbor not in explored:
                heapq.heappush(frontier, Node(neighbor, node, node.cost + cost))
    return None, None

# Graph kota yang ada di Jawa
graph = {
    'Jakarta': [('Bandung', 150), ('Cirebon', 220)],
    'Bandung': [('Jakarta', 150), ('Cirebon', 130), ('Yogyakarta', 390)],
    'Cirebon': [('Jakarta', 220), ('Bandung', 130), ('Semarang', 240)],
    'Semarang': [('Cirebon', 240), ('Solo', 110), ('Yogyakarta', 120)],
    'Yogyakarta': [('Bandung', 390), ('Semarang', 120), ('Solo', 60)],
    'Solo': [('Yogyakarta', 60), ('Semarang', 110), ('Surabaya', 260), ('Malang', 300)],
    'Surabaya': [('Solo', 260), ('Malang', 100)],
    'Malang': [('Solo', 300), ('Surabaya', 100)]
}

# Input dari user
print("Daftar kota:", ', '.join(graph.keys()))
start = input("Masukkan kota asal: ").strip().title()
goal = input("Masukkan kota tujuan: ").strip().title()

if start not in graph or goal not in graph:
    print("Kota tidak ditemukan.")
    exit()

path, cost = uniform_cost_search(graph, start, goal)

if not path:
    print("Rute tidak ditemukan.")
    exit()

print(f"\nRute terbaik dari {start} ke {goal}:")
print(" -> ".join(path))
print(f"Total jarak: {cost} km")

# Visualisasi 
G = nx.Graph()
for city, neighbors in graph.items():
    for neighbor, weight in neighbors:
        G.add_edge(city, neighbor, weight=weight)

pos = nx.spring_layout(G, seed=42)

edge_colors = []
edge_widths = []
for u, v in G.edges():
    if u in path and v in path:
        idx_u = path.index(u)
        if (idx_u + 1 < len(path) and path[idx_u + 1] == v) or (idx_u - 1 >= 0 and path[idx_u - 1] == v):
            edge_colors.append("red")
            edge_widths.append(3.5)
        else:
            edge_colors.append("gray")
            edge_widths.append(1)
    else:
        edge_colors.append("gray")
        edge_widths.append(1)

plt.figure(figsize=(12, 8))
nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=1000,
        edge_color=edge_colors, width=edge_widths, font_weight='bold', font_size=10)

# Label jarak
edge_labels = {(u, v): f"{d['weight']} km" for u, v, d in G.edges(data=True)}
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)

# Tambahkan total jarak di bawah grafik
plt.title(f"Rute Terbaik dari {start} ke {goal} (UCS)", fontsize=14)
plt.text(0, -1.15, f"Total Jarak: {cost} km", fontsize=12, ha='center', color='darkblue')
plt.tight_layout()
plt.show()
