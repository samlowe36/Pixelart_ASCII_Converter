import pygame as pg
import numpy as np
import pygame.gfxdraw
import cv2


class ArtConverter:
    def __init__(self, path="img/fieri.jpg", pixel_size=7, color_lvl=8):
        pg.init()
        self.path = path
        self.pixel_size = pixel_size
        self.color_lvl = color_lvl
        self.image = self.get_image()
        self.res = self.width, self.height = self.image.shape[0], self.image.shape[1]
        self.surface = pg.display.set_mode(self.res)    #working window size matches image size
        self.clock = pg.time.Clock()
        self.palette, self.color_coeff = self.create_palette()

    def draw_converted_image(self):
        color_indices = self.image // self.color_coeff
        for x in range(0, self.width, self.pixel_size):
            for y in range(0, self.height, self.pixel_size):
                color_key = tuple(color_indices[x, y])
                if sum(color_key):
                    color = self.palette[color_key]
                    pygame.gfxdraw.box(self.surface, (x, y, self.pixel_size, self.pixel_size), color)

    def create_palette(self):
        colors, color_coeff = np.linspace(0, 255, num=self.color_lvl, dtype=int, retstep=True)
        color_palette = [np.array([r, g, b]) for r in colors for g in colors for b in colors]
        palette = {}
        color_coeff = int(color_coeff)
        for color in color_palette:
            color_key = tuple(color // color_coeff)
            palette[color_key] = color
        return palette, color_coeff

    def get_image(self):
        self.cv2_image = cv2.imread(self.path)
        transposed_image = cv2.transpose(self.cv2_image)
        image = cv2.cvtColor(transposed_image, cv2.COLOR_BGR2RGB)
        return image

    def draw_cv2_image(self):
        resized_cv2_image = cv2.resize(self.cv2_image, (640, 360), interpolation=cv2.INTER_AREA)
        cv2.imshow("img", resized_cv2_image)

    def draw(self): #display image in 2 windows. one using pygame and one suing open cv
        #pg.surfarray.blit_array(self.surface, self.image)  #draw image in pygame
        self.surface.fill("black")
        self.draw_converted_image()
        self.draw_cv2_image()

    def save_image(self):
        pygame_image = pg.surfarray.array3d(self.surface)
        cv2_img = cv2.transpose(pygame_image)
        cv2.imwrite("output/ascii_image.jpg", cv2_img)

    def run(self):
        while True:
            for i in pg.event.get():
                if i.type == pg.QUIT:
                    exit()
                elif i.type == pg.KEYDOWN:
                    if i.key == pg.K_s:
                        self.save_image()
            self.draw()
            pg.display.set_caption(str(self.clock.get_fps()))
            pg.display.flip()
            self.clock.tick()


if __name__ == "__main__":
    app = ArtConverter()
    app.run()
