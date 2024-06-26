from deliveryBots import *

import tkinter as tk
import PIL
from PIL import Image, ImageTk

class Delivery_bots_visualization(Delivery_bots_map):

    def __init__(self, map, root, sprite_size, *agentSpriteFiles):
        super().__init__(map)
    
        self.root = root
        self.sprite_size = sprite_size
        self.sprites = [[None for _ in range(self.cols)] for _ in range(self.rows)]
        
        # set up GUI
        self.canvas = tk.Canvas(root, width=self.cols * sprite_size, height=self.rows * sprite_size)
        self.canvas.pack()
        
        # load land sprites
        self.land_sprites = dict()
        self.land_sprites['.'] = Image.open("floor.png").convert("RGBA")
        self.land_sprites['#'] = Image.open("rock.png").convert("RGBA")
        self.land_sprites['!'] = Image.open("danger.png").convert("RGBA")
        
        # load agent sprites
        self.agent_sprites = [Image.open(fn).convert("RGBA") for fn in agentSpriteFiles]
        assert len(self.agent_sprites) == len(self.agent_locations), "need one sprite for each agent"
        
        # load other sprites
        self.package_sprite = Image.open("package.png").convert("RGBA")
        
        # initialize sprite grid
        for i in range(len(self.sprites)):
            for j in range(len(self.sprites[0])):
                x = i * self.sprite_size
                y = j * self.sprite_size
                self.update_tile(i, j)
        
    def update_tile(self, r, c):
        additional_images = []

	# add package sprite if neccessary
        if self.get_packages_on_tile(r, c):
            additional_images.append(self.package_sprite)
        
        # add agent sprites
        if (r,c) in self.agent_locations:
            for i in range(len(self.agent_locations)):
                if self.agent_locations[i] == (r,c):
                    additional_images.append(self.agent_sprites[i])
                    
        # glue all sprites together with land sprite
        self.set_sprite(r, c, self.land_sprites[self.map[r, c]], additional_images)
        
     
    def set_sprite(self, r, c, new_sprite_image, additional_images=[]):
        """update GUI to include multiple sprites on a given tile"""
        new_sprite_image = new_sprite_image.resize((self.sprite_size, self.sprite_size), Image.ANTIALIAS)
        for im in additional_images:
            next_img = im.resize((self.sprite_size, self.sprite_size), Image.ANTIALIAS)
            new_sprite_image.paste(next_img, (0,0), mask=next_img)
        new_sprite = ImageTk.PhotoImage(new_sprite_image)
        if not self.sprites[r][c]:
            sprite_label = tk.Label(self.canvas, image=new_sprite)
            sprite_label.image = new_sprite_image 
            sprite_label.place(x=c*self.sprite_size, y=r*self.sprite_size)
            self.sprites[r][c] = sprite_label
        self.sprites[r][c].config(image=new_sprite)
        self.sprites[r][c].image = new_sprite  


