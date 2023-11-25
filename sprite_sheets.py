import pygame
from PIL import Image

sprite_sheets = {
    'test_sheet' : 'TileTest'
}

images = {}

def split_sheet(sheet_name, path_name, tile_size):

    # Get file
    filename = "Dev 1.1 - Abstraction\\Assets\\SpriteSheets\\{}.png".format(path_name)
    filepath = f"{filename}"
    currentSheet = pygame.image.load(f"{filename}")

    for y in range(0, Image.open(filepath).size[1], tile_size):
        for x in range(0, Image.open(filepath).size[0], tile_size):

            # Creates surface with only the desired sprite/tile
            surf = pygame.Surface((tile_size, tile_size))
            surf.blit(currentSheet, (0, 0), (x, y, tile_size, tile_size))

            # Sets transparency
            surf.set_colorkey((0, 0, 0))

            images[sheet_name].append(surf)

def generate_sprite_sheets(tile_size):
    # Sheets is a dictionary of the raw sprite sheat images

    for sheet_name in sprite_sheets:
        images[sheet_name] = []
        split_sheet(sheet_name, sprite_sheets[sheet_name], tile_size)
    
    return images
