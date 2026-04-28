import random
from types import NoneType
from data.engine.level.level import Level
from data.topdownshooter.content.levels.levelloader.levelloader import LevelLoader
from data.topdownshooter.content.levels.levelloader.room import Room
from data.topdownshooter.content.objects.camera.shootercam import ShooterCamera
from data.topdownshooter.content.objects.enemy.boss_enemy import BossEnemy
from data.topdownshooter.content.objects.hazard.hole.hole import Hole
from data.topdownshooter.content.objects.levelgenerator.level_generator import LevelGenerator
from data.topdownshooter.content.objects.player.player import ShooterPlayer
from data.topdownshooter.content.objects.turret.turret import Turret
from data.topdownshooter.content.objects.weapon.weapons.weapons import DevGun, Pistol
from data.topdownshooter.content.objects.widget.shooterwidget import ShooterWidget



class BossLevel(Level):
    def __init__(self, man, pde):
        super().__init__(man, pde)
        self.changebackground(r'data\topdownshooter\assets\sprites\backgrounds\bg.png')

        lm = self.objectManager.add_object(LevelLoader(man=self.objectManager, pde=pde, position=[-240, -240],level="default"))

        p = self.objectManager.add_object(ShooterPlayer(man=self.objectManager, pde=pde, position=lm.objects['p'][0], hp=self.pde.game.playerData.hp))

        self.pde.game.ui = self.pde.display_manager.userInterface.add_object(ShooterWidget(man=self.pde.display_manager.userInterface, pde=self.pde, owner=p))


        b = self.objectManager.add_object(BossEnemy(man=self.objectManager, pde=pde, position=lm.objects['b'][0]))

        b.onDeathEvent.bind(self.on_boss_killed)


        x = self.pde.game.playerData

        p.weapons = x.loadout

        p.currentweapon = x.currentWeapon
        p.switchweapon(p.currentweapon)
        cam = self.objectManager.add_object(ShooterCamera(man=self.objectManager, pde=pde, position=p.position, target=p))


        

    def on_boss_killed(self, enemy, killer):
        print("Boss Down!")


    def deconstruct(self):
        return super().deconstruct()


