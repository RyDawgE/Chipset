import random
from data.engine.actor.actor import Actor
from data.engine.eventdispatcher.eventdispatcher import EventDispatcher
from data.engine.fl.world_fl import getobjectlookatvector, getpositionlookatvector, objectlookatposition, objectlookattarget
from data.engine.particle.particle_emitter import ParticleEmitter
from data.topdownshooter.content.objects.particles.blood import Blood
from data.topdownshooter.content.objects.weapon.bullets.bullet import Bullet
from data.topdownshooter.content.objects.weapon.pickup.pickupweapon import PickupWeapon
from data.topdownshooter.content.objects.weapon.weapons.weapon import WeaponData
from data.topdownshooter.content.objects.widget.shooterwidget import HealthBar
import data.topdownshooter.content.objects.weapon.upgrade.upgrades as u


class ShooterEntity(Actor):
    def __init__(self, man, pde, position=[0, 0], maxhp=100, hp=100):
        super().__init__(man, pde)
        #----------< Transform Info >----------#

        self.position = position
        self.scale = [32, 32]
        self.maxVelocity = 0
        self.moveable = True

        #----------< Weapon Info >----------#
        
        self.weapon = None
        self.weapons = []
        self.stock = []
        self.currentweapon = 1
        self.maxweapons = 6
        self.weaponoffset = 10
        self.item = None

        self.ignoreEntities = []

        #----------< Stat Info >----------#

        self.maxhp = maxhp
        self.hp = hp
        self.dead = False
        self.damagable = True
        self.falling = False
        self.canGrantHP = True
        self.speed = 3
        self.handeling = 1

        #----------< Dodge Info >----------#

        self.dodgeframe = 0
        self.dodgetime = 10
        self.dodging = False
        self.dodgecooldown = 200
        self.dodgecooldowntime = 50

        #----------< Tag Info >----------#
        
        self.homable = True
        self.canPickupWeapons = True
        self.canCollectExp = True
        self.canShoot = True
        
        #----------< Visual Info >----------#

        self.bleed = False

        #----------< Timer Info >----------#

        self.deadticks = 0

        #----------< Event Dispatchers >----------#

        self.onDeathEvent = EventDispatcher()
        self.onSwitchWeaponEvent = EventDispatcher()
        self.onKillEvent = EventDispatcher()
        self.onKillEvent.bind(self.onKill)

        

    def construct(self):
        super().construct()

        self.components["Particle"] = ParticleEmitter(owner=self)

        self.healthbar = self.man.add_object(obj=HealthBar(man=self.man, pde=self.pde, owner=self))
        return
    
    def switchweapon(self, index):
        self.onSwitchWeaponEvent.call(self.currentweapon, index)
        self.currentweapon = index
        if index <= len(self.weapons):
            self.removeweapon()
            self.weapon = self.man.add_object(obj=self.createweapon(self.weapons[index-1]))
        else:
            self.removeweapon()
            self.weapon = None

    def createweapon(self, WeaponData):
        w = WeaponData.weaponClass(man=self.man, pde=self.pde, owner=self, position=[0,0])
        w.upgrades = WeaponData.weaponUpgrades.copy()
        return w

    def shootweapon(self, target):
        if self.weapon != None and self.canShoot:
            shot = self.weapon.shoot(target=target, bullet=self.weapon.bullet)
            return shot

    def altShot(self, target):
        if self.weapon != None:
            self.weapon.altShot(target)

    def update(self):
        super().update()
        
        if self.dead:
            self.deadticks += 1

        self.dodgebuffer()
        self.offsetweapon(weapon=self.weapon, offset=self.weaponoffset)

        if self.falling:
            self.fall()
        if self.speed > 3:
            self.speed -= 0.4
            
    def takedamage(self, obj, dmg):
        if self.damagable:
            self.hp -= dmg
            if self.hp <= 0 and self.hp != -1:
                if not self.dead:
                    self.die(obj)
            return True
        else:
            return False

    def dodgeroll(self):
        self.speed = 10
        return

    def dodgebuffer(self):
        self.dodgecooldown += 1
        if self.dodgecooldown >= self.dodgecooldowntime:
            if self.dodging:
                self.dodgeroll()
                self.dodgecooldown = 0
                self.dodging = False
        else:
            self.dodging = False
        return

    def die(self, killer):
        self.onDeathEvent.call(self, killer)
        if (killer.owner.owner is not None):
            killer.owner.owner.onKillEvent.call(self)
        self.dead = True
        if killer is not None:
            rot = killer.rotation
            self.dropweapon(rot)
        else:
            self.removeweapon()
        if self.weapon != None:
            self.weapon.queuedeconstruction()

    

    def offsetweapon(self, weapon, offset=10):
        if weapon is not None:
            weapon.rect.centerx = self.rect.centerx + offset
            weapon.rect.centery = self.rect.centery + offset

    def dropweapon(self, rotation=0, weapon=None):
        
        if weapon == None:
            w = self.weapon
        else:
            w = weapon

        if self.weapon is not None:
            wd = WeaponData(w.__class__, self.weapon.upgrades.copy())
            self.man.add_object(obj=PickupWeapon(man=self.man, pde=self.pde, position=list(self.rect.center), rotation=rotation, weaponData=wd, speed=[4, 4]))

            self.removeweapon()

    def interact(self):
        for o in self.overlapInfo["Objects"]:
            if o.__class__ == PickupWeapon:
                if self.canPickupWeapons:
                    self.pickupweapon(o)
                    o.deconstruct()
                    return
            
    def pickupweapon(self, obj):
        dc = WeaponData(weaponClass=obj.weaponData.weaponClass, upgrades=obj.weaponData.weaponUpgrades)
        self.addweapon(dc)
        return 
    
    def addweapon(self, dataClass):
        dc = dataClass
        if len(self.weapons) < self.maxweapons:
                self.weapons.append(dc)
                self.switchweapon(self.weapons.index(dc)+1)
        else:
            self.dropweapon(rotation=objectlookatposition(self, self.target))
            self.weapons[self.currentweapon-1] = dc
            self.switchweapon(self.weapons.index(dc)+1)


    def changeweapon(self, cls):
        self.removeweapon()
        self.weapon = self.man.add_object(obj=cls(man=self.man, pde=self.pde, owner=self, position=[self.rect.centerx + 10, self.rect.centery + 10]))
        return

    def removeweapon(self):
        if self.weapon is not None:
            self.weapon.deconstruct()
            self.weapon = None
        return
        
    def useitem(self, item):
        return item.use()


    def checkXcollision(self, movement):
        if self.canMove:
            self.rect.x += self.movement.x * round(self.speed)
            hits = self.getoverlaps()  
            for object in hits:
                if hasattr(object, 'checkForCollision') and object.checkForCollision and self.checkForCollision:
                    if not isinstance(object, Bullet):
                        if object not in self.collideInfo["Objects"]:
                            self.collideInfo["Objects"].append(object)
                        if movement[0] > 0:
                            self.rect.right = object.rect.left
                            self.collideInfo["Right"] = True
                            object.collide(self, "Left")
                        elif movement[0] < 0:
                            self.rect.left = object.rect.right
                            self.collideInfo["Left"] = True
                            object.collide(self, "Right")
        return

    def checkYcollision(self, movement):
        if self.canMove:
            self.rect.y += self.movement.y * round(self.speed)
            hits = self.getoverlaps()  
            for object in hits:
                if hasattr(object, 'checkForCollision') and object.checkForCollision and self.checkForCollision:
                    if not isinstance(object, Bullet):
                        if object not in self.collideInfo["Objects"]:
                            self.collideInfo["Objects"].append(object)
                        if movement[1] > 0:
                            self.rect.bottom = object.rect.top
                            self.collideInfo["Bottom"] = True
                            object.collide(self, "Top")
                        elif movement[1] < 0:
                            self.rect.top = object.rect.bottom
                            self.collideInfo["Top"] = True
                            object.collide(self, "Bottom")
        return

    def fall(self):
        self.canMove = False
        self.takedamage(obj=None, dmg=10)
        self.removeweapon()
        if self.rect.height > 0 and self.rect.width > 0:
            self.rect.height -= 1
            self.rect.width -= 1
        else:
            self.die(killer=None)

    def onKill(self, enemy):
        self.stock.append(random.choice(u.upgrades))
        print(self.stock)

    def deconstruct(self):
        self.healthbar.deconstruct()
        self.healthbar = None
        return super().deconstruct()