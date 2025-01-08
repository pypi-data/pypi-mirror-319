from torch import nn

from ..basic.constants import *
from ..basic.J_fn import J_mod, single_k_J_mod

g_vec = torch.ones(n_mod, dtype=torch.float64) * 0.1
w_vec = torch.rand(int(n_mod * (n_mod + 1) / 2), dtype=torch.float64) * 8 - 4
w_vec[diagonal_idx] = torch.rand(len(diagonal_idx), dtype=torch.float64) * 5
k_vec = torch.ones(n_mod, dtype=torch.float64) * 5


class Net(nn.Module):
    def __init__(self, g_vec=g_vec, w_vec=w_vec, k_vec=k_vec):
        super().__init__()

        # 初始化参数
        self.g_vec = nn.Parameter(g_vec)
        self.w_vec = nn.Parameter(w_vec)
        self.k_vec = nn.Parameter(k_vec)

    def forward(self, w):
        return J_mod(w, self.g_vec, self.w_vec, self.k_vec)


class SingleKNet(nn.Module):
    def __init__(self, g_vec=g_vec, w_vec=w_vec, k_vec=k_vec):
        super().__init__()

        # 初始化参数
        self.g_vec = nn.Parameter(g_vec)
        self.w_vec = nn.Parameter(w_vec)
        self.k_vec = nn.Parameter(k_vec)

    def forward(self, w):
        return single_k_J_mod(w, self.g_vec, self.w_vec, self.k)
