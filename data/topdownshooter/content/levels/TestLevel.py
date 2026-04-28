from data.engine.level.level import Level
from data.topdownshooter.content.objects.camera.shootercam import ShooterCamera
from data.topdownshooter.content.objects.chest.chest import Chest
from data.topdownshooter.content.objects.dummy.dummy import Dummy
from data.topdownshooter.content.objects.player.player import ShooterPlayer
from data.topdownshooter.content.objects.turret.turret import Turret
from data.topdownshooter.content.objects.weapon.pickup.pickupweapon import PickupWeapon
from data.topdownshooter.content.objects.weapon.weapons.weapon import WeaponData
from data.topdownshooter.content.objects.weapon.weapons.weapons import P90, SMG, AntiMatterRifle, AutoShotgun, AutomaticRifle, Biblizer, Buckshot, ChainRifle, DartRifle, DevGun, ElectroLauncher, Enderpearl, FlamePistol, Flamethrower, Friendship, Godray, GrenadeLauncher, InfinityRifle, LaserMachineGun, LaserPistol, LaserRifle, LooseChange, Medpack, Pistol, Revolver, RiskGun, RocketLauncher, Scorcher, Shotgun, SniperRifle, SpawnerWeapon, SplatGun, Starmada, Terminator
from data.topdownshooter.content.levels.levelloader.levelloader import LevelLoader
from data.topdownshooter.content.objects.widget.shooterwidget import ShooterWidget


class TestLevel(Level):
    def __init__(self, man, pde) -> None:
        self.ticks = 0
        super().__init__(man, pde)
        self.changebackground(r'data\topdownshooter\assets\sprites\backgrounds\bg.png')

        p = self.objectManager.add_object(ShooterPlayer(man=self.objectManager, pde=pde, position=[320, 0]))
        p.removeweapon()

        itemlist = [SMG, AutomaticRifle, SniperRifle, LaserMachineGun, GrenadeLauncher, Shotgun, ElectroLauncher, SpawnerWeapon, Enderpearl, SplatGun, RocketLauncher, Revolver, ChainRifle, LaserPistol, Pistol, RiskGun, FlamePistol, LooseChange, AutoShotgun, Flamethrower, DartRifle, Starmada, AntiMatterRifle, Godray, Friendship, Biblizer, P90, Scorcher, InfinityRifle, Buckshot, SpawnerWeapon]

        c = 0
        r = 0
        for inx, w in enumerate(itemlist):
            c += 1
            if c >= 7:
                r += 1
                c = 1
            w = itemlist[inx]
            self.objectManager.add_object(PickupWeapon(man=self.objectManager, pde=self.pde, position=[(c) * 64, r*32], speed=[0, 0], weaponData=WeaponData(weaponClass=w, upgrades=[])))
        

        lm = self.objectManager.add_object(LevelLoader(man=self.objectManager, pde=pde, position=[320,300],level="room2"))
        chest = self.objectManager.add_object(Chest(man=self.objectManager, pde=pde, position=[320,-128], items=[DevGun]))
        dummy = self.objectManager.add_object(Dummy(man=self.objectManager, pde=pde, position=[320,-64]))
        turret = self.objectManager.add_object(Turret(man=self.objectManager, pde=pde, position=[360,400]))


        self.pde.game.ui = self.pde.display_manager.userInterface.add_object(ShooterWidget(man=self.pde.display_manager.userInterface, pde=self.pde, owner=p))

        cam = self.objectManager.add_object(ShooterCamera(man=self.objectManager, pde=pde, position=p.position, target=p))


        pd = self.pde.game.playerData

        p.weapons = pd.loadout
        p.currentweapon = pd.currentWeapon
        p.switchweapon(p.currentweapon)