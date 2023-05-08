import torch
from prepare import DataInformation, getDataLoader
import torch.nn as nn

args = DataInformation()
args.data_dir = "./"
args.batch_size = 64

train_dataloader, dev_dataloader, test_dataloader = getDataLoader(args)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = torch.load('net.pkl').to(device)

criterion = nn.CrossEntropyLoss()
model.eval()
eval_loss = 0
eval_acc = 0
for data in test_dataloader:
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
    eval_loss / (len(test_dataloader)*args.batch_size),
    eval_acc / (len(test_dataloader)*args.batch_size)
))
