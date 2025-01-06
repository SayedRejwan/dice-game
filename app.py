import tkinter as tk
from tkinter import messagebox
import random
import time

# Function to roll the dice
def roll_dice():
    return random.randint(1, 6)

# Function to update the dice face
def update_dice_face(canvas, roll):
    canvas.delete("all")  # Clear the canvas

    # Dot positions for dice faces
    dot_positions = {
        1: [(2, 2)],
        2: [(1, 1), (3, 3)],
        3: [(1, 1), (2, 2), (3, 3)],
        4: [(1, 1), (1, 3), (3, 1), (3, 3)],
        5: [(1, 1), (1, 3), (2, 2), (3, 1), (3, 3)],
        6: [(1, 1), (1, 2), (1, 3), (3, 1), (3, 2), (3, 3)],
    }

    # Draw dots on the canvas
    for x, y in dot_positions[roll]:
        canvas.create_oval(
            x * 30 - 10,
            y * 30 - 10,
            x * 30 + 10,
            y * 30 + 10,
            fill="black"
        )

# Function to animate the dice roll
def animate_dice(canvas):
    for _ in range(10):  # Simulate the dice rolling 10 times
        temp_roll = roll_dice()
        update_dice_face(canvas, temp_roll)
        app.update()
        time.sleep(0.1)  # Small delay between rolls

# Function for Player vs Player turn
def player_vs_player_turn():
    global player_turn_tracker, player1_score, player2_score, rounds_left

    if rounds_left <= 0:
        messagebox.showinfo("Game Over", "The game has ended! Restart to play again.")
        return

    current_player = "Player 1" if player_turn_tracker == 1 else "Player 2"
    animate_dice(dice_canvas)  # Show dice rolling animation
    roll = roll_dice()
    update_dice_face(dice_canvas, roll)
    status_label.config(text=f"{current_player} rolled a {roll}!")

    if player_turn_tracker == 1:
        player1_roll = roll
        result_label.config(text="Player 2, it's your turn!")
        player_turn_tracker = 2
    else:
        player2_roll = roll
        result_label.config(text="Calculating result...")
        determine_player_vs_player_winner(player1_roll, player2_roll)
        rounds_left -= 1
        player_turn_tracker = 1

# Determine winner for Player vs Player
def determine_player_vs_player_winner(player1_roll, player2_roll):
    global player1_score, player2_score

    if player1_roll > player2_roll:
        player1_score += 1
        result_label.config(text="Player 1 wins this round!")
    elif player2_roll > player1_roll:
        player2_score += 1
        result_label.config(text="Player 2 wins this round!")
    else:
        result_label.config(text="It's a tie this round!")

    score_label.config(
        text=f"Score: Player 1 {player1_score} - {player2_score} Player 2"
    )

    if rounds_left == 0:
        declare_winner(player_vs="player_vs_player")

# Function for Player vs AI turn
def player_vs_ai_turn():
    global player_score, ai_score, rounds_left

    if rounds_left <= 0:
        messagebox.showinfo("Game Over", "The game has ended! Restart to play again.")
        return

    animate_dice(dice_canvas)  # Show dice rolling animation
    player_roll = roll_dice()
    update_dice_face(dice_canvas, player_roll)
    status_label.config(text=f"You rolled a {player_roll}!")

    # Simulate AI roll
    app.after(1500, lambda: ai_turn(player_roll))

# Function for AI's turn
def ai_turn(player_roll):
    global player_score, ai_score, rounds_left

    ai_roll = roll_dice()
    animate_dice(dice_canvas)  # Show dice rolling animation for AI
    update_dice_face(dice_canvas, ai_roll)
    status_label.config(text=f"AI rolled a {ai_roll}!")

    if player_roll > ai_roll:
        player_score += 1
        result_label.config(text="You win this round!")
    elif player_roll < ai_roll:
        ai_score += 1
        result_label.config(text="AI wins this round!")
    else:
        result_label.config(text="It's a tie!")

    rounds_left -= 1
    score_label.config(text=f"Score: You {player_score} - {ai_score} AI")

    if rounds_left == 0:
        declare_winner(player_vs="player_vs_ai")

# Function to declare the winner
def declare_winner(player_vs):
    if player_vs == "player_vs_ai":
        if player_score > ai_score:
            messagebox.showinfo("Game Over", "Congratulations! You won the game!")
        elif player_score < ai_score:
            messagebox.showinfo("Game Over", "Sorry! AI won the game!")
        else:
            messagebox.showinfo("Game Over", "It's a tie!")
    elif player_vs == "player_vs_player":
        if player1_score > player2_score:
            messagebox.showinfo("Game Over", "Player 1 wins the game!")
        elif player2_score > player1_score:
            messagebox.showinfo("Game Over", "Player 2 wins the game!")
        else:
            messagebox.showinfo("Game Over", "It's a tie!")

# Function to restart the game
def restart_game():
    global player_score, ai_score, player1_score, player2_score, rounds_left, player_turn_tracker

    player_score = 0
    ai_score = 0
    player1_score = 0
    player2_score = 0
    rounds_left = 5
    player_turn_tracker = 1

    score_label.config(text="")
    result_label.config(text="Choose your game mode to start!")
    status_label.config(text="")
    update_dice_face(dice_canvas, 1)  # Reset dice to default face

# Function to choose the game mode
def choose_game_mode(mode):
    global game_mode

    game_mode = mode
    restart_game()
    if mode == "player_vs_ai":
        score_label.config(text="Score: You 0 - 0 AI")
        roll_button.config(command=player_vs_ai_turn)
    elif mode == "player_vs_player":
        score_label.config(text="Score: Player 1 0 - 0 Player 2")
        roll_button.config(command=player_vs_player_turn)

# Initialize the main application
app = tk.Tk()
app.title("Dice Roll Game")
app.geometry("500x500")
app.resizable(False, False)

# Initialize game variables
player_score = 0
ai_score = 0
player1_score = 0
player2_score = 0
rounds_left = 5
player_turn_tracker = 1  # Tracks whose turn it is (1 = Player 1, 2 = Player 2)
game_mode = "player_vs_ai"

# Title Label
title_label = tk.Label(app, text="Dice Roll Game", font=("Helvetica", 18, "bold"), fg="blue")
title_label.pack(pady=10)

# Mode Selection Buttons
mode_frame = tk.Frame(app)
mode_frame.pack(pady=10)
ai_mode_button = tk.Button(mode_frame, text="Player vs AI", font=("Helvetica", 12), command=lambda: choose_game_mode("player_vs_ai"), bg="green", fg="white")
ai_mode_button.pack(side=tk.LEFT, padx=10)
pvp_mode_button = tk.Button(mode_frame, text="Player vs Player", font=("Helvetica", 12), command=lambda: choose_game_mode("player_vs_player"), bg="orange", fg="white")
pvp_mode_button.pack(side=tk.LEFT, padx=10)

# Score Label
score_label = tk.Label(app, text="", font=("Helvetica", 14))
score_label.pack(pady=10)

# Result Label
result_label = tk.Label(app, text="Choose your game mode to start!", font=("Helvetica", 12, "italic"))
result_label.pack(pady=10)

# Dice Canvas
dice_canvas = tk.Canvas(app, width=120, height=120, bg="white", highlightthickness=2, highlightbackground="black")
dice_canvas.pack(pady=20)

# Default Dice Face
update_dice_face(dice_canvas, 1)

# Status Label
status_label = tk.Label(app, text="", font=("Helvetica", 12))
status_label.pack(pady=10)

# Roll Dice Button
roll_button = tk.Button(app, text="Roll Dice", font=("Helvetica", 12), bg="green", fg="white")
roll_button.pack(pady=10)

# Restart Game Button
restart_button = tk.Button(app, text="Restart Game", font=("Helvetica", 12), command=restart_game, bg="red", fg="white")
restart_button.pack(pady=10)

# Run the main event loop
app.mainloop()
