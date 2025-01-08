from .basic.constants import *


def apply_bound(model):
    with torch.no_grad():
        for name, param in model.named_parameters():
            if name == 'g_vec':
                param.data.clamp_(min=0)
            elif name == 'w_vec':
                idx = 0
                for w_ij in param.data.view(-1):
                    if idx in diagonal_idx:  # 对角线元素
                        w_ij.clamp_(min=0)
                    else:
                        w_ij.clamp_(min=-30, max=30)
                    idx += 1
            elif name == 'k_vec':
                param.data.clamp_(min=0)


def train_step(dataset, model, loss_fn, optimizer):
    model.train()
    w, J = dataset[0]

    # 前向传播
    pred = model(w)

    # 计算损失
    loss = loss_fn(w, pred, J)

    # 反向传播
    loss.backward()

    # 更新参数
    optimizer.step()
    optimizer.zero_grad()

    # 应用参数限制
    apply_bound(model)

    return loss


def test_step(dataset, model, loss_fn):
    model.eval()
    w, J = dataset[0]
    pred = model(w)
    test_loss = loss_fn(w, pred, J)
    return test_loss

