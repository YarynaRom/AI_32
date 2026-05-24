import numpy as np
import pygame
from PIL import Image
from sklearn.datasets import load_digits

class NeuralNetwork:
    def __init__(self, input_nodes, hidden_nodes, output_nodes, learning_rate):
        self.inodes = input_nodes
        self.hnodes = hidden_nodes
        self.onodes = output_nodes
        self.lr = learning_rate

        self.wih = np.random.normal(0.0, pow(self.inodes, -0.5), (self.hnodes, self.inodes))
        self.who = np.random.normal(0.0, pow(self.hnodes, -0.5), (self.onodes, self.hnodes))

        self.activation_function = lambda x: 1 / (1 + np.exp(-x))

    def train(self, inputs_list, targets_list):
        inputs = np.array(inputs_list, ndmin=2).T
        targets = np.array(targets_list, ndmin=2).T

        hidden_inputs = np.dot(self.wih, inputs)
        hidden_outputs = self.activation_function(hidden_inputs)
        
        final_inputs = np.dot(self.who, hidden_outputs)
        final_outputs = self.activation_function(final_inputs)

        output_errors = targets - final_outputs
        hidden_errors = np.dot(self.who.T, output_errors)

        self.who += self.lr * np.dot((output_errors * final_outputs * (1.0 - final_outputs)), np.transpose(hidden_outputs))
        self.wih += self.lr * np.dot((hidden_errors * hidden_outputs * (1.0 - hidden_outputs)), np.transpose(inputs))

    def query(self, inputs_list):
        inputs = np.array(inputs_list, ndmin=2).T
        hidden_inputs = np.dot(self.wih, inputs)
        hidden_outputs = self.activation_function(hidden_inputs)
        final_inputs = np.dot(self.who, hidden_outputs)
        final_outputs = self.activation_function(final_inputs)
        return final_outputs

print("Завантаження реальних образів рукописних цифр...")
digits = load_digits()
X = digits.data 
y = digits.target

X_scaled = (X / 16.0) * 0.98 + 0.01

input_nodes = 64  
hidden_nodes = 80
output_nodes = 10
learning_rate = 0.3

nn = NeuralNetwork(input_nodes, hidden_nodes, output_nodes, learning_rate)

print("Навчання нейромережі на реальних даних (очікуйте кілька секунд)...")
epochs = 30
for epoch in range(epochs):
    for i in range(len(X_scaled)):
        targets = np.zeros(output_nodes) + 0.01
        targets[y[i]] = 0.99
        nn.train(X_scaled[i], targets)
print("Навчання завершено успішно!")

WINDOW_WIDTH = 400
WINDOW_HEIGHT = 500
CANVAS_SIZE = 280

CANVAS_X = (WINDOW_WIDTH - CANVAS_SIZE) // 2
CANVAS_Y = 40

BG_COLOR = (30, 30, 30)
CANVAS_COLOR = (0, 0, 0)
DRAW_COLOR = (255, 255, 255)
TEXT_COLOR = (240, 240, 240)
BUTTON_COLOR = (70, 70, 70)
BUTTON_HOVER_COLOR = (100, 100, 100)

BRUSH_RADIUS = 16 

pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Лаба 7: Нейромережа Рашида")
clock = pygame.time.Clock()

font = pygame.font.SysFont("Arial", 22)
small_font = pygame.font.SysFont("Arial", 16)

canvas_surface = pygame.Surface((CANVAS_SIZE, CANVAS_SIZE))
canvas_surface.fill(CANVAS_COLOR)

prediction_text = "Намалюй цифру"
running = True
drawing = False

predict_button = pygame.Rect(60, 360, 120, 50)
clear_button = pygame.Rect(220, 360, 120, 50)

def draw_button(rect, text, current_mouse_pos):
    color = BUTTON_HOVER_COLOR if rect.collidepoint(current_mouse_pos) else BUTTON_COLOR
    pygame.draw.rect(screen, color, rect, border_radius=10)
    label = small_font.render(text, True, TEXT_COLOR)
    label_rect = label.get_rect(center=rect.center)
    screen.blit(label, label_rect)

def draw_on_canvas(pos):
    mouse_x, mouse_y = pos
    local_x = mouse_x - CANVAS_X
    local_y = mouse_y - CANVAS_Y
    if 0 <= local_x < CANVAS_SIZE and 0 <= local_y < CANVAS_SIZE:
        pygame.draw.circle(canvas_surface, DRAW_COLOR, (local_x, local_y), BRUSH_RADIUS)

def preprocess_canvas(surface):
    raw_str = pygame.image.tostring(surface, "RGB")
    img = Image.frombytes("RGB", (CANVAS_SIZE, CANVAS_SIZE), raw_str).convert("L")
    bbox = img.getbbox()

    if bbox is None:
        return np.zeros(64) + 0.01

    img = img.crop(bbox)
    max_side = max(img.size)
    square = Image.new("L", (max_side, max_side), 0)
    paste_x = (max_side - img.size[0]) // 2
    paste_y = (max_side - img.size[1]) // 2
    square.paste(img, (paste_x, paste_y))
    
    square = square.resize((6, 6), Image.Resampling.LANCZOS)
    final_img = Image.new("L", (8, 8), 0)
    final_img.paste(square, (1, 1))

    img_array = np.array(final_img).flatten().astype("float32")
    
    if np.max(img_array) > 0:
        img_array = (img_array / np.max(img_array)) * 0.98 + 0.01
    else:
        img_array = np.zeros(64) + 0.01
        
    return img_array

def predict_digit():
    global prediction_text
    img_vector = preprocess_canvas(canvas_surface)
    
    outputs = nn.query(img_vector)
    
    digit = int(np.argmax(outputs))
    confidence = float(outputs[digit]) * 100
    
    prediction_text = f"Результат: {digit} ({confidence:.1f}%)"

def clear_canvas():
    global prediction_text
    canvas_surface.fill(CANVAS_COLOR)
    prediction_text = "Намалюй цифру"

while running:
    mouse_pos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if predict_button.collidepoint(event.pos):
                predict_digit()
            elif clear_button.collidepoint(event.pos):
                clear_canvas()
            else:
                event_x, event_y = event.pos
                if CANVAS_X <= event_x < CANVAS_X + CANVAS_SIZE and CANVAS_Y <= event_y < CANVAS_Y + CANVAS_SIZE:
                    drawing = True
                    draw_on_canvas(event.pos)
        elif event.type == pygame.MOUSEBUTTONUP:
            drawing = False
        elif event.type == pygame.MOUSEMOTION and drawing:
            draw_on_canvas(event.pos)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                predict_digit()
            elif event.key == pygame.K_c:
                clear_canvas()

    screen.fill(BG_COLOR)
    pygame.draw.rect(screen, (200, 200, 200), (CANVAS_X - 2, CANVAS_Y - 2, CANVAS_SIZE + 4, CANVAS_SIZE + 4), border_radius=4)
    screen.blit(canvas_surface, (CANVAS_X, CANVAS_Y))

    draw_button(predict_button, "Вгадати", mouse_pos)
    draw_button(clear_button, "Очистити", mouse_pos)

    title = font.render("Намалюй цифру (0-9)", True, TEXT_COLOR)
    screen.blit(title, (WINDOW_WIDTH // 2 - title.get_width() // 2, 10))

    result = font.render(prediction_text, True, TEXT_COLOR)
    screen.blit(result, (WINDOW_WIDTH // 2 - result.get_width() // 2, 430))

    hint = small_font.render("Enter = вгадати, C = очистити", True, TEXT_COLOR)
    screen.blit(hint, (WINDOW_WIDTH // 2 - hint.get_width() // 2, 465))

    pygame.display.flip()
    clock.tick(120)

pygame.quit()