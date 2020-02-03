import Dominion
import testUtility
import random
import string
from unittest import TestCase

class TestCard(TestCase):
    # set up a game with 3 players, taken from testUtility file
    def setUp(self):

        self.player_names = ["Annie","*Becky","*Carla"]
        self.supply_order = testUtility.supplyOrder

        # Pick 10 cards from box to be in the supply.
        self.supply = testUtility.buildSupply(self.player_names)

        # initialize the trash
        self.trash = []

        # Costruct the Player objects
        self.players = testUtility.buildPlayers(self.player_names)
        self.player = Dominion.Player('Annie')

# Derived class for testing Action Card
class TestAction(TestCard):
    # Test initializtion of card
    def test_init(self):
        self.setUp()
        chars = string.ascii_letters
        # test 100 times,
        for i in range(100):

            # generate random values for Action Card initialization
            name = ''.join(random.choice(chars) for x in range(random.randint(0, 100)))
            cost = random.randint(-1000000, 1000000)
            buys = random.randint(-1000000, 1000000)
            actions = random.randint(-1000000, 1000000)
            cards = random.randint(-1000000, 1000000)
            coins = random.randint(-1000000, 1000000)

            card = Dominion.Action_card(name, cost, actions, cards, buys, coins) 

            # assert that the card's attributes match the randomly generated data
            self.assertEqual(name, card.name)
            self.assertEqual(cost, card.cost)
            self.assertEqual(buys, card.buys)
            self.assertEqual(actions, card.actions)
            self.assertEqual(cards, card.cards)
            self.assertEqual(coins, card.coins)

            # these variables should always be 0 for an action card
            self.assertEqual(0, card.vpoints)
            self.assertEqual(0, card.buypower)

    # unit test for use method on Action Card
    def test_use(self):

        self.setUp()
        card = Dominion.Action_card("fakeCard", 1, 1, 1, 1, 1)
        self.assertFalse(self.player.played)

        # add to player's hand for test
        self.player.hand.append(card)
        self.assertIn(card, self.player.hand)

        card.use(self.player, self.trash)

        # make sure card is removed from hand
        # and that the card is added to 'played' list
        self.assertNotIn(card, self.player.hand)
        self.assertIn(card, self.player.played)
    
    # test augment method
    def test_augment(self):
        chars = string.ascii_letters

        # generate data
        for i in range(100):
            self.setUp()
            name = ''.join(random.choice(chars) for x in range(random.randint(0, 100)))
            cost = random.randint(-1000000, 1000000)
            buys = random.randint(-1000000, 1000000)
            actions = random.randint(-1000000, 1000000)
            cards = 2
            coins = random.randint(-1000000, 1000000)
            self.player.purse = 0
            self.player.actions = 0
            self.player.buys = 0

            card = Dominion.Action_card(name, cost, actions, cards, buys, coins)   
            handlen = len(self.player.hand)
            card.augment(self.player)

            # assert that the card gives the player the correct number of actions,
            # buys, coins, and number of cards after drawing
            self.assertEqual(self.player.actions, card.actions)
            self.assertEqual(self.player.buys, card.buys)
            self.assertEqual(self.player.purse, card.coins)
            self.assertEqual(handlen + cards, len(self.player.hand))

# Derived class for testing method of Player class
class TestPlayer(TestCase):
    def setUp(self):

        self.player_names = ["Annie","*Becky","*Carla"]
        self.supply_order = testUtility.supplyOrder

        #Pick 10 cards from box to be in the supply.
        self.supply = testUtility.buildSupply(self.player_names)

        # initialize the trash
        self.trash = []

        # Costruct the Player objects
        self.players = testUtility.buildPlayers(self.player_names)
        self.player = Dominion.Player('Annie')


    # unit test for action_balance
    def test_action_balance(self):
        self.setUp()

        # add some actions cards
        self.player.hand.append(Dominion.Action_card("action_card1", 1, 2, 0, 1, 1))
        self.player.hand.append(Dominion.Action_card("action_card2", 1, 2, 0, 1, 1))
        self.player.deck.append(Dominion.Action_card("action_card3", 1, 2, 0, 1, 1))

        # assert that the balance is calculated correctly based on number of cards the player has
        self.assertEqual(self.player.action_balance(), 70 * 3 / len(self.player.stack()))

        self.setUp()

        #repeat with different # of actions
        self.player.hand.append(Dominion.Action_card("action_card4", 1, 4, 0, 1, 1))
        self.player.hand.append(Dominion.Action_card("action_card5", 1, 2, 0, 1, 1))
        self.player.deck.append(Dominion.Action_card("action_card6", 1, 3, 0, 1, 1))

        self.assertEqual(self.player.action_balance(), 70 * 6 / len(self.player.stack()))


    # unit test for calcpoints method
    def test_calcpoints(self):
        self.setUp()
        # generate data
        x = random.randint(0, 100)
        y = random.randint(0, 100)
        z = random.randint(0, 100)

        self.player.hand.append(Dominion.Victory_card("victory_card2", 1, x))
        self.player.hand.append(Dominion.Victory_card("victory_card3", 1, y))
        self.player.hand.append(Dominion.Victory_card("victory_card4", 1, z))

        self.player.hand.append(Dominion.Gardens())
        self.player.hand.append(Dominion.Gardens())

        # count number of cards
        n = 0
        for _ in self.player.stack():
            n += 1

        answer = (x + y + z + 3 + (n // 10) * 2)
        # make sure calcpoints() is equal to answer calculated above
        self.assertEqual(self.player.calcpoints(), answer)

    # unit test for draw method
    def test_draw(self):
        self.setUp()

        # create card named "topCard" to draw
        topCard = Dominion.Action_card("topCard", 1, 1, 0, 1, 1)

        # insert onto top of deck
        self.player.deck.insert(0, topCard)

        self.player.draw()
        self.assertIn(topCard, self.player.hand)
        self.assertNotIn(topCard, self.player.deck)

        self.player.discard.append(self.player.hand.pop())
        self.assertIn(topCard, self.player.discard)

        self.assertNotIn(topCard, self.player.deck)
        self.assertNotIn(topCard, self.player.hand)

        # empty deck so a call to draw will shuffle the discard pile into the deck
        self.player.deck = []
        # draw to a location of than the default (player.deck)
        # for more complete code coverage
        self.player.draw(self.player.played)
        self.assertIn(topCard, self.player.played)

    # unit test for cardsummary
    def test_cardsummary(self):
        self.setUp()

        # generate data
        x = random.randint(0, 100)
        y = random.randint(0, 100)
        z = random.randint(0, 100)

        # add victory cards to hand
        self.player.hand.append(Dominion.Victory_card("victory_card", 1, x))
        self.player.hand.append(Dominion.Victory_card("victory_card", 1, y))
        self.player.hand.append(Dominion.Victory_card("victory_card", 1, z))

        summary  = self.player.cardsummary()
        # assert there are 3 victory cards, 3 estates, 7 coppers.
        # "VICTORY POINTS" are equal to x + y + z, and then 3 extra for the 
        # 3 Estates that are also in the player's hand
        self.assertEqual(summary["victory_card"], 3)
        self.assertEqual(summary["Estate"], 3)
        self.assertEqual(summary["Copper"], 7)
        self.assertEqual(summary["VICTORY POINTS"], x + y + z + 3)

# Derived class for testing gameover method
class GameOver(TestCase):
    def setUp(self):

        self.player_names = ["Annie","*Becky","*Carla"]
        self.supply_order = testUtility.supplyOrder

        # Pick 10 cards from box to be in the supply.
        self.supply = testUtility.buildSupply(self.player_names)

        # initialize the trash
        self.trash = []

        # Costruct the Player objects
        self.players = testUtility.buildPlayers(self.player_names)
        self.player = Dominion.Player('Annie')

    def test_gameover(self):
        self.setUp()

        self.assertFalse(Dominion.gameover(self.supply))
        
        # remove provinces from supply, gameover should return true
        self.supply["Province"] = [] 
        self.assertTrue(Dominion.gameover(self.supply))

        # reset game
        self.setUp()
        self.assertFalse(Dominion.gameover(self.supply))
        # empty the supply stacks (do not empty the "Province" stack, so that
        # other gameover conditions can be tested)
        for stack in self.supply:
            if stack != "Province":
                self.supply[stack] = []

        self.assertTrue(Dominion.gameover(self.supply))

