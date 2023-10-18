
import pygame
import random
import color_constants
import thorpy
import json
import os
from datetime import datetime
import enum
from cart import Cart

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
    MOUSEBUTTONDOWN
)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
pygame.font.init()
font = pygame.font.Font(pygame.font.get_default_font(), 14)
os.chdir('vrail')



class AppMode(enum.IntEnum):
    DEFAULT = 0
    DELETE_NODE = 1
    ADD_NODE = 2




TRACK_FILE_NAME = 'rail_track'
class Track():

    col1 = color_constants.AQUA
    col2 = color_constants.CHARTREUSE1

    def __init__(self,screen):
        self.screen = screen

        with open(TRACK_FILE_NAME + '.json') as f:
            self.data = json.load(f)
            self.reset_ids()

    def reset_ids(self):
        for i,p in enumerate(self.data):
            p['id'] = i
            p['col'] = self.col1 if i%2==0 else self.col2


    def update(self):
        pygame.draw.lines(screen, (255, 255, 255), True,
                          [p['pos'] for p in self.data if p['type'] == 'track'])
        for p in self.data:
            pygame.draw.circle(screen, p['col'], p['pos'],20,1)

            text = font.render(str(p['id']), True, p['col'])
            screen.blit(text, (p['pos'][0] -  10,p['pos'][1] - 10))


pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

cart = Cart(SCREEN_WIDTH,SCREEN_HEIGHT)
track = Track(screen)

all_sprites = pygame.sprite.Group()
all_sprites.add(cart)
cart.set_pos( track.data[0]['pos'], track.data[1]['pos'] )

running = True
App_State = AppMode.DEFAULT

def save_track() :
    print(os.getcwd())
    os.rename(TRACK_FILE_NAME + '.json', "track_backups/"+TRACK_FILE_NAME + '_' +datetime.now().strftime("%d-%b-%Y--%H-%M-%S-%f")+'.json' )
    with open('rail_track.json', 'w') as f:
        json.dump(track.data, f)

def delete_track_point():
    global App_State
    App_State = AppMode.DELETE_NODE

def add_track_point():
    global App_State
    App_State = AppMode.ADD_NODE


def start_drive():
    global cart
    cart.toggle_drive()


button1 = thorpy.make_button("save track", func=save_track)
button2 = thorpy.make_button("delete track point", func=delete_track_point)
button3 = thorpy.make_button("add track point", func=add_track_point)
button4 = thorpy.make_button("Toggle Drive", func=start_drive)
box = thorpy.Box(elements=[button1,button2,button3,button4])
menu = thorpy.Menu(box)


for element in menu.get_population():
    element.surface = screen
box.set_topleft((0,0))


def choose_node(pos):
    ret = None
    for n in track.data:
        if (pow(n['pos'][0] - event.pos[0], 2) + pow(n['pos'][1] - event.pos[1], 2)) < 20 * 20:
            ret = n
    return ret

first_chosen_node = second_chosen_node = None
while running:

    screen.fill((0, 0, 0))
    track.update()

    box.blit() # ; box.update()

    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == QUIT:
            running = False
        elif event.type == MOUSEBUTTONDOWN:
            if App_State == AppMode.DEFAULT:
                print(event.pos)
            elif App_State == AppMode.DELETE_NODE:
                chosen = choose_node(event.pos)
                if chosen != None:
                    track.data.remove(chosen)
                    App_State = AppMode.DEFAULT

            elif App_State == AppMode.ADD_NODE:
                chosen = choose_node(event.pos)
                if first_chosen_node == None:
                    first_chosen_node = chosen
                elif second_chosen_node == None:
                    second_chosen_node = chosen
                elif chosen == None:
                    node_to_add_after = first_chosen_node if first_chosen_node['id'] > second_chosen_node['id'] else second_chosen_node
                    new_node = {"type": "track", "pos": event.pos, "col":node_to_add_after['col'] , "id": 0}
                    track.data.insert(node_to_add_after['id'],new_node)
                    first_chosen_node = second_chosen_node = None
                    track.reset_ids()



        menu.react(event) #the menu automatically integrate your elements


    pressed_keys = pygame.key.get_pressed()
    cart.update(pressed_keys)



    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    pygame.display.flip()
