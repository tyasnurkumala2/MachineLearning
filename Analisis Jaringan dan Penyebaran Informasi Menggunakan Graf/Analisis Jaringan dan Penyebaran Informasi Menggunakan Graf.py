# -*- coding: utf-8 -*-
"""Copy of MidtermAJS_Code.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/19MddgYYr7K4Budn2DVxEk_eIIpX5MhnD

# Import Library
"""

# Commented out IPython magic to ensure Python compatibility.
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
import random
# %matplotlib inline

"""# Loading Datasets"""

# Memeriksa struktur file nodes
with open('fb-pages-food.nodes', 'r') as file:
    for _ in range(5):
        print(file.readline())

"""

*   id: ID unik untuk setiap halaman
*   name: nama halaman yang merupakan identitas publik
*   new_id: ID baru yang mungkin dihasilkan untuk penyesuaian data



"""

# Memeriksa struktur file nodes
with open('fb-pages-food.edges', 'r') as file:
    for _ in range(5):
        print(file.readline())

"""

*   source: ID halaman yang menjadi asal dari koneksi
*   target: ID halaman yang menjadi tujuan dari koneksi


Setiap baris menggambarkan hubungan antara dua halaman, dan secara keseluruhan, data ini menunjukkan bagaimana halaman-halaman tersebut terhubung dalam jaringan.
"""

edges = pd.read_csv('fb-pages-food.edges', sep=',', header=None, names=['source', 'target'])
nodes = pd.read_csv('fb-pages-food.nodes', sep=',', header=None, names=['id', 'name', 'new_id'])

nodes.head()

edges.head(100)

edges.shape

G = nx.from_pandas_edgelist(edges, 'source', 'target')

print(G)

G.nodes

G.edges()

"""# Visualization"""

nx.draw_networkx(G)

nx.draw_networkx(G, with_labels=True, node_size=100, width=2)

"""# Network Centrality Measures

## Degree Centrality
"""

G.nodes

degrees = dict(G.degree())
for node, degree in sorted(degrees.items()):
  print(f"Node {node} memiliki derajat {degree}")

degree_df = pd.DataFrame(degrees.items(), columns=['Node', 'Degree'])
print(degree_df)

degrees = [G.degree(n) for n in G.nodes()]
plt.hist(degrees, bins=range(min(degrees), max(degrees) + 1), edgecolor="black")
plt.xlabel("Degree")  # Menambahkan label sumbu x
plt.ylabel("Frequency")  # Menambahkan label sumbu y
plt.title("Degree Distribution of Graph")  # Menambahkan judul
plt.show()

# Menghitung Degree Centrality dari awal
n_nodes = len(G.nodes)
for node in G.nodes():
  print(node, G.degree(node)/(n_nodes-1))

"""Menghitung degree centrality secara manual yaitu dengan cara membagi degree dari suatu node dengan jumlah maksimal node lain yang dapat dihubungkan (n_nodes-1).

Pembagian ini menghasilkan nilai normalisasi, sehingga degree centrality berada dalam rentang 0 hingga 1.
"""

# menghitung degree centrality menggunakan networkx
degree_centrality = nx.degree_centrality(G)
degree_centrality_df = pd.DataFrame(list(degree_centrality.items()), columns=['node', 'degree_centrality'])
print(degree_centrality_df)

for node in sorted(degree_centrality, key=degree_centrality.get, reverse=True):
  print(node, degree_centrality[node])

"""Setelah menghitung degree centrality, kemudian kita urutkan berdasarkan node yang paling berpengaruh.

Dari perhitungan menggunakan degree centrality didapatkan bahwa node **265** merupakan yang paling berpengaruh diantara node lainnya dengan degree centrality sebesar **0.21647819063004847**.

## Closeness Centrality
"""

closeness_centrality = nx.closeness_centrality(G)

#Sort for identifying most inflential nodes
for node in sorted(closeness_centrality, key=closeness_centrality.get, reverse=True):
  print(node, closeness_centrality[node])

"""Node 265 memiliki closeness cnetrality yang lebih tinggi dibandingkan node lain. Sehingga, hal ini dapat berarti bahwa node 265 lebih "pusat dibandingkan node lain dalam konteks penyebaran informasi."""

nx.draw_networkx(G)

"""## Betweenness Centrality"""

betweenness_centrality = nx.betweenness_centrality(G)

#Sort for identifying most inflential nodes using closeness_centrality
for node in sorted(betweenness_centrality, key=betweenness_centrality.get, reverse=True):
  print(node, betweenness_centrality[node])

"""Berdasarkan perhitungan Betweenness Centrality di atas, hasil menunjukkan bahwa node 265 memiliki BC tertinggi di antara node lainnya. hal tersebut berarti node 265 dianggap memiliki peran penting sebagai "penghubung" dalam jaringan."""

nx.draw(G, with_labels=True)

"""## PageRank Centrality"""

pagerank = nx.pagerank(G, alpha=0.85)

pagerank_df = pd.DataFrame(list(pagerank.items()), columns=["Node", "PageRank"])
pagerank_df = pagerank_df.sort_values(by="PageRank", ascending=False)
print(pagerank_df)

"""Berdasarkan perhitungan PageRank di atas, hasil menunjukkan bahwa node 265 memiliki nilai PageRank tertinggi di antara node lainnya. hal tersebut berarti node 265 dianggap memiliki peran penting dan banyak dirujuk oleh node lainnya.

# Contagion
"""

# Membaca data dan membuat graph
G = nx.read_edgelist("fb-pages-food.edges", delimiter=",", nodetype=int)

# Probabilitas penyebaran
spread_prob = 0.1  # Probabilitas penyebaran (0.1 = 10%)

# Pilih seed nodes (misalnya, simpul dengan degree tertinggi)
seed_nodes = sorted(G.degree, key=lambda x: x[1], reverse=True)[:5]  # Ambil 5 simpul
seed_nodes = [node[0] for node in seed_nodes]  # Hanya ambil ID simpul


# Simulasi ICM
def independent_cascade(G, seeds, prob):
    # Set status awal semua simpul (False = non-aktif)
    active_nodes = set(seeds)  # Simpul aktif awal
    new_active = set(seeds)  # Simpul yang baru aktif
    all_activated = list(seeds)  # Riwayat aktivasi

    while new_active:
        current_active = set()  # Simpul yang aktif pada iterasi saat ini
        for node in new_active:
            neighbors = set(G.neighbors(node)) - active_nodes  # Tetangga yang belum aktif
            for neighbor in neighbors:
                if random.random() < prob:  # Penyebaran berhasil
                    current_active.add(neighbor)

        active_nodes.update(current_active)  # Update simpul aktif
        all_activated.extend(current_active)  # Simpan riwayat
        new_active = current_active  # Iterasi berikutnya

    return active_nodes, all_activated

# Jalankan simulasi
activated_nodes, activation_history = independent_cascade(G, seed_nodes, spread_prob)

# Output hasil
print(f"Seed Nodes: {seed_nodes}")
print(f"Total Activated Nodes: {len(activated_nodes)}")
print(f"Activation History: {activation_history}")

import matplotlib.pyplot as plt
pos = nx.spring_layout(G)

# Seed nodes
nx.draw_networkx_nodes(G, pos, nodelist=seed_nodes, node_color="red", node_size=200, label="Seed Nodes")
# Activated nodes
nx.draw_networkx_nodes(G, pos, nodelist=activation_history, node_color="green", node_size=50, label="Activated Nodes")
# Labeling
labels = {node: str(node) for node in seed_nodes}
nx.draw_networkx_labels(G, pos, labels, font_size=8, font_color="white")

plt.legend()
plt.show()

"""Seed nodes menunjukkan node awal yang digunakan untuk memulai proses tertentu di jaringan. Node ini merupakan node yang memiliki peran penting, seperti memulai penyebaran informasi atau tren. Seed nodes diambil dari node dengan degree centrality tertinggi. Activated node adalah node yang "diaktifkan" sebagai hasil dari proses yang dimulai oleh seed nodes seperti penyebaran ide."""

import networkx as nx
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Membaca file nodes dan edges
nodes_file = "fb-pages-food.nodes"
edges_file = "fb-pages-food.edges"

# Membaca file nodes
nodes_df = pd.read_csv(nodes_file)
edges_df = pd.read_csv(edges_file, sep="\s+", header=None, names=["Source", "Target"])

# Membuat graf dari nodes dan edges
G = nx.DiGraph()

# Menambahkan simpul ke graf dengan atribut dari file nodes
for _, row in nodes_df.iterrows():
    G.add_node(row['id'], **row.to_dict())

# Menambahkan edge ke graf
for _, row in edges_df.iterrows():
    G.add_edge(row['Source'], row['Target'])

# Periksa apakah graf terhubung, gunakan komponen terhubung terbesar
if not nx.is_connected(G.to_undirected()):
    largest_cc = max(nx.connected_components(G.to_undirected()), key=len)
    G = G.subgraph(largest_cc).copy()

# Hitung eigenvalue terbesar matriks adjacency graf
A = nx.to_numpy_array(G)
largest_eigenvalue = max(np.linalg.eigvals(A).real)

# Tangani kasus eigenvalue nol
if largest_eigenvalue == 0:
    alpha = 0.01  # Tetapkan alpha kecil secara manual
else:
    alpha = 1 / largest_eigenvalue * 0.9  # Misalnya 90% dari batas atas

# Menghitung Katz Centrality dengan iterasi maksimal yang ditingkatkan
try:
    katz_centrality = nx.katz_centrality(G, alpha=alpha, beta=1.0, max_iter=10000, tol=1e-06)
except nx.PowerIterationFailedConvergence as e:
    print(f"Perhitungan Katz Centrality gagal: {e}")
    katz_centrality = {}

# Normalisasi Katz Centrality untuk visualisasi
if katz_centrality:
    max_katz = max(katz_centrality.values())
    centrality_values = {node: value / max_katz for node, value in katz_centrality.items()}  # Normalisasi
    node_sizes = {node: 500 + 3000 * value for node, value in centrality_values.items()}  # Ukuran node
    node_colors = centrality_values  # Warna node berdasarkan centrality

    # Membatasi visualisasi ke subgraf (opsional)
    top_nodes = sorted(centrality_values, key=centrality_values.get, reverse=True)[:100]  # Pilih top 100 node
    subgraph = G.subgraph(top_nodes)

    # Tata letak graf
    pos = nx.spring_layout(subgraph, seed=42)

    # Visualisasi graf
    plt.figure(figsize=(15, 10))
    nx.draw_networkx_edges(subgraph, pos, edge_color='gray', alpha=0.6)
    nodes = nx.draw_networkx_nodes(
        subgraph, pos,
        node_size=[node_sizes[n] for n in subgraph.nodes],
        cmap=plt.cm.viridis,
        node_color=[node_colors[n] for n in subgraph.nodes],
        alpha=0.9
    )
    nx.draw_networkx_labels(subgraph, pos, font_size=8, font_color="black")
    sm = plt.cm.ScalarMappable(cmap=plt.cm.viridis,
                               norm=plt.Normalize(vmin=min(centrality_values.values()), vmax=max(centrality_values.values())))
    sm.set_array([])
    plt.colorbar(sm, ax=plt.gca(), label='Katz Centrality')
    plt.title("Visualisasi Katz Centrality (Top 100 Nodes)")
    plt.axis("off")
    plt.show()
else:
    print("Gagal menghitung Katz Centrality. Pastikan parameter alpha sesuai.")

"""Node dengan label "NaN":

Node berwarna kuning dengan label "NaN" menandakan bahwa nilai Katz Centrality untuk node tersebut tidak terdefinisi (Not a Number). Ini terjadi ketika algoritma Katz Centrality gagal menghitung nilai untuk node tersebut, kemungkinan besar karena:
Node isolasi: Node tersebut tidak memiliki edge keluar atau masuk, sehingga tidak ada pengaruh yang dapat dihitung.
Kesalahan iterasi: Nilai Katz Centrality mungkin tidak terkonsolidasi selama iterasi karena parameter tertentu (seperti nilai alpha yang terlalu besar atau graf tidak cocok untuk algoritma ini).
Node lainnya:

Node dengan nilai 0.276 menunjukkan Katz Centrality berhasil dihitung untuk node tersebut, meskipun relatif rendah dibandingkan maksimum (1.0, yang diwakili oleh colorbar).
Struktur graf:

Hanya terdapat dua node dalam subgraf yang divisualisasikan (mungkin Anda sedang melihat bagian kecil dari keseluruhan graf). Node "NaN" mungkin adalah node isolasi, sedangkan node dengan nilai 0.276 memiliki koneksi yang valid.

"""

import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt

# Membaca file nodes dan edges
nodes_file = "fb-pages-food.nodes"
edges_file = "fb-pages-food.edges"

# Membaca file nodes
nodes_df = pd.read_csv(nodes_file)
edges_df = pd.read_csv(edges_file, sep="\s+", header=None, names=["Source", "Target"])

# Membuat graf dari nodes dan edges
G = nx.DiGraph()

# Menambahkan simpul ke graf dengan atribut dari file nodes
for _, row in nodes_df.iterrows():
    G.add_node(row['id'], **row.to_dict())

# Menambahkan edge ke graf
for _, row in edges_df.iterrows():
    G.add_edge(row['Source'], row['Target'])

# Menghitung Katz Centrality
alpha = 0.1  # Faktor peluruhan
beta = 1.0   # Konstanta bias
katz_centrality = nx.katz_centrality(G, alpha=alpha, beta=beta)

# Normalisasi Katz Centrality untuk visualisasi
max_katz = max(katz_centrality.values())
centrality_values = {node: value / max_katz for node, value in katz_centrality.items()}  # Normalisasi
node_sizes = {node: 500 + 3000 * value for node, value in centrality_values.items()}  # Ukuran node
node_colors = centrality_values  # Warna node berdasarkan centrality

# Membatasi visualisasi ke subgraf (opsional)
top_nodes = sorted(centrality_values, key=centrality_values.get, reverse=True)[:100]  # Pilih top 100 node
subgraph = G.subgraph(top_nodes)

# Tata letak graf
pos = nx.spring_layout(subgraph, seed=42)  # Gunakan tata letak untuk subgraf

# Visualisasi graf
plt.figure(figsize=(15, 10))

# Menggambar edges
nx.draw_networkx_edges(subgraph, pos, edge_color='gray', alpha=0.6)

# Menggambar nodes
nodes = nx.draw_networkx_nodes(
    subgraph, pos,
    node_size=[node_sizes[n] for n in subgraph.nodes],  # Ambil ukuran node dari dictionary
    cmap=plt.cm.viridis,
    node_color=[node_colors[n] for n in subgraph.nodes],  # Ambil warna node dari dictionary
    alpha=0.9
)

# Menambahkan label (opsional: hanya pada top nodes)
nx.draw_networkx_labels(subgraph, pos, font_size=8, font_color="black")

# Menambahkan colorbar
sm = plt.cm.ScalarMappable(cmap=plt.cm.viridis,
                           norm=plt.Normalize(vmin=min(centrality_values.values()), vmax=max(centrality_values.values())))
sm.set_array([])

# Berikan parameter ax agar colorbar dapat dihubungkan dengan visualisasi
plt.colorbar(sm, ax=plt.gca(), label='Katz Centrality')

# Menampilkan graf
plt.title("Visualisasi Katz Centrality (Top 100 Nodes)")
plt.axis("off")
plt.show()

"""Analisis Visualisasi Katz Centrality
Gambar menunjukkan visualisasi Katz Centrality untuk 100 node teratas.

Keterangan:

Warna: Warna setiap lingkaran menunjukkan nilai Katz Centrality, dengan warna yang lebih terang menunjukkan nilai yang lebih tinggi.
Ukuran Lingkaran: Ukuran setiap lingkaran menunjukkan nilai Katz Centrality, dengan lingkaran yang lebih besar menunjukkan nilai yang lebih tinggi.
Teks di dalam Lingkaran: Teks "nan" menunjukkan bahwa node tersebut tidak memiliki nilai Katz Centrality.
Kesimpulan:

Visualisasi ini menunjukkan bahwa beberapa node memiliki nilai Katz Centrality yang tinggi, sementara yang lain memiliki nilai yang lebih rendah.
Node dengan nilai Katz Centrality yang tinggi cenderung berada di pusat lingkaran.
Kemungkinan besar terdapat beberapa node yang memiliki nilai Katz Centrality yang sama, sehingga diberi warna yang sama dan digambarkan sebagai lingkaran yang saling tumpang tindih.
Informasi lebih lanjut diperlukan untuk menentukan makna dari nilai Katz Centrality yang ditampilkan dalam visualisasi ini.
Catatan:

Katz Centrality adalah metrik yang mengukur pengaruh sebuah node dalam jaringan berdasarkan koneksi langsung dan tidak langsungnya dengan node lain.
Nilai Katz Centrality yang tinggi menunjukkan bahwa node tersebut memiliki pengaruh yang besar dalam jaringan.
Rekomendasi:

Untuk mendapatkan pemahaman yang lebih baik, perlu dilakukan analisis lebih lanjut mengenai data yang digunakan untuk membuat visualisasi ini.
Analisis tersebut harus mencakup identifikasi node dengan nilai Katz Centrality yang tinggi dan hubungannya dengan node lain dalam jaringan.

**Kesimpulan dan Perbandingan kedua percobaan**

Perbandingan:
Gambar pertama memperlihatkan bahwa jaringan besar memiliki masalah dalam data Katz Centrality (banyak nilai "NaN").
Gambar kedua adalah subset jaringan sederhana yang memperlihatkan Katz Centrality bekerja normal, tetapi hanya untuk dua node.


Kesimpulan Akhir:
Jaringan besar (Gambar 1) memiliki isu data yang signifikan sehingga analisis Katz Centrality tidak dapat dilakukan secara efektif.
Jaringan kecil (Gambar 2) menunjukkan Katz Centrality dapat diukur, tetapi jaringan terlalu sederhana untuk menyimpulkan pola yang signifikan.
Disarankan untuk memperbaiki data awal (misalnya, mengatasi masalah "NaN") sebelum menganalisis jaringan yang lebih besar.

**EPIDERMIC MODEL**

**Membaca File dan Memuat Graf**
"""

import networkx as nx

# Fungsi untuk membaca file dan memuat graf
def load_graph_from_file(file_path):
    # Membaca graf dari file dalam format adjacency list
    G = nx.read_adjlist(file_path)
    return G

# Misalkan file berada di 'fb-pages-food.nodes' di direktori saat ini
file_path = "fb-pages-food.nodes"
G = load_graph_from_file(file_path)

# Menampilkan informasi tentang graf untuk memastikan data telah dimuat
print(f"Jumlah node: {G.number_of_nodes()}")
print(f"Jumlah edge: {G.number_of_edges()}")

"""**Inisialisasi Status**"""

import random

# Fungsi untuk menginisialisasi status setiap node
def initialize_status(G, initial_infected):
    status = {}
    for node in G.nodes():
        status[node] = 'S'  # Semua node mulai sebagai susceptible
    infected_nodes = random.sample(list(G.nodes()), initial_infected)
    for node in infected_nodes:
        status[node] = 'I'  # Menetapkan beberapa node sebagai terinfeksi
    return status

# Misalkan kita menginisialisasi 5 node yang terinfeksi
initial_infected = 5
status = initialize_status(G, initial_infected)

# Menampilkan beberapa status awal untuk memastikan inisialisasi
for node in list(status.keys())[:10]:  # Menampilkan status 10 node pertama
    print(f"Node {node}: {status[node]}")

"""**Simulasi Penyebaran Penyakit dalam Satu Langkah**"""

def step_SIR(G, status, beta, gamma):
    new_status = status.copy()

    for node in G.nodes():
        if status[node] == 'I':
            # Jika node terinfeksi, ia akan sembuh dengan probabilitas gamma
            if random.random() < gamma:
                new_status[node] = 'R'  # Menjadi sembuh
            # Penyebaran penyakit ke tetangga yang rentan
            for neighbor in G.neighbors(node):
                if status[neighbor] == 'S' and random.random() < beta:
                    new_status[neighbor] = 'I'  # Menyebar ke yang rentan
    return new_status

# Misalkan kita menggunakan beta = 0.1 dan gamma = 0.05
beta = 0.1  # Probabilitas penularan
gamma = 0.05  # Probabilitas kesembuhan

# Simulasi satu langkah SIR
new_status = step_SIR(G, status, beta, gamma)

# Menampilkan beberapa status setelah satu langkah
for node in list(new_status.keys())[:10]:  # Menampilkan status 10 node pertama
    print(f"Node {node}: {new_status[node]}")

"""** Menjalankan Simulasi Selama Beberapa Langkah**"""

def simulate_SIR(G, initial_infected, beta, gamma, steps):
    status = initialize_status(G, initial_infected)
    susceptible, infected, recovered = [], [], []

    # Menyimpan status dalam setiap langkah
    for _ in range(steps):
        s = sum(1 for state in status.values() if state == 'S')
        i = sum(1 for state in status.values() if state == 'I')
        r = sum(1 for state in status.values() if state == 'R')

        susceptible.append(s)
        infected.append(i)
        recovered.append(r)

        status = step_SIR(G, status, beta, gamma)  # Melakukan langkah simulasi SIR

    return susceptible, infected, recovered

# Menjalankan simulasi selama 100 langkah
steps = 100
susceptible, infected, recovered = simulate_SIR(G, initial_infected, beta, gamma, steps)

# Menampilkan hasil jumlah individu setiap status setelah simulasi
print(f"Susceptible: {susceptible[-1]}")
print(f"Infected: {infected[-1]}")
print(f"Recovered: {recovered[-1]}")

"""**Menampilkan Grafik Hasil Simulasi**"""

import matplotlib.pyplot as plt

# Fungsi untuk memplot hasil simulasi
def plot_SIR(susceptible, infected, recovered):
    plt.figure(figsize=(10, 6))
    plt.plot(susceptible, label="Susceptible")
    plt.plot(infected, label="Infected")
    plt.plot(recovered, label="Recovered")
    plt.xlabel("Time Steps")
    plt.ylabel("Population Count")
    plt.title("SIR Model Simulation")
    plt.legend()
    plt.show()

# Menampilkan grafik hasil simulasi
plot_SIR(susceptible, infected, recovered)

"""Penjelasan Komponen:
Sumbu X (Time Steps):

Merepresentasikan waktu dalam langkah diskret. Setiap langkah menunjukkan perkembangan simulasi selama periode tertentu.
Sumbu Y (Population Count):

Merepresentasikan jumlah individu dalam populasi yang berada dalam salah satu dari tiga kategori: Susceptible, Infected, atau Recovered.
Garis-Garis dalam Grafik:

Biru (Susceptible): Populasi yang rentan terhadap infeksi. Tampaknya jumlah populasi rentan menurun sedikit seiring waktu, tetapi tetap mendominasi jumlah total populasi.
Oranye (Infected): Populasi yang terinfeksi. Jumlahnya sangat kecil dibandingkan dengan total populasi dan tampaknya hanya sedikit meningkat sebelum stabil.
Hijau (Recovered): Populasi yang sembuh. Jumlahnya juga sangat kecil tetapi sedikit meningkat seiring waktu.
Interpretasi:
Pada simulasi ini, sebagian besar populasi tetap berada dalam kategori susceptible sepanjang waktu, dengan hanya sedikit individu yang berpindah ke kategori infected atau recovered.
Tingkat infeksi tampaknya sangat rendah, menunjukkan bahwa model ini mensimulasikan penyebaran penyakit dengan tingkat penularan yang rendah atau sistem dengan intervensi yang sangat efektif (misalnya vaksinasi atau isolasi).
Kesimpulan:
Penyakit tidak menyebar secara signifikan dalam populasi.
Sebagian besar individu tetap tidak terinfeksi selama simulasi.
Hasil ini bisa terjadi jika model menggunakan parameter seperti tingkat kontak rendah, tingkat penularan rendah, atau tingkat pemulihan yang sangat tinggi.

**EIGENVECTOR**

**Membuat Graph**
"""

import networkx as nx
import matplotlib.pyplot as plt

# Membuat graf acak dengan 10 node dan probabilitas edge 0.3
G = nx.erdos_renyi_graph(10, 0.3)

# Menampilkan informasi graf
print(f"Jumlah node dalam graf: {G.number_of_nodes()}")
print(f"Jumlah edge dalam graf: {G.number_of_edges()}")

"""**Menampilkan Graf**"""

# Memvisualisasikan graf
nx.draw(G, with_labels=True, node_color='skyblue', font_weight='bold')
plt.title("Graf Acak dengan 10 Node")
plt.show()

"""**Menghitung Eigenvector Centrality**"""

# Menghitung eigenvector centrality
eigenvector_centrality = nx.eigenvector_centrality(G)

# Menampilkan nilai centrality untuk setiap node
print("\nEigenvector Centrality:")
for node, centrality in eigenvector_centrality.items():
    print(f"Node {node}: {centrality:.4f}")

"""**Visualisasi Berdasarkan Eigenvector Centrality**"""

# Menentukan ukuran node berdasarkan nilai eigenvector centrality
node_sizes = [5000 * eigenvector_centrality[node] for node in G.nodes()]

# Memvisualisasikan graf dengan ukuran node berdasarkan centrality
nx.draw(G, with_labels=True, node_size=node_sizes, node_color='skyblue', font_weight='bold')
plt.title("Graf dengan Eigenvector Centrality")
plt.show()

"""Interpretasi:
Node Sentral:
Node 6, 4, dan 7 adalah node yang paling sentral dalam jaringan. Node-node ini memiliki koneksi ke banyak node penting lainnya dan mungkin memainkan peran kunci dalam penyebaran informasi atau pengaruh dalam graf ini.
Node Perifer:
Node seperti 1 dan 5 berada di pinggiran jaringan dan memiliki sedikit koneksi dengan node penting, sehingga kontribusi mereka dalam jaringan ini kecil.

Kesimpulan:
Gambar ini menunjukkan analisis Eigenvector Centrality, di mana node yang besar (seperti node 6) memainkan peran utama dalam jaringan karena koneksi mereka dengan node penting lainnya.
Node dengan ukuran kecil mungkin memiliki peran yang lebih marginal dalam struktur jaringan ini. Ini memberikan wawasan tentang bagaimana pengaruh atau informasi dapat mengalir dalam jaringan berdasarkan hubungan antar node.
"""