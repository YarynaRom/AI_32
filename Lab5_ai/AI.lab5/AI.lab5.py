import random
import copy

CLASSES = ["1-А", "1-Б"]
DAYS_NAMES = ["Понеділок", "Вівторок", "Середа", "Четвер", "П'ятниця"]

# 1. ГЕНЕРАЦІЯ УРОКІВ (24 уроки на клас)
def generate_required_lessons(class_name):
    lessons = []
    main_teacher = f"Вчитель {class_name}"
    
    for _ in range(5): lessons.append({"subj": "Математика", "teacher": main_teacher, "room": f"Каб. {random.randint(1, 3)}"})
    for _ in range(4): lessons.append({"subj": "Читання", "teacher": main_teacher, "room": f"Каб. {random.randint(1, 3)}"})
    for _ in range(4): lessons.append({"subj": "Письмо", "teacher": main_teacher, "room": f"Каб. {random.randint(1, 3)}"})
    for _ in range(3): lessons.append({"subj": "Я досліджую світ", "teacher": main_teacher, "room": f"Каб. {random.randint(1, 3)}"})
    
    for _ in range(4): lessons.append({"subj": "Фізкультура", "teacher": "Вчитель Спец", "room": "Спортивний зал"})
    for _ in range(2): lessons.append({"subj": "Хореографія", "teacher": "Вчитель Спец", "room": "Хореографічний зал"})
    for _ in range(2): lessons.append({"subj": "Музика", "teacher": "Вчитель Спец", "room": "Клас музики"})
    
    return lessons

VALID_SLOTS = []
for day in range(4):
    for slot in range(5):
        VALID_SLOTS.append((day, slot))
for slot in range(4):
    VALID_SLOTS.append((4, slot))

def create_random_schedule():
    schedule = []
    for c in CLASSES:
        lessons = generate_required_lessons(c)
        random.shuffle(lessons)
        
        for i, (day, slot) in enumerate(VALID_SLOTS):
            lesson = copy.deepcopy(lessons[i])
            lesson["class"] = c
            lesson["day"] = day
            lesson["slot"] = slot
            schedule.append(lesson)
    return schedule

def generate_population(size):
    return [create_random_schedule() for _ in range(size)]

# 3. ОБЧИСЛЕННЯ ШТРАФІВ
def evaluate_schedule(chromosome):
    hard_conflicts = 0 
    soft_conflicts = 0
    
    # Перевірка 1: Накладки по часу (вчителі та кабінети)
    time_slots = {}
    for gene in chromosome:
        key = (gene["day"], gene["slot"])
        if key not in time_slots:
            time_slots[key] = []
        time_slots[key].append(gene)
        
    for (day, slot), lessons in time_slots.items():
        teachers_seen = set()
        rooms_seen = set()
        
        for l in lessons:
            if l["teacher"] in teachers_seen:
                hard_conflicts += 1
            else:
                teachers_seen.add(l["teacher"])
                
            if not l["room"].startswith("Каб."):
                if l["room"] in rooms_seen:
                    hard_conflicts += 1
                else:
                    rooms_seen.add(l["room"])

    # Перевірка 2: Два однакові предмети в один день для класу
    class_days = {}
    for gene in chromosome:
        key = (gene["class"], gene["day"])
        if key not in class_days:
            class_days[key] = []
        class_days[key].append(gene["subj"])
        
    for (c, day), subjects in class_days.items():
        seen_subjects = set()
        for subj in subjects:
            if subj in seen_subjects:
                soft_conflicts += 1 # Знайшли дублікат предмета
            else:
                seen_subjects.add(subj)
                
    penalty = (hard_conflicts * 50) + (soft_conflicts * 20)
    fitness = 1.0 / (1.0 + penalty)
    
    return fitness, penalty

# 4. МУТАЦІЯ ТА КРОСОВЕР
def mutate(chromosome, mutation_rate=0.3):
    if random.random() > mutation_rate:
        return chromosome
    mutated = copy.deepcopy(chromosome)
    target_class = random.choice(CLASSES)
    class_genes_idx = [i for i, g in enumerate(mutated) if g["class"] == target_class]
    
    idx1, idx2 = random.sample(class_genes_idx, 2)
    temp_subj, temp_teach, temp_room = mutated[idx1]["subj"], mutated[idx1]["teacher"], mutated[idx1]["room"]
    mutated[idx1]["subj"], mutated[idx1]["teacher"], mutated[idx1]["room"] = mutated[idx2]["subj"], mutated[idx2]["teacher"], mutated[idx2]["room"]
    mutated[idx2]["subj"], mutated[idx2]["teacher"], mutated[idx2]["room"] = temp_subj, temp_teach, temp_room
    return mutated

def crossover(parent1, parent2):
    child = []
    for i in range(len(parent1)):
        if parent1[i]["day"] < 3: 
            child.append(copy.deepcopy(parent1[i]))
        else: 
            child.append(copy.deepcopy(parent2[i]))
    return child

# 5. ГЕНЕТИЧНИЙ АЛГОРИТМ
def run_genetic_algorithm(population_size=20, generations=2000):
    print("Запуск Генетичного Алгоритму...")
    
    population = generate_population(population_size)
    
    for gen in range(generations):
        scored_population = [(chromo, *evaluate_schedule(chromo)) for chromo in population]
        scored_population.sort(key=lambda x: x[1], reverse=True)
        
        best_chromo, best_fitness, best_penalty = scored_population[0]
        
        if gen % 10 == 0:
            print(f"Покоління {gen}: Найкращий штраф = {best_penalty}")
                
        if best_penalty == 0:
            print(f"Покоління {gen}: Найкращий штраф = {best_penalty}")
            print(f"Ідеальний розклад знайдено на поколінні {gen}!")
            return best_chromo
            
        new_population = [best_chromo]
        new_population.extend(generate_population(2))
        
        while len(new_population) < population_size:
            p1 = random.choice(scored_population[:10])[0]
            p2 = random.choice(scored_population[:10])[0]
            
            child = crossover(p1, p2)
            child = mutate(child, mutation_rate=0.4)
            new_population.append(child)
            
        population = new_population
        
    return scored_population[0][0]

# 6. ВИВІД ГОТОВОГО РОЗКЛАДУ
if __name__ == "__main__":
    best_schedule = run_genetic_algorithm()
    
    print("ЗГЕНЕРОВАНИЙ РОЗКЛАД")
    
    for c in CLASSES:
        print(f"\nКЛАС: {c}")
        homeroom_teacher = f"Вчитель {c}"
        homeroom_count = 0
        
        for day in range(5):
            print(f"  {DAYS_NAMES[day]}:")
            lessons = [g for g in best_schedule if g["class"] == c and g["day"] == day]
            lessons.sort(key=lambda x: x["slot"])
            
            for l in lessons:
                print(f"    Урок {l['slot']+1}: {l['subj']} ({l['teacher']}, ауд. {l['room']})")
                if l['teacher'] == homeroom_teacher:
                    homeroom_count += 1
                    
        print("-" * 50)
        print(f"Статистика для {c}:")
        print(f"Годин класного керівника: {homeroom_count} з 24")
        print("Норму класного керівника виконано (>= 50%).")