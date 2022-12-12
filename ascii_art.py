import pygame as pg
import cv2


class ArtConverter:
    def __init__(self, path="img/fieri.jpg", font_size=12, ):
        pg.init()
        self.path = path
        self.image = self.get_image()
        self.res = self.width, self.height = self.image.shape[0], self.image.shape[1]
        self.surface = pg.display.set_mode(self.res)    #working window size matches image size
        self.clock = pg.time.Clock()

        self.ascii_chars = '.",:;!~+-xmo*#W&8@'
        self.ascii_coeff = 255 // (len(self.ascii_chars) - 1)

        self.font = pg.font.SysFont("Courier", font_size, bold=True)
        self.char_step = int(font_size * 0.6)
        self.rendered_ascii_chars = [self.font.render(char, False, "white") for char in self.ascii_chars]

    def draw_converted_image(self):
        char_indices = self.image // self.ascii_coeff
        for x in range(0, self.width, self.char_step):
            for y in range(0, self.height, self.char_step):
                char_index = char_indices[x, y]
                if char_index:
                    self.surface.blit(self.rendered_ascii_chars[char_index], (x, y))

    def get_image(self):
        self.cv2_image = cv2.imread(self.path)
        transposed_image = cv2.transpose(self.cv2_image)
        gray_image = cv2.cvtColor(transposed_image, cv2.COLOR_BGR2GRAY)
        return gray_image

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
