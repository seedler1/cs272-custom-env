# Texas Hold'em
## Project Summary
<!-- Around 200 Words -->
<!-- Cover (1) What problem you are solving, (2) Who will use this RL module and be happy with the learning, and (3) a brief description of the results -->
(1) What problem you are solving?

Simplified Texas Hold'em (Poker variation) with two players, and only one of the players is the agent

(2) Who will use this RL module and be happy with the learning?

People who are interested in Poker and want to explore simulated Poker strategies

(3) a brief description of the results

The cards played and whether the decisions made were winning decisions

## State Space
<!-- See the Cart Pole Env example https://gymnasium.farama.org/environments/classic_control/cart_pole/ -->
Cards on the board (5 cards) 
Agent's card (2 cards)
Villain's card (2 cards)
Agent's Stack Size ($100) 
Villain's Stack Size ($100) 

## Action Space
<!-- See the Cart Pole Env example https://gymnasium.farama.org/environments/classic_control/cart_pole/ -->
The action is a dictionary mapping with the following mapping
1 : Raise $100 ,
2 : Fold
## Rewards
<!-- See the Cart Pole Env example https://gymnasium.farama.org/environments/classic_control/cart_pole/ -->
A reward of 1 is given if the agent wins the hand.
A reward of 0 if the agent ties with the villain or folds.
A reward of -1 is given if the agent loses the hand.

## RL Algorithm 

## Starting State [if applicable]
<!-- See the Cart Pole Env example https://gymnasium.farama.org/environments/classic_control/cart_pole/ -->
At the start, each player will be dealt two cards and five cards will be dealt on the table. Also, each player will start with a stack of $100. 

## Episode End [if applicable]
<!-- See the Cart Pole Env example https://gymnasium.farama.org/environments/classic_control/cart_pole/ -->
The episode will end in one of several scenarios: the agent folds, if the agent raises and the villain folds, and if the agent raises, the villain raises, and they go to showdown.  

## Results

