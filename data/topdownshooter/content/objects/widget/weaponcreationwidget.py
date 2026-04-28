import json
from data.engine.actor.actor import Actor
from data.engine.sprite.sprite_component import SpriteComponent
from data.engine.widgets.button import Button

class UpgradeSlot(Actor):
    def __init__(self, man, pde, position=[0, 0], selector=None):
        self.position = position
        self.scale = [100, 100]
        self.useCenterForPosition = True
        self.selector = selector
        self.upgradedata = json.load(open(r"data\topdownshooter\data\upgradedata.json"))

        super().__init__(man, pde)

    def construct(self):
        super().construct()
        self.components["Sprite"] = SpriteComponent(owner=self, sprite=r'data\topdownshooter\assets\sprites\objects\upgrades\blank.png', layer=0)

    def click(self, button):

        if button.side == 'left' and self.selector.upgradeindex > 0:
            self.selector.upgradeindex -= 1
        elif button.side == 'right' and self.selector.upgradeindex < len(self.selector.widget.allupgrades)-1:
            self.selector.upgradeindex += 1

        self.components["Sprite"] = SpriteComponent(owner=self, sprite=self.upgradedata[self.selector.widget.allupgrades[self.selector.upgradeindex]]["spriteinfo"]["sprite"], layer=0)

class UpgradeSwitchButton(Actor):
    def __init__(self, man, pde, position=[0, 0], side='left', slot=None, widget=None):
        super().__init__(man, pde)
        self.position = position
        self.scale = [20, 40]
        self.useCenterForPosition = True
        self.side = side
        self.slot = slot
        self.widget = widget
        self.components["Button"] = Button(owner=self, bind=self.click)

    def construct(self):
        super().construct()
        self.components["Sprite"] = SpriteComponent(owner=self, sprite='', layer=0)

    def click(self):
        self.slot.click(self)

class UpgradeSelector(Actor):
    def __init__(self, man, pde, position=[0,0], widget=None):
        self.position=position
        self.scale = [1, 1]
        self.widget = widget
        self.upgradeindex = 0
        super().__init__(man, pde)

    def construct(self):
        super().construct()
        self.slot = self.man.add_object(UpgradeSlot(man=self.man, pde=self.pde, position=self.rect.center, selector=self))
        self.rightbutton = self.man.add_object(UpgradeSwitchButton(man=self.man, pde=self.pde, position=[self.rect.centerx + 75, self.rect.centery], side='right', slot=self.slot, widget=self.widget))
        self.leftbutton = self.man.add_object(UpgradeSwitchButton(man=self.man, pde=self.pde, position=[self.rect.centerx - 75, self.rect.centery], side='left', slot=self.slot, widget=self.widget))

class WeaponSlot(Actor):
    def __init__(self, man, pde, position=[0, 0], selector=None):
        self.position = position
        self.scale = [100, 100]
        self.useCenterForPosition = True
        self.selector = selector
        self.weapondata = json.load(open(r"data\topdownshooter\data\weapondata.json"))

        super().__init__(man, pde)

    def construct(self):
        super().construct()
        self.components["Sprite"] = SpriteComponent(owner=self, sprite=self.weapondata["AutomaticRifle"]["spriteinfo"]["sprite"], layer=0)

    def click(self, button):

        if button.side == 'left' and self.selector.upgradeindex > 0:
            self.selector.upgradeindex -= 1
        elif button.side == 'right' and self.selector.upgradeindex < len(self.selector.widget.allupgrades)-1:
            self.selector.upgradeindex += 1

        self.components["Sprite"] = SpriteComponent(owner=self, sprite=self.weapondata[self.selector.widget.allupgrades[self.selector.upgradeindex]]["spriteinfo"]["sprite"], layer=0)



class WeaponCreatorWidget(Actor):
    def __init__(self, man, pde, position):
        self.position = position
        self.scale = [1, 1]
        self.allupgrades = ["Empty", "Vamprism", "ExplosiveBullets", "SplitStream", "Disarmament"]
        self.allweapons = ["AutomaticRifle", "SMG", "SniperRifle"]
        self.availableupgrades = self.allupgrades
        super().__init__(man, pde)

    def construct(self):
        super().construct()
        self.midslot = self.man.add_object(UpgradeSelector(man=self.man, pde=self.pde, position=self.rect.center, widget=self))
        self.rightslot = self.man.add_object(UpgradeSelector(man=self.man, pde=self.pde, position=[self.rect.centerx + 200, self.rect.centery], widget=self))
        self.leftslot = self.man.add_object(UpgradeSelector(man=self.man, pde=self.pde, position=[self.rect.centerx - 200, self.rect.centery], widget=self))
        self.slots = [self.midslot, self.rightslot, self.leftslot]

    def update(self):
        return super().update()

