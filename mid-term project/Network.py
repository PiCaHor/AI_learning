import torch.nn as nn
import torch.nn.functional as F
import torch


# 1: 0.063492
# class MyCNN(nn.Module):
#     def __init__(self):
#         super(MyCNN, self).__init__()
#         self.conv1 = nn.Conv2d(3, 16, 5)
#         torch.nn.BatchNorm2d(16)
#         self.pool = nn.MaxPool2d(2, 2)
#         self.conv2 = nn.Conv2d(16, 32, 5)
#         torch.nn.BatchNorm2d(32)
#         self.pool = nn.MaxPool2d(2, 2)
#         self.fc1 = nn.Linear(32 * 53 * 53, 120)
#         self.fc2 = nn.Linear(120, 84)
#         self.fc3 = nn.Linear(84, 500)
#
#     def forward(self, x):
#         x = self.pool(F.relu(self.conv1(x)))
#         x = self.pool(F.relu(self.conv2(x)))
#         x = x.view(-1, 32 * 53 * 53)
#         x = F.relu(self.fc1(x))
#         x = F.relu(self.fc2(x))
#         x = self.fc3(x)
#         x = F.softmax(x, dim=1)
#         return x

# 2:0.032000
class MyCNN(nn.Module):
    def __init__(self):
        super(MyCNN, self).__init__()
        self.conv = torch.nn.Sequential(
            torch.nn.Conv2d(in_channels=3,
                            out_channels=32,
                            kernel_size=5),
            torch.nn.BatchNorm2d(32),
            torch.nn.ReLU(),
            torch.nn.MaxPool2d(2, 2),
            torch.nn.Conv2d(32, 64, 5),
            torch.nn.BatchNorm2d(64),
            torch.nn.ReLU(),
            torch.nn.MaxPool2d(2, 2),
            torch.nn.Conv2d(64, 128, 3),
            torch.nn.ReLU(),
            torch.nn.Conv2d(128, 64, 3),
            torch.nn.ReLU(),
            torch.nn.Conv2d(64, 32, 3),
            torch.nn.ReLU(),
            torch.nn.MaxPool2d(3, 2),
        )
        self.fc = torch.nn.Sequential(
            torch.nn.Linear(32*23*23, 2048),
            torch.nn.ReLU(),
            torch.nn.Linear(2048, 2048),
            torch.nn.ReLU(),
            torch.nn.Linear(2048, 500),
            torch.nn.Softmax(dim=1)
        )

    def forward(self, x):
        x = self.conv(x)
        x = x.contiguous().view(-1, 32*23*23)
        x = self.fc(x)
        return x


# test: 0.367676 eopch: 100 batch_size:64 lr:0.01 step_size:10 gamma:0.5   linear： 2048
# test: 0.330078 eopch: 100 batch_size:64 lr:0.01 step_size:10 gamma:0.5   linear： 4096
# test: 0.453125 eopch: 100 batch_size:128 lr:0.01 step_size:10 gamma:0.5   linear： 4096 dropout: 0.2->0.5
class AlexNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.features = nn.Sequential(
            nn.Conv2d(3, 96, kernel_size=11, stride=4, padding=2),  # [None, 3, 224, 224] --> [None, 96, 55, 55]
            nn.BatchNorm2d(96),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=3, stride=2),  # [None, 96, 55, 55] --> [None, 96, 27, 27]
            nn.Conv2d(96, 256, kernel_size=5, padding=2),  # [None, 96, 27, 27] --> [None, 256, 27, 27]
            nn.BatchNorm2d(256),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=3, stride=2),  # [None, 256, 27, 27] --> [None, 256, 13, 13]
            nn.Conv2d(256, 384, kernel_size=3, padding=1),  # [None, 256, 27, 27] --> [None, 384, 13, 13]
            nn.BatchNorm2d(384),
            nn.ReLU(inplace=True),
            nn.Conv2d(384, 384, kernel_size=3, padding=1),  # [None, 384, 13, 13] --> [None, 384, 13, 13]
            nn.BatchNorm2d(384),
            nn.ReLU(inplace=True),
            nn.Conv2d(384, 256, kernel_size=3, padding=1),  # [None, 384, 13, 13] --> [None, 256, 13, 13]
            nn.BatchNorm2d(256),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=3, stride=2)  # [None, 256, 13, 13] --> [None, 256, 6, 6]
        )

        self.classifier = nn.Sequential(

            nn.Linear(256 * 6 * 6, 4096),
            nn.ReLU(inplace=True),
            nn.Dropout(p=0.5),

            nn.Linear(4096, 4096),
            nn.ReLU(inplace=True),
            nn.Dropout(p=0.5),

            nn.Linear(4096, 500)
        )

    def forward(self, inputs):
        x = self.features(inputs)
        x = torch.flatten(x, start_dim=1)
        outputs = self.classifier(x)
        return outputs


#
class VGG16Net(nn.Module):
    def __init__(self):
        super().__init__()
        self.features = nn.Sequential(
            nn.Conv2d(3, 64, kernel_size=3, stride=1, padding=1),  # [None, 3, 224, 224] --> [None, 64, 224, 224]
            nn.ReLU(inplace=True),
            nn.Conv2d(64, 64, kernel_size=3, stride=1, padding=1),  # [None, 64, 224, 224] --> [None, 64, 224, 224]
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),  # [None, 64, 224, 224] --> [None, 64, 112, 112]
            nn.Conv2d(64, 128, kernel_size=3, stride=1, padding=1),  # [None, 64, 112, 112] --> [None, 128, 112, 112]
            nn.ReLU(inplace=True),
            nn.Conv2d(128, 128, kernel_size=3, stride=1, padding=1),  # [None, 128, 112, 112] --> [None, 128, 112, 112]
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),  # [None, 128, 112, 112] --> [None, 128, 56, 56]
            nn.Conv2d(128, 256, kernel_size=3, stride=1, padding=1),  # [None, 128, 56, 56]--> [None, 256, 56, 56]
            nn.ReLU(inplace=True),
            nn.Conv2d(256, 256, kernel_size=3, stride=1, padding=1),  # [None, 256, 56, 56] --> [None, 256, 56, 56]
            nn.ReLU(inplace=True),
            nn.Conv2d(256, 256, kernel_size=3, stride=1, padding=1),  # [None, 256, 56, 56] --> [None, 256, 56, 56]
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),  # [None, 256, 56, 56] --> [None, 256, 28, 28]
            nn.Conv2d(256, 512, kernel_size=3, stride=1, padding=1),  # [None, 256, 28, 28]--> [None, 512, 28, 28]
            nn.ReLU(inplace=True),
            nn.Conv2d(512, 512, kernel_size=3, stride=1, padding=1),  # [None, 512, 28, 28] --> [None, 512, 28, 28]
            nn.ReLU(inplace=True),
            nn.Conv2d(512, 512, kernel_size=3, stride=1, padding=1),  # [None, 512, 28, 28] --> [None, 512, 28, 28]
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),  # [None, 512, 28, 28] --> [None, 512, 14, 14]
            nn.Conv2d(512, 512, kernel_size=3, stride=1, padding=1),  # [None, 512, 14, 14]--> [None, 512, 14, 14]
            nn.ReLU(inplace=True),
            nn.Conv2d(512, 512, kernel_size=3, stride=1, padding=1),  # [None, 512, 14, 14] --> [None, 512, 14, 14]
            nn.ReLU(inplace=True),
            nn.Conv2d(512, 512, kernel_size=3, stride=1, padding=1),  # [None, 512, 14, 14] --> [None, 512, 14, 14]
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),  # [None, 512, 14, 14] --> [None, 512, 7, 7]
        )

        self.classifier = nn.Sequential(
            nn.Linear(512 * 7 * 7, 4096),
            nn.ReLU(inplace=True),
            nn.Dropout(p=0.5),
            nn.Linear(4096, 4096),
            nn.ReLU(inplace=True),
            nn.Dropout(p=0.5),
            nn.Linear(4096, 500),
            nn.Softmax(dim=1)
        )

    def forward(self, inputs):
        x = self.features(inputs)
        x = torch.flatten(x, start_dim=1)
        outputs = self.classifier(x)
        return outputs
