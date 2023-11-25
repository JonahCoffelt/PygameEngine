import pygame
from pygame import font

class FontRenderer():
    def __init__(self):
        self.fonts = {}
        self.load_font("Calibri")

    def load_font(self, font):
        self.fonts[font] = []
        self.fonts[font].append(pygame.font.SysFont("font", 16))
        self.fonts[font].append(pygame.font.SysFont("font", 24))
        self.fonts[font].append(pygame.font.SysFont("font", 48))
    
    def render_text(self, win, pos, text, font="Calibri", size=1, color=(255, 255, 255), bold=False, underline=False, italic=False, center_width=False):
        self.fonts[font][size].set_bold(bold)
        self.fonts[font][size].set_underline(underline)
        self.fonts[font][size].set_italic(italic)

        text_img = self.fonts[font][size].render(text, True, color)

        if center_width:
            win.blit(text_img, (pos[0] - text_img.get_width() / 2, pos[1] - self.fonts[font][size].get_height() / 2))
        else:
            win.blit(text_img, (pos[0], pos[1] - self.fonts[font][size].get_height() // 2))