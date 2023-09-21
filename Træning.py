import cv2 as cv
import numpy as np
import os
import tkinter as tk
from PIL import Image, ImageTk
import json

# Directory to save JSON files
json_dir = "terrain_json"
os.makedirs(json_dir, exist_ok=True)

# Main function containing the backbone of the program
def main():
    image_path = r"/Users/rubenkronborg/Desktop/Universitet/1. Semester/P0 - Projekt/hmm/King Domino dataset (1)/60.jpg"
    if not os.path.isfile(image_path):
        print("Image not found")
        return
    image = cv.imread(image_path)
    tiles = get_tiles(image)
    print(len(tiles))
    for y, row in enumerate(tiles):
        for x, tile in enumerate(row):
            print(f"Tile ({x}, {y}):")
            terrain = get_terrain(tile)
            selected_terrain = display_tile_with_buttons(tile, terrain)  # Display the tile with buttons
            save_hsv_values(x, y, selected_terrain, tile)  # Save the HSV values
            print("=====")

# Display a tile with buttons for each terrain in a popup using Tkinter
def display_tile_with_buttons(tile, terrain):
    root = tk.Tk()
    root.title("Tile Viewer")

    # Convert the OpenCV image to a Tkinter PhotoImage
    image = cv.cvtColor(tile, cv.COLOR_BGR2RGB)
    image = Image.fromarray(image)
    photo = ImageTk.PhotoImage(image=image)

    # Create a label to display the image
    label = tk.Label(root, image=photo)
    label.photo = photo  # Store a reference to avoid garbage collection
    label.pack()

    selected_terrain = tk.StringVar()
    selected_terrain.set(terrain)

    def on_button_click(terrain_type):
        selected_terrain.set(terrain_type)
        print(f"Selected terrain: {terrain_type}")
        root.destroy()  # Close the current tile viewer window

    # Create buttons for each terrain type
    for terrain_type in ["Fields", "Forest", "Lake", "Grassland", "Swamp", "Mine", "Home", "Unknown"]:
        button = tk.Button(root, text=terrain_type, command=lambda t=terrain_type: on_button_click(t))
        button.pack()

    root.mainloop()

    return selected_terrain.get()

# Save HSV values in a JSON file
def save_hsv_values(x, y, terrain, tile):
    hsv_tile = cv.cvtColor(tile, cv.COLOR_BGR2HSV)
    hue, saturation, value = np.median(hsv_tile, axis=(0, 1))

    json_filename = os.path.join(json_dir, f"{terrain.lower()}_tiles.json")

    if os.path.exists(json_filename):
        with open(json_filename, "r") as json_file:
            data = json.load(json_file)
    else:
        data = []

    data.append({
        "Hue": hue, "Saturation": saturation, "Value": value
    })

    with open(json_filename, "w") as json_file:
        json.dump(data, json_file, indent=4)

# Break a board into tiles
def get_tiles(image):
    tiles = []
    for y in range(5):
        tiles.append([])
        for x in range(5):
            tiles[-1].append(image[y*100:(y+1)*100, x*100:(x+1)*100])
    return tiles

# Determine the type of terrain in a tile
def get_terrain(tile):
    hsv_tile = cv.cvtColor(tile, cv.COLOR_BGR2HSV)
    hue, saturation, value = np.median(hsv_tile, axis=(0, 1))
    print(f"[Hue: {hue}, S: {saturation}, V: {value}]")

if __name__ == "__main__":
    main()
