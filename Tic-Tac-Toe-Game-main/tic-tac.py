import tkinter as tk
from tkinter import messagebox
import random

def start_game():
    global current_player, player_symbol, ai_symbol

    player_symbol = player_choice.get()
    ai_symbol = "✔" if player_symbol == "X" else "X"
    current_player = "X"

    window = tk.Tk()
    window.title("Tic Tac Toe - Owais")
    window.geometry("600x600")
    window.label = tk.Label(window, text="Tic Tac Toe", font=("impact", 22, "bold"), fg="black")
    window.label.pack()
    

    board = tk.Frame(window)
    board.pack()
    

    buttons = []
    for i in range(3):
        row = []
        for j in range(3):
            button = tk.Button(board, width=10, height=5)
            button.grid(row=i, column=j)
            row.append(button)
        buttons.append(row)

    def minimax(board, depth, isMaximizing, alpha, beta):
        winner = check_win()
        if winner:
            return scores[winner]

        if isMaximizing:
            bestScore = float('-inf')
            for i in range(3):
                for j in range(3):
                    if board[i][j]["text"] == "":
                        board[i][j]["text"] = ai_symbol
                        score = minimax(board, depth + 1, False, alpha, beta)
                        board[i][j]["text"] = ""
                        bestScore = max(score, bestScore)
                        alpha = max(alpha, score)
                        if beta <= alpha:
                            break
                if beta <= alpha:
                    break
            return bestScore
        else:
            bestScore = float('inf')
            for i in range(3):
                for j in range(3):
                    if board[i][j]["text"] == "":
                        board[i][j]["text"] = player_symbol
                        score = minimax(board, depth + 1, True, alpha, beta)
                        board[i][j]["text"] = ""
                        bestScore = min(score, bestScore)
                        beta = min(beta, score)
                        if beta <= alpha:
                            break
                if beta <= alpha:
                    break
            return bestScore

    def button_click(row, col):
        global current_player, moves
        button = buttons[row][col]
        if button["text"] == "":
            button["text"] = current_player
            button.config(fg="red" if current_player == "X" else "blue", font=("Arial", 9, "bold"))
            moves += 1
            winner = check_win()
            if winner:
                show_win_screen(winner)
            elif moves < 9:
                current_player = "✔" if current_player == "X" else "X"
                if current_player == ai_symbol:
                    ai_move()

    def ai_move():
        bestScore = float('-inf')
        bestMove = None
        for i in range(3):
            for j in range(3):
                if buttons[i][j]["text"] == "":
                    buttons[i][j]["text"] = ai_symbol
                    score = minimax(buttons, 0, False, float('-inf'), float('inf'))
                    buttons[i][j]["text"] = ""
                    if score > bestScore:
                        bestScore = score
                        bestMove = (i, j)
        button_click(bestMove[0], bestMove[1])

    def check_win():
        for i in range(3):
            if buttons[i][0]["text"] == buttons[i][1]["text"] == buttons[i][2]["text"] != "":
                return buttons[i][0]["text"]
        for j in range(3):
            if buttons[0][j]["text"] == buttons[1][j]["text"] == buttons[2][j]["text"] != "":
                return buttons[0][j]["text"]
        if buttons[0][0]["text"] == buttons[1][1]["text"] == buttons[2][2]["text"] != "":
            return buttons[0][0]["text"]
        if buttons[0][2]["text"] == buttons[1][1]["text"] == buttons[2][0]["text"] != "":
            return buttons[0][2]["text"]
        if all(button["text"] != "" for row in buttons for button in row):
            return "tie"
        return None

    def show_win_screen(winner):
        if winner != "tie":
            messagebox.showinfo("Game Over", f"Player {winner} wins!")
        else:
            messagebox.showinfo("Game Over", "It's a tie!")
        window.destroy()

    for i in range(3):
        for j in range(3):
            buttons[i][j].config(command=lambda row=i, col=j: button_click(row, col))

    if ai_symbol == "X":
        row, col = random.randint(0, 2), random.randint(0, 2)
        button_click(row, col)
        
        
    window.mainloop()

# Create the initial window for symbol selection
root = tk.Tk()
root.title("Tic Tac Toe - Owais")
root.geometry("600x600")
tk.Label(root, text="Welcome to Tic Tac Toe!",font=("impact",22,"bold"),fg="light green").pack()
# Load the image
image = tk.PhotoImage(file="tic.png")

# Resize by subsampling (divides width & height by 2)
resized_image = image.subsample(20, 20)  # You can use 3, 4, etc., for smaller

# Show in label
label = tk.Label(root, image=resized_image)
label.image = resized_image  # Keep a reference
label.pack()
tk.Label(root, text="Choose symbol to play against the AI:",font=("Arial",16)).pack()

player_choice = tk.StringVar(value="X")
tk.Radiobutton(root, text="X", variable=player_choice, value="X",font=("Arial",16)).pack()
tk.Radiobutton(root, text="✔", variable=player_choice, value="✔",font=("Arial",16)).pack()
tk.Button(root, text="Start Game",font=("Arial",16), command=lambda: [root.destroy(), start_game()]).pack()

current_player = "X"
moves = 0
scores = {"X": -10, "✔": 10, "tie": 0}

root.mainloop()