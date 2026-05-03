from pygame import *

level = [
       "r                                                                    .",
       "r                                                                    .",
       "r                                                                    .",
       "r                                                                    .",
       "rr    °  °      l                             r    °  °  °     l     .",
       "r  ------------                                ---------------       .",
       "rr / l                                       r / l         r / l     .",
       "rr   l                                       r   l         r   l     .",
       "rr     °  l                       r     °  °     l   r         l     .",
       "r  ------                           ------------       -------       .",
       "r     r / l                                          r / l           .",
       "r     r   l                                          r   l           .",
       "r     r       °  °   l                       r   °  °    l           .",
       "r       ------------                           ---------             .",
       "r                r / l                       r / l                   .",
       "r                r   l                       r   l                   .",
       "r                                                                    .",
       "----------------------------------------------------------------------"]

class Settings(sprite.Sprite):
    def __init__(self, x, y, w, h, speed, img):
        super().__init__()
        
        self.x = x
        self.y = y
        self.speed = speed
        self.height = h
        self.width = w
        self.image = transform.scale(image.load(img), (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        
    def reset(self):
        win.blit(self.image, (self.rect.x, self.rect.y))
        
class Player(Settings):
    def move_r_l(self):
        global ball,img
        f=1
        keys = key.get_pressed()
        if keys[K_a]:
            self.rect.x -= self.speed
            ball.side='left'
            f=1
        if keys[K_d]:
            self.rect.x += self.speed
            ball.side='right'
            f=2
        if f==1:
            self.image=transform.scale(image.load(hero_l_img),(self.width,self.height))
        if f==2:
            self.image=transform.scale(image.load(hero_r_img),(self.width,self.height))
    def move_u_d(self):
        keys = key.get_pressed()
        if keys[K_w]:
            self.rect.y -= self.speed
            self.image=transform.scale(image.load(hero_stair_img),(self.width,self.height))
        if keys[K_s]:
            self.rect.y += self.speed
            self.image=transform.scale(image.load(hero_stair_img),(self.width,self.height))

class Ball(Settings):
    def __init__(self,x,y,w,h,speed,img,side):
        Settings.__init__(self,x,y,w,h,speed,img)
        self.side=side
    def update(self):
        global side
        if self.side=='left':
            self.rect.x-=self.speed
        if self.side=='right':
            self.rect.x+=self.speed

            
class Enemy(Settings):
    def __init__(self, x, y,w,h,speed,img,side):
        Settings.__init__(self, x, y,w,h,speed,img)
        self.side = side
    def update(self):
        global side
        if self.side == 'right':
            self.rect.x -= self.speed
        if self.side == 'left':
            self.rect.x += self.speed

class Camera():
    def __init__(self, camera_func, w, h):
        self.camera_func = camera_func
        self.state = Rect(0, 0, w, h)
    def apply(self, target):
        return target.rect.move(self.state.topleft)
    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)

def camera_configure(camera, target_rect):
    left, top, _, _ = target_rect
    _, _, w, h = camera
    left, top = -left +W//2, -top + H//2

    left = min(0,left)
    left = max(-(camera.width - W), left)
    top = max(-(camera.height - H), top)
    top = min(0, top)

    return Rect(left, top,w,h)

level_w = len(level[0])*40
level_h = len(level)*40

W, H = 1280, 720
win = display.set_mode((W,H))
bg_image = transform.scale(image.load("images/background.png"), (W,H)) #SV
display.set_caption("Princess VS Monsters")

font.init()
font1 = font.SysFont(('font/ariblk.ttf'), 200) 
g_name = font1.render('Princess VS Monsters', True, (106,90,205), (250,235,215))
font2 = font.SysFont(('font/ariblk.ttf'), 60) 
e_tap = font2.render('press (e)', True, (255, 0, 255))
k_need = font2.render('You need a key to open!', True, (255, 0, 255))
space = font2.render('press (space) to kill the enemy', True, (255, 0, 255))

font3 = font.SysFont(('font/calibrib.ttf'), 45) 
wasd_b = font3.render('WASD - move buttons. You can only go up and down the stairs', True, (255, 0, 0))
space_b = font3.render('Space - shoot button. You are a wizard who only knows one spell', True, (255, 0, 0))
e_b = font3.render('E - interaction button. Open doors, collect keys, activate portals', True, (255, 0, 0))

font4 = font.SysFont(('font/ariblk.ttf'), 150)
done = font4.render('LEVEL DONE!', True, (0, 255, 0), (255, 100, 0))
lose = font4.render('YOU LOSE!', True, (255, 0, 0), (245, 222, 179))
pausa = font4.render('PAUSE', True, (255, 0, 0), (245, 222, 179))

mixer.init()
fire_sound = mixer.Sound('sounds/fire.wav')
kick_sound = mixer.Sound('sounds/kick.ogg')
key_up_sound = mixer.Sound('sounds/key.wav')
coin_colected_sound = mixer.Sound('sounds/coin.wav')
door_open_sound = mixer.Sound('sounds/lock.wav')
teleport_sound = mixer.Sound('sounds/portal.wav')
click_sound = mixer.Sound('sounds/click.wav')
chest_open_sound = mixer.Sound('sounds/chest.wav') 

hero_r_img = "images/persr.png"
hero_l_img = "images/persl.png"
hero_stair_img='images/perss.png'
enemy1_r_img = "images/enemyrr.png"
enemy1_l_img = "images/enemyll.png"
enemy2_r_img='images/enemy2r.png'
enemy2_l_img='images/enemy2l.png'
coin_img = "images/coin.png"
door_img = "images/door.png"
key_img='images/key.png'
chest_open_img = "images/open.png" 
chest_close_img = "images/close.png"
stairs_img = "images/stairs.png"
teleport_img = "images/portal.png"
platform_img = "images/platform.png"
nothing_img = "images/not.png"
power_img = "images/ball.png"

player = Player(300, 650, 60,60, 5, hero_l_img)
enemy1 = Enemy(400, 400,50, 50, 3,enemy1_l_img, 'left')
enemy2 = Enemy(230, 300,90, 70, 3,enemy2_l_img, 'left')
door = Settings(1000, 585, 70, 100, 0, door_img)
key1 = Settings(160, 350, 50, 20, 0, key_img)
key2 = Settings(160, 350, 50, 20, 0, key_img)
teleport = Settings(2700, 600, 100, 100, 0, teleport_img)
chest = Settings(450, 150, 60, 60, 0, chest_close_img)
camera = Camera(camera_configure, level_w, level_h)
ball=Ball(0,-100,35,35,35,power_img,'left')

blocks_r = []
blocks_l = []
coins = []
stairs = []
platforms = []

items = sprite.Group()
balls=sprite.Group()


x = y = 0
for row in level:
    for col in row:
        if col == "r":
            tile1 = Settings(x, y, 30, 30, 0, nothing_img)
            blocks_r.append(tile1)
            items.add(tile1)
        if col == "l":
            tile2 = Settings(x, y, 30, 30, 0, nothing_img)
            blocks_l.append(tile2)
            items.add(tile2)
        if col == "/":
            tile3 = Settings(x, y-40, 40, 180, 0, stairs_img)
            stairs.append(tile3)
            items.add(tile3)
        if col == "°":
            tile4 = Settings(x, y, 40, 40, 0, coin_img)
            coins.append(tile4)
            items.add(tile4)
        if col == "-":
            tile5 = Settings(x, y, 40, 40, 0, platform_img)
            platforms.append(tile5)
            items.add(tile5)
        if col == "*":
            tile6 = Settings(x, y, 40, 40, 0, teleport_img)
            items.add(tile6)
        if col == ">":
            tile7 = Settings(x, y-40, 80,80, 0, chest_close_img)
            items.add(tile7)
        x += 40
    y += 40
    x = 0
items.add(door)
items.add(key1) 
items.add(key2)
items.add(teleport)
items.add(chest)
items.add(enemy1)
items.add(enemy2)
items.add(player)  



game = True
win.blit(bg_image, (0,0))
coin_colected = 0

while game:
    keys = key.get_pressed()
    time.delay(30)
    win.blit(bg_image, (0,0))
    for e in event.get():
        if e.type == QUIT:
            game = False
    
    enemy1.update()
    enemy2.update()
    player.move_r_l()
    for r_b in blocks_r:
        if sprite.collide_rect(player,r_b):
            player.rect.x=r_b.rect.x + player.width
        if sprite.collide_rect(enemy1,r_b):
            enemy1.side='left'
            enemy1.image=transform.scale(image.load(enemy1_r_img),(enemy1.width,enemy1.height)) #sv?
        if sprite.collide_rect(enemy2,r_b):
            enemy2.side='left'
            enemy2.image=transform.scale(image.load(enemy2_r_img),(enemy2.width,enemy2.height)) #sv?
    
    for l_b in blocks_l:
        if sprite.collide_rect(player, l_b):
            player.rect.x = l_b.rect.x - player.width
        if sprite.collide_rect(enemy1, l_b):
            enemy1.side = 'right'
            enemy1.image = transform.scale(image.load(enemy1_l_img), (enemy1.width, enemy1.height)) #sv?
        if sprite.collide_rect(enemy2, l_b):
            enemy2.side = 'right'
            enemy2.image = transform.scale(image.load(enemy2_l_img), (enemy2.width, enemy2.height)) #sv?
            
    for stair in stairs:
        if sprite.collide_rect(player,stair):
            player.move_u_d()
            #player.image=transform.scale(image.load(hero_stair_img))
            if player.rect.y<=(stair.rect.y-40):
                player.rect.y=stair.rect.y-40
            if player.rect.y>=(stair.rect.y+130):
                player.rect.y=stair.rect.y+130

    coin_col_text=font2.render("Coins: "+str(coin_colected),True,(255,255,255)) 
    win.blit(transform.scale(image.load('images/coin.png'),(50,50)),(10,10))  #sv?
    win.blit(coin_col_text,(55,15))
    
    for coin in coins:
        if sprite.collide_rect(player,coin):
            coin_colected_sound.play()
            coin_colected+=1
            coins.remove(coin)
            items.remove(coin)

    if sprite.collide_rect(player, key1):
        win.blit(e_tap, (500, 50))
        if keys[K_e]:
            key_check = True
            key_up_sound.play()
            key1.rect.y = -100
            items.remove(key1)
            key_up_sound.play()
            
    if sprite.collide_rect(player, key2):
        win.blit(e_tap, (500, 50))
        if keys[K_e]:
            key_check = True
            key_up_sound.play()
            key2.rect.y = -100
            items.remove(key2)
            key_up_sound.play()


    balls.update()
    
    if keys[K_SPACE]:
        ball.rect.x,ball.rect.y=player.rect.centerx,player.rect.centery
        balls.add(ball)
        items.add(ball)
        fire_sound.play()
    if sprite.spritecollide(enemy1,balls,True):
        enemy1.rect.y=-150
        items.remove(balls)
        kick_sound.play()
    if sprite.spritecollide(enemy2,balls,True):
        enemy2.rect.y=-150
        items.remove(balls)
        kick_sound.play()
    
    camera.update(player)
    for item in items:
        win.blit(item.image, camera.apply(item))
        
    display.update()
    