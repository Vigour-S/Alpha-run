from baselines.common import set_global_seeds, tf_util as U
from baselines import bench
import os.path as osp
import gym, logging
from baselines import logger
import sys
import tensorflow as tf
from argparse import ArgumentParser

def train(env_id, num_timesteps, seed):
    from baselines.ppo1 import pposgd_simple, cnn_policy
    sess = U.make_session(num_cpu=1)
    sess.__enter__()
    logger.configure()
    set_global_seeds(seed)
    env = gym.make(env_id)
    def policy_fn(name, ob_space, ac_space):
        return cnn_policy.CnnPolicy(name=name, ob_space=ob_space, ac_space=ac_space)
    env = bench.Monitor(env, osp.join(logger.get_dir(), "monitor.json"))
    env.seed(seed)
    gym.logger.setLevel(logging.WARN)
    pposgd_simple.learn(env, policy_fn,
                        max_timesteps=int(num_timesteps * 1.1),
                        timesteps_per_actorbatch=256,
                        clip_param=0.2, entcoeff=0.01,
                        optim_epochs=4, optim_stepsize=1e-3, optim_batchsize=64,
                        gamma=1, lam=0.95,
                        schedule='linear'
                        )
    env.close()
    saver = tf.train.Saver()
    saver.save(sess, '/tmp/model')

def main():
    import argparse
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--env', help='environment ID', default='BreakoutNoFrameskip-v4')
    parser.add_argument('--seed', help='RNG seed', type=int, default=0)
    parser.add_argument('--num-timesteps', type=int, default=int(10e3))
    args = parser.parse_args()
    train(args.env, num_timesteps=args.num_timesteps, seed=args.seed)

if __name__ == "__main__":
    main()