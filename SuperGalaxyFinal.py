from livewires import games, color
import random
import math

games.init(screen_width = 640, screen_height=540, fps=50)

about_message = games.Message(value = "Super Awesome Galaxy Shooter",
                              size = 50, color = color.red,
                              x = games.screen.width/2,
                              y = games.screen.width/2 - 90,
                              lifetime=95, after_death= None,
                              is_collideable=False)

games.screen.add(about_message)

about_message2 = games.Message(value = "by Adam Sestina",
                              size = 40, color = color.red,
                              x = games.screen.width/2,
                              y = games.screen.width/2 - 60,
                              lifetime=95, after_death= None, is_collideable=False)
games.screen.add(about_message2)

# class Collider(games.Sprite):
#
#
#     def update(self):
#         super(Collider, self).update()
#
#         if self.overlapping_sprites:
#             for sprite in self.overlapping_sprites:
#                 print(sprite, "!!!!!")
#                 # sprite.die()
#             self.die()
#
#
#     def die(self):
#         new_explosion = Explosion(x = self.x, y = self.y)  ## was x = self.s
#         games.screen.add(new_explosion)
#         # self.destroy()


class Stars(games.Sprite):
    """ stars to simulate movement """
    SMALL = 1
    MEDIUM = 2
    LARGE = 3
    images = {SMALL: games.load_image("small2.bmp"),
              MEDIUM: games.load_image("small3.bmp")}
    SPEED = 3

    def __init__(self, x, y, size):

        """ Initialize star sprite. """
        super(Stars, self).__init__(
            image=Stars.images[size],
            x=x, y=y,
            dy = random.choice([1]) * Stars.SPEED * random.random(), is_collideable= False)

        self.size = size

    def update(self):
        """ Wrap around screen. """
        if self.top > games.screen.height:
            self.bottom = 0

        if self.bottom < 0:
            self.top = games.screen.height

        if self.left > games.screen.width:
            self.right = 0

        if self.right < 0:
            self.left = games.screen.width

class EnemyBomb(games.Sprite):
    POINTS = 0
    image = games.load_image("aliendropping0001small.png")
    speed = 3
    BUFFER = 40


    def __init__(self, x, y):

        super(EnemyBomb, self).__init__(image = EnemyBomb.image,
                                        x= x, y= 130 + EnemyBomb.BUFFER,
                                        dy = EnemyBomb.speed,
                                        is_collideable = True)

    def update(self):

        if self.bottom > games.screen.height + 80:
            self.destroy()

        self.check_collison()

    def check_collison(self):
        for bomb in self.overlapping_sprites:
            print("in collision enemybomb")
            bomb.handleCollision()
            self.handleCollision()

    def handleCollision(self):
        print("in collision - enemy bomb")
        # EnemyBomb.POINTS += Game.SCORE.value
        self.die()

    def die(self):
        Game.SCORE.value += 10
        self.destroy()

class EnemyShip(games.Sprite):

    HEALTH = 3
    DELAY = 5
    speed = 1

    image = games.load_image("ufo.bmp", transparent=True)


    def __init__(self, y = 55, speed = 5, odds_change = 200):
        super(EnemyShip, self).__init__(image = EnemyShip.image,
                                        x = games.screen.width / 2,
                                        y = y, dx = EnemyShip.speed, is_collideable=True)

        self.odds_change = odds_change
        self.time_til_drop = 0


    def update(self):
        if self.left < 0 or self.right > games.screen.width:
            self.dx = -self.dx
        elif random.randrange(self.odds_change) == 0:
            self.dx = -self.dx

        self.check_drop()


    def check_drop(self):
        if self.time_til_drop > 0:
            self.time_til_drop -= 1
        else:
            new_bomb = EnemyBomb(x = self.x, y = 90)
            games.screen.add(new_bomb)

            # self.time_til_drop = int(new_bomb.height * 1.3 / EnemyBomb.speed) + 1
            self.time_til_drop = int(new_bomb.height * 1.3 / EnemyBomb.speed) + 1

        self.check_collision()

    def check_collision(self):
        for ufo in self.overlapping_sprites:
            ufo.handleCollision()
            self.handleCollision()

    def handleCollision(self):
        print("in collision - enemy ship",  EnemyShip.HEALTH)
        EnemyShip.HEALTH -= 1
        if EnemyShip.HEALTH == 0:
            # new_explosion = BigExplosion(x=self.x, y=self.y)  ## was x = self.s
            # games.screen.add(new_explosion)
            self.die()


    def die(self):
        Game.SCORE.value += 50
        # new_explosion = BigExplosion(x=self.x, y=self.y)  ## was x = self.s
        # games.screen.add(new_explosion)
        self.destroy()

        new_explosion = BigExplosion(x=self.x, y=self.y)  ## was x = self.s
        games.screen.add(new_explosion)

        # if EnemyShip.DELAY == 0:
        #     newEnemy = EnemyShip()
        #     games.screen.add(newEnemy)
        #     EnemyShip.HEALTH += 3
        #     EnemyShip.DELAY += 5
        #     newEnemy.dx += 1
        # else:
        #     EnemyShip.DELAY -= 1
        newEnemy = EnemyShip()
        games.screen.add(newEnemy)
        EnemyShip.HEALTH += 3
        EnemyShip.DELAY += 5
        EnemyShip.speed += 3
        print(EnemyShip.speed)

class Ship(games.Sprite):

    images = {"first":games.load_image("redTopsmall.png"),
    "left" : games.load_image("redRightsmall.png"),
    "right" : games.load_image("redLeftsmall.png")}

    MISSILE_DELAY = 15

    def __init__(self, imageString, wait, destroyed):
        super(Ship, self).__init__(image = Ship.images[imageString],
                                    x = games.mouse.x,
                                    y = games.mouse.y,
                                   is_collideable=True)
        self.saveX = self.x
        self.saveY = self.y
        self.missile_wait = wait
        self.destroyed = destroyed


    def update(self):


        if self.missile_wait > 0:
            self.missile_wait -= 1

        if games.mouse.is_pressed(0) and self.missile_wait == 0:
            self.missile_wait = Ship.MISSILE_DELAY
            print("adding missile")
            new_missile = Missile(self.x, self.y -30)
            games.screen.add(new_missile)

        self.check_collision()
        """ Move to mouse position. """
        self.x = games.mouse.x
        self.y = games.mouse.y

        if self.x == self.saveX and not self.destroyed:
            ship = Ship("first", self.missile_wait, self.destroyed)
            games.screen.add(ship)
            self.destroy()
        elif self.x < self.saveX and not self.destroyed:
            ship = Ship("right", self.missile_wait, self.destroyed)
            games.screen.add(ship)
            self.destroy()
        elif self.x > self.saveX and not self.destroyed:
            ship = Ship("left", self.missile_wait, self.destroyed)
            games.screen.add(ship)
            self.destroy()


    def check_collision(self):
        for ship in self.overlapping_sprites:
            if not (isinstance(ship, Ship)):
                ship.handleCollision()
                self.handleCollision()  ## CB added

    def handleCollision(self):
        print("in collision - ship")
        self.destroyed = True
        self.die()

    def die(self):
        self.end()


    def end(self):
        gameOver = games.Message(value="GAME OVER",
                                 size=90, color=color.red,
                                 x=games.screen.width / 2,
                                 y=games.screen.width / 2 - 90,
                                 lifetime=25, after_death=games.screen.quit,
                                 is_collideable=False)
        games.screen.add(gameOver)

        self.destroy()

class Missile(games.Sprite):
    image = games.load_image("laserGreen.png")
    BUFFER = 80
    VELOCITY_FACTOR = 7
    LIFETIME = 40

    def __init__(self, ship_x, ship_y):
        buffer_y = Missile.BUFFER
        x = ship_x
        y = ship_y - buffer_y
        #
        dx = 0
        dy = 7 ## Changed this to 1


        # super(Missile, self).__init__(image = Missile.image,x = ship_x, y = ship_y,
        #                               dx = 0, dy = 1)
        # super(Missile, self).__init__(x=ship_x, y=ship_y,
        #                              dx=0, dy=1)

        super(Missile, self).__init__(image=Missile.image,
                                       x=x, y=y,
                                      dx=dx, dy=-dy)

        self.lifetime = Missile.LIFETIME

    def update(self):
        super(Missile,self).update()
        self.lifetime  -= 1
        if self.lifetime == 0:
            self.handleCollision()

    def check_collision(self):
        for missile in self.overlapping_sprites:
            missile.handleCollision()
            self.handleCollision()

    def handleCollision(self):
        print("in collision - missile")
        new_explosion = Explosion(x=self.x, y=self.y)  ## was x = self.s
        games.screen.add(new_explosion)
        self.die()

    def die(self):
        self.destroy()



class Explosion(games.Animation):
    images = ["explosion1.bmp",
              "explosion2.bmp",
              "explosion3.bmp",
              # "explosion4.bmp",
              # "explosion5.bmp",
              # "explosion6.bmp",
              "explosion7.bmp",
              "explosion8.bmp",
              "explosion9.bmp"]


    def __init__(self, x, y):
        super(Explosion, self).__init__(images = Explosion.images,
                                        x= x, y= y,
                                        repeat_interval = 1, n_repeats = 1,
                                        is_collideable = False)
class BigExplosion(games.Animation):
    images = ["explosion1.bmp",
              "explosion2.bmp",
              "explosion3.bmp",
              "explosion4.bmp",
              "explosion5.bmp",
              "explosion6.bmp",
              "explosion7.bmp",
              "explosion8.bmp",
              "explosion9.bmp",
              "explosion1.bmp",
              "explosion2.bmp",
              "explosion3.bmp",
              "explosion4.bmp",
              "explosion5.bmp",
              "explosion6.bmp",
              "explosion7.bmp",
              "explosion8.bmp",
              "explosion9.bmp"]


    def __init__(self, x, y):
        super(BigExplosion, self).__init__(images = Explosion.images,
                                        x= x, y= y,
                                        repeat_interval = 1, n_repeats = 1,
                                        is_collideable = False)


class Game(object):
    # DELAY = 5
    SCORE = games.Text(value=0,
                            size=40,
                            color=color.red,
                            top=5,
                            right=games.screen.width - 10,
                            is_collideable=False)

    def __init__(self):
        self.level = 0


        games.screen.add(Game.SCORE)

        wall_image = games.load_image("600space.jpg", transparent=False)
        games.screen.background = wall_image

        for i in range(250):
            x = random.randrange(games.screen.width)
            y = random.randrange(games.screen.height)
            size = random.choice([Stars.SMALL, Stars.MEDIUM])
            new_star = Stars(x=x, y=y, size=size)
            games.screen.add(new_star)

        the_ship = Ship("first",0, False)
        games.screen.add(the_ship)

        enemy_ship = EnemyShip()
        games.screen.add(enemy_ship)

        games.mouse.is_visible = False

        games.screen.event_grab = False

        games.screen.mainloop()

    # def end(self):
    #     gameOver = games.Message(value="GAME OVER",
    #                              size=90, color=color.red,
    #                              x=games.screen.width / 2,
    #                              y=games.screen.width / 2 - 90,
    #                              lifetime=25, after_death=games.screen.quit,
    #                              is_collideable=False)
    #     games.screen.add(gameOver)

    # def advance(self):
    #
    #     newWave = games.Message(Value="Next Wave",
    #                             size= 90, color=color.green,
    #                             x =games.screen.width / 2,
    #                             y = games.screen.width / 2 - 90,
    #                             lifetime=25, is_collideable=False)
    #
    #     games.screen.add(newWave)
    #
    #     EnemyShip.HEALTH = EnemyShip.HEALTH + EnemyShip.HEALTH
    #     new_enemy= EnemyShip()
    #     games.screen.add(new_enemy)

def main():
    superGalaxy = Game()
    superGalaxy.play()

main()