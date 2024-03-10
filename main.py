"""Self Play
"""

import argparse
import os
import tensorflow as tf
import numpy as np
from env.Combat3DoF import Combat3DoF
from alg import mfac
from alg import tools
from common.play import play
from common.decay import linear_decay
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--algo', type=str, choices={'ac', 'mfac', 'mfq', 'il'}, help='choose an algorithm from the preset', required=True)
    parser.add_argument('--save_every', type=int, default=10, help='decide the self-play update interval')
    parser.add_argument('--update_every', type=int, default=5, help='decide the udpate interval for q-learning, optional')
    parser.add_argument('--n_round', type=int, default=2000, help='set the trainning round')
    parser.add_argument('--render', action='store_true', help='render or not (if true, will render every save)')
    parser.add_argument('--max_steps', type=int, default=400, help='set the max steps')

    args = parser.parse_args()

    # Initialize the environment
    env = Combat3DoF()
    handles = env.get_handles()

    tf_config = tf.ConfigProto(allow_soft_placement=True, log_device_placement=False)
    tf_config.gpu_options.allow_growth = True

    log_dir = os.path.join(BASE_DIR,'data/tmp'.format(args.algo))
    model_dir = os.path.join(BASE_DIR, 'data/models/{}'.format(args.algo))

    if args.algo in ['mfq', 'mfac']:
        use_mf = True
    else:
        use_mf = False

    start_from = 0

    sess = tf.Session(config=tf_config)
    MFAC = mfac.MFAC

    models = [MFAC(sess, args.algo + '-me',  handles[0], env), MFAC(sess, args.algo + '-opponent',  handles[1], env)]
    sess.run(tf.global_variables_initializer())
    runner = tools.Runner(sess, env, handles, args.max_steps, models, play,
                            render_every=args.save_every if args.render else 0, save_every=args.save_every, tau=0.01, log_name=args.algo,
                            log_dir=log_dir, model_dir=model_dir, train=True)

    for k in range(start_from, start_from + args.n_round):
        eps = linear_decay(k, [0, int(args.n_round * 0.8), args.n_round], [1, 0.2, 0.1])
        runner.run(eps, k)
