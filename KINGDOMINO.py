import cv2 as cv
import numpy as np
import os

# Main function containing the backbone of the program
def main():
    print("+-------------------------------+")
    print("| King Domino points calculator |")
    print("+-------------------------------+")
    image_path = r"C:\Users\Victor Steinrud\Downloads\King Domino dataset\40.jpg"
    if not os.path.isfile(image_path):
        print("Image not found")
        return
    image = cv.imread(image_path)
    tiles = get_tiles(image)
    print(len(tiles))
    for y, row in enumerate(tiles):
        for x, tile in enumerate(row):
            print(f"Tile ({x}, {y}):")
            print(get_terrain(tile))
            print("=====")

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
    hue, saturation, value = np.median(hsv_tile, axis=(0,1)) # Consider using median instead of mean
    print(f"H: {hue}, S: {saturation}, V: {value}")
    if 21.4 < hue < 32.01 and 172.44 < saturation < 320.25 and 126.55 < value < 235.03:
        return "Field"
    if 28.4 < hue < 77.75 and 67.48 < saturation < 205.17 and 31.74 < value < 74.95:
        return "Forest"
    if 74 < hue < 138 and 174 < saturation < 324 and 104 < value < 199:
        return "Lake"
    if 28.2 < hue < 52.3 and 156 < saturation < 289 and 83 < value < 167:
        return "Grassland"
    if 14 < hue < 27 and 37 < saturation < 169 and 72 < value < 145:
        return "Swamp"
    if 15.48 < hue < 28.76 and 39.03 < saturation < 130.49 and 28.44 < value < 70.83:
        return "Mine"
    if 19 < hue < 40 and 40 < saturation < 120.73 and 52.42 < value < 144.49:
        return "Home"
    return "Unknown"

if __name__ == "__main__":
    main()