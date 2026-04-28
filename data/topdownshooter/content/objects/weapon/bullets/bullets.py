import math
import random
from numpy import isin
import pygame
from data.engine.actor.actor import Actor
from data.engine.fl.world_fl import getpositionlookatpositionvector, getpositionlookatvector, objectlookatposition, objectlookattarget, positionlookatposition
from data.engine.sprite.sprite_component import SpriteComponent
from data.topdownshooter.content.objects.hazard.blackhole.blackhole import BlackHole
from data.topdownshooter.content.objects.hazard.explosion.explosion import Explosion
from data.topdownshooter.content.objects.hazard.mine.mine import Mine
from data.topdownshooter.content.objects.hazard.splat.splat import Splat
import data.topdownshooter.content.objects.shooterentity.shooterentity as se
from data.topdownshooter.content.objects.weapon.bullets.bullet import Bullet
from data.topdownshooter.content.tiles.tile import Tile




class HomingActor(Actor):
    def __init__(self, man, pde, position=[0, 0], owner=None):
        super().__init__(man, pde)
        self.position = position
        self.scale = [400, 400]
        self.owner = owner
        self.target = None
        self.foundtarget = False
        self.checkForCollision = False

    def overlap(self, obj):
        if self.foundtarget == False:
            self.target = obj
            if hasattr(obj, 'homable'):
                if isinstance(obj, se.ShooterEntity) and obj != self.owner.owner.owner:
                    self.owner.target = getpositionlookatvector(self, obj.position)
                    self.owner.rotation = objectlookattarget(self, obj)
        return super().overlap(obj)

    def update(self):
        self.rect.center = self.owner.rect.center
        return super().update()

class DefaultBullet(Bullet):
    def __init__(self, man, pde, owner=None, position=[0, 0], target=[0, 0]):
        super().__init__(man, pde, owner, position, target)

class DevBullet(Bullet):
    def __init__(self, man, pde, owner=None, target=[0,0], position=[0, 0], scale=[20, 4]):
        super().__init__(man, pde, owner, position=position, scale=scale,target=target, sprite=r'data\topdownshooter\assets\sprites\weapons\devgun\devbullet.png')
        self.scale = scale
        self.damage = 5
        self.homing = False
        self.hometicks = 0
        self.starthometime = 1
        self.area = None
        self.speed=24

    def update(self):
        self.hometicks += 1
        if self.hometicks >= self.starthometime:
            if not self.homing:
                self.homing = True
        for obj in self.getNeighboringObjects():
            if hasattr(obj, 'homable'):
                if isinstance(obj, se.ShooterEntity) and obj is not self.shooter:
                    if self.shooter is not None:
                        if type(obj) not in self.shooter.ignoreEntities:
                            self.target = getpositionlookatvector(self, obj.position)
                            self.rotation = objectlookattarget(self, obj)

        return super().update()

    def deconstruct(self, outer=None):
        return super().deconstruct(outer)


class Grenade(Bullet):
    def __init__(self, man, pde, owner=None, target=[0,0], scale = [20, 14],position=[0, 0]):
        super().__init__(man, pde, owner, position=position, scale=scale, target=target, sprite=r'data\topdownshooter\assets\sprites\weapons\grenadelauncher\grenade.png')
        self.lifetime = 120
        self.destroyOnCollide = False
        self.checkForCollision = True
        self.speed = 12
        self.damage = 3
        self.fuse=60
        self.fusetime = 0
        self.explosion = Explosion
        

    def update(self):

        if self.speed > 0.3:
            self.speed -= 0.3
        else:
            self.speed = 0

        self.fusetime += 1
        if self.fusetime >= self.fuse:
            self.explode()
            self.queuedeconstruction()
        
        return super().update()

    def collide(self, obj, side):
        if side == "Left":
            self.target = pygame.Vector2(self.target.reflect((-1,0)))
        if side == "Right":
             self.target = pygame.Vector2(self.target.reflect((1,0)))
        if side == "Top":
             self.target = pygame.Vector2(self.target.reflect((0, -1)))
        if side == "Bottom":
            self.target = pygame.Vector2(self.target.reflect((0, 1)))
        return super().collide(obj, side)

    def checkXcollision(self, movement):
        if self.canMove:
            self.rect.x += self.movement.x * self.velocity
            hits = self.getoverlaps()  
            for object in hits:
                if hasattr(object, 'checkForCollision') and object.checkForCollision and self.checkForCollision:
                    if object != self.owner and object != self.owner.owner and not isinstance(self, object.__class__):
                        if object not in self.collideInfo["Objects"]:
                            self.collideInfo["Objects"].append(object)
                        if movement[0] > 0:
                            self.rect.right = object.rect.left
                            self.collideInfo["Right"] = True
                            self.collide(self, "Right")
                        elif movement[0] < 0:
                            self.rect.left = object.rect.right
                            self.collideInfo["Left"] = True
                            self.collide(self, "Left")

    def checkYcollision(self, movement):
        if self.canMove:
            self.rect.y += self.movement.y * self.velocity
            hits = self.getoverlaps()  
            for object in hits:
                if hasattr(object, 'checkForCollision') and object.checkForCollision and self.checkForCollision:
                    if object != self.owner and object != self.owner.owner and not isinstance(self, object.__class__):
                        if object not in self.collideInfo["Objects"]:
                            self.collideInfo["Objects"].append(object)
                        if movement[1] > 0:
                            self.rect.bottom = object.rect.top
                            self.collideInfo["Bottom"] = True
                            self.collide(self, "Bottom")
                        elif movement[1] < 0:
                            self.rect.top = object.rect.bottom
                            self.collideInfo["Top"] = True
                            self.collide(self, "Top")

    def explode(self):
        self.man.add_object(obj=Explosion(man=self.man, pde=self.pde, owner=self.owner, position=self.rect.center, scale=[128, 128]))

class LaserBullet(Bullet):
    def __init__(self, man, pde, owner=None, position=[0, 0], target=[0, 0]):
        super().__init__(man, pde, owner, position, target, scale=[20, 4], sprite=r'data\topdownshooter\assets\sprites\weapons\lasermachinegun\laserbullet.png')
        self.speed = 20
        self.damage = 5

class SniperBullet(Bullet):
    def __init__(self, man, pde, owner=None, position=[0, 0], target=[0, 0]):
        super().__init__(man, pde, owner, position, target, scale=[24, 3], sprite=r'data\topdownshooter\assets\sprites\weapons\sniper\sniperbullet.png')
        self.speed = 24
        self.damage = random.randint(80, 120)

class RevolverBullet(Bullet):
    def __init__(self, man, pde, owner=None, position=[0, 0], target=[0, 0]):
        super().__init__(man, pde, owner, position, target, scale=[24, 3], sprite=r'data\topdownshooter\assets\sprites\weapons\sniper\sniperbullet.png')
        self.speed = 32
        self.damage = 20

class ShotgunBullet(Bullet):
    def __init__(self, man, pde, owner=None, position=[0, 0], target=[0, 0]):
        super().__init__(man, pde, owner, position, target, sprite=r'data\topdownshooter\assets\sprites\weapons\shotgun\shotgunbullet.png')
        self.damage = 6
        self.speed = 18

    def update(self):
        super().update()
        self.speed -= 0.75
        if self.speed < 4:
            self.deconstruct()


class SMGBullet(Bullet):
    def __init__(self, man, pde, owner=None, position=[0, 0], target=[0, 0]):
        super().__init__(man, pde, owner, position, target)
        self.speed = 20
        self.damage = 2

class Electrosphere(Bullet):
    def __init__(self, man, pde, owner=None, position=[0, 0], target=[0, 0]):
        super().__init__(man, pde, owner, position, target, scale=[16, 16], sprite=r'data\topdownshooter\assets\sprites\weapons\electrospherelauncher\electroball.png')
        self.speed = 8
        self.destroyOnCollide = False
        self.checkForCollision = True
        self.mines = []
        self.trailticks = 0
        self.destroyOnOOB = False
        self.exploding = False

        self.explosion = Explosion
        self.explodeticks = 0
        self.lastoverlap = None

    def update(self):
        super().update()
        self.trailticks += 1
        if self.trailticks >= 6:
            self.trailticks = 0
            self.mines.append(self.man.add_object(obj=Mine(man=self.man, pde=self.pde, position=self.position, rotation=self.rotation)))

        if self.exploding:
            self.explode()
            

    def collide(self, obj, side):
        if side != self.lastoverlap:
            r = random.randint(0, 100)
            if r <= 25:
                self.exploding = True



        if side == "Left":
            self.target = pygame.Vector2(self.target.reflect((-1,0)))
        if side == "Right":
             self.target = pygame.Vector2(self.target.reflect((1,0)))
        if side == "Top":
             self.target = pygame.Vector2(self.target.reflect((0, -1)))
        if side == "Bottom":
            self.target = pygame.Vector2(self.target.reflect((0, 1)))

        self.lastoverlap = side
        
        return super().collide(obj, side)

    def checkXcollision(self, movement):
        if self.canMove:
            self.rect.x += self.movement.x * self.velocity
            hits = self.getoverlaps()  
            for object in hits:
                if hasattr(object, 'checkForCollision') and object.checkForCollision and self.checkForCollision:
                    if object != self.owner and object != self.owner.owner and not isinstance(self, object.__class__):
                        if object not in self.collideInfo["Objects"]:
                            self.collideInfo["Objects"].append(object)
                        if movement[0] > 0:
                            self.rect.right = object.rect.left
                            self.collideInfo["Right"] = True
                            self.collide(self, "Right")
                        elif movement[0] < 0:
                            self.rect.left = object.rect.right
                            self.collideInfo["Left"] = True
                            self.collide(self, "Left")

    def checkYcollision(self, movement):
        if self.canMove:
            self.rect.y += self.movement.y * self.velocity
            hits = self.getoverlaps()  
            for object in hits:
                if hasattr(object, 'checkForCollision') and object.checkForCollision and self.checkForCollision:
                    if object != self.owner and object != self.owner.owner and not isinstance(self, object.__class__):
                        if object not in self.collideInfo["Objects"]:
                            self.collideInfo["Objects"].append(object)
                        if movement[1] > 0:
                            self.rect.bottom = object.rect.top
                            self.collideInfo["Bottom"] = True
                            self.collide(self, "Bottom")
                        elif movement[1] < 0:
                            self.rect.top = object.rect.bottom
                            self.collideInfo["Top"] = True
                            self.collide(self, "Top")

    def explode(self):
        if self.explodeticks < len(self.mines):
            self.mines[self.explodeticks].explode()
            self.explodeticks += 1
        else:
            e = self.man.add_object(obj=self.explosion(man=self.man, pde=self.pde, owner=self.owner, position = self.position, scale = [128, 128]))
            self.deconstruct()

class SplatBullet(Bullet):
    def __init__(self, man, pde, owner=None, position=[0, 0], target=[0, 0]):
        self.color = random.choice(['blue', 'orange'])
        if self.color == 'orange':
            s = r'data\topdownshooter\assets\sprites\weapons\splatgun\splatorange.png'
        elif self.color == 'blue':
            s = r'data\topdownshooter\assets\sprites\weapons\splatgun\splatblue.png'
        super().__init__(man, pde, owner, position, target, sprite=s)
        self.speed = 15
        self.damage = 5
        self.splatticks = 0
        self.splattime = random.randint(10, 20)
        
    def hit(self, obj):
        self.splat()
        return super().hit(obj)

    def update(self):
        super().update()
        self.splatticks += 1
        if self.splatticks >= self.splattime:
            self.splat()
            self.queuedeconstruction()
            return

    def splat(self):
        self.pde.display_manager.particleManager.add_object(obj=Splat(man=self.pde.display_manager.particleManager, pde=self.pde, position=list(self.rect.center), owner=self, color=self.color))

class Rocket(Bullet):
    def __init__(self, man, pde, owner=None, position=[0, 0], target=[0, 0]):
        super().__init__(man, pde, owner, position, target, scale = [30, 20], sprite=r'data\topdownshooter\assets\sprites\weapons\rocketlauncher\rocket.png')
        self.speed = 10
        self.damage = 15
        self.reachedTarget = False
        self.spawnedRocket = False

    def hit(self, object):
        if isinstance(object, se.ShooterEntity) or isinstance(object, Tile):
            if not self.spawnedRocket:
                self.man.add_object(obj=Explosion(man=self.man, pde=self.pde, owner=self.owner, position=self.rect.center, scale=[128, 128]))
                self.spawnedRocket = True
        return super().hit(object)

class LaserBullet2(Bullet):
    def __init__(self, man, pde, owner=None, position=[0, 0], target=[0, 0]):
        super().__init__(man, pde, owner, position, target, scale = [32, 4], sprite=r'data\topdownshooter\assets\sprites\weapons\laserrifle\chainriflebullet.png')
        self.speed = 15
        self.damage = 15

class TurretBullet(Bullet):
    def __init__(self, man, pde, owner=None, position=[0, 0], target=[0, 0]):
        super().__init__(man, pde, owner, position, target, scale=[24, 3], sprite=r'data\topdownshooter\assets\sprites\weapons\turret\turret_bullet.png')
        self.speed = 30
        self.damage = 4

class PistolBullet(Bullet):
    def __init__(self, man, pde, owner=None, position=[0, 0], target=[0, 0]):
        super().__init__(man, pde, owner, position, target, scale=[12, 3], sprite=r'data\topdownshooter\assets\sprites\weapons\pistol\pistolbullet.png')
        self.speed = 18
        self.damage = 8

class FireBall(Bullet):
    def __init__(self, man, pde, owner=None, position=[0, 0], target=[0, 0]):
        super().__init__(man, pde, owner, position, target, scale = [26, 12], sprite=r'data\topdownshooter\assets\sprites\weapons\flamepistol\fireball.png')
        self.speed = 12
        self.damage = 12

class Coin(Bullet):
    def __init__(self, man, pde, owner=None, position=[0, 0], target=[0, 0]):
        super().__init__(man, pde, owner, position, target, scale = [4,4], sprite=r'data\topdownshooter\assets\sprites\weapons\loosechange\coin.png')
        self.speed = 20
        self.damage = 5

class Flame(Bullet):
    def __init__(self, man, pde, owner=None, position=[0, 0], target=[0, 0]):
        super().__init__(man, pde, owner, position, target,scale=[26,12], sprite=r'data\topdownshooter\assets\sprites\weapons\flamepistol\fireball.png')
        self.damage = 0.45
        self.speed = 18
        self.size = self.scale.copy()
        self.piercing = True

    def construct(self):
        super().construct()
        


    def update(self):
        super().update()
        if not self.paused:
            self.speed -= 0.75
            
            self.size[1] += 1
            self.components["Sprite"].sprite.scale = self.size

            if self.speed < 4:
                self.deconstruct()

class DartBullet(Bullet):
    def __init__(self, man, pde, owner=None, position=[0, 0], target=[0, 0]):
        super().__init__(man, pde, owner, position, target, scale=[20, 4], sprite=r'data\topdownshooter\assets\sprites\weapons\dartrifle\dartbullet.png')
        self.speed = 22
        self.damage = 8

class StarmadaBullet(Bullet):
    def __init__(self, man, pde, owner=None, position=[0, 0], target=[0, 0]):
        color = random.choice(['r', 'o', 'y', 'g', 'b', 'p'])
        self.color = r"data\topdownshooter\assets\sprites\weapons\starmada\starmada_" + color + ".png"


        super().__init__(man, pde, owner, position, target, sprite=self.color)
        self.speed = 20
        self.damage = 7
        self.splatticks = 0
        self.splattime = random.randint(10, 20)

class AntiMatterBullet(Bullet):
    def __init__(self, man, pde, owner=None, position=[0, 0], target=[0, 0]):
        super().__init__(man, pde, owner, position, target, scale=[20, 4], sprite=r'data\topdownshooter\assets\sprites\weapons\antimatterrifle\antimatterbullet.png')
        self.speed = 30
        self.damage = 100
        self.spawned = False

    def hit(self, obj):
        if not self.spawned:
            self.spawned = True
            b = self.man.add_object(BlackHole(man=self.man, pde=self.pde, position=self.position, owner=self.owner.owner))

class GodrayBullet(Bullet):
    def __init__(self, man, pde, owner=None, position=[0, 0], target=[0, 0]):
        super().__init__(man, pde, owner, position, target, scale=[20, 4], sprite=r'data\topdownshooter\assets\sprites\weapons\godray\godraybullet.png')
        self.lifetime = 360
        self.speed = 18
        self.damage = 1

    def update(self):
        if self.ticks >= 300:
            self.components["Sprite"].sprite.opacity -= 5
        super().update()

    def construct(self):
        super().construct()

class BiblizerBullet(Bullet):
    def __init__(self, man, pde, owner=None, position=[0, 0], target=[0, 0]):
        super().__init__(man, pde, owner, position, target, sprite=r'data\topdownshooter\assets\sprites\weapons\godray\godraybullet.png')
        self.damage = 8
        self.speed = 18

    def update(self):
        super().update()
        self.speed -= 0.75
        if self.speed < 4:
            self.deconstruct()

class BuckshotBullet(Bullet):
    def __init__(self, man, pde, owner=None, position=[0, 0], target=[0, 0]):
        super().__init__(man, pde, owner, position, target, sprite=r'data\topdownshooter\assets\sprites\weapons\shotgun\shotgunbullet.png')
        self.damage = 6
        self.speed = 18
        self.destroyOnCollide = False
        self.checkForCollision = True
        self.lastoverlap = None


    def update(self):
        super().update()
        if self.lifetime > 360:
            self.speed -= 0.75
            if self.speed < 4:
                self.deconstruct()

    def collide(self, obj, side):
        if side != self.lastoverlap:
            r = random.randint(0, 100)
            if r <= 25:
                self.exploding = True



        if side == "Left":
            self.target = pygame.Vector2(self.target.reflect((-1,0)))
        if side == "Right":
             self.target = pygame.Vector2(self.target.reflect((1,0)))
        if side == "Top":
             self.target = pygame.Vector2(self.target.reflect((0, -1)))
        if side == "Bottom":
            self.target = pygame.Vector2(self.target.reflect((0, 1)))

        self.components["Sprite"].sprite.rotation = objectlookatposition(self, obj.rect.center) + 180

        self.lastoverlap = side
        
        return super().collide(obj, side)

    def checkXcollision(self, movement):
        if self.canMove:
            self.rect.x += self.movement.x * self.velocity
            hits = self.getoverlaps()  
            for object in hits:
                if hasattr(object, 'checkForCollision') and object.checkForCollision and self.checkForCollision:
                    if object != self.owner and object != self.owner.owner and not isinstance(self, object.__class__):
                        if object not in self.collideInfo["Objects"]:
                            self.collideInfo["Objects"].append(object)
                        if movement[0] > 0:
                            self.rect.right = object.rect.left
                            self.collideInfo["Right"] = True
                            self.collide(self, "Right")
                        elif movement[0] < 0:
                            self.rect.left = object.rect.right
                            self.collideInfo["Left"] = True
                            self.collide(self, "Left")

    def checkYcollision(self, movement):
        if self.canMove:
            self.rect.y += self.movement.y * self.velocity
            hits = self.getoverlaps()  
            for object in hits:
                if hasattr(object, 'checkForCollision') and object.checkForCollision and self.checkForCollision:
                    if object != self.owner and object != self.owner.owner and not isinstance(self, object.__class__):
                        if object not in self.collideInfo["Objects"]:
                            self.collideInfo["Objects"].append(object)
                        if movement[1] > 0:
                            self.rect.bottom = object.rect.top
                            self.collideInfo["Bottom"] = True
                            self.collide(self, "Bottom")
                        elif movement[1] < 0:
                            self.rect.top = object.rect.bottom
                            self.collideInfo["Top"] = True
                            self.collide(self, "Top")

class VelocityRocket(Rocket):
    def construct(self):
        super().construct()
        self.speed = 20