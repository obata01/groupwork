import sys
import gc
import pygame
from pygame.locals import *



class PygameWindow:
    def __init__(self, size=(800, 950)):
        pygame.init()
        self.screen = pygame.display.set_mode(size)
        pygame.display.set_caption('Cash Register system')
        self.screen.fill((0,0,0))
        self.h = 30


    def blit(self, txt, size=30):
        font = pygame.font.SysFont(None, size)
        text = font.render(txt, True, (255,255,255))
        self.screen.blit(text, (40, self.h))
        pygame.display.update()
        self.h += 30


    def clear(self):
        pygame.display.flip()


    def event_enter(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and \
                        (event.key == K_RETURN or event.key == K_KP_ENTER):
                    return
    
    def blit_image(self, img_pass):
        show_img = pygame.image.load(img_pass)
        self.screen.blit(show_img, (40, self.h))
        pygame.display.update()
        del show_img
        gc.collect()
        self.h += 440
        
        
#    def blit_image(self, img_pass):
#        with pygame.image.load(img_pass) as img:
#            self.screen.blit(img, (40, self.h))
#            pygame.display.update()
#        self.h += 500
        
    
    def clear_(self):
        self.h = 30
        self.screen.fill((0,0,0))
        pygame.display.update()
    
    def event_enter(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and \
                        (event.key == K_RETURN or event.key == K_KP_ENTER):
                    return
    
    def event(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and \
                        (event.key == K_ESCAPE):
                    return "esc"
                elif event.type == pygame.KEYDOWN and \
                        (event.key == K_RETURN or event.key == K_KP_ENTER):
                    return "enter"