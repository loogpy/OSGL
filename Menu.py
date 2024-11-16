import requests
import json
import tkinter as tk
from tkinter import simpledialog, messagebox
import os

# Default URL to the JSON file in your GitHub repo
DEFAULT_GITHUB_JSON_URL = "https://raw.githubusercontent.com/Loogpy/OSGL/main/games.json"

# Variable to store the current repo URL
current_repo_url = DEFAULT_GITHUB_JSON_URL

# Function to fetch JSON data from GitHub
def fetch_games():
    try:
        # Send a GET request to the current repo URL
        response = requests.get(current_repo_url)
        response.raise_for_status()  # Check for HTTP errors
        games_data = response.json()  # Parse the JSON response
        
        return games_data
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"Failed to fetch data: {e}")
        return []

# Function to update the UI with the fetched games data
def update_game_list(games_data):
    for widget in game_list_frame.winfo_children():
        widget.destroy()  # Clear the current list of games

    for game in games_data:
        game_button = tk.Button(game_list_frame, text=game['name'], command=lambda game=game: show_game_details(game))
        game_button.pack(pady=5, fill='x')

# Function to show game details when clicked
def show_game_details(game):
    for widget in game_info_frame.winfo_children():
        widget.destroy()  # Clear previous game details

    details_label = tk.Label(game_info_frame, text=f"Game Name: {game['name']}", font=("Arial", 14))
    details_label.pack(pady=10)

    description_label = tk.Label(game_info_frame, text=f"Description: {game['description']}", wraplength=300)
    description_label.pack(pady=10)

    author_label = tk.Label(game_info_frame, text=f"Author: {game['author']}")
    author_label.pack(pady=5)

    launch_button = tk.Button(game_info_frame, text="Play Game", command=lambda: launch_game(game['python_file']))
    launch_button.pack(pady=10)

    download_button = tk.Button(game_info_frame, text="Download Game", command=lambda: download_game(game))
    download_button.pack(pady=5)

# Function to launch the game
def launch_game(python_file):
    try:
        # Run the Python file using Python 3
        import subprocess
        subprocess.run(["python3", python_file], check=True)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to launch game: {e}")

# Function to download game files and save them
def download_game(game):
    # Get the game files URLs
    python_file_url = game['python_file_url']
    image_url = game['image_url']

    # Download the Python file
    try:
        response = requests.get(python_file_url)
        response.raise_for_status()
        python_file_name = os.path.basename(python_file_url)
        with open(python_file_name, 'wb') as file:
            file.write(response.content)
        messagebox.showinfo("Success", f"Downloaded {python_file_name}")
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"Failed to download Python file: {e}")

    # Download the image file
    try:
        response = requests.get(image_url)
        response.raise_for_status()
        image_name = os.path.basename(image_url)
        with open(image_name, 'wb') as file:
            file.write(response.content)
        messagebox.showinfo("Success", f"Downloaded {image_name}")
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"Failed to download image file: {e}")

# Function to show the store (list of games)
def show_store():
    store_window = tk.Toplevel(root)
    store_window.title("Game Store")
    store_window.geometry("800x400")

    # Create two frames: one for game list and one for game details
    global game_list_frame, game_info_frame

    game_list_frame = tk.Frame(store_window, width=300)
    game_list_frame.pack(side='left', fill='y', padx=10)

    game_info_frame = tk.Frame(store_window)
    game_info_frame.pack(side='right', fill='both', expand=True, padx=10)

    # Add buttons for changing and resetting repo URL
    repo_controls_frame = tk.Frame(store_window)
    repo_controls_frame.pack(side='top', fill='x')

    change_repo_button = tk.Button(repo_controls_frame, text="Change Repo", command=change_repo)
    change_repo_button.pack(side='left', padx=10)

    reset_repo_button = tk.Button(repo_controls_frame, text="Back to Default Repo", command=reset_to_default_repo)
    reset_repo_button.pack(side='left', padx=10)

    # Search bar and button for searching games
    search_frame = tk.Frame(store_window)
    search_frame.pack(side='top', fill='x', padx=10, pady=10)

    search_label = tk.Label(search_frame, text="Search Game:")
    search_label.pack(side='left')

    search_entry = tk.Entry(search_frame)
    search_entry.pack(side='left', padx=5)

    search_button = tk.Button(search_frame, text="Search", command=lambda: search_games(search_entry.get()))
    search_button.pack(side='left', padx=5)

    # Fetch the list of games
    games_data = fetch_games()
    
    if games_data:
        update_game_list(games_data)  # Update game list in the new window
    else:
        messagebox.showinfo("No Games", "No games available at the moment.")

# Function to search games based on user input
def search_games(query):
    games_data = fetch_games()
    filtered_games = [game for game in games_data if query.lower() in game['name'].lower()]
    
    if filtered_games:
        update_game_list(filtered_games)  # Update the game list with filtered results
    else:
        messagebox.showinfo("No Results", "No games found matching your search.")

# Function to change the repo URL
def change_repo():
    global current_repo_url
    new_repo_url = simpledialog.askstring("Change Repo", "Enter the new GitHub repository URL (games.json):")
    
    if new_repo_url:
        current_repo_url = new_repo_url
        messagebox.showinfo("Success", f"Repository changed to: {new_repo_url}")
        show_store()  # Refresh the store with the new repo
    else:
        messagebox.showwarning("Warning", "No repository URL entered.")

# Function to reset to the default repo URL
def reset_to_default_repo():
    global current_repo_url
    current_repo_url = DEFAULT_GITHUB_JSON_URL
    messagebox.showinfo("Success", "Repository reset to the default one.")
    show_store()  # Refresh the store with the default repo

# Tkinter UI Setup
root = tk.Tk()
root.title("Game Launcher")
root.geometry("600x400")

# Create a Store Button at the top
store_button = tk.Button(root, text="Store", command=show_store)
store_button.pack(pady=20)

root.mainloop()
