class GameCharacter:
    def __init__(self, name):
        # 1. Attributes initialized directly to their private variables
        self.name = name
        self.health = 100
        self.mana = 50
        self.level = 1

    @property
    def name(self):
        # 2. Read-only access to the character's name
        return self._name 
    
    @name.setter
    def name(self, value):
        self._name = value

    @property
    def health(self):
        # 3. Getter for current health
        return self._health

    @health.setter
    def health(self, value):
        # 4. Setter that clamps health between 0 and 100
        if value < 0:
            self._health = 0
        elif value > 100:
            self._health = 100
        else:
            self._health = value

    @property
    def mana(self):
        # 5. Getter for current mana
        return self._mana

    @mana.setter
    def mana(self, value):
        # 6. Setter that clamps mana between 0 and 50
        if value < 0:
            self._mana = 0
        elif value > 50:
            self._mana = 50
        else:
            self._mana = value

    @property
    def level(self):
        # 7. Getter for read-only access to level
        return self._level
    
    @level.setter
    def level(self, value):
        self._level = value

    def level_up(self):
        # 8. Level up requirements:
        self._level += 1          # Increase level directly (it has no setter)
        self.health = 100         # Reset health using property setter
        self.mana = 50            # Reset mana using property setter
        print(f"{self.name} leveled up to {self.level}!")

    def __str__(self):
        # 9. Properly formatted string matching the exact requested output
        return (f"Name: {self.name}\n"
                f"Level: {self.level}\n"
                f"Health: {self.health}\n"
                f"Mana: {self.mana}")


# --- Verification ---
if __name__ == '__main__': # pragma: no cover
    kratos = GameCharacter('Kratos')
    print(kratos)