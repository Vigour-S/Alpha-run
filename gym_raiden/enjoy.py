from baselines.common import set_global_seeds
from mpi4py import MPI
from baselines import bench
import os.path as osp
import gym, logging
from baselines import logger
import tensorflow as tf
from argparse import ArgumentParser

def enjoy(env_id, num_timesteps, seed):
    from baselines.ppo1 import pposgd_simple, cnn_policy
    import baselines.common.tf_util as U
    rank = MPI.COMM_WORLD.Get_rank()
    sess = U.single_threaded_session()
    sess.__enter__()
    if rank == 0:
        logger.configure()
    else:
        logger.configure(format_strs=[])
    workerseed = seed + 10000 * MPI.COMM_WORLD.Get_rank()
    set_global_seeds(workerseed)
    env = gym.make(env_id)
    def policy_fn(name, ob_space, ac_space): #pylint: disable=W0613
        return cnn_policy.CnnPolicy(name=name, ob_space=ob_space, ac_space=ac_space)
    env = bench.Monitor(env, osp.join(logger.get_dir(), "monitor.json"))
    obs = env.reset()
    env.seed(seed)
    gym.logger.setLevel(logging.WARN)
    pi = policy_fn('pi', env.observation_space, env.action_space)
    tf.train.Saver().restore(sess, '/tmp/model')
    done = False
    while not done:
        action = pi.act(True, obs)[0]
        obs, reward, done, info = env.step(action)
        env.render()

def main():
    parser = ArgumentParser()
    parser.add_argument('--env', type=str, default='BreakoutNoFrameskip-v4')
    enjoy(parser.parse_args().env, num_timesteps=10e3, seed=0)


if __name__ == '__main__':
    main()