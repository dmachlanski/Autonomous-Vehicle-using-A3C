import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.multiprocessing as mp

from utils import v_wrap, set_init, push_and_pull, record
from shared_adam import SharedAdam
# import gym
import os
os.environ["OMP_NUM_THREADS"] = "1"

from model import feature_vec
from server import step, reset

UPDATE_GLOBAL_ITER = 10
GAMMA = 0.9
MAX_EP = 40
# MAX_EP = 4000

# game_name = 'MountainCar-v0'
game_name = 'CartPole-v0'
# env = gym.make(game_name)

N_S = 25088
# env.observation_space.shape[0]
N_A = 3
# env.action_space.n


class Net(nn.Module):
    def __init__(self, s_dim, a_dim):
        super(Net, self).__init__()
        self.s_dim = s_dim
        self.a_dim = a_dim
        self.pi1 = nn.Linear(s_dim, 200)
        self.pi2 = nn.Linear(200, a_dim)
        self.v1 = nn.Linear(s_dim, 100)
        self.v2 = nn.Linear(100, 1)
        set_init([self.pi1, self.pi2, self.v1, self.v2])
        self.distribution = torch.distributions.Categorical

    def forward(self, x):
        pi1 = F.relu6(self.pi1(x))
        logits = self.pi2(pi1)
        v1 = F.relu6(self.v1(x))
        values = self.v2(v1)
        return logits, values

    def choose_action(self, s):
        self.eval()
        logits, _ = self.forward(s)
        prob = F.softmax(logits, dim=1).data
        m = self.distribution(prob)
        return m.sample().numpy()[0]

    def loss_func(self, s, a, v_t):
        self.train()
        logits, values = self.forward(s)
        td = v_t - values
        c_loss = td.pow(2)

        probs = F.softmax(logits, dim=1)
        m = self.distribution(probs)
        exp_v = m.log_prob(a) * td.detach().squeeze()
        a_loss = -exp_v
        total_loss = (c_loss + a_loss).mean()
        return total_loss


class Worker(mp.Process):
    def __init__(self, gnet, opt, global_ep, global_ep_r, res_queue, name):
        super(Worker, self).__init__()
        self.name = 'w%i' % name
        self.g_ep, self.g_ep_r, self.res_queue = global_ep, global_ep_r, \
            res_queue
        self.gnet, self.opt = gnet, opt
        # local network
        self.lnet = Net(N_S, N_A)
        # self.env = gym.make(game_name).unwrapped

    def run(self):
        total_step = 1
        while self.g_ep.value < MAX_EP:
            s = reset()
            print("img_array", s)
            s = feature_vec(s)
            print("feat", s)

            # s = self.env.reset()
            # feature_vec
            buffer_s, buffer_a, buffer_r = [], [], []
            ep_r = 0.
            while True:
                # if self.name == 'w0':
                    # self.env.render()
                    # feature_vec
                a = self.lnet.choose_action(s)
                # a = self.lnet.choose_action(v_wrap(s[None, :]))
                s_, r, done = step(a)
                # s_, r, done, _ = self.env.step(a)
                # feature_vec
                print("a", a)
                print("s_", s_)
                print("r", r)
                print("done", done)
                if done:
                    r = -1
                ep_r += r
                buffer_a.append(a)
                buffer_s.append(s)
                buffer_r.append(r)

                # update global and assign to local net
                if total_step % UPDATE_GLOBAL_ITER == 0 or done:  
                    # sync
                    push_and_pull(self.opt, self.lnet, self.gnet, done, s_,
                                  buffer_s, buffer_a, buffer_r, GAMMA)
                    buffer_s, buffer_a, buffer_r = [], [], []

                    if done:  # done and print information
                        record(self.g_ep, self.g_ep_r, ep_r, self.res_queue,
                               self.name)
                        break
                s = s_
                total_step += 1
        self.res_queue.put(None)


if __name__ == "__main__":
    # global network
    gnet = Net(N_S, N_A)
    # share the global parameters in multiprocessing
    gnet.share_memory()
    opt = SharedAdam(gnet.parameters(), lr=0.0001)      # global optimizer
    global_ep, global_ep_r, res_queue = (mp.Value('i', 0), mp.Value('d', 0.),
                                         mp.Queue())

    # parallel training
    workers = [Worker(gnet, opt, global_ep, global_ep_r, res_queue,
               i) for i in range(1)]
            #    i) for i in range(mp.cpu_count())]
    [w.start() for w in workers]
    res = []                    # record episode reward to plot
    while True:
        r = res_queue.get()
        if r is not None:
            res.append(r)
        else:
            break
    [w.join() for w in workers]

    import matplotlib.pyplot as plt
    plt.plot(res)
    plt.ylabel('Moving average ep reward')
    plt.xlabel('Step')
    plt.show()
