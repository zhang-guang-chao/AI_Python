import faiss
import numpy as np
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt

# 加载 Faiss 索引文件
index = faiss.read_index('/Users/zhangruize/Documents/project/work/langchain/Libraries_External/v1.0.0(检索pdf文本 生成向量)/faiss_index/index.faiss')

# 提取所有向量
vectors = []
for i in range(index.ntotal):
    vector = index.reconstruct(i)
    vectors.append(vector)
vectors = np.array(vectors)

# 使用 t-SNE 进行降维
tsne = TSNE(n_components=2, random_state=42)
vectors_2d = tsne.fit_transform(vectors)

# 可视化
plt.scatter(vectors_2d[:, 0], vectors_2d[:, 1])
plt.show()