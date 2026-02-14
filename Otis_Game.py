import pygame
#Your almost there! Happy Valentines babe!
# Love you so much <3

#game variables
TILE_SIZE = 32
GAME_WIDTH = 1280
GAME_HEIGHT = 720

SCALER = 1.8
PLAYER_X = GAME_WIDTH / 2
PLAYER_Y = GAME_HEIGHT / 2
PLAYER_WIDTH = 60 * SCALER
PLAYER_HEIGHT = 57 * SCALER
PLAYER_WALK_WIDTH = 66 * SCALER
PLAYER_WALK_HEIGHT = 54 * SCALER
PLAYER_JUMP_WIDTH = 75 * SCALER * .9
PLAYER_JUMP_HEIGHT = 84 * SCALER *.9
PLAYER_HIT_BOX_WIDTH = 60
PLAYER_HIT_BOX_HEIGHT = 57

PLAYER_VEL_X = 5

PLAYER_VELOCITY_Y = -17
JUMP_CUT = PLAYER_VELOCITY_Y*.5
GRAVITY = 0.5
FRICTION = 0.4

NPC_X = 50
NPC_Y = 668-PLAYER_HEIGHT
#images
def load_image (image_name, scale=None):
    image = pygame.image.load(image_name)
    if scale is not None:
        image = pygame.transform.scale(image, scale)
    return image

background_image = load_image("Images/Otis_Background.png", (GAME_WIDTH, GAME_HEIGHT))


otis_image_right =  load_image("Images/Otis_right.gif", (PLAYER_WIDTH, PLAYER_HEIGHT))

otis_image_idle_right = [load_image(f"Images/Otis_right_idle{i}.tiff",
                                      (PLAYER_WIDTH, PLAYER_HEIGHT)) for i in range(4)]
otis_image_idle_left = [load_image(f"Images/Otis_left_idle{i}.tiff",
                                      (PLAYER_WIDTH, PLAYER_HEIGHT)) for i in range(4)]
otis_image_walk_left = [load_image(f"Images/Otis_left_walk-{i+1} (dragged).tiff",
                                      (PLAYER_WIDTH, PLAYER_HEIGHT)) for i in range(8)]
otis_image_walk_right = [load_image(f"Images/Otis_rightt_walk-{i+1} (dragged).tiff",
                                      (PLAYER_WIDTH, PLAYER_HEIGHT)) for i in range(8)]
otis_image_jump_right = [load_image(f"Images/Otis_right_jump-{i+1} (dragged).tiff",
                                      (PLAYER_JUMP_WIDTH, PLAYER_JUMP_HEIGHT)) for i in range(7)]
otis_image_jump_left = [load_image(f"Images/Otis_left_jump-{i+1} (dragged).tiff",
                                      (PLAYER_JUMP_WIDTH, PLAYER_JUMP_HEIGHT)) for i in range(7)]
#Sound effects and music
pygame.init()
jump_sound = pygame.mixer.Sound("Sound Effects/jump.wav")
jump_sound.set_volume(.5)
bacgkround_music = pygame.mixer.music.load("Sound Effects/background music.mp3")

pygame.display.set_icon(otis_image_right)
WIN = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT), pygame.SCALED, vsync=1)
pygame.display.set_caption("OTIS VIDEOGAME")

class Player(pygame.Rect):
    def __init__(self, x = PLAYER_X, y = PLAYER_Y, width = PLAYER_WIDTH, height = PLAYER_HEIGHT):
        super().__init__(x, y, width, height)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = None
        self.animations = {
            "idle": {"left" : otis_image_idle_left, "right" : otis_image_idle_right},
            "walk": {"left" : otis_image_walk_left, "right" : otis_image_walk_right},
            "jump": {"left" : otis_image_jump_left, "right" : otis_image_jump_right}
        }
        self.velocity_x = 0
        self.velocity_y = 0
        self.direction ="right"
        self.state = "idle" #current state: idle, walking, jumping
        self.in_air = False
        self.current_jumping_index = 0
        self.last_updated_jumping_index = pygame.time.get_ticks()
        self.current_idle_index = 0
        self.last_updated_idle_index = pygame.time.get_ticks()
        self.current_walking_index = 0
        self.last_updated_walking_index = pygame.time.get_ticks()
        self.current_falling_index = 0
        self.last_updated_falling_index = pygame.time.get_ticks()

    def update_image(self):
        if self.state == "idle":
            if self.direction == "right":
                self.image = self.animations["idle"]["right"][self.current_idle_index]
            elif self.direction =="left":
                self.image = self.animations["idle"]["left"][self.current_idle_index]
            self.update_idle_animation()
        else:
            self.current_idle_index = 0

        if self.state == "walking":
            if self.direction == "right":
                self.image = self.animations["walk"]["right"][self.current_walking_index]
            elif self.direction == "left":
                self.image = self.animations["walk"]["left"][self.current_walking_index]
            self.update_walking_animation()
        else:
            self.current_walking_index = 0

        if self.state == "jumping":
            if self.direction == "right":
                self.image = self.animations["jump"]["right"][self.current_jumping_index]
            elif self.direction == "left":
                self.image = self.animations["jump"]["left"][self.current_jumping_index]
            self.update_jumping_animation()
        else:
            self.current_jumping_index = 0

        if self.state == "falling": #note: this is specific to otis jump animation
            if self.direction == "right":
                self.image = self.animations["jump"]["right"][self.current_falling_index+3]
            elif self.direction == "left":
                self.image = self.animations["jump"]["left"][self.current_falling_index+3]
            self.update_falling_animation()
        else:
            self.current_falling_index = 0
    def update_idle_animation(self):
        now = pygame.time.get_ticks()
        if self.current_idle_index == 0 and now - self.last_updated_idle_index > 300:
            self.last_updated_idle_index = now
            self.current_idle_index = (self.current_idle_index + 1) % len(self.animations["idle"]["right"])
        elif (self.current_idle_index == 1 or self.current_idle_index ==3) and now - self.last_updated_idle_index > 100:
            self.last_updated_idle_index = now
            self.current_idle_index = (self.current_idle_index + 1) % len(self.animations["idle"]["right"])
        elif self.current_idle_index == 2 and now - self.last_updated_idle_index > 200:
            self.last_updated_idle_index = now
            self.current_idle_index = (self.current_idle_index + 1) % len(self.animations["idle"]["right"])
    def update_jumping_animation(self):
        #Switch to y velocity
        now = pygame.time.get_ticks()
        if (self.current_jumping_index == 0) and now - self.last_updated_jumping_index > 100:
            self.last_updated_jumping_index = now
            self.current_jumping_index = (self.current_jumping_index +1) % len(self.animations["jump"]["right"])
        elif (self.current_jumping_index in (1, 5)) and now - self.last_updated_jumping_index > 150:
            self.last_updated_jumping_index = now
            self.current_jumping_index = (self.current_jumping_index +1) % len(self.animations["jump"]["right"])
        elif (self.current_jumping_index in (2, 3, 4)) and now - self.last_updated_jumping_index > 200:
            self.last_updated_jumping_index = now
            self.current_jumping_index = (self.current_jumping_index +1) % len(self.animations["jump"]["right"])
    def update_falling_animation(self):
        now = pygame.time.get_ticks()
        if (self.current_falling_index == 0) and now - self.last_updated_falling_index > 200:
            self.last_updated_falling_index = now
            self.current_falling_index = (self.current_falling_index+1) % 4
        if (self.current_falling_index == 1) and now - self.last_updated_falling_index > 200:
            self.last_updated_falling_index = now
            self.current_falling_index = (self.current_falling_index+1) % 4
        if (self.current_falling_index == 2) and now - self.last_updated_falling_index > 150:
            self.last_updated_falling_index = now
            self.current_falling_index = (self.current_falling_index+1) % 4
    def update_walking_animation(self):
        now = pygame.time.get_ticks()
        if now - self.last_updated_walking_index > 100:
            self.last_updated_walking_index = now
            self.current_walking_index = (self.current_walking_index + 1) % len(self.animations["walk"]["right"])

    def input_logic(self):
        keys = pygame.key.get_pressed()

        if (keys[pygame.K_UP] or keys[pygame.K_SPACE]) and (self.state == "walking" or self.state == "idle"):
            self.velocity_y = PLAYER_VELOCITY_Y
            jump_sound.play()
        if event.type == pygame.KEYUP:
            if (event.key == pygame.K_SPACE or pygame.K_UP) and self.velocity_y < JUMP_CUT:
                self.velocity_y = JUMP_CUT
        if keys[pygame.K_LEFT]:
            self.direction = "left"
            self.velocity_x = -PLAYER_VEL_X
        if keys[pygame.K_RIGHT]:
            self.direction = "right"
            self.velocity_x = PLAYER_VEL_X

        # check in air, idle, falling, and walking
        if self.velocity_y != 0:
            self.in_air = True

        if self.in_air:
            if self.velocity_y < 0:
                self.state = "jumping"
            else:
                self.state = "falling"
        else:
            if self.velocity_x != 0:
                self.state = "walking"
            else:
                self.state = "idle"

    def check_tile_collision(self):
        for tile in tiles:
            if self.colliderect(tile):
                return tile
        return None

    def check_tile_collision_x(self):
        tile = self.check_tile_collision()
        if tile is not None and not tile.one_way:
            if self.velocity_x < 0:
                self.x = tile.x + tile.width
            elif self.velocity_x > 0:
                self.x = tile.x - self.width
            self.velocity_x = 0

    def check_tile_collision_y(self):
        tile = self.check_tile_collision()
        if tile is not None:
            #for solid tiles
            if tile.one_way == False:
                if self.velocity_y < 0:
                    self.y = tile.y + tile.height
                    self.velocity_y = 0

                elif self.velocity_y > 0:
                    self.y = tile.y - self.height
                    self.velocity_y = 0
                    self.in_air = False


            #for one-way platforms
            elif tile.one_way == True:
                if self.velocity_y > 0:
                    self.y = tile.y - self.height
                    self.velocity_y = 0
                    self.in_air = False

    def move(self):
        # x movement
        if self.direction == "left" and self.velocity_x < 0:
            self.velocity_x += FRICTION
        elif self.direction == "right" and self.velocity_x > 0:
            self.velocity_x -= FRICTION
        else:
            self.velocity_x = 0

        self.x += self.velocity_x
        if self.x < 0:
            self.x = 0
        elif self.x + self.width > GAME_WIDTH:
            self.x = GAME_WIDTH - self.width

        self.check_tile_collision_x()

        # y movement
        self.velocity_y += GRAVITY
        self.y += self.velocity_y
        self.check_tile_collision_y()

class NPC(Player):
    def __init__(self, x = NPC_X, y = NPC_Y):
        super().__init__(x, y)


class Tile (pygame.Rect):
    def __init__(self, x, y, is_one_way=False):
        pygame.Rect.__init__(self, x, y, TILE_SIZE, 5)
        #self.image = image
        self.one_way = is_one_way

def create_map():

    for i in range(64):
        tile = Tile(i*TILE_SIZE, 668)
        tiles.append(tile)

    for i in range(12):
        tile = Tile(i*TILE_SIZE+490, 550, is_one_way=True)
        tiles.append(tile)

    for i in range(12):
        tile = Tile(i*TILE_SIZE+490, 375, is_one_way=True)
        tiles.append(tile)

    for i in range(6):
        tile = Tile(i * TILE_SIZE + 1095, 150, is_one_way=True)
        tiles.append(tile)

def draw():
    WIN.blit(background_image, (0, 0))
    #uncomment to check player boundaries
    #pygame.draw.rect(WIN, "blue", otis)
    # pygame.draw.rect(WIN, "green", basha)
    otis.update_image()
    WIN.blit(otis.image, otis)
    #uncomment to see tiles
    # for tile in tiles:
    #      pygame.draw.rect(WIN, "red", tile)




clock = pygame.time.Clock()

# Start game
otis = Player()
basha = NPC()
tiles = []
create_map()
run = True
pygame.mixer.music.play(-1)
while run:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break

    otis.input_logic()

    otis.move()


    draw()
    pygame.display.update()

pygame.quit()