from turtle import speed
import pygame, random

Width = 800 # размеры окна игры
Height = 600

W_Gun = 20 # размеры орудия
W_Fire = 4

W_Fly = 50 # размеры самолета
H_Fly = 10


# цвета 
Color_BG = (150, 255, 188) # фон
Color_Gun = (219, 186, 0) # орудие
Color_Fire = (255, 0, 0) # снаряд
Color_Fly = (0, 0, 255) # летящий объект
Color_Boom = (255, 0, 0) # взрыв

random.seed() # инициализировать ГСЧ

# класс снаряда
class TFire(pygame.sprite.Sprite):
    def __init__(self, location, speed):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface((W_Fire, W_Gun)) # задать образ снаряда
        self.image.fill(Color_Fire) # покрасить его в цвет
        self.rect = self.image.get_rect() # получить координаты
        self.rect.x, self.rect.y = location # установить координаты
        self.speed = speed # задать скорость
    
    # движение снаряда
    def Run(self):
        self.rect.y -= self.speed # меняем координаты

# класс самолета
class TFly(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface((W_Fly, H_Fly)) # задать образ самолета
        self.image.fill(Color_Fly) # покрасить в цвет
        self.rect = self.image.get_rect() # получить координаты

        self.speed = 5 # задать скорость

        if random.random() < 0.5: # определяем направление движения самолета
            x = 0
        else:
            x = Width
            self.speed = -self.speed # если справа, то меняем знак скорости

        y = random.randint(20, 200) # получаем случайную высоту самолета
        self.rect.x, self.rect.y = (x, y) # установить координаты

    # движение самолета
    def Run(self):
        self.rect.x += self.speed # меняем координаты


pygame.init() # запустить движок

win = pygame.display.set_mode((Width, Height)) # создаем окно

FPS = 60 # количество кадров в секунду

Sprites = pygame.sprite.Group() # спрайты - движущиеся объекты 

clock = pygame.time.Clock() # создаем часы

Gun_X = Width // 2 # координата орудия
Gun_speed = 10 # скорость перемещения орудия

# функция для рисования орудия
def DrawGun():
    pygame.draw.line(win, Color_Gun, (Gun_X, Height - W_Gun), (Gun_X - W_Gun, Height), 5)
    pygame.draw.line(win, Color_Gun, (Gun_X, Height - W_Gun), (Gun_X + W_Gun, Height), 5)

IsFire = False # выпущен ли снаряд
IsFly = False # летит ли самолет
IsBoom = False # есть ли взрыв

# постоянный цикл пока не снят флаг Running
Running = True
while Running:
    win.fill(Color_BG) # рисуем фон

    keys = pygame.key.get_pressed() # получаем какие клавиши нажаты

    if keys[pygame.K_SPACE]: # если нажат пробел
        if not IsFire: # если уже не запущен снаряд
            IsFire = True # устанавливаем флаг, что снаряд летит
            Fire = TFire((Gun_X - W_Fire / 2, Height - W_Gun), 10) # запускаем снаряд
            Sprites.add(Fire) # добавляем созданный снаряд в спрайты
    
    if keys[pygame.K_LEFT]: # если нажата клавиша влево
        Gun_X -= Gun_speed # сдвигаем орудие
        if Gun_X < 0: # если выходим за пределы поля
            Gun_X = Width # перемещаемся с другой край 

    if keys[pygame.K_RIGHT]: # если нажата клавиша вправо
        Gun_X += Gun_speed # сдвигаем орудие
        if Gun_X > Width: # если выходим за пределы поля
            Gun_X = 0 # перемещаемся на другой край

    if IsFire:
        Fire.Run() # если снаряд запущен, то перемещаем его

        if Fire.rect.y < 0:
            Sprites.remove(Fire) # если снаряд выходит за пределы поля, то удаляем его из спрайтов
            IsFire = False # снимаем флаг, что сняряд летит

        hit = pygame.sprite.collide_rect(Fly, Fire) # проверяем столкновение снаряда и самолета
        if hit: 
            Sprites.remove(Fly) # если столкновение есть, то удаляем самолет
            IsFly = False # снимае флаг полета самолета
            IsBoom = True # устанавливаем флаг взрыва
            R = 1 # задаем начальный радиус взрыва

    if (not IsFly) and (not IsBoom): # если самолет не летит и нет взрыва
        Fly = TFly() # создаем самолет
        Sprites.add(Fly) # добавляем самолет в спрайты
        IsFly = True # устанавливаем флаг

    if IsFly:
        Fly.Run() # если самолет запущен, то перемещаем

        if (Fly.rect.x > Width) or (Fly.rect.x < 0): # если самоет уходит за пределы поля
            Sprites.remove(Fly) # удаляем самолет из спрайтов
            IsFly = False # снимаем флаг

    if IsBoom: # если в режиме взрыва
       pygame.draw.circle(win, Color_Boom, (Fly.rect.x, Fly.rect.y), R, R // 2) # рисуем взрыв
       R += 1 # увеличиваем радиус
       if R > 50: # если радиус больше
           IsBoom = False # снимаем флаг взрыва 

    DrawGun() # рисуем орудие
    Sprites.draw(win) # рисуем все спрайты
    pygame.display.flip() # обновляем экран
    clock.tick(FPS) # задержка по времени

    for event in pygame.event.get():
        if event.type == pygame.QUIT: # если произошло событие QUIT
            pygame.quit() # закрываем pygame
            Running = False # выходим из цикла

