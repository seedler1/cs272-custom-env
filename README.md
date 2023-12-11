# Texas Hold'em
## Project Summary
<!-- Around 200 Words -->
<!-- Cover (1) What problem you are solving, (2) Who will use this RL module and be happy with the learning, and (3) a brief description of the results -->
(1) What problem you are solving?

No-Limit Texas Hold’em (NLHE) is a variant of poker where each player in the game is dealt two cards that only they can see and they use the cards dealt on the table with their two cards to try to win the money on the table. It involves multiple betting rounds and each player is allowed to bet various amounts of money with the limit being how much money they have.

Since NLHE is a very complex game, we are going to solve a simplified version of No-Limit Texas Hold’em. In our simplified version, there will only be two players. Each player will be dealt two cards and there will be five cards dealt on the table. The agent will always go first, and there are no blinds (money that must be put onto the table). Upon seeing his cards, the agent can decide to raise or fold. If the agent decides to raise, then the villain (the other player) will play the following strategy: if the villain has a hand that is a pair or higher in ranking (two-pairs, three of a kind, straight, etc…), then 90% of the time it will call and 10% of the time it will fold. If the villain doesn’t, then the villain will call 10% of the time and fold 90% of the time. If the villain does call, then the villain and hero will show their card and whoever has the better hand will win the money on the table. However, if they have the same hand, then the money will be returned to them. If the hero folds, then a new round will begin. The goal of the agent is to find the optimal strategy against the strategy of the villain. 


(2) Who will use this RL module and be happy with the learning?

The people who will use this RL module are people who are interested in NLHE and want to use RL to find the optimal strategy in a specific situation. 

(3) a brief description of the results

The cards played and whether the decisions made were winning decisions.


## State Space
<!-- See the Cart Pole Env example https://gymnasium.farama.org/environments/classic_control/cart_pole/ -->
The state space is a dictionary containing 
- Agent's card (2-tuple representing the cards on the table)
- Villain's card (2-tuple representing the cards on the table)
- Cards on the table (5-tuple representing the cards on the table)
- Agent's Stack Size (An integer in the range {0, 200}) 
- Villain's Stack Size (An integer in the range {0, 200})

Each card was saved as an integer mapped to a card dictionary (suit,rank).  This mapping can be found in our poker.py file.

## Action Space
<!-- See the Cart Pole Env example https://gymnasium.farama.org/environments/classic_control/cart_pole/ -->
The action shape is (1,) in the range {0, 1} indicating whether to raise or fold. Note that the action raises the entire stack (in poker terms, "raise all-in"). 
- 0 : Raise.
- 1 : Fold.
## Rewards
<!-- See the Cart Pole Env example https://gymnasium.farama.org/environments/classic_control/cart_pole/ -->
- A reward of 1 is given if the agent wins the hand.
- A reward of 0 if the agent ties with the villain in the hand type, if the agent folds, or if the villain folds.
- A reward of -1 is given if the agent loses the hand.

## RL Algorithm 
We used the reinforcement learning algorithm DQN. DQN is a model-free, off-policy reinforcement learning algorithm. We chose this deep RL algorithm specifically because the poker environment per episode requires a lot of states (since there are 9 cards randomly selected from the 52 cards in the deck per round/episode, or 52!/43! possibilities to consider) and the solving the problem of the environment would be greatly benefitted from the experience replay buffer utilized in DQN.  Additionally, the ray rllib implementation of DQN was intuitive.   The original paper for DQN can be found [here](https://arxiv.org/pdf/1312.5602.pdf). 

For the ray rllib implementation of DQN, we initially used its default setting. The action policy is epsilon greedy with an initial epsilon of 1.0 and a final epsilon of 0.02. The epsilon timestep was 10000. The number of rollout workers is 0. 

## Starting State [if applicable]
<!-- See the Cart Pole Env example https://gymnasium.farama.org/environments/classic_control/cart_pole/ -->
At the start, each player will be dealt two cards and five cards will be dealt on the table. Also, each player will start with a stack of 100. 

## Episode End [if applicable]
<!-- See the Cart Pole Env example https://gymnasium.farama.org/environments/classic_control/cart_pole/ -->
The episode will terminate in one of several scenarios: 
- The agent folds
- The agent raises and the villain folds
- The agent raises, the villain raises, and they go to showdown to see who wins the hand or if they draw.  

## Results
Using TensorBoard, we have plotted the episode reward mean of the DQN algorithm on two separate occasions.  One of the DQN outputs ran for fewer episodes than the other because we did not anticipate how long the DQN training process would take.  But, as it is clearly shown in the graph below, the DQN episode reward mean stayed consistently around the 0.3 value around the 60k episode mark for both runs. The longer DQN run that continued up to 160,000 episodes was able to reach a maximum episode reward mean of approximately 0.4.

!(/assets/images/Two_runs_of_DQN.png)
