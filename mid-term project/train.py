import torch.nn as nn
import torch
from prepare import DataInformation, getDataLoader
import torch.optim as optim
from Network import MyCNN, AlexNet, VGG16Net

args = DataInformation()
args.data_dir = "./"
args.batch_size = 128
args.learning_rate = 0.01
epoch_num = 100
step_size = 10
gamma = 0.5

train_dataloader, dev_dataloader, test_dataloader = getDataLoader(args)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# model = MyCNN().to(device)
model = AlexNet().to(device)
# model = VGG16Net().to(device)
# model = torch.load('net.pkl').to(device)
criterion = nn.CrossEntropyLoss()
optimizer = optim.SGD(model.parameters(), lr=args.learning_rate, momentum=0.9)
schedule = optim.lr_scheduler.StepLR(optimizer, step_size=step_size, gamma=gamma, last_epoch=-1)
# train
for epoch in range(epoch_num):
    running_loss = 0
    model.train()
    for i, data in enumerate(train_dataloader):
        img, label = data

        img = img.to(device)
        label = label.to(device)

        optimizer.zero_grad()
        out = model(img)

        loss = criterion(out, label)
        loss.backward()
        optimizer.step()
        running_loss += loss.data.item()
        if i % 50 == 49:
            print('[%d %d] loss: %.3f' % (epoch+1, i+1, running_loss/50))
            running_loss = 0

    model.eval()
    eval_loss = 0
    eval_acc = 0
    for data in dev_dataloader:
        img, label = data

        img = img.to(device)
        label = label.to(device)

        out = model(img)

        loss = criterion(out, label)
        eval_loss += loss.data.item() * label.size(0)
        _, pred = torch.max(out, 1)
        num_correct = (pred == label).sum()
        eval_acc += num_correct.item()

    print('Test Loss: {:.6f}, Acc: {:.6f}'.format(
        eval_loss / (len(dev_dataloader) * args.batch_size),
        eval_acc / (len(dev_dataloader) * args.batch_size)
    ))

print("Finish Training!")
torch.save(model, 'net.pkl')



