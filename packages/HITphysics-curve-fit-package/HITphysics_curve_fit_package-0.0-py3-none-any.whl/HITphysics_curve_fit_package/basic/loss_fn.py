import torch
from torch import nn


class LogLoss(nn.Module):
    def __init__(self):
        super().__init__()

    def forward(self, w, pred, target):
        w = torch.tensor(w, dtype=torch.float64)
        log = torch.log(target / pred)

        # if torch.isnan(log).any():
        #     nan_indices = torch.nonzero(torch.isnan(torch.log(target / pred))).flatten()
        #     print("w = ", w[nan_indices].tolist())
        #     print("pred = ", pred[nan_indices].tolist())
        #     print("target = ", target[nan_indices].tolist())
        #     print("target / pred = ", (target / pred)[nan_indices].tolist())
        #     return -1

        non_nan_log = log[~torch.isnan(log)]
        if non_nan_log.numel() > 0:
            max_log = torch.max(non_nan_log)
            log[torch.isnan(log)] = max_log * 2
            loss1 = torch.sum(
                torch.where(
                    w >= 0,
                    log ** 2,
                    torch.zeros_like(pred)
                )
            )
            loss2 = torch.sum(
                torch.where(
                    w < 0,
                    torch.where(
                        pred > target,
                        torch.ones_like(pred),
                        torch.zeros_like(pred)
                    ) * log ** 2,
                    torch.zeros_like(pred)
                )
            )
            loss = torch.sqrt(loss1 + loss2)
            return loss
        else:
            return -1


class LogL1Loss(nn.Module):
    def __init__(self):
        super().__init__()

    def forward(self, w, pred, target):
        w = torch.tensor(w, dtype=torch.float64)
        log = torch.log(target / pred)

        # if torch.isnan(log).any():
        #     nan_indices = torch.nonzero(torch.isnan(torch.log(target / pred))).flatten()
        #     print("w = ", w[nan_indices].tolist())
        #     print("pred = ", pred[nan_indices].tolist())
        #     print("target = ", target[nan_indices].tolist())
        #     print("target / pred = ", (target / pred)[nan_indices].tolist())
        #     return -1

        non_nan_log = log[~torch.isnan(log)]
        if non_nan_log.numel() > 0:
            max_log = torch.max(non_nan_log)
            log[torch.isnan(log)] = max_log * 2
            loss1 = torch.sum(
                torch.where(
                    w >= 0,
                    log ** 2,
                    torch.zeros_like(pred)
                )
            )
            loss2 = torch.sum(
                torch.where(
                    w < 0,
                    torch.where(
                        pred > target,
                        torch.ones_like(pred),
                        torch.zeros_like(pred)
                    ) * log ** 2,
                    torch.zeros_like(pred)
                )
            )
            loss3 = torch.sum(
                torch.where(
                    (pred - target) ** 2 > 1e-5,
                    torch.abs(pred - target),
                    torch.zeros_like(pred)
                )
            )
            loss = torch.sqrt(loss1 + loss2) + loss3
            return loss
        else:
            return -1


def PadeLog24(x):
    PadeLog = (-1 + x) ** 2 / (20 * (-1 + x) ** 2 - (-1 + x) ** 4 + 240 * x)
    Linear = 1.58325 - 428.203 * x
    return torch.where(x >= -0.09, PadeLog, Linear)


def PadeLog22(x):
    PadeLog = (x - 1) ** 2 / ((x - 1) ** 2 / 12 + x)
    Linear = 12 - 144 * x
    return torch.where(x >= 0, PadeLog, Linear)


class PadeLoss(nn.Module):
    def __init__(self):
        super().__init__()

    def forward(self, w, pred, target):
        # 获取pred中的零元素索引
        zero_indices = torch.nonzero(pred == 0).flatten()

        # 将pred中的零元素替换为1e-6
        pred[zero_indices] = 1e-6

        PadeLog = PadeLog22(target / pred)

        loss1 = torch.sum(
            torch.where(
                w >= 0,
                PadeLog,
                torch.zeros_like(pred)
            )
        )
        loss2 = torch.sum(
            torch.where(
                w < 0,
                torch.where(
                    pred > target,
                    torch.ones_like(pred),
                    torch.zeros_like(pred)
                ) * PadeLog,
                torch.zeros_like(pred)
            )
        )
        loss = torch.sqrt(loss1 + loss2)
        if torch.isnan(loss):
            print("*** Error ***\n    loss = NaN!")
            nan_indices = torch.nonzero(torch.isnan(PadeLog22(target / pred))).flatten()
            print("    w = ", w[nan_indices].tolist())
            print("    pred = ", pred[nan_indices].tolist())
            print("    target / pred = ", (target / pred)[nan_indices].tolist())
            print("    PadeLog(target / pred) = ", (PadeLog22(target / pred))[nan_indices].tolist())
            exit()
        else:
            return loss
