from environment import PokerWorldEnv

from ray.tune.registry import register_env 

from ray.rllib.algorithms.dqn.dqn import DQNConfig, DQN 
from ray.rllib.algorithms.sac.sac import SACConfig, SAC
from ray.rllib.algorithms.ppo import PPOConfig, PPO


"""
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

for _ in range(50): # 50 means 50000 episodes
    algo.train()
"""


# SAC does not work with our environment unfortunately. 
"""
def env_creator(env_config):
    return PokerWorldEnv() # custom env 

register_env("Poker", env_creator)

# getting the config dict
# set the environment
config = SACConfig().training(gamma=0.9, lr=0.01)
config = config.environment(env="Poker")
config = config.resources(num_gpus=0) 
config = config.rollouts(num_rollout_workers=4) 

algo = SAC(config=config)

for _ in range(20):
    algo.train()

"""

# The follow 
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

for _ in range(25):
    algo.train()


"""

obs, _ = env.reset()

num_steps = 100
for _ in range(num_steps):
    # taking a random action
    a = env.action_space.sample()
    
    obs, r, terminated, truncaed, _ = env.step(a)
    env.step(a)
    
    if terminated or truncaed:
        obs, _ = env.reset() 
        
env.close()
"""