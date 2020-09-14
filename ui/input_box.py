from minijuegos.constantes import configuration, color
import pygame as pg
class InputBox:

    def __init__(self, x, y, w, h, text=''):
        self.rect = pg.Rect(x, y, w, h)
        self.color = color.WHITE
        self.text = text
        self.__font = pg.font.Font('data\\font\\dpcomic.ttf', 32)
        self.txt_surface = self.__font.render(text, True, self.color)
        self.active = False
        self.end = False
        self.save = True

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
        if event.type == pg.KEYDOWN:
            if self.active:
                if event.key == pg.K_RETURN:
                    self.end = True
                elif event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                elif event.key == pg.K_ESCAPE:
                    self.active = False
                elif len(self.text)<9:
                    self.text += event.unicode
                    self.text = self.text.upper()
                # Re-render the text.
                self.txt_surface = self.__font.render(self.text, True, self.color)
            else:
                if event.key == pg.K_RETURN:
                    self.active = True
                elif event.key == pg.K_ESCAPE:
                    print("Vuevlo al menu :D")
                    self.save = False
                    self.end = True
                    
        # Change the current color of the input box.
        self.color = color.RED if self.active else color.WHITE
            
    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pg.draw.rect(screen, self.color, self.rect, 2)