from data.engine.debug.debugObject import SpinProjectile, TestActor, TestPlayer
from data.engine.level.level import Level
from data.engine.util.gameobjects.collider import Collider
from data.topdownshooter.content.levels.levelloader.levelloader import LevelLoader
from data.topdownshooter.content.objects.camera.shootercam import ShooterCamera
from data.topdownshooter.content.objects.chest.chest import Chest
from data.topdownshooter.content.objects.dummy.dummy import Dummy
from data.topdownshooter.content.objects.enemy.boss_enemy import BossEnemy
from data.topdownshooter.content.objects.enemy.enemy import ShooterEnemy
from data.topdownshooter.content.objects.exp.exp import EXP
from data.topdownshooter.content.objects.hazard.blackhole.blackhole import BlackHole
from data.topdownshooter.content.objects.hazard.magnet.magnet import Magnet
from data.topdownshooter.content.objects.player.player import ShooterPlayer
from data.topdownshooter.content.objects.shooterentity.shooterentity import ShooterEntity
from data.topdownshooter.content.objects.turret.turret import Turret
from data.topdownshooter.content.objects.weapon.hitmarker.hitmarker import Hitmarker
from data.topdownshooter.content.objects.weapon.pickup.pickupweapon import PickupWeapon
from data.topdownshooter.content.objects.weapon.weapons.weapon import WeaponData
from data.topdownshooter.content.objects.weapon.weapons.weapons import P90, SMG, AntiMatterRifle, AutoShotgun, AutomaticRifle, Biblizer, Buckshot, ChainRifle, DartRifle, DevGun, ElectroLauncher, Enderpearl, FlamePistol, Flamethrower, Friendship, Godray, GrenadeLauncher, InfinityRifle, LaserMachineGun, LaserPistol, LaserRifle, LooseChange, Medpack, Pistol, Revolver, RiskGun, RocketLauncher, Scorcher, Shotgun, SniperRifle, SpawnerWeapon, SplatGun, Starmada, Terminator
from data.topdownshooter.content.objects.widget.fadeout import FadeOut
from data.topdownshooter.content.objects.widget.shooterwidget import ShooterWidget


class DevLevel(Level):
    def __init__(self, man, pde) -> None:
        self.ticks = 0
        super().__init__(man, pde)
        self.changebackground(r'data\topdownshooter\assets\sprites\backgrounds\bg.png')


        #self.pde.game.ui = self.pde.display_manager.userInterface.add_object(ShooterWidget(man=self.pde.display_manager.userInterface, pde=self.pde, owner=p))


        #self.objectManager.add_object(ShooterEnemy(man=self.objectManager, pde=pde, position=[732/2, 412/2], weapon=LaserMachineGun))
        itemlist = [SMG, AutomaticRifle, SniperRifle, LaserMachineGun, GrenadeLauncher, Shotgun, ElectroLauncher, SpawnerWeapon, Enderpearl, SplatGun, RocketLauncher, Revolver, ChainRifle, LaserPistol, Pistol, RiskGun, FlamePistol, LooseChange, AutoShotgun, Flamethrower, DartRifle, Starmada, AntiMatterRifle, Godray, Friendship, Biblizer, P90, Scorcher, InfinityRifle, Buckshot, Terminator, SpawnerWeapon]

        lm = self.objectManager.add_object(LevelLoader(man=self.objectManager, pde=pde, position=[320,300],level="room2"))
        chest = self.objectManager.add_object(Chest(man=self.objectManager, pde=pde, position=[320,-128], items=[DevGun]))
        dummy = self.objectManager.add_object(Dummy(man=self.objectManager, pde=pde, position=[320,-64]))


        #b = self.objectManager.add_object(BlackHole(man=self.objectManager, pde=pde, position=[320,-64], owner=p))
