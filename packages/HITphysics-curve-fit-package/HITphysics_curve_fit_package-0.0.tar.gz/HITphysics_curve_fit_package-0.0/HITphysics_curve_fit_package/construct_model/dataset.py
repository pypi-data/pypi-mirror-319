from ..basic.constants import *
from ..basic.J_fn import J_tar


class SearchDataset:
    def __init__(self):
        input_array = np.concatenate((
            np.linspace(-3, -1, 5 * 3),
            np.linspace(-1, -0.08, 5 * 3),
            np.linspace(-0.04, 0.4, 20 * 6),
            np.linspace(0.405, 1, 20 * 6),
            np.linspace(1.05, 3, 30 * 3)
        ))

        # input_array = np.concatenate((
        #         np.linspace(-3, -0.5, 5 * 3),
        #         np.linspace(-0.5, -0.01, 50 * 3),
        #         np.linspace(-0.01, 0.05, 300 * 6),
        #         np.linspace(0.05, 1, 20 * 6),
        #         np.linspace(1.05, 3, 30 * 3)
        #     ))

        self.inputs = input_array
        self.outputs = J_tar(self.inputs)

    def __len__(self):
        return len(self.inputs)

    def __getitem__(self, idx):
        return self.inputs, self.outputs


class OptimizeDataset:
    def __init__(self):
        input_array = np.concatenate((
            np.linspace(-3, -1, 7 * 5),
            np.linspace(-1, -0.08, 11 * 5),
            np.linspace(-0.04, 0.4, 26 * 10),
            np.linspace(0.405, 1, 21 * 10),
            np.linspace(1.05, 3, 26 * 5)
        ))

        self.inputs = input_array
        self.outputs = J_tar(self.inputs)

    def __len__(self):
        return len(self.inputs)

    def __getitem__(self, idx):
        return self.inputs, self.outputs


class TestDataset:
    def __init__(self):
        input_array = np.concatenate((
            np.linspace(-3, -0.08, 10),
            np.linspace(-0.04, 0.4, 25),
            np.linspace(0.405, 1, 20),
            np.linspace(1.05, 3, 25)
        ))

        self.inputs = input_array
        self.outputs = J_tar(self.inputs)

    def __len__(self):
        return len(self.inputs)

    def __getitem__(self, idx):
        return self.inputs, self.outputs


class CustomDataset:
    def __init__(self, input_array):
        self.inputs = input_array
        self.outputs = J_tar(self.inputs)

    def __len__(self):
        return len(self.inputs)

    def __getitem__(self, idx):
        return self.inputs, self.outputs
