import sys
import gc
import pygame
from pygame.locals import *



class PygameWindow:
    def __init__(self, size=(800, 850)):
        pygame.init()
        self.screen_size = size
        self.screen = pygame.display.set_mode(size)
        pygame.display.set_caption('Cash Register system')
        self.screen.fill((0,0,0))
        self.h = 30
        self.font = None


    def blit(self, txt, size=30, point=None):
        font = pygame.font.SysFont(self.font, size)
        text = font.render(txt, True, (255,255,255))
        if point == None:
            self.screen.blit(text, (40, self.h))
        else:
            self.screen.blit(text, (point[0], point[1]))
        pygame.display.update()
        self.h += size
        

    def clear(self):
        pygame.display.flip()



    def event_enter(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and \
                        (event.key == K_RETURN or event.key == K_KP_ENTER):
                    return


    def blit_image(self, img_path, point=None, img_size=None):
        show_img = pygame.image.load(img_path)
        if img_size ==None:
            pass
        else:
            show_img = pygame.transform.scale(show_img, (img_size[0], img_size[1]))
        if point == None:
            self.screen.blit(show_img, (40, self.h))
        else:
            self.screen.blit(show_img, (point[0], point[1]))
        pygame.display.update()
        del show_img
        gc.collect()
        self.h += 440
        
        
    
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

    def event_012(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == K_0:
                    return 0
                elif event.type == pygame.KEYDOWN and event.key == K_1:
                    return 1
                elif event.type == pygame.KEYDOWN and event.key == K_2:
                    return 2
