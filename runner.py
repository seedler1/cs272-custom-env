from environment import PokerWorldEnv

from ray.tune.registry import register_env 

from ray.rllib.algorithms.dqn.dqn import DQNConfig, DQN 
from ray.rllib.algorithms.ppo import PPOConfig



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

for _ in range(50):
    algo.train()


"""
env1 = PokerWorldEnv()

config = PPOConfig()  
config = config.training(gamma=0.9, lr=0.01, kl_coeff=0.3)
config = config.resources(num_gpus=0)
config = config.rollouts(num_rollout_workers=4)
print(config.to_dict())
algo = config.build(env=env1)
algo.train() 
"""

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