import sys
import gc
import pygame
from pygame.locals import *



class PygameWindow:
    def __init__(self, size=(800, 900)):
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


    def blit_2col(self, txt1, txt2, size=30, w=300):
        font = pygame.font.SysFont(self.font, size)
        text1 = font.render(txt1, True, (255,255,255))
        text2 = font.render(txt2, True, (255,255,255))
        self.screen.blit(text1, (40, self.h))
        self.screen.blit(text2, (w, self.h))
        pygame.display.update()
        self.h += size


    def blit_3col(self, txt1, txt2, txt3, size=30, w1=300, w2=500):
        font = pygame.font.SysFont(self.font, size)
        text1 = font.render(txt1, True, (255,255,255))
        text2 = font.render(txt2, True, (255,255,255))
        text3 = font.render(txt3, True, (255,255,255))
        self.screen.blit(text1, (40, self.h))
        self.screen.blit(text2, (w1, self.h))
        self.screen.blit(text3, (w2, self.h))
        pygame.display.update()
        self.h += size


    def blit_image(self, img_path, point=None, img_size=None):
        show_img = pygame.image.load(img_path)
        if img_size ==None:
            pass
        else:
            show_img = pygame.transform.scale(show_img, (img_size[0], img_size[1]))
        if point == None:
            self.screen.blit(show_img, (100, self.h))
        else:
            self.screen.blit(show_img, (point[0], point[1]))
        pygame.display.update()
        del show_img
        gc.collect()
        self.h += 410


    def clear(self):
        pygame.display.flip()
        
    
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

    def event_number(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == K_0:
                    return 0
                elif event.type == pygame.KEYDOWN and event.key == K_1:
                    return 1
                elif event.type == pygame.KEYDOWN and event.key == K_2:
                    return 2
                elif event.type == pygame.KEYDOWN and event.key == K_3:
                    return 3 
                elif event.type == pygame.KEYDOWN and event.key == K_4:
                    return 4 
                elif event.type == pygame.KEYDOWN and event.key == K_5:
                    return 5 
