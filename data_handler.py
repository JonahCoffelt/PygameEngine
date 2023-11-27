# Configs : {'win_size': (int width, int height), 'tile_size': int pixels}

project_path = 'Dev 1.1 - Abstraction'


def configs(current_config=None):
    if current_config:
        with open(f'{project_path}\\Assets\\SpriteSheets\\config.txt', 'w') as config_file:
            config_file.write(str(current_config))
    else:
        with open(f'{project_path}\\Assets\\SpriteSheets\\config.txt', 'r') as config_file:
            file_lines = list(config_file)
            config = eval(file_lines[0])
        return config