from .basic.constants import *
from .construct_model.model import Net
from .train_method import train_step, test_step
from .construct_model.dataset import OptimizeDataset, TestDataset, CustomDataset, SearchDataset
from .basic.loss_fn import LogLoss, LogL1Loss
from .test_method import visualise_model, model_input, path_input


def optimize(path, model, learning_rate=1e-4, epochs=1000000, check_interval=100):
    model.load_state_dict(torch.load(path))

    loss_fn = LogLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

    # Create dataset instances
    train_dataset = SearchDataset()
    test_dataset = TestDataset()
    train_losses = []
    test_losses = []

    for t in range(epochs + 1):
        # Test
        test_loss = test_step(test_dataset, model, loss_fn)

        # Train
        train_loss = train_step(train_dataset, model, loss_fn, optimizer)
        if train_loss == -1:
            break

        train_losses.append(train_loss.item())
        test_losses.append(test_loss.item())
        if t % 500 == 0 and t != 0:
            # print(f"\n-----Epoch {t}------")
            # print(f"Train Error: \n Avg loss: {np.mean(train_losses[-500:]):>8f}")
            # print(f"Test Error: \n Avg loss: {np.mean(test_losses[-500:]):>8f}")
            torch.save(model.state_dict(), 'best_model.pth')
            # print("*** model saved! ***")

        if t % check_interval == 0 and t != 0:
            # fig, ax = plt.subplots(1, 2, figsize=(12, 6))
            # ax[0].plot([loss for loss in test_losses if loss < 500], label='test_loss')
            # ax[1].plot([loss for loss in train_losses if loss < 500], label='train_loss')
            # plt.savefig(f'./optimizing/{t / 100000}.jpg')

            print(visualise_model(path_input('./best_model.pth'), print_params=False, draw=True))
            # name1 = visualise_model(model_input('./best_models/k/4.88_4.23_2.44.pth'), print_params=False, draw=True)
            # plt.legend()
            # plt.show()
