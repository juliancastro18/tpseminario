from minijuegos.constantes import configuration, color
import pygame as pg
class InputBox:
    #TODO: Hacer sin el recuadro :D
    def __init__(self, x, y, w, h, text='', limit_len_txt = 9, size_font = 32, limit_char = '_'):
        self.rect = pg.Rect(x, y, w, h)
        self.color = color.WHITE
        self.text = text 
        self.__font = pg.font.Font('data\\font\\dpcomic.ttf', size_font)
        self.txt_surface = self.__font.render(text, True, self.color)
        
        self.active = True
        self.end = False
        self.save = True
        self.script_activated = True
        
        self.limit_char = limit_char
        
        self.limit_len_txt = limit_len_txt
        self.blink_time = -1
        
       

    def handle_event(self, event):
        if event.type == pg.KEYDOWN:
            if self.active:
                if event.key == pg.K_RETURN:
                    self.end = True
                elif event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]#Lo que hace es generar un nuevo string sin el ultimo caracter
                elif event.key == pg.K_ESCAPE:
                    self.save = False
                    self.end = True
                elif len(self.text)<self.limit_len_txt:
                    self.text += event.unicode #retorna el caracter de la tecla presionada en el evento
                    self.text = self.text.upper()
                # Re-render the text.
                self.txt_surface = self.__font.render(self.text, True, self.color)
            else:
                if event.key == pg.K_RETURN:
                    self.active = True
                elif event.key == pg.K_ESCAPE:
                    self.save = False
                    self.end = True
                    
        # self.color = color.WHITE if self.active else color.WHITE
            
    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width
        
        #Esto permite el parpadeo de la barra |
        #Lo hago apartir de un temporizador, cada 300 ms
        if self.blink_time==-1:
            self.script_activated = not self.script_activated
            self.blink_time = pg.time.get_ticks() + 300
        elif self.blink_time < pg.time.get_ticks():
            self.blink_time=-1
        
        
        if self.script_activated and self.active:
            self.txt_surface = self.__font.render(self.text + self.limit_char, True, self.color)
        else:
            self.txt_surface = self.__font.render(self.text , True, self.color)

    def draw(self, screen):
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))