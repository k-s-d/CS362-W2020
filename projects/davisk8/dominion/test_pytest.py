import Dominion
import testUtility
from unittest import TestCase

class TestCard(TestCase):
    def setUp(self):

        self.player_names = ["Annie","*Becky","*Carla"]
        self.supply_order = testUtility.supplyOrder

        #Pick 10 cards from box to be in the supply.
        self.supply = testUtility.buildSupply(self.player_names)

        #initialize the trash
        self.trash = []

        #Costruct the Player objects
        self.players = testUtility.buildPlayers(self.player_names)
        self.player = Dominion.Player('Annie')
    
    def test_init(self):
        self.setUp()
        cost = 1
        buypower = 5

        card = Dominion.Coin_card(self.player.name, cost, buypower)

        self.assertEqual('Annie', card.name)
        self.assertEqual(buypower, card.buypower)
        self.assertEqual(cost, card.cost)
        self.assertEqual("coin", card.category)
        self.assertEqual(0, card.vpoints)


    def test_react(self):
        self.assertEqual(5, 5)