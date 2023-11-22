from environment_creation import GridWorldEnv

from ray.tune.registry import register_env 

from ray.rllib.algorithms.dqn.dqn import DQNConfig, DQN 

"""

def env_creator(env_config):
    return GridWorldEnv() # custom env 

register_env("MyGrid", env_creator)

# getting the config dict
# set the environment
config = DQNConfig()
config = config.environment(env="MyGrid")

print('----------------')
print(config.env_config) # Initially 0 {} when professor ran
print(config.exploration_config) # 
print(config.num_rollout_workers) # Iniially 0 when professor ran
print('----------------')

algo = DQN(config=config)

for _ in range(10):
    algo.train()

"""

env = GridWorldEnv(render_mode="human")

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
