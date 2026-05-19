from abc import ABC, abstractmethod
import random

class Player(ABC):
    def __init__(self):
        # The method now purely has 'self' with no type decorations
        self.moves = []
        self.position = (0, 0)
        self.path = [self.position]

    def make_move(self):
        # Removed the '-> tuple' type hint from here as well
        selected_move = random.choice(self.moves)
        
        current_x, current_y = self.position
        move_x, move_y = selected_move
        
        self.position = (current_x + move_x, current_y + move_y)
        self.path.append(self.position)
        return self.position

    @abstractmethod
    def level_up(self):
        pass # pragma: no cover


class Pawn(Player):
    def __init__(self):
        super().__init__()
        self.moves = [
            (0, 1),   # Up
            (0, -1),  # Down
            (-1, 0),  # Left
            (1, 0)    # Right
        ]

    def level_up(self):
        diagonal_moves = [
            (1, 1),   # Up-Right
            (1, -1),  # Down-Right
            (-1, -1), # Down-Left
            (-1, 1)   # Up-Left
        ]
        self.moves.extend(diagonal_moves)