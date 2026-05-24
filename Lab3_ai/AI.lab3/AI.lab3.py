import numpy as np
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import linkage, fcluster

# Етап 2: Згенерувати тестову послідовність N >= 1000
def generate_data(N=1000):
   # np.random.seed(42)
    return np.random.rand(N, 2)

# Етап 3: Допоміжна функція для обчислення міри віддалі
def euclidean_distance(point1, point2):
    return np.sqrt(np.sum((point1 - point2) ** 2))

# Етап 4: Допоміжна функція для алгоритму K-means
def run_kmeans(data, k, max_iters=100):
    # Випадкові початкові центроїди
    centroids = data[np.random.choice(data.shape[0], k, replace=False)]
    labels = np.zeros(data.shape[0])
    
    for _ in range(max_iters):
        # Призначаємо точки до найближчого центроїда
        for i, point in enumerate(data):
            distances = [euclidean_distance(point, c) for c in centroids]
            labels[i] = np.argmin(distances)
            
        # Перераховуємо центроїди
        new_centroids = np.array([data[labels == j].mean(axis=0) if len(data[labels == j]) > 0 else centroids[j] for j in range(k)])
        
        # Якщо центри не змінилися - зупиняємось
        if np.allclose(centroids, new_centroids):
            break
        centroids = new_centroids
        
    return labels, centroids

# Етап 5: Допоміжна функція для Ієрархічної кластеризації
def run_hierarchical(data, k):
    # linkage - злиття кластерів
    Z = linkage(data, method='ward')
    # fcluster - отримує рівно k кластерів
    labels = fcluster(Z, t=k, criterion='maxclust') - 1 
    
    centroids = np.array([data[labels == j].mean(axis=0) for j in range(k)])
    return labels, centroids

# Етап 7 (частина 1): Функція оцінки якості (середньо-зважене)
def calculate_quality(data, labels, centroids, k):
    total_error = 0
    for i in range(k):
        cluster_points = data[labels == i]
        for point in cluster_points:
            total_error += euclidean_distance(point, centroids[i])**2
    # Середнє значення похибки на одну точку
    return total_error / len(data)

# Етап 6: Безпосередньо виконати кластеризацію та порівняти
if __name__ == "__main__":
    N = 5000
    K = 6
    
    X = generate_data(N)
    
    # Виконуємо K-means
    kmeans_labels, kmeans_centers = run_kmeans(X, K)
    
    # Виконуємо Ієрархічну кластеризацію
    hierarchical_labels, hierarchical_centers = run_hierarchical(X, K)
    
    # Етап 7 (частина 2): Порівняння результатів
    kmeans_score = calculate_quality(X, kmeans_labels, kmeans_centers, K)
    hierarchical_score = calculate_quality(X, hierarchical_labels, hierarchical_centers, K)
    
    print("=== Результати порівняння алгоритмів ===")
    print(f"Похибка (якість) K-means:       {kmeans_score:.5f}")
    print(f"Похибка (якість) Ієрархічного:  {hierarchical_score:.5f}")
    
    # Візуалізація
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    ax1.scatter(X[:, 0], X[:, 1], c=kmeans_labels, cmap='viridis', s=10)
    ax1.scatter(kmeans_centers[:, 0], kmeans_centers[:, 1], c='red', marker='X', s=100, edgecolors='black')
    ax1.set_title(f'Метод K-середніх\nПохибка: {kmeans_score:.4f}')
    
    ax2.scatter(X[:, 0], X[:, 1], c=hierarchical_labels, cmap='plasma', s=10)
    ax2.scatter(hierarchical_centers[:, 0], hierarchical_centers[:, 1], c='red', marker='X', s=100, edgecolors='black')
    ax2.set_title(f'Ієрархічна кластеризація\nПохибка: {hierarchical_score:.4f}')
    
    plt.show()