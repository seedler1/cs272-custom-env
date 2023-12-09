import gymnasium as gym
import random
import poker  # https://github.com/Sondar4/poker-sim/blob/master/poker.py
from gymnasium import spaces


# Hand classes that can keep track of the cards of the agent, villain, and table respectively
# agent = poker.Hand('Agent')
# villain = poker.Hand('Villain')
# table = poker.Hand('Table')


def card_to_int(suit, rank):
    """
    Converts a card into an integer to store in the observation space
    :param suit: suit of a card (0->3, refer to Card class)
    :param rank: rank of a card (2->14, refer to Card class)
    :return: integer representing the unique card
    """
    rank_modified = rank - 2
    return 13 * suit + rank_modified

def int_to_card(card_int):
    """
    Converts an integer into a card to store in the observation space
    integer representing the unique card
    :param card_int: integer representing a specific card
    :return: suit of a card (0->3, refer to Card class) and rank of a card (2->14, refer to Card class)
    """
    rank_modified = card_int % 13
    rank = rank_modified + 2
    suit = (card_int - rank_modified)/13
    return suit, rank




class PokerWorldEnv(gym.Env):
    def __init__(self):
        # We have 2 actions, corresponding to "Raise", "Fold"
        self.action_space = spaces.Discrete(2)

        # any of the following are okay for the observation space (1,2), "2 of hearts", "2H"
        self.observation_space = spaces.Dict(
            {
                "agent": spaces.Tuple(spaces.Discrete(52), spaces.Discrete(52)),
                "agent's best hand": int,
                "agent's highest card": int,
                "villain": spaces.Tuple(spaces.Discrete(52), spaces.Discrete(52)), #unknown to agent
                "villain's best hand": int, #unknown to agent
                "villain's highest card": int, #unknown to agent
                "table": spaces.Tuple(spaces.Discrete(52),
                                      spaces.Discrete(52),
                                      spaces.Discrete(52),
                                      spaces.Discrete(52), 
                                      spaces.Discrete(52)),
                "pot": spaces.Discrete(200),
                "agent_stack": spaces.Discrete(100),
                "villain_stack": spaces.Discrete(100),
            }
        )
        
        self._actions = {
            1: 100, # Raise
            2: 0 # Fold
        }

        # pls change
# # %% Following won't work well bc we would need to call the deck three separate times
# # Dealing the cards
# # Parameters:
# #   num_of_cards : The number of cards dealt
# # Returns:
# #   A tuple of number representing the cards
# # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# # Author: Jennifer Chun
#
#     def _deal(self, num_of_cards):
#         """
#         Deals specified number of cards to the player
#         """
#
#         #pass

# %%
#<<<<<<< HEAD
# Dealing a specified number of cards from the deck with their corresponding
# suit and rank
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Author: Jennifer Chun

    def _deal_all(self):
        """Shuffles the deck then deals all cards to the agent, the villain, and the table

        Returns the cards of the agent, villain, and table respectively

        Deck of cards is class Deck

        Hand (applying to agent, villain, and table) are of class Hand

        Cards are in the form of class Card
        :returns agent's hand, villain's hand, and table's hand(cards)
        """
        # creates then shuffles the deck
        deck = poker.Deck()
        deck.shuffle()

        # gives corresponding cards to the players and the table
        agent = poker.Hand('Agent')
        villain = poker.Hand('Villain')
        table = poker.Hand('Table')

        deck.move_cards(agent, 2)
        deck.move_cards(villain, 2)
        deck.move_cards(table, 5)

        # 12-8-23 10:15 AM
        # How to access the observations spaces from this method???
        #self.observation_space. ???
        return agent, villain, table

        #pass



# %%
# Getting the kind of hands that either play has given their hole cards and 
# what's on the board
#=======
# Getting the kind of hands (ranking) that either play has given their hole cards
# and what's on the board.
#>>>>>>> b6f2d1bb4638cc2d2d06b14ba061ddb163b245d4
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Author: Jennifer Chun

    #def _hands(self, hole_cards):
    def _hands(self, player, table):
        """
        Returns the details of the best hand that the player has (hand value, name of hand, and highest card)
        :param player: the player's cards (class Card)
        :param table: the table's cards (class Card)
        :returns hand value, name of hand (string), and highest card value
        """
        hand_value, hand_name, cards = player.best_hand(table)
        highest_card = cards[0]
        #return hand_value, hand_name, highest_card # if we want all details
        #return hand_value, highest_card  # if we want only the hand value and the highest card
        return hand_value # if we want only the hand value
        #pass
    
# %%
# If the villain "has something" (in our case, means the villain has 
# something greater than just "high card") 
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Author: Jennifer Chun

    #def _has_something(self, hole_cards):
     #  pass

    def _has_something(self, villain, table):
       """
       Returns a boolean based on whether villain has a hand that's not a "high card"
       :param villain: villain's cards
       :param table: table's cards
       :return: boolean whether villain has a hand that's not a "high card"
       """
       if self._hands(villain, table)[0] != 0:
           return True
       return False

       #pass
        
# %%
# Constructing Observations From Environment States
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# Since we will need to compute observations both in ``reset`` and
# ``step``, it is often convenient to have a (private) method ``_get_obs``
# that translates the environment’s state into an observation. However,
# this is not mandatory and you may as well compute observations in
# ``reset`` and ``step`` separately:

    def _get_obs(self):
        return {"agent": self._agent_cards, "villain": self._villain_cards,
                "table": self._table, "pot": self._pot, "agent_stack": self._agent_stack,
                "villain_stack": self._villain_stack}

# %%
# We can also implement a similar method for the auxiliary information
# that is returned by ``step`` and ``reset``. In our case, we would like
# to provide what kind of hand the hero has:

    def _get_info(self):
        return {
            "hands": self._hands(self._agent_cards)
        }
        
# %%
# Oftentimes, info will also contain some data that is only available
# inside the ``step`` method (e.g. individual reward terms). In that case,
# we would have to update the dictionary that is returned by ``_get_info``
# in ``step``.

# %%
# Reset
# ~~~~~
#
# The ``reset`` method will be called to initiate a new episode. You may
# assume that the ``step`` method will not be called before ``reset`` has
# been called. Moreover, ``reset`` should be called whenever a done signal
# has been issued. Users may pass the ``seed`` keyword to ``reset`` to
# initialize any random number generator that is used by the environment
# to a deterministic state. It is recommended to use the random number
# generator ``self.np_random`` that is provided by the environment’s base
# class, ``gymnasium.Env``. If you only use this RNG, you do not need to
# worry much about seeding, *but you need to remember to call
# ``super().reset(seed=seed)``* to make sure that ``gymnasium.Env``
# correctly seeds the RNG. Once this is done, we can randomly set the
# state of our environment. In our case, we randomly choose the agent’s
# location and the random sample target positions, until it does not
# coincide with the agent’s position.
#
# The ``reset`` method should return a tuple of the initial observation
# and some auxiliary information. We can use the methods ``_get_obs`` and
# ``_get_info`` that we implemented earlier for that:

    def reset(self, seed=None, options=None):

        # if trying to deal cards separately (may run into issues if using classes)
        # self._villain_cards = self._deal(2)
        # self._agent_cards = self._deal(2)
        # self._cards = self._deal(5)

        # if dealing cards altogether, output the respective classes of Hand
        agent, villain, table = self._deal_all()

        # only needed if we need to access the Hand classes outside this function
        # global agent = agent
        # global villain = villain
        # global table = table

        # if okay with cards in being a list of tuples
        # self._agent_cards = agent.print_list_tuple()
        # self._villain_cards = agent.print_list_tuple()
        # self._cards = agent.print_list_tuple()

        # if want cards for each to be a tuple of tuples
        self._agent_cards = agent.print_tuple_tuple()
        self._villain_cards = agent.print_tuple_tuple()
        self._cards = agent.print_tuple_tuple()

        # if want to get the best hand details for both the agent and villain in one quick part
        # so we don't need to access things later
        # only if we just want the hand value
        agent_hand_value = self._hands(agent, table)
        villain_hand_value = self._hands(villain, table)

        # if we want to get the hand value AND the highest card (need to modify _hands() based on what we want)
        # agent_hand_value, agent_highest_card = self._hands(agent, table)
        # villain_hand_value, villain_highest_card = self._hands(villain, table)

        self._villain_stack = 100
        self._hero_stack = 100

        observation = self._get_obs()
        info = self._get_info()


        return observation, info

# %%
# Step
# ~~~~
# In our simplified game version, the agent will always go first postflop.
# This does not occur in a real game, where players will alternate going first
# postflop. 
#
# The ``step`` method usually contains most of the logic of your
# environment. It accepts an ``action``, computes the state of the
# environment after applying that action and returns the 5-tuple
# ``(observation, reward, terminated, truncated, info)``. See
# :meth:`gymnasium.Env.step`. Once the new state of the environment has
# been computed, we can check whether it is a terminal state and we set
# ``done`` accordingly. Since we are using sparse binary rewards in
# ``GridWorldEnv``, computing ``reward`` is trivial once we know
# ``done``.To gather ``observation`` and ``info``, we can again make
# use of ``_get_obs`` and ``_get_info``:

    def step(self, action):
        tied = False # If the hero and villain has the same hand. 
        villain_folded = False # If the villain decides to fold
        villain_raised = False # If the villain decides to raise.
        
        if action == 1: # If the agent decides to Raise
            if (self._has_something(self._villain_cards)):
                if random.random() <= 0.75: 
                    villain_raised = True
                    if self._hands(self._villain_cards) > self._hands(self._hero_cards):
                        self._villain_stack = 200
                        self._hero_stack = 0
                    elif self._hands(self._hero_cards) > self._hands(self._villain_cards):
                        self._villain_stack = 0
                        self._hero_stack = 200
                    else:
                        self._villain_stack = 100
                        self._hero_stack = 100
                else:
                    villain_folded = True
            else:
                if random.random() <= 0.10: 
                    villain_raised = True 
                    if self._hands(self._villain_cards) > self._hands(self._hero_cards):
                        self._villain_stack = 200
                        self._hero_stack = 0
                    elif self._hands(self._hero_cards) > self._hands(self._villain_cards):
                        self._villain_stack = 0
                        self._hero_stack = 200
                    else:
                        self._villain_stack = 100
                        self._hero_stack = 100
                else:
                    villain_folded = True
        elif action == 2: # Agent decides to fold
            self._villain_stack = 100
            self._hero_stack = 100
        
        
        # An episode is done iff the agent has reached the target
        terminated = self._villain_stack == 200 or self._hero_stack == 200 or action == 2 or tied or villain_folded
        if (terminated and self._hero_stack == 200 and self._villain_stack == 0) or (terminated and villain_folded):
            reward = 1
        elif terminated and action == 2:
            reward = 0
        elif terminated and tied:
            reward = 0
        elif terminated and self._villain_stack == 200 and self._hero_stack == 0:
            reward = -1
        
        observation = self._get_obs()
        info = self._get_info()


        return observation, reward, terminated, False, info        
    
# %%
# Close
# ~~~~~
#
# The ``close`` method should close any open resources that were used by
# the environment. In many cases, you don’t actually have to bother to
# implement this method. However, in our example ``render_mode`` may be
# ``"human"`` and we might need to close the window that has been opened:

    def close(self):
        pass