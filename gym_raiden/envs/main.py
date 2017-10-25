import gym_raiden.envs.raiden_env as raiden_env

def main():
    env = raiden_env.Raiden_ENV()
    while True:
        action = env.action_space.sample()
        env.step(action)
        env.render()

if __name__ == '__main__':
    main()
