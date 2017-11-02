import gym_raiden.envs.raiden_env as raiden_env

def main():
    env = raiden_env.Raiden_ENV()
    while True:
        action = env.action_space.sample()
        _, _, over, _ = env.step(action)
        env.render()
        if over:
            env.reset()

if __name__ == '__main__':
    main()
