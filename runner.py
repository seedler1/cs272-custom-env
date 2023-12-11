from environment import PokerWorldEnv

from ray.tune.registry import register_env 

from ray.rllib.algorithms.dqn.dqn import DQNConfig, DQN 
from ray.rllib.algorithms.ppo import PPOConfig, PPO



import matplotlib.pyplot as plt
import torch
import matplotlib

is_ipython = 'inline' in matplotlib.get_backend()
if is_ipython:
    from IPython import display

plt.ion()


env = PokerWorldEnv()

# Get number of actions from gym action space
n_actions = env.action_space.n
# Get the number of state observations
state, info = env.reset()
n_observations = len(state)

rewards = []
mean_rewards = []

def plot_durations(show_result=False):
    plt.figure(1)
    durations_t = torch.tensor(rewards, dtype=torch.float)
    if show_result:
        plt.title('Result')
    else:
        plt.clf()
        plt.title('Training...')
    plt.xlabel('Episode')
    plt.ylabel('Episode reward mean')
    # Take 100 episode averages and plot them too
    mean_rewards.append(durations_t.unfold(0, 1, 1).mean().view(-1).numpy()[0])
    episode_r = torch.tensor(mean_rewards, dtype=torch.float)
   
    plt.plot(episode_r.numpy())

    
    plt.pause(0.001)  # pause a bit so that plots are updated
    if is_ipython:
        if not show_result:
            display.display(plt.gcf())
            display.clear_output(wait=True)
        else:
            display.display(plt.gcf())

    plt.savefig('Poker_episode_reward_mean_vs_episode.png')




# The following is DQN. Out of all the other algorithms in rayllib, it works the best with our environment

#"""
def env_creator(env_config):
    return PokerWorldEnv() # custom env

register_env("Poker", env_creator)


# getting the config dict
# set the environment
config = DQNConfig()
config = config.environment(env="Poker")

print('----------------')
print(config.env_config) # Initially 0 {} when professor ran
print(config.exploration_config) #
print(config.num_rollout_workers) # Iniially 0 when professor ran
print('----------------')

algo = DQN(config=config)

for _ in range(160): # 50 means 50000 episodes, 10 means 10000 episodes (we think)
    algo.train()
#"""


"""
# The following algorithm is PPO. Unfortunately, it does not run very well
def env_creator(env_config):
    return PokerWorldEnv() # custom env 

register_env("Poker", env_creator)

# getting the config dict
# set the environment
config = PPOConfig()
config = config.training(gamma=0.9, lr=0.01) 
config = config.environment(env="Poker")
config = config.resources(num_gpus=0) 
config = config.rollouts(num_rollout_workers=4) 

algo = PPO(config=config)

for _ in range(400):
    algo.train()

"""

"""
# The following is code for random action taken by agent

obs, _ = env.reset()

num_steps = 500000 # episode count #500
for e in range(num_steps):
    # taking a random action
    a = env.action_space.sample()
    
    obs, r, terminated, truncaed, _ = env.step(a)
    env.step(a)
    obs, _ = env.reset() 
    
    rewards.append(r)
    plot_durations()
        
        
env.close()
"""

"""
# The following is code for agent always raising

obs, _ = env.reset()

num_steps =500
for e in range(num_steps):
    # taking a random action
    a = 0
    
    obs, r, terminated, truncaed, _ = env.step(a)
    env.step(a)
    obs, _ = env.reset() 
    
    rewards.append(r)
    plot_durations()
        
env.close()

"""
