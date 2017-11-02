import gym
from gym_raiden.envs import alpha
import pygame
from gym import spaces
import numpy as np

NUM_GAME_STATUS_STATES = 3
IN_GAME, WIN, DEAD = list(range(NUM_GAME_STATUS_STATES))
STATUS_STRINGS = {IN_GAME: "InGame",
                  WIN: "Win",
                  DEAD: "Dead"}

class Raiden_ENV(gym.Env):

    metadata = {'render.modes': ['human']}

    def __init__(self):
        alpha.render_init(alpha.screen)
        self.status = IN_GAME
        self.action_space = spaces.Discrete(8)
        (screen_width, screen_height) = alpha.size
        self.observation_space = spaces.Box(low=0, high=255, shape=(screen_width, screen_height, 3))
        self.num_step = 0

    def _step(self, action):
        self._take_action(action)
        alpha.step()
        self.status = self.status_update()
        reward = self._get_reward()
        img_data = np.array(pygame.surfarray.pixels3d(alpha.screen))

        # test if we capture the screen
        # if self.num_step % 100 == 0:
        #     size = (700, 900)
        #     screen = pygame.display.set_mode(size)
        #     pygame.surfarray.blit_array(screen, img_data)
        #     pygame.image.save(screen, str(self.num_step / 100) + '.jpg')

        episode_over = self.status != IN_GAME
        self.num_step += 1

        return img_data, reward, episode_over, 'action info: ' + ACTION_LOOKUP[action]

    def status_update(self):
        if alpha.player.live <= 0:
            return DEAD
        elif alpha.game_end:
            return WIN
        else:
            return IN_GAME

    def _take_action(self, action):
        """ Converts the action space into an action. """
        action_type = ACTION_LOOKUP[action]
        if action_type == 'up':
            alpha.player.moveY(-5)
        elif action_type == 'down':
            alpha.player.moveY(5)
        elif action_type == 'left':
            alpha.player.moveX(-5)
        elif action_type == 'right':
            alpha.player.moveX(5)
        elif action_type == 'up_left':
            alpha.player.moveY(-5)
            alpha.player.moveX(-5)
        elif action_type == 'up_right':
            alpha.player.moveY(-5)
            alpha.player.moveX(5)
        elif action_type == 'down_left':
            alpha.player.moveY(5)
            alpha.player.moveX(-5)
        elif action_type == 'down_right':
            alpha.player.moveY(5)
            alpha.player.moveX(5)
        elif action_type == 'noop':
            pass
        else:
            print('Unrecognized action %s' % action_type)
        alpha.player.playershoot = True

    def _get_reward(self):
        """ Reward is achieving score minus the score got in previous step. """
        return alpha.reward

    def _reset(self):
        alpha.game_end = False
        alpha.reset()
        return alpha.render_init(alpha.screen)

    def _render(self, mode='human', close=False):
        alpha.render(alpha.instrucfont, alpha.screen)



ACTION_LOOKUP = {
    0 : 'up',
    1 : 'down',
    2 : 'left',
    3 : 'right',
    4 : 'up_left',
    5 : 'up_right',
    6 : 'down_left',
    7 : 'down_right',
    8 : 'noop'
}

