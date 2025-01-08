from torch import nn

from ..basic.J_fn import J_tar, J_mod
from ..basic.loss_fn import LogLoss
from model import Net
from ..basic.constants import *

evaluate_input = np.concatenate((
    np.linspace(-3, -0.08, 10 * 5),
    np.linspace(-0.04, 0.4, 25 * 10),
    np.linspace(0.405, 1, 20 * 10),
    np.linspace(1.05, 3, 25 * 5)
))


def cat_input(cat_param):
    """
    这个函数用于将合并在一起的 params 差分
    :param cat_param: 合并的 params
    :return: 拆分的 params ([torch]格式)
    """
    len_g_vec = n_mod
    len_w_vec = int(n_mod * (n_mod + 1) / 2)
    len_k_vec = n_mod

    g_vec = cat_param[:len_g_vec]
    w_vec = cat_param[len_g_vec:len_g_vec + len_w_vec]
    k_vec = cat_param[len_g_vec + len_w_vec:len_g_vec + len_w_vec + len_k_vec]

    g_vec = torch.tensor(g_vec)
    w_vec = torch.tensor(w_vec)
    k_vec = torch.tensor(k_vec)

    return [g_vec, w_vec, k_vec]


def path_input(path):
    """
    这个函数用于提取模型中的参数
    :param path: 模型地址
    :return: 拆分的模型参数（[torch]格式）
    """
    model = Net()
    model.load_state_dict(torch.load(path))

    params_dict = {}
    for name, param in model.named_parameters():
        params_dict[name] = param.clone().detach()

    g_vec = params_dict['g_vec']
    w_vec = params_dict['w_vec']
    k_vec = params_dict['k_vec']

    return [g_vec, w_vec, k_vec]


def model_input(model):
    """
    这个函数用于提取模型中的参数
    :return: 拆分的模型参数（[torch]格式）
    """
    params_dict = {}
    for name, param in model.named_parameters():
        params_dict[name] = param.clone().detach()

    g_vec = params_dict['g_vec']
    w_vec = params_dict['w_vec']
    k_vec = params_dict['k_vec']

    return [g_vec, w_vec, k_vec]


def visualise_model(param_list, evaluate_w=evaluate_input, print_params: bool = False, draw: bool = True):
    """
    这个函数用于
    画给定模型的拟合曲线
     print 参数
    计算模型 loss
    """
    g_vec = param_list[0]
    w_vec = param_list[1]
    k_vec = param_list[2]

    # 计算 loss
    target = J_tar(evaluate_w)
    pred = J_mod(evaluate_w, g_vec, w_vec, k_vec)
    loss_fn = LogLoss()
    loss = loss_fn(evaluate_w, pred, target).item()

    pos_idx = np.where(evaluate_w > 0)[0]
    loss_pos = loss_fn(evaluate_w[pos_idx], pred[pos_idx], target[pos_idx]).item()

    mid_idx = np.where((0 < evaluate_w) & (evaluate_w < 0.4))[0]
    loss_mid = loss_fn(evaluate_w[mid_idx], pred[mid_idx], target[mid_idx]).item()

    neg_idx = np.where(evaluate_w < 0)[0]
    loss_neg = loss_fn(evaluate_w[neg_idx], pred[neg_idx], target[neg_idx]).item()

    # print(f'total loss:{round(loss, 2)}')
    # print(f'positive loss:{round(loss_pos, 2)}')
    # print(f'negative loss:{round(loss_neg, 2)}')
    # print(f'middle loss:{round(loss_mid, 2)}')
    name = f'{round(loss, 2)}_{round(loss_pos, 2)}_{round(loss_neg, 2)}'
    # print(name)

    # print 参数
    if print_params:
        print(f'g:{g_vec.tolist()}')
        print(f'w:{w_vec.tolist()}')
        print(f'k:{k_vec.tolist()}')

    # 画图
    if draw:
        w_plot = np.linspace(-3, 3, 1000)
        plt.plot(w_plot, J_tar(w_plot), label='target', linewidth=1)
        plt.plot(w_plot, J_mod(w_plot, g_vec, w_vec, k_vec), label='pred', linewidth=1)

        plt.yscale('log')
        plt.ylim([1e-10, 1])

    return name, loss_pos, loss_neg


def reorder(param_list, save_model: bool = False, path=''):
    """
    重新排列参数顺序
    """
    g_vec = param_list[0]
    w_vec = param_list[1]
    k_vec = param_list[2]

    # 检索 k_vec 中的非零值的索引
    idx = torch.where(k_vec != 0)
    if len(idx) != 1:
        raise ValueError("k_vec 中非零值的数量不为 1")
    else:
        # 交换非零元素与第一个元素的位置
        idx = idx[0].item()

        temp = g_vec[0].clone()
        g_vec[0] = g_vec[idx]
        g_vec[idx] = temp

        tril_indices = torch.tril_indices(n_mod, n_mod, offset=0)
        w_lower = torch.zeros((n_mod, n_mod), dtype=torch.float64)
        w_lower[tril_indices[0], tril_indices[1]] = w_vec
        w_ij = w_lower.t() + w_lower - torch.diag(torch.diag(w_lower))

        temp = w_ij[0].clone()
        w_ij[0] = w_ij[idx]
        w_ij[idx] = temp

        temp = w_ij[:, 0].clone()
        w_ij[:, 0] = w_ij[:, idx]
        w_ij[:, idx] = temp

        w_vec = w_ij[tril_indices[0], tril_indices[1]]

        k_vec[0] = k_vec[idx]
        k_vec[idx] = 0

        if save_model:
            model = Net()

            model.g_vec = nn.Parameter(g_vec)
            model.w_vec = nn.Parameter(w_vec)
            model.k_vec = nn.Parameter(k_vec)
            # print(path)
            torch.save(model.state_dict(), path.replace('.pth', '_reordered.pth'))
        return [g_vec, w_vec, k_vec]


if __name__ == '__main__':
    visualise_model(path_input(path='./best_model.pth'), print_params=True)
    # visualise_model(path_input(path='./best_models/k/4.66_3.62_2.93_reordered.pth'), print_params=True)
    plt.show()
