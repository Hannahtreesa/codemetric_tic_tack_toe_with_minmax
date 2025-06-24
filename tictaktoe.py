import tkinter as tk
import math
from tkinter import messagebox

class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe (Minimax AI)")
        self.board = [[" " for _ in range(3)] for _ in range(3)]
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.create_widgets()
        self.player = "X"
        self.computer = "O"

    def create_widgets(self):
        frame = tk.Frame(self.root)
        frame.pack()

        for i in range(3):
            for j in range(3):
                btn = tk.Button(frame, text=" ", font=('Arial', 24), width=5, height=2,
                                command=lambda r=i, c=j: self.player_move(r, c))
                btn.grid(row=i, column=j)
                self.buttons[i][j] = btn

        self.reset_btn = tk.Button(self.root, text="Play Again", font=('Arial', 14),
                                   command=self.reset_board)
        self.reset_btn.pack(pady=10)

    def player_move(self, row, col):
        if self.board[row][col] == " ":
            self.make_move(row, col, self.player)
            if not self.check_game_over():
                self.root.after(300, self.computer_turn)

    def make_move(self, row, col, player):
        self.board[row][col] = player
        self.buttons[row][col].config(text=player, state="disabled")

    def computer_turn(self):
        best_score = -math.inf
        best_move = None
        for r in range(3):
            for c in range(3):
                if self.board[r][c] == " ":
                    self.board[r][c] = self.computer
                    score = self.minimax(False)
                    self.board[r][c] = " "
                    if score > best_score:
                        best_score = score
                        best_move = (r, c)
        if best_move:
            self.make_move(best_move[0], best_move[1], self.computer)
            self.check_game_over()

    def minimax(self, is_maximizing):
        if self.check_winner(self.computer):
            return 1
        elif self.check_winner(self.player):
            return -1
        elif self.is_draw():
            return 0

        if is_maximizing:
            best_score = -math.inf
            for r in range(3):
                for c in range(3):
                    if self.board[r][c] == " ":
                        self.board[r][c] = self.computer
                        score = self.minimax(False)
                        self.board[r][c] = " "
                        best_score = max(score, best_score)
            return best_score
        else:
            best_score = math.inf
            for r in range(3):
                for c in range(3):
                    if self.board[r][c] == " ":
                        self.board[r][c] = self.player
                        score = self.minimax(True)
                        self.board[r][c] = " "
                        best_score = min(score, best_score)
            return best_score

    def check_winner(self, player):
        # Rows and columns
        for i in range(3):
            if all(self.board[i][j] == player for j in range(3)) or \
               all(self.board[j][i] == player for j in range(3)):
                return True
        # Diagonals
        if all(self.board[i][i] == player for i in range(3)) or \
           all(self.board[i][2 - i] == player for i in range(3)):
            return True
        return False

    def is_draw(self):
        return all(self.board[i][j] != " " for i in range(3) for j in range(3))

    def check_game_over(self):
        if self.check_winner(self.player):
            messagebox.showinfo("Game Over", "🎉 You win!")
            self.disable_all_buttons()
            return True
        elif self.check_winner(self.computer):
            messagebox.showinfo("Game Over", "💻 Computer wins!")
            self.disable_all_buttons()
            return True
        elif self.is_draw():
            messagebox.showinfo("Game Over", "😐 It's a draw!")
            self.disable_all_buttons()
            return True
        return False

    def disable_all_buttons(self):
        for row in self.buttons:
            for btn in row:
                btn.config(state="disabled")

    def reset_board(self):
        self.board = [[" " for _ in range(3)] for _ in range(3)]
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(text=" ", state="normal")


if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()
