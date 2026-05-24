import random
import math

N = 9
INITIAL_TEMPERATURE = 30.0
FINAL_TEMPERATURE = 0.5
ALPHA = 0.98
STEPS_PER_CHANGE = 100 # Кількість спроб на кожному кроці охолодження

def get_energy(solution):
    conflicts = 0
    for i in range(N):
        for j in range(i + 1, N):
            if solution[i] == solution[j] or abs(solution[i] - solution[j]) == abs(i - j):
                conflicts += 1
    return conflicts

def simulated_annealing():
    # Початкова ініціалізація
    current_sol = [random.randint(0, N - 1) for _ in range(N)]
    current_energy = get_energy(current_sol)
    
    # Зберігаємо найкращий результат за весь час
    best_sol = list(current_sol)
    best_energy = current_energy
    
    temp = INITIAL_TEMPERATURE
    
    while temp > FINAL_TEMPERATURE and best_energy > 0:
        # Внутрішній цикл для ретельного пошуку при поточній температурі
        for _ in range(STEPS_PER_CHANGE):
            # робимо випадкову зміну
            neighbor = list(current_sol)
            col = random.randint(0, N - 1)
            neighbor[col] = random.randint(0, N - 1)
            
            new_energy = get_energy(neighbor)
            delta = new_energy - current_energy
            
            # Умова прийняття нового рішення
            if delta < 0 or random.random() < math.exp(-delta / temp):
                current_sol = neighbor
                current_energy = new_energy
                
                # Оновлюємо найкращий розв'язок, якщо знайшли його
                if current_energy < best_energy:
                    best_sol = list(current_sol)
                    best_energy = current_energy
                    if best_energy == 0: break

        temp *= ALPHA # Геометричне охолодження
        print(f"Температура: {temp:.2f}, Конфліктів: {best_energy}")
        
    return best_sol

# Вивід результату
def print_board(sol):
    for row in range(N):
        print(" ".join("Q" if sol[c] == row else "." for c in range(N)))

result = simulated_annealing()
print("\nНайкращий знайдений результат:")
print_board(result)