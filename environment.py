"""
The following code is a modification of the following template
https://github.com/sjsu-interconnect/cs272-custom-env/blob/main/intro-custom-env-and-ray/environment_creation.py

"""
import gymnasium as gym
import random
import poker  # modified version of https://github.com/Sondar4/poker-sim/blob/master/poker.py
from gymnasium import spaces
import numpy as np



class PokerWorldEnv(gym.Env):
    def __init__(self):
        # We have 2 actions, corresponding to "Raise", "Fold"
        self.action_space = spaces.Discrete(2)

        # any of the following are okay for the observation space (1,2), "2 of hearts", "2H"
        self.observation_space = spaces.Dict(
            {
               "agent": spaces.Tuple((spaces.Discrete(52), spaces.Discrete(52))),
                "villain": spaces.Tuple((spaces.Discrete(52), spaces.Discrete(52))), #unknown to agent
                "table": spaces.Tuple((spaces.Discrete(52),
                                      spaces.Discrete(52),
                                      spaces.Discrete(52),
                                      spaces.Discrete(52), 
                                      spaces.Discrete(52))),
                "agent_stack": spaces.Discrete(201),
                "villain_stack": spaces.Discrete(201),
            }
        )


# %%
# Dealing all the cards to the agent, the villain, and the table
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Author: Jennifer Chun

    def _deal_all(self):
        """Shuffles the deck then deals all cards to the agent, the villain, and the table

        Returns the cards of the agent, villain, and table respectively

        Deck of cards is class Deck

        Hand (applying to agent, villain, and table) are of class Hand

        Cards are in the form of class Card
        :returns agent's hand, villain's hand, and table's hand(cards) of class Hand
        """
        # creates then shuffles the deck
        deck = poker.Deck()
        deck.shuffle()

        # creates Hand classes for the players and the table
        agent = poker.Hand('Agent')
        villain = poker.Hand('Villain')
        table = poker.Hand('Table')

        # gives corresponding cards to the players and the table
        deck.move_cards(agent, 2)
        deck.move_cards(villain, 2)
        deck.move_cards(table, 5)

        return agent, villain, table

        #pass



# %%
# Getting the kind of hands that a player has in their hands and the table
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Author: Jennifer Chun

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
# something greater than just a "high card")
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Author: Jennifer Chun

    def _has_something(self, villain, table):
       """
       Returns a boolean based on whether villain has a hand that's not a "high card"
       :param villain: villain's cards
       :param table: table's cards
       :return: boolean whether villain has a hand that's not a "high card"
       """
       if self._hands(villain, table) != 0:
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
                "table": self._table, "agent_stack": self._agent_stack,
                "villain_stack": self._villain_stack}

# %%
# We can also implement a similar method for the auxiliary information
# that is returned by ``step`` and ``reset``. In our case, we would like
# to provide what kind of hand the hero has:

    def _get_info(self):
        return {
            "hands": self._hands(self._agent, self._table_cards)
          # "hands" : 0
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

        # deals all cards to the player and table in the form of Hand classes
        agent, villain, table = self._deal_all()
        
    #  agent_card_1 , agent_card_2 = agent.print_tuple_tuple()
    #  villain_cards_1 , villain_cards_2 = villain.print_tuple_tuple()
    #  table_cards_1 , tuple_cards_2 , tuple_cards_3 , tuple_cards_4 , tuple_cards_5 = table.print_tuple_tuple()

        # saving the cards as a tuple of tuples for each hand
        self._agent_cards = agent.print_tuple_tuple_tuple()
        self._villain_cards = villain.print_tuple_tuple_tuple()
        self._table = table.print_tuple_tuple_tuple()

        # saving the corresponding Hand classes for future reference
        self._agent = agent
        self._villain = villain
        self._table_cards = table
       
       # self._agent_cards = (1, 2)
       # self._villain_cards = (3, 4)
       # self._table = (5, 6, 7, 8, 9)
        

        # if want to get the best hand details for both the agent and villain in one quick part
        # so we don't need to access things later
        # only if we just want the hand value
        # agent_hand_value = self._hands(agent, table)
        # villain_hand_value = self._hands(villain, table)

        # if we want to get the hand value AND the highest card (need to modify _hands() based on what we want)
        # agent_hand_value, agent_highest_card = self._hands(agent, table)
        # villain_hand_value, villain_highest_card = self._hands(villain, table)

        self._villain_stack = 100
        self._agent_stack = 100

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
        assert self.action_space.contains(action)
        reward = 0 # The reward
        tied = False # If the hero and villain has the same hand. 
        villain_folded = False # If the villain decides to fold
        villain_raised = False # If the villain decides to raise.
        
        if action == 0: # If the agent decides to Raise
            if (self._has_something(self._villain, self._table_cards)): # If the villain has a card better than a "high card"
                """
                villain_raised = True
                if self._hands(self._villain, self._table_cards) > self._hands(self._agent, self._table_cards):
                    self._villain_stack = 200
                    self._agent_stack = 0
                elif self._hands(self._agent, self._table_cards) > self._hands(self._villain, self._table_cards):
                    self._villain_stack = 0
                    self._agent_stack = 200
                else:
                    self._villain_stack = 100
                    self._agent_stack = 100
                """
                if random.random() < 0.90: # 90% of the time, villain will bet
                    villain_raised = True
                    # if agent has the better hand, it wins the stack
                    if self._hands(self._villain, self._table_cards) > self._hands(self._agent, self._table_cards):
                        self._villain_stack = 200
                        self._agent_stack = 0
                    # if villain has the better hand, it wins the stack
                    elif self._hands(self._agent, self._table_cards) > self._hands(self._villain, self._table_cards):
                        self._villain_stack = 0
                        self._agent_stack = 200
                    # if both agent and villain have the same hand, both tie and get their corresponding stack back
                    else:
                        tied = True
                        self._villain_stack = 100
                        self._agent_stack = 100
                else: # 10% of the time, villain will fold
                    villain_folded = True
                
            else: # Otherwise, if villain's best hand is a "high card"
                #villain_folded = True
                if random.random() < 0.10: # 10% of the time, villain will bet
                    villain_raised = True 
                    # if agent has the better hand, it wins the stack
                    if self._hands(self._villain, self._table_cards) > self._hands(self._agent, self._table_cards):
                        self._villain_stack = 200
                        self._agent_stack = 0
                    # if villain has the better hand, it wins the stack
                    elif self._hands(self._agent, self._table_cards) > self._hands(self._villain, self._table_cards):
                        self._villain_stack = 0
                        self._agent_stack = 200
                    # if both agent and villain have the same hand, both tie and get their corresponding stack back
                    else:
                        tied = True
                        self._villain_stack = 100
                        self._agent_stack = 100
                else: # 90% of the time, villain will fold
                    villain_folded = True

        elif action == 1: # Agent decides to fold
            self._villain_stack = 100
            self._agent_stack = 100
        
        
        # An episode is done iff the agent has reached the target
        terminated = self._villain_stack == 200 or self._agent_stack == 200 or action == 1 or tied or villain_folded
        if (terminated and self._agent_stack == 200 and self._villain_stack == 0) or (terminated and villain_folded):
            reward = 1
        elif terminated and action == 1:
            reward = 0
        elif terminated and tied:
            reward = 0
        elif terminated and self._villain_stack == 200 and self._agent_stack == 0:
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