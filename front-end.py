import os, json, sys
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame
from random import randrange
from backend_functions import *
from pygame_functions import *
#from button import Button
#from character import Character
from pygame_components import *



pygame.init()
pygame.mixer.init()
pygame.display.set_caption('PhiloSim')
font = get_font(18)
width = 800
height = 500
SCREEN = pygame.display.set_mode((width, height))
BG = pygame.image.load("./assets/backgrounds/mountain_pixelart.png")
BG = pygame.transform.scale(BG, (width, height))

scripts_root = "scripts"


## Nietzsche
nietzsche_images = [
    "assets/characters/nietzsche.png",
    "assets/characters/nietzsche_grey.png"
]
nietzsche = Character(3, nietzsche_images, (700, 320))

## Socrates
socrates_images = [
    "assets/characters/socrates.png",
    "assets/characters/socrates_grey.png"
]
socrates = Character(4.5, socrates_images, (50, 400))

# message formalities

timer = pygame.time.Clock()
snip = font.render('', True, 'white')


# menus
def main_menu():
    MENU_SCALE = 1
    MENU_LOGO = pygame.image.load("assets/logo/logo.png").convert_alpha()
    MENU_LOGO = pygame.transform.scale(MENU_LOGO, (MENU_LOGO.get_width() * MENU_SCALE, MENU_LOGO.get_height() * MENU_SCALE))
    MENU_RECT = MENU_LOGO.get_rect()
    MENU_RECT.center = (width/2, 100)
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()
        

        # TODO: make smaller and create a background
        # TODO: add my own hove effect for a pixelated button
        PLAY_BUTTON = Button(image=pygame.image.load("assets/button/rect.png"), pos=(width/2, 250), 
                            text_input="PLAY", font=get_font(34), base_color="#bad8e5", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/button/rect.png"), pos=(width/2, 420), 
                            text_input="QUIT", font=get_font(34), base_color="#bad8e5", hovering_color="White")

        SCREEN.blit(MENU_LOGO, MENU_RECT)

        for button in [PLAY_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

def play():
    # get a random script
    random = randrange(get_count(scripts_root))
    print(f"script_{random}")
    script_root = f"./scripts/script_{random}"
    script = fetch_lines(script_root)
    root_audio = fetch_audios(script_root)
    active_line = 0
    line = script[active_line]['message']
    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()
        
        SCREEN.blit(BG, (0, 0))
        timer.tick(60)
        # displaying the characters
        nietzsche.draw(SCREEN)
        socrates.draw(SCREEN)
        # displaying the text
        blit_text(SCREEN, line, (5, 5), font, pygame.Color('black'))
    
        # handles showing the messages one by one and also the audio
        if pygame.mixer.music.get_busy() == False and active_line < len(script):
            #print(f"Playing audio_{active_line}.mp3")
            if (script[active_line]["name"]).lower() == "Socrates".lower():
                # change to grey image for Nietzsche and color for Socrates
                nietzsche.disable()
                socrates.enable()
            else:
                socrates.disable()
                nietzsche.enable()
            pygame.mixer.music.load(os.path.join(root_audio, f"audio_{active_line}.mp3"))
            pygame.mixer.music.play()
            line = script[active_line]['message']
            active_line += 1




        # later TODO: make escape button to go back to main menu
        #PLAY_BACK = Button(image=None, pos=(width/2, 460), 
        #                    text_input="BACK", font=get_font(75), base_color="White", hovering_color="Green")

        #PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        #PLAY_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.mixer.music.stop()
                    main_menu()



        pygame.display.update()


main_menu()
