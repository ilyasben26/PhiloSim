import os, json
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame
from functions import *

def fetch_lines(root_script):
    script_file = os.path.join(root_script,'script.json')
    with open(script_file) as json_file:
        script = json.load(json_file)
    return script

def fetch_audios(root_script):
    return os.path.join(root_script, "audio")

def textHollow(font, message, fontcolor):
    notcolor = [c^0xFF for c in fontcolor]
    base = font.render(message, 0, fontcolor, notcolor)
    size = base.get_width() + 2, base.get_height() + 2
    img = pygame.Surface(size, 16)
    img.fill(notcolor)
    base.set_colorkey(0)
    img.blit(base, (0, 0))
    img.blit(base, (2, 0))
    img.blit(base, (0, 2))
    img.blit(base, (2, 2))
    base.set_colorkey(0)
    base.set_palette_at(1, notcolor)
    img.blit(base, (1, 1))
    img.set_colorkey(notcolor)
    return img

""" def blit_text(surface, text, pos, font, color=pygame.Color('black'), outlinecolor=pygame.Color('white')):
    words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
    space = font.size(' ')[0]  # The width of a space.
    max_width, max_height = surface.get_size()
    max_width = 700
    x, y = pos
    for line in words:
        for word in line:
            base = font.render(word, 0, color)
            outline = textHollow(font, word, outlinecolor)
            word_width, word_height = base.get_size()
            img = pygame.Surface(outline.get_size(), 16)
            img.blit(base, (1, 1))
            img.blit(outline, (0, 0))
            img.set_colorkey(0)
            if x + word_width >= max_width:
                x = pos[0]  # Reset the x.
                y += word_height  # Start on new row.
            
            surface.blit(img, (x, y))
            surface.blit(base, (x,y))
            
            x += word_width + space
        x = pos[0]  # Reset the x.
        y += word_height  # Start on new row. """

def blit_text(surface, text, pos, font, color=pygame.Color('black'), outlinecolor=pygame.Color('white')):
    words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
    space = font.size(' ')[0]  # The width of a space.
    max_width, max_height = surface.get_size()
    #max_width = 700
    x, y = pos
    for line in words:
        for word in line:
            base = font.render(word, 0, color)
            outline = textHollow(font, word, outlinecolor)
            word_width, word_height = base.get_size()
            img = pygame.Surface(outline.get_size(), 16)
            img.blit(base, (1, 1))
            img.blit(outline, (0, 0))
            img.set_colorkey(0)
            if x + word_width >= max_width:
                x = pos[0]  # Reset the x.
                y += word_height  # Start on new row.
            
            surface.blit(img, (x, y))
            surface.blit(base, (x,y))
            
            x += word_width + space
        x = pos[0]  # Reset the x.
        y += word_height  # Start on new row.

# creating the charcater class
class Character(pygame.sprite.Sprite):
    def __init__(self, scale_factor, image_paths, position):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
        # load image from proviede image path
        loaded_image_enabled = pygame.image.load(image_paths[0])
        loaded_image_disabled = pygame.image.load(image_paths[1])

        # scale the image and set it
        self.image_enabled = pygame.transform.scale(loaded_image_enabled, (loaded_image_enabled.get_width() * scale_factor, loaded_image_enabled.get_height() * scale_factor))
        self.image_disabled = pygame.transform.scale(loaded_image_disabled, (loaded_image_disabled.get_width() * scale_factor, loaded_image_disabled.get_height() * scale_factor))
        self.image = self.image_enabled
        # set rect
        self.rect = self.image.get_rect()
        # set position
        self.rect.center = position

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def enable(self):
        self.image = self.image_enabled
    
    def disable(self):
        self.image = self.image_disabled




pygame.init()
pygame.mixer.init()
pygame.display.set_caption('PhiloSim')
font = pygame.font.Font('freesansbold.ttf', 22)
width = 800
height = 500

# TODO: write a function that checks if the mp3 file is not corrupted, if it is then generate a new one
script_root = "./scripts/script_6"


script = fetch_lines(script_root)
root_audio = fetch_audios(script_root)

# loading the sprites

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
screen = pygame.display.set_mode((width, height))
timer = pygame.time.Clock()
snip = font.render('', True, 'white')
active_line = 0
line = script[active_line]['message']
done = False

# load background image
bg_image = pygame.image.load("./assets/backgrounds/mountain_pixelart.png")
bg_image = pygame.transform.scale(bg_image, (width, height))



run = True
while run:
    screen.blit(bg_image, (0, 0))
    timer.tick(60)
    # displaying the characters
    #screen.blit(nietzsche_sprite.image, nietzsche_sprite.rect)
    nietzsche.draw(screen)
    socrates.draw(screen)
    # displaying the text
    print(active_line)
    blit_text(screen, line, (5, 5), font, pygame.Color('black'))
    

    # handles showing the messages one by one and also the audio
    if pygame.mixer.music.get_busy() == False and active_line < len(script):
        print(f"Playing audio_{active_line}.mp3")
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
        
  

    

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and done and active_message < len(messages) - 1:
                active_message += 1
                done = False
                message = messages[active_message]
                counter = 0

    pygame.display.flip()

pygame.quit()
