import numpy as np
import matplotlib.pyplot as plt
import random
import json

# 1. Генерація карти
def generate_fresh_map(filename='map_data.json'):
    num_cities = random.randint(25, 35)
    
    coords = np.random.rand(num_cities, 2) * 100
    distances = np.zeros((num_cities, num_cities))
    
    for i in range(num_cities):
        for j in range(i + 1, num_cities):
            dist = random.randint(10, 100)
            distances[i][j] = dist
            distances[j][i] = dist

    with open(filename, 'w') as f:
        json.dump({'coords': coords.tolist(), 'distances': distances.tolist()}, f)
    
    print(f"Згенеровано карту ({num_cities} міст) із хаотичними відстанями.\n")
    return coords, distances

# 2. Мурашиний алгоритм
def ant_colony_optimization(distances, num_ants, rho, alpha, beta, iterations=50):
    num_cities = len(distances)
    pheromone = np.ones((num_cities, num_cities))
    visibility = np.zeros((num_cities, num_cities))
    
    for i in range(num_cities):
        for j in range(num_cities):
            if i != j and distances[i][j] != 0:
                visibility[i][j] = 1.0 / distances[i][j]

    best_path = None
    best_length = float('inf')
    Q = 100 

    for _ in range(iterations):
        all_paths = []
        all_lengths = []

        for _ in range(num_ants):
            current_city = random.randint(0, num_cities - 1)
            path = [current_city]
            unvisited = set(range(num_cities))
            unvisited.remove(current_city)
            path_length = 0

            while unvisited:
                probs = []
                for city in unvisited:
                    p = (pheromone[current_city][city] ** alpha) * (visibility[current_city][city] ** beta)
                    probs.append((city, p))
                
                total_prob = sum(p for _, p in probs)
                
                if total_prob == 0:
                    next_city = random.choice(list(unvisited))
                else:
                    probs = [(c, p / total_prob) for c, p in probs]
                    r = random.random()
                    cumulative = 0
                    for c, p in probs:
                        cumulative += p
                        if r <= cumulative:
                            next_city = c
                            break
                
                path.append(next_city)
                path_length += distances[current_city][next_city]
                unvisited.remove(next_city)
                current_city = next_city

            path_length += distances[path[-1]][path[0]]
            all_paths.append(path)
            all_lengths.append(path_length)

            if path_length < best_length:
                best_length = path_length
                best_path = path

        pheromone = (1 - rho) * pheromone
        
        for path, length in zip(all_paths, all_lengths):
            for i in range(num_cities):
                from_city = path[i]
                to_city = path[(i + 1) % num_cities]
                pheromone[from_city][to_city] += Q / length
                pheromone[to_city][from_city] += Q / length 

    return best_path, int(best_length)

# 3. Побудова графіка
def plot_best_route(coords, path, best_length):
    plt.figure(figsize=(10, 8))
    
    for i in range(len(path)):
        start_pos = coords[path[i]]
        end_pos = coords[path[(i + 1) % len(path)]]
        plt.annotate("", xy=end_pos, xycoords='data', xytext=start_pos, textcoords='data',
                     arrowprops=dict(arrowstyle="->", color="blue", alpha=0.6, lw=1.5))

    plt.plot(coords[:, 0], coords[:, 1], 'ro', markersize=8, label="Міста")
    
    for i, (cx, cy) in enumerate(coords):
        plt.text(cx, cy + 1.5, str(i), fontsize=10, ha='center', fontweight='bold')

    start_city = path[0]
    plt.plot(coords[start_city][0], coords[start_city][1], 'g*', markersize=18, 
             markeredgecolor='black', label="Старт")

    finish_city = path[-1] 
    plt.plot(coords[finish_city][0], coords[finish_city][1], 'y*', markersize=18, 
             markeredgecolor='black', label="Фініш")

    plt.title(f"Найкращий маршрут (Довжина: {best_length})", fontsize=14, fontweight='bold')
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.legend()
    plt.show()

# Головний блок
if __name__ == "__main__":
    coords, distances = generate_fresh_map()

    simulations = [
        (20, 0.5, 1, 2, "База"),
        (5,  0.5, 1, 2, "Мало мурах"),
        (50, 0.5, 1, 2, "Багато мурах"),
        (20, 0.1, 1, 2, "Мале rho"),
        (20, 0.9, 1, 2, "Велике rho"),
        (20, 0.5, 1, 1, "alpha=beta"),
        (20, 0.5, 3, 1, "alpha > beta"),
        (20, 0.5, 1, 5, "beta > alpha"),
        (10, 0.3, 2, 3, "Мікс 1"),
        (30, 0.7, 1, 4, "Мікс 2")
    ]

    print("RESULTS:\n")
    best_overall_path = None
    best_overall_length = float('inf')

    for i, (ants, rho, a, b, label) in enumerate(simulations, 1):
        path, length = ant_colony_optimization(distances, num_ants=ants, rho=rho, alpha=a, beta=b)
        
        print(f"{i:2}. ants={ants:<2} rho={rho:.1f} a={a} b={b} -> Довжина: {length:<4} | {label}")
        
        if length < best_overall_length:
            best_overall_length = length
            best_overall_path = path

    print("\nГрафік найкращого маршруту згенеровано!")
    
    route_str = " -> ".join(str(city) for city in best_overall_path)
    
    print("Послідовність міст найкращого маршруту:")
    print(route_str)
    
    plot_best_route(coords, best_overall_path, best_overall_length)