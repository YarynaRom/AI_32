import numpy as np
import matplotlib.pyplot as plt

#  2 & 3. Визначення функцій
def test_function(x):
    return np.sin(x) 

def main_function(x):
    return np.exp(x**2)  # Основна: e^(x^2)

# Точне значення для тестової функції
def get_exact_test_value():
    return 1.0

# Допоміжна функція для генерування випадкових точок
def generate_random_points(n_points, x_min, x_max, y_max):
    """Повертає пару (x, y) рівномірно розподілених випадкових значень."""
    x_random = np.random.uniform(x_min, x_max, n_points)
    y_random = np.random.uniform(0, y_max, n_points)
    return x_random, y_random

# Допоміжна функція для обчислення значення з двома режимами
def evaluate_function(x, mode):
    """Повертає значення підінтегральної функції залежно від режиму."""
    if mode == 1 or mode == "test":
        return test_function(x)
    elif mode == 2 or mode == "main":
        return main_function(x)
    else:
        raise ValueError("Невідомий режим! Використовуйте 'test' або 'main'.")

#  Алгоритм Монте-Карло
def monte_carlo_integrate(x_min, x_max, mode="test", n_points=10000):
    # Знаходимо максимум функції на інтервалі для побудови прямокутника
    x_range = np.linspace(x_min, x_max, 1000)
    y_max = np.max(evaluate_function(x_range, mode))
    
    # Використовуємо функцію з кроку 5
    x_random, y_random = generate_random_points(n_points, x_min, x_max, y_max)
    
    # Використовуємо функцію з кроку 6
    f_x = evaluate_function(x_random, mode)
    
    # Перевірка, чи точка під графіком
    under_curve = y_random < f_x
    
    # Обчислення інтеграла
    area_rect = (x_max - x_min) * y_max
    integral_eval = area_rect * np.sum(under_curve) / n_points
    
    return integral_eval, x_random, y_random, under_curve, y_max

def visualize_results(x_min, x_max, x_rnd, y_rnd, under_curve, mode, title):
    x_plot = np.linspace(x_min, x_max, 200)
    y_plot = evaluate_function(x_plot, mode)
    
    plt.figure(figsize=(10, 6))
    plt.plot(x_plot, y_plot, color='red', linewidth=2, label='f(x)')
    plt.scatter(x_rnd[under_curve], y_rnd[under_curve], color='green', s=1, alpha=0.5, label='Під кривою')
    plt.scatter(x_rnd[~under_curve], y_rnd[~under_curve], color='blue', s=1, alpha=0.3, label='Над кривою')
    plt.title(title)
    plt.legend()
    plt.show()


n = 100000

# Тестова задача
val_test, x_r, y_r, under, y_m = monte_carlo_integrate(0, np.pi/2, mode="test", n_points=n)
exact_test = get_exact_test_value()
abs_err = abs(val_test - exact_test)
rel_err = (abs_err / exact_test) * 100

print(f"--- Тестовий приклад: f(x) = sin(x) на [0, pi/2] ---")
print(f"Точне значення: {exact_test:.6f}")
print(f"Метод Монте-Карло: {val_test:.6f}")
print(f"Абсолютна похибка: {abs_err:.6f}")
print(f"Відносна похибка: {rel_err:.2f}%\n")

visualize_results(0, np.pi/2, x_r, y_r, under, "test", "Метод Монте-Карло: sin(x)")

# Основна задача
val_main, x_r_m, y_r_m, under_m, y_m_m = monte_carlo_integrate(1, 2, mode="main", n_points=n)
approx_main_exact = 14.98997 

print(f"--- Основна задача: f(x) = e^(x^2) на [1, 2] ---")
print(f"Оцінка Монте-Карло: {val_main:.6f}")
print(f"Орієнтовна похибка (відносно аналітичного наближення): {abs(val_main - approx_main_exact):.6f}")

visualize_results(1, 2, x_r_m, y_r_m, under_m, "main", "Метод Монте-Карло: e^(x^2)")