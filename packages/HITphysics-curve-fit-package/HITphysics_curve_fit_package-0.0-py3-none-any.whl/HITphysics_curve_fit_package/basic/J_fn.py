from .constants import *


def J_sm(w):
    """
    :param w: numpy array
    :return: single tensor value
    """

    J_positive = (2 * g_const ** 2 / np.pi *
                  (kappa * w_c * w /
                   ((w_c ** 2 - w ** 2) ** 2 + kappa ** 2 * w ** 2)))
    # 阶跃函数
    J = np.where(w >= w_0, J_positive, 0)
    return torch.tensor(J, dtype=torch.float64)


# 定义目标函数 J_tar
def J_tar(w):
    """
    :param w: numpy array
    :return: single tensor value
    """
    J = np.float64(
        np.where(
            w >= w_0,
            J_sm(w),
            J_t + k / (w_cc - w) ** 20
        ))
    return torch.tensor(J, dtype=torch.float64)


import torch


def J_mod(w, g_vec, w_vec, k_vec):
    """
    :param w: numpy array
    :param g_vec: tensor array
    :param w_vec: tensor array
    :param k_vec: tensor array
    :return: tensor array as w
    """
    w = torch.tensor(w, dtype=torch.float64)

    # omega_ij:H矩阵的实部
    tril_indices = torch.tril_indices(n_mod, n_mod, offset=0)
    w_lower = torch.zeros((n_mod, n_mod), dtype=torch.float64)
    w_lower[tril_indices[0], tril_indices[1]] = w_vec

    real_part = w_lower.t() + w_lower  # 对称化

    # kappa_ij：H矩阵的虚部
    imag_part = -torch.diag(k_vec) / 2

    # H矩阵
    H_mat = torch.complex(real_part, imag_part)

    # 添加batch维度
    H_mat = H_mat.unsqueeze(0).expand(w.shape[0], -1, -1)

    # omega * I
    eye = torch.eye(n_mod, dtype=torch.float64).unsqueeze(0).expand_as(H_mat)
    w_eye = w.view(-1, 1, 1) * eye

    # H - omega * I
    H_w_mat = H_mat - w_eye

    # 计算逆矩阵
    inverse_mat = torch.inverse(H_w_mat)

    # 取虚部
    imag_mat = inverse_mat.imag

    # g' * Im(H-w) * g
    g_vec_mat = g_vec.view(1, -1, 1).expand(w.shape[0], -1, 1)
    result = torch.bmm(torch.bmm(g_vec_mat.transpose(1, 2), imag_mat), g_vec_mat)

    return (result / pi).view(-1)


def inverse_first_column(matrix):
    """
    只计算逆矩阵的第一列

    :param matrix: The input matrix (torch tensor) with batch dimension.
    :return: The first column of the inverse matrix for each batch.
    """
    identity = torch.eye(n_mod, dtype=torch.float64).unsqueeze(0).expand(matrix.shape[0], -1, -1)
    first_column = torch.linalg.solve(matrix, identity[:, :, 0])
    return first_column.unsqueeze(2)


def inverse_first_row(matrix):
    """
    只计算逆矩阵的第一行

    :param matrix: The input matrix (torch tensor) with batch dimension.
    :return: The first row of the inverse matrix for each batch as column vectors.
    """
    identity = torch.eye(n_mod, dtype=torch.float64).unsqueeze(0).expand(matrix.shape[0], -1, -1)
    first_row = torch.linalg.solve(matrix, identity[:, 0, :])
    return first_row.unsqueeze(1)


def single_k_J_mod(w, g_vec, w_vec, k):
    """
    :param w: numpy array
    :param g_vec: tensor array
    :param w_vec: tensor array
    :param k: tensor array
    :return: tensor array as w
    """
    # 计算 w_ij - omega (H - omega 实部)
    tril_indices = torch.tril_indices(n_mod, n_mod, offset=0)
    w_ij = torch.zeros((n_mod, n_mod), dtype=torch.float64)
    w_ij[tril_indices[0], tril_indices[1]] = w_vec

    w_ij_mat = w_ij.t() + w_ij  # 对称化

    w_ij_mat = w_ij_mat.unsqueeze(0).expand(w.shape[0], -1, -1)  # 添加 batch 维度

    eye = torch.eye(n_mod, dtype=torch.float64).unsqueeze(0).expand_as(w_ij_mat)
    w_eye = torch.tensor(w, dtype=torch.float64).view(-1, 1, 1) * eye
    w_w_mat = w_ij_mat - w_eye

    # 计算逆矩阵虚部
    kk = k / 2
    inverse_column = inverse_first_column(w_w_mat)
    temp_mat = w_w_mat.clone()
    temp_mat[:, 0, 0] = temp_mat[:, 0, 0] + inverse_column[:, 0, 0] * (kk ** 2)
    inverse_row = inverse_first_row(temp_mat)
    imag_mat = torch.bmm(inverse_column, inverse_row) * kk

    # print(f'single k :{imag_mat[0]}')
    print(temp_mat[0])

    # g' * Im(H-w) * g
    g_vec_mat = g_vec.view(1, -1, 1).expand(w.shape[0], -1, 1)
    result = torch.bmm(torch.bmm(g_vec_mat.transpose(1, 2), imag_mat), g_vec_mat)

    return (result / pi).view(-1)

# # 计算逆矩阵虚部
#     kk = k / 2
#     inverse_column = inverse_first_column(H_w_mat)
#     temp_mat = H_w_mat.clone()
#     temp_mat[:, 0, 0] = temp_mat[:, 0, 0] + inverse_column[:, 0, 0] * kk ** 2
#     inverse_row = inverse_first_row(temp_mat)
#
#     # g' * Im(H-w) * g
#     g_vec_mat = g_vec.view(1, -1, 1).expand(w.shape[0], -1, 1)
#     result = torch.bmm(g_vec_mat.transpose(1, 2), inverse_column) * torch.bmm(inverse_row, g_vec_mat) * kk
