import gym
import gym_raiden.envs.alpha as alpha
import pygame

NUM_GAME_STATUS_STATES = 3
IN_GAME, WIN, DEAD = list(range(NUM_GAME_STATUS_STATES))
STATUS_STRINGS = {IN_GAME: "InGame",
                  WIN: "Win",
                  DEAD: "Dead"}


class Raiden_ENV(gym.Env):

    metadata = {'render.modes': ['human']}

    def __init__(self):
        self.status = IN_GAME

    def _step(self, action):
        self._take_action(action)
        self.status = self.status_update()
        reward = self._get_reward()
        img_data = pygame.image.tostring(alpha.screen, "RGB")
        episode_over = self.status != IN_GAME

        return img_data, reward, episode_over

    def status_update(self):
        if alpha.player.live <= 0:
            return DEAD
        elif alpha.game_end:
            return WIN
        else:
            return IN_GAME

    def _take_action(self, action):
        """ Converts the action space into an action. """
        action_type = ACTION_LOOKUP[action[0]]
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
        elif action_type == 'still':
            pass
        else:
            print('Unrecognized action %s' % action_type)
        alpha.player.playershoot = True
        alpha.render()

    def _get_reward(self):
        """ Reward is given for scoring a goal. """
        return alpha.player.score

    def _reset(self):
        alpha.game_start = False


ACTION_LOOKUP = {
    0 : 'up',
    1 : 'down',
    2 : 'left',
    3 : 'right',
    4 : 'up_left',
    5 : 'up_right',
    6 : 'down_left',
    7 : 'down_right',
    8 : 'still'
}

