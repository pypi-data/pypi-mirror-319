from torch.optim.lr_scheduler import ReduceLROnPlateau

from .basic.constants import *
from .train_method import train_step, test_step
from .construct_model.dataset import SearchDataset, TestDataset
from .basic.loss_fn import LogLoss
from .construct_model.model import Net, SingleKNet
from .test_method import visualise_model, model_input, path_input


def crude_train(model, train_dataset, test_dataset, loss_fn, optimizer, scheduler, model_number):
    """
    这个函数用于粗糙地对随机模型进行梯度下降
    返回最终的 loss 以反映粗糙训练后模型的质量
    :param model: 未训练的模型
    :return: 训练完成后的 loss
    """
    epoch_counter = 0
    while optimizer.param_groups[0]['lr'] > min_lr:
        # Test
        test_loss = test_step(test_dataset, model, loss_fn)

        # Train
        train_loss = train_step(train_dataset, model, loss_fn, optimizer)
        if train_loss == -1:
            print("\n!!! loss = NaN ,model dumped !!!\n")
            break

        # print every 500 epoch
        if epoch_counter % 1000 == 0:
            print(f"\n---Model {model_number} Epoch {epoch_counter}---")
            print(f"Train Error: \n Avg loss: {train_loss:>8f}")
            print(f"Test Error: \n Avg loss: {test_loss:>8f}")
            if epoch_counter == 15000:
                model.k_vec.requires_grad = True
            torch.save(model.state_dict(), './best_model.pth')

        # Update learning rate
        scheduler.step(test_loss)

        epoch_counter += 1

    print("\n！！！Stopping training！！！\n")
    return model


if __name__ == '__main__':
    learning_rate = 1e-3  # 初始学习率
    min_lr = 1e-5  # 最小学习率

    train_dataset = SearchDataset()
    test_dataset = TestDataset()

    # 每次循环训练一个随机初值模型
    model_counter = 0
    while True:
        print(f'### Begin to train model No.{model_counter+1} ###')
        # 初始化
        model = Net()

        loss_fn = LogLoss()
        optimizer = torch.optim.Adam([
            {'params': model.g_vec, 'lr': learning_rate / 10},
            {'params': model.w_vec, 'lr': learning_rate},
            {'params': model.k_vec, 'lr': learning_rate / 10}
        ])
        scheduler = ReduceLROnPlateau(
            optimizer,
            mode='min',
            factor=0.1,
            patience=1000,
            min_lr=min_lr,
            verbose=True,
        )

        # 粗糙训练
        trained_model = crude_train(
            model,
            train_dataset,
            test_dataset,
            loss_fn,
            optimizer,
            scheduler,
            model_number=model_counter+1,
        )

        # 保存优秀模型
        torch.save(trained_model.state_dict(), './best_model.pth')
        name, loss_pos, loss_neg = visualise_model(path_input('./best_model.pth'), draw=True)
        torch.save(trained_model.state_dict(), f'./models/1.5/{name}.pth')

        model_counter += 1

