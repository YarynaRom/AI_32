import tkinter as tk
from tkinter import messagebox
import random # Додали модуль для випадкових чисел

class TicTacToeTreeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Хрестики-нулики (Шанс на перемогу!)")
        self.board = [' ' for _ in range(9)] 
        self.current_player = 'X' 
        self.buttons = []
        self.create_gui()

    def create_gui(self):
        for i in range(9):
            btn = tk.Button(self.root, text=' ', font=('Arial', 24, 'bold'), width=5, height=2,
                            command=lambda i=i: self.user_click(i))
            btn.grid(row=i//3, column=i%3, padx=5, pady=5)
            self.buttons.append(btn)

    def user_click(self, index):
        if self.board[index] == ' ' and self.current_player == 'X':
            self.make_move(index, 'X')
            
            if not self.check_winner('X') and not self.is_draw():
                self.current_player = 'O'
                self.computer_move()

    def make_move(self, index, player):
        self.board[index] = player
        self.buttons[index].config(text=player, state=tk.DISABLED, 
                                   disabledforeground="blue" if player == 'X' else "red")
        
        if self.check_winner(player):
            self.end_game(f"Переміг {player}!")
        elif self.is_draw():
            self.end_game("Нічия!")

    def computer_move(self):
        if random.random() < 0.30: 
            available_moves = [i for i in range(9) if self.board[i] == ' ']
            if available_moves:
                random_move = random.choice(available_moves)
                self.make_move(random_move, 'O')
                self.current_player = 'X'
                return
        # Якщо випадковості не сталося (70% випадків), граємо ідеально
        best_score = -float('inf')
        best_move = None
        
        for i in range(9):
            if self.board[i] == ' ':
                self.board[i] = 'O'
                score = self.minimax(self.board, 0, False)
                self.board[i] = ' '
                
                if score > best_score:
                    best_score = score
                    best_move = i
                    
        if best_move is not None:
            self.make_move(best_move, 'O')
            self.current_player = 'X'

    def minimax(self, board, depth, is_maximizing):
        if self.check_winner('O'):
            return 10 - depth 
        if self.check_winner('X'):
            return depth - 10 
        if self.is_draw():
            return 0 

        if is_maximizing:
            best_score = -float('inf')
            for i in range(9):
                if board[i] == ' ':
                    board[i] = 'O'
                    score = self.minimax(board, depth + 1, False)
                    board[i] = ' '
                    best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for i in range(9):
                if board[i] == ' ':
                    board[i] = 'X'
                    score = self.minimax(board, depth + 1, True)
                    board[i] = ' '
                    best_score = min(score, best_score)
            return best_score

    def check_winner(self, player):
        win_conditions = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8), 
            (0, 3, 6), (1, 4, 7), (2, 5, 8), 
            (0, 4, 8), (2, 4, 6)             
        ]
        for condition in win_conditions:
            if self.board[condition[0]] == self.board[condition[1]] == self.board[condition[2]] == player:
                return True
        return False

    def is_draw(self):
        return ' ' not in self.board

    def end_game(self, message):
        messagebox.showinfo("Кінець гри", message)
        self.reset_game()

    def reset_game(self):
        self.board = [' ' for _ in range(9)]
        for btn in self.buttons:
            btn.config(text=' ', state=tk.NORMAL)
        self.current_player = 'X'

if __name__ == "__main__":
    root = tk.Tk()
    app = TicTacToeTreeGame(root)
    root.mainloop()