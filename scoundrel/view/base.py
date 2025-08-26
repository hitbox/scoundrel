from abc import ABC
from abc import abstractmethod

class ViewBase(ABC):

    @abstractmethod
    def init_game(self, game):
        """
        Method to initialize view interface after game is created.
        """

    @abstractmethod
    def prompt_for_turn(self, game, available_choices):
        """
        Return choice of card to play from player.
        """
