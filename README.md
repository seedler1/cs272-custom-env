# Texas Hold'em
## Project Summary
<!-- Around 200 Words -->
<!-- Cover (1) What problem you are solving, (2) Who will use this RL module and be happy with the learning, and (3) a brief description of the results -->
(1) What problem you are solving?

No-Limit Texas Hold’em (NLHE) is a variant of poker where each player in the game is dealt two cards that only they can see and they use the cards dealt on the table with their two cards to try to win the money on the table. It involves multiple betting rounds and each player is allowed to bet various amounts of money with the limit being how much money they have.

Since NLHE is a very complex game, we are going to solve a simplified version of No-Limit Texas Hold’em. In our simplified version, there will only be two players, the hero (agent) and the villain (environment). Each player will be dealt two cards and there will be five cards dealt on the table. The agent will always go first, and there are no blinds (money that must be put onto the table). Upon seeing their cards, the agent can decide to raise or fold. If the agent decides to raise, then the villain will play the following strategy: if the villain has a hand that is a pair or higher in ranking (two-pairs, three of a kind, straight, etc…), then 90% of the time it will raise (note that in poker, the villain would actually be "calling") and 10% of the time it will fold. If the villain doesn’t, then the villain will raise 10% of the time and fold 90% of the time. If the villain does raise, then the villain and hero will place their money on the table and show their cards in a showdown. Whoever has the better hand will win the money on the table. However, if they have the same hand, then the money will be returned to them. A new betting round will begin after either player folds or once the showdown has been completed. The goal of the agent is to find the optimal strategy against the strategy of the villain. 


(2) Who will use this RL module and be happy with the learning?

The people who will use this RL module are people who are interested in NLHE and want to use RL to find the optimal strategy in a specific situation. 

(3) a brief description of the results

We compared the performance of DQN with PPO as well as the policy where the agent is takingrandom actions and the policy where the agent is always folding. We found that using DQN resulted in the best performance. 


## State Space
<!-- See the Cart Pole Env example https://gymnasium.farama.org/environments/classic_control/cart_pole/ -->
The state space is a dictionary containing 
- Agent's card (2-tuple representing the cards on the table)
- Villain's card (2-tuple representing the cards on the table)
- Cards on the table (5-tuple representing the cards on the table)
- Agent's Stack Size (An integer in the range {0, 200}) 
- Villain's Stack Size (An integer in the range {0, 200})

Each card was saved as an integer mapped to a card dictionary (suit, rank).  This mapping can be found in our poker.py file.

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
We used the reinforcement learning algorithm DQN. DQN is a model-free, off-policy reinforcement learning algorithm. We chose this deep RL algorithm specifically because the poker environment per episode required a lot of states (since there are 9 cards randomly selected from the 52 cards in the deck per round/episode, or 52!/43! possibilities to consider) and solving the problem of the environment would've been greatly benefitted from the experience replay buffer utilized in DQN.  Additionally, the ray rllib implementation of DQN was intuitive.   The original paper for DQN can be found [here](https://arxiv.org/pdf/1312.5602.pdf). 

For the ray rllib implementation of DQN, we used its default setting. The action policy was epsilon greedy with an initial epsilon of 1.0 and a final epsilon of 0.02. The epsilon timestep was 10000. The number of rollout workers was 0. 

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
Using TensorBoard, we plotted the episode reward mean of the DQN algorithm on two separate occasions.  One of the DQN outputs (black) ran for fewer episodes than the other because we did not originally anticipate that the DQN training process would take as long as it did.  But, as it is clearly shown in the graph below, the DQN episode reward mean stayed consistently around the 0.3 value around the 60,000 episode mark for both runs. The longer DQN run that continued up to 160,000 episodes (yellow) was able to reach a maximum episode reward mean of approximately 0.4.

![Two runs of DQN](/images/Two_runs_of_DQN.png)

We tested the results of the poker environment test against two non-reinforcement method tests.  In our first test, we had the agent take random actions.  After 1,000 episodes, its episode reward mean was consistently slightly below 0.10, approximately around 0.08. We attempted to run more than 1,000 episodes, but the program became so slow around the 1,000-episode point that we had to stop at 1,000.

![Agent taking random actions](/images/Agent_Taking_Random_Actions2.png)

In our second test, we had the agent always choose the action of raising (or, in our code, taking action 0). Initially, the episode reward mean results for always raising were better than those of the random action.  However, after 1,000 episodes, its episode reward mean was consistently slightly below 0.10, approximately around 0.08.  The ending results were very similar to those of the random action. Again, we stopped at around 1,000 episodes because the program became too slow.

![Agent always raising](/images/Agent_Always_Raising2.png)

Therefore, the DQN algorithm performed better than the tested non-reinforcement-based policies in the poker environment.  

We also compared the DQN algorithm with another reinforcement learning algorithm in the poker environment.  The RL algorithm that we used as a comparison to DQN was Proximal Policy Optimization (PPO), an on-policy, model-free policy gradient-based approach.  PPO was chosen for two reasons.  First, although both PPO and DQN are model-free RL algorithms, DQN is categorized under Q-learning whereas PPO is categorized under policy optimization.  Second, PPO is an algorithm that is easy to implement in ray rllib.  The source paper of PPO is found [here](https://arxiv.org/pdf/1707.06347.pdf).  

The ray rllib implementation we used for PPO had a gamma of 0.9 and a learning rate of 0.01.  Additionally, the number of rollouts was 4 and the number of GPUs was 0.

We first implemented two separate occasions of PPO.  Even though both PPOs ran for 160,000 episodes, the two occasions had dramatically different results in both episode reward mean and runtime.  The PPO occasion that ran for a few minutes more (magenta) consistently performed better than the PPO occasion that ran for less time (teal).  

![Two runs of PPO](/images/Two_runs_of_PPO.png)

When we compared both the runs of PPO and DQN, we found that although the longer PPO run produced overall results that were better than or equal to those of both DQN implementations starting around 60,000 episodes, the shorter PPO run always had an episode reward mean that was lower than both DQN runs.  This proved that PPO wasn’t nearly as consistent as DQN when it was used in our poker environment.  Additionally, the runtimes for PPO (18.79 and 23.11 minutes) were far faster than that of the longest DQN run (nearly 2 hours).  So although PPO was more time efficient, DQN was far more consistent in its episode reward mean values.

![Two runs of DQN vs two runs of PPO](/images/Two_runs_of_DQN_vs_two_runs_of_PPO.png)

Therefore, we concluded that DQN was the best algorithm for solving the poker environment that we tested (out of DQN, random actions, all raise, and PPO).
