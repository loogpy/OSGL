import json
import os
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import subprocess
import time

# Function to load game data from the JSON file
def load_game_data():
    try:
        if not os.path.exists("game_data.json"):
            # If game_data.json doesn't exist, create it with an empty games list
            with open("game_data.json", "w") as file:
                json.dump({"games": []}, file, indent=4)
            return []

        with open("game_data.json", "r") as file:
            data = json.load(file)
            return data["games"]
    except Exception as e:
        messagebox.showerror("Error", f"Error loading game data: {e}")
        return []

# Function to update game progress in the JSON file
def update_game_progress(game_name, progress, status):
    try:
        with open("game_data.json", "r") as file:
            data = json.load(file)

        for game in data["games"]:
            if game["name"] == game_name:
                game["progress"] = progress
                game["status"] = status
                break

        with open("game_data.json", "w") as file:
            json.dump(data, file, indent=4)
    except Exception as e:
        messagebox.showerror("Error", f"Error saving game progress: {e}")

# Function to automatically add games to game_data.json
def auto_add_games():
    try:
        launcher_name = os.path.basename(__file__)  # Get the name of the launcher script
        game_files = [f for f in os.listdir() if f.endswith('.py') and f != launcher_name]
        
        # Load the existing game data from the JSON
        game_data = load_game_data()

        # Check if each Python file has a corresponding image and is not already in the list
        for game_file in game_files:
            game_name = game_file[:-3]  # Remove the ".py" extension to get the game name
            thumbnail = f"{game_name}.png"  # Expect a thumbnail with the same name
            
            # If the game is already in the JSON, skip adding it
            if any(game['name'] == game_name for game in game_data):
                continue
            
            # Check if the thumbnail exists in the current directory
            if os.path.exists(thumbnail):
                game_data.append({
                    "name": game_name,
                    "thumbnail": thumbnail,
                    "lastPlayed": time.strftime("%Y-%m-%d"),
                    "progress": "Not Started",
                    "status": "not_started"
                })
        
        # Save the updated game data back to the JSON file
        with open("game_data.json", "w") as file:
            json.dump({"games": game_data}, file, indent=4)
    
    except Exception as e:
        messagebox.showerror("Error", f"Error adding games to JSON: {e}")

# Function to show game details on the side
def show_game_details(game):
    # Clear previous details
    for widget in details_frame.winfo_children():
        widget.destroy()

    # Game Name
    game_name_label = tk.Label(details_frame, text=f"Game: {game['name']}", font=("Arial", 16, "bold"), bg="#2c3e50", fg="#ecf0f1")
    game_name_label.pack(pady=5)

    # Game Thumbnail (if exists)
    if os.path.exists(game["thumbnail"]):
        img = Image.open(game["thumbnail"])
        img = img.resize((100, 100))  # Resize the thumbnail to fit the UI
        img = ImageTk.PhotoImage(img)
        thumbnail_label = tk.Label(details_frame, image=img, bg="#2c3e50")
        thumbnail_label.image = img
        thumbnail_label.pack(pady=5)

    # Game Progress
    progress_label = tk.Label(details_frame, text=f"Progress: {game['progress']}", font=("Arial", 12), bg="#2c3e50", fg="#ecf0f1")
    progress_label.pack(pady=5)

    # Last Played
    last_played_label = tk.Label(details_frame, text=f"Last Played: {game['lastPlayed']}", font=("Arial", 12), bg="#2c3e50", fg="#ecf0f1")
    last_played_label.pack(pady=5)

    # Game Status
    status_label = tk.Label(details_frame, text=f"Status: {game['status']}", font=("Arial", 12), bg="#2c3e50", fg="#ecf0f1")
    status_label.pack(pady=5)

    # Add the play button dynamically
    play_button = tk.Button(details_frame, text="Play", font=("Arial", 14), command=lambda: launch_game(game), bg="#3498db", fg="#fff", bd=0, relief="flat")
    play_button.pack(pady=10)

# Function to launch the game (runs the game script)
def launch_game(game):
    try:
        # Launch the game Python script using subprocess
        game_script = f"{game['name']}.py"
        
        # Check if the game script exists
        if os.path.exists(game_script):
            subprocess.run(["python3", game_script], check=True)
            messagebox.showinfo("Launching", f"Launching {game['name']}...")
        else:
            messagebox.showerror("Error", f"Game file {game_script} not found!")
        
        # Update the game progress when it is launched (for demo, set status to 'in_progress')
        update_game_progress(game['name'], "level 2", "in_progress")
        show_game_details(game)  # Update the game details after launching
    
    except Exception as e:
        messagebox.showerror("Error", f"Error launching the game: {e}")

# Function to close the application
def close_app():
    root.quit()

# Create the Tkinter window
root = tk.Tk()
root.title("Game Launcher")

# Set the window to full-screen
root.attributes('-fullscreen', True)
root.config(bg="#2c3e50")

# Create a frame for the list of games (left side)
games_frame = tk.Frame(root, bg="#34495e")
games_frame.pack(side=tk.LEFT, fill=tk.Y, padx=20, pady=20)

# Create a frame for the game details (right side)
details_frame = tk.Frame(root, bg="#2c3e50", padx=20, pady=20)
details_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Close Button (top-right corner)
close_button = tk.Button(root, text="Close", font=("Arial", 12), command=close_app, bg="#e74c3c", fg="#fff", bd=0, relief="flat")
close_button.place(x=root.winfo_screenwidth() - 80, y=10)

# Load and display the games
games = load_game_data()
auto_add_games()  # Automatically add games if missing from the JSON

# List the games
for game in games:
    game_button = tk.Button(games_frame, text=game["name"], font=("Arial", 14), command=lambda g=game: show_game_details(g), bg="#3498db", fg="#fff", bd=0, relief="flat")
    game_button.pack(pady=10)

root.mainloop()
