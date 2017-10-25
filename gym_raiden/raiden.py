import gym_raiden.envs.alpha as alpha

class RaidenEnvironment(object):
    def __init__(self):
        self.obj = hfo_lib.HFO_new()

    def __del__(self):
        hfo_lib.HFO_del(self.obj)

    def connectToServer(self,
                        feature_set=LOW_LEVEL_FEATURE_SET,
                        config_dir='bin/teams/base/config/formations-dt',
                        server_port=6000,
                        server_addr='localhost',
                        team_name='base_left',
                        play_goalie=False,
                        record_dir=''):
        """
          Connects to the server on the specified port. The
          following information is provided by the ./bin/HFO
          feature_set: High or low level state features
          config_dir: Config directory. Typically HFO/bin/teams/base/config/
          server_port: port to connect to server on
          server_addr: address of server
          team_name: Name of team to join.
          play_goalie: is this player the goalie
          record_dir: record agent's states/actions/rewards to this directory
        """
        hfo_lib.connectToServer(self.obj,
                                feature_set,
                                config_dir.encode('utf-8'),
                                server_port, server_addr.encode('utf-8'),
                                team_name.encode('utf-8'),
                                play_goalie,
                                record_dir.encode('utf-8'))

    def getStateSize(self):
        """ Returns the number of state features """
        return hfo_lib.getStateSize(self.obj)

    def getState(self, state_data=None):
        """ Returns the current state features """
        if state_data is None:
            state_data = np.zeros(self.getStateSize(), dtype=np.float32)
        hfo_lib.getState(self.obj, as_ctypes(state_data))
        return state_data

    def act(self, action_type, *args):
        """ Performs an action in the environment """
        n_params = hfo_lib.numParams(action_type)
        assert n_params == len(args), 'Incorrect number of params to act: ' \
                                      'Required %d, provided %d' % (n_params, len(args))
        params = np.asarray(args, dtype=np.float32)
        hfo_lib.act(self.obj, action_type, params.ctypes.data_as(POINTER(c_float)))

    def say(self, message):
        """ Transmits a message """
        hfo_lib.say(self.obj, message.encode('utf-8'))

    def hear(self):
        """ Returns the message heard from another player """
        return hfo_lib.hear(self.obj).decode('utf-8')

    def playerOnBall(self):
        """ Returns a player object who last touched the ball """
        return hfo_lib.playerOnBall(self.obj)

    def step(self):
        """ Advances the state of the environment """
        return hfo_lib.step(self.obj)

    def actionToString(self, action):
        """ Returns a string representation of an action """
        return ACTION_STRINGS[action]

    def statusToString(self, status):
        """ Returns a string representation of a game status """
        return STATUS_STRINGS[status]

    def getUnum(self):
        """ Returns the uniform number of the agent """
        return hfo_lib.getUnum(self.obj)

    def getNumTeammates(self):
        """ Returns the number of teammates of the agent """
        return hfo_lib.getNumTeammates(self.obj)

    def getNumOpponents(self):
        """ Returns the number of opponents of the agent """
        return hfo_lib.getNumOpponents(self.obj)