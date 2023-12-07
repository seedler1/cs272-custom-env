import gymnasium as gym
import random
from gymnasium import spaces

class PokerWorldEnv(gym.Env):
    def __init__(self):
        # We have 3 actions, corresponding to "Check", "Raise", "Fold"
        self.action_space = spaces.Discrete(3)
        
       
        self.observation_space = spaces.Dict(
            {
                "agent": spaces.Tuple(spaces.Discrete(52), spaces.Discrete(52)),
                "villain": spaces.Tuple(spaces.Discrete(52), spaces.Discrete(52)),
                "cards": spaces.Tuple(spaces.Discrete(52), 
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
            1: 0, # Check
            2: 100, # Raise
            3: 0 # Fold
        }

# %%
# Dealing a specified number of cards from the deck with their corresponding
# suit and rank
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Author: Jennifer Chun

    def _deal(self, num_cards):
        pass

# %%
# Getting the kind of hands that either play has given their hole cards and 
# what's on the board
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Author: Jennifer Chun
        
    def _hands(self, hole_cards):
        pass
    
# %%
# If the villain "has something" (in our case, means the villain has 
# something greater than just "high card") 
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Author: Jennifer Chun

    def _has_something(self, hole_cards):
       pass 
        
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
                "cards": self._cards, "pot": self._pot, "agent_stack": self._agent_stack, 
                "vilain_stack": self._villain_stack}

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
        
        if action == 1: # If the agent decides to check
            if (self._has_something(self._villain_cards)):
                if random.random() <= 0.75: 
                    pass
                else:
                    pass
            else:
                if random.random() <= 0.45: 
                    pass 
                else:
                    pass
        elif action == 2: # If the agent decides to raise
            if (self._has_something(self._villain_cards)):
                if random.random() <= 0.80: 
                    pass
                else:
                    pass
            else:
                if random.random() <= 0.20: 
                    pass 
                else:
                    pass

        
        # An episode is done iff the agent has reached the target
        terminated = self._villain_stack == 200 or self._hero_stack == 200
        reward = 1 if terminated else -1  # Binary sparse rewards
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