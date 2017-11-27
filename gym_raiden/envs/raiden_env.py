import gym
from gym_raiden.envs import alpha
import pygame
from gym import spaces
import numpy as np
from gym.utils import seeding

NUM_GAME_STATUS_STATES = 3
IN_GAME, WIN, DEAD = list(range(NUM_GAME_STATUS_STATES))
STATUS_STRINGS = {IN_GAME: "InGame",
                  WIN: "Win",
                  DEAD: "Dead"}

class Raiden_ENV(gym.Env):

    metadata = {'render.modes': ['human', 'rgb_array']}

    def __init__(self, game='Raiden', obs_type='image', frameskip=3, repeat_action_probability=0., compressed_weight=160, compressed_height=210):
        alpha.render_init(alpha.screen)
        self.status = IN_GAME
        self.action_space = spaces.Discrete(8)
        self.observation_space = spaces.Box(low=0, high=255, shape=(compressed_weight, compressed_height, 3))
        self.num_step = 0
        self.num_game = 0
        self.frameskip = frameskip
        self.compressed_weight = compressed_weight
        self.compressed_height = compressed_height
        self._obs_type = obs_type

    def _step(self, action):
        reward = 0.0
        for _ in range(self.frameskip):
            if self.status_update() != IN_GAME:
                break
            self._take_action(action)
            alpha.step()
            reward += self._get_reward()
        reward += 0.001

        self.status = self.status_update()
        new_surface = pygame.transform.smoothscale(alpha.screen.copy(), (self.compressed_weight, self.compressed_height))
        img_data = np.array(pygame.surfarray.pixels3d(new_surface))

        # # test if we capture the screen
        # if self.num_step % 100 == 0:
        #     pygame.surfarray.blit_array(new_surface, img_data)
        #     pygame.image.save(new_surface, str(self.num_step / 100) + '.jpg')

        episode_over = self.status != IN_GAME
        self.num_step += 1
        if episode_over:
            self.num_game += 1
            print('--------')
            print('game', self.num_game)
            print('number of steps: ', self.num_step)
            print('score: ', alpha.player.score)
            print('--------')
            self.num_step = 0

        if self.num_step % 100 == 0:
            print(self.num_step)

        # return format: observation space, reward amount, episode over or not, additional info (must be a dict)
        return img_data, reward, episode_over, {"player lives": alpha.player.live}

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
        screen = alpha.render_init(alpha.screen)
        new_surface = pygame.transform.smoothscale(screen.copy(),
                                                   (self.compressed_weight, self.compressed_height))
        img_data = np.array(pygame.surfarray.pixels3d(new_surface))
        return img_data

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

