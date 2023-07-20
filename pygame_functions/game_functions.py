import os, json
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame


def get_font(size): 
    return pygame.font.Font("assets/fonts/kongtext.ttf", size)

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