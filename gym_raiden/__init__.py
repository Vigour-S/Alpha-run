from gym.envs.registration import register

register(
    id='raiden-v0',
    entry_point='gym_raiden.envs:Raiden_ENV',
)
