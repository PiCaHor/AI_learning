from torchvision.datasets import ImageFolder
from torch.utils.data import RandomSampler
from torch.utils.data import DataLoader
from torchvision import transforms


class DataInformation:
    def __init__(self):
        self.data_dir = ""
        self.batch_size = 0
        self.learning_rate = 0


def getDataLoader(args):
    train_transform = transforms.Compose([
                transforms.RandomHorizontalFlip(p=0.5),
                transforms.RandomVerticalFlip(p=0.5),
                transforms.ToTensor()
            ])

    test_transform = transforms.Compose([
                transforms.ToTensor()
            ])

    args.train_path = args.data_dir + "train_sample"
    train_dataset = ImageFolder(args.train_path, transform=train_transform)
    train_sampler = RandomSampler(train_dataset)
    train_dataloader = DataLoader(train_dataset,
                                  sampler=train_sampler,
                                  batch_size=args.batch_size)

    args.dev_path = args.data_dir + "dev_sample"
    dev_dataset = ImageFolder(args.dev_path, transform=test_transform)
    dev_sampler = RandomSampler(dev_dataset)
    dev_dataloader = DataLoader(dev_dataset,
                                sampler=dev_sampler,
                                batch_size=args.batch_size)

    args.test_path = args.data_dir + "test_sample"
    test_dataset = ImageFolder(args.test_path, transform=test_transform)
    test_sampler = RandomSampler(test_dataset)
    test_dataloader = DataLoader(test_dataset,
                                 sampler=test_sampler,
                                 batch_size=args.batch_size)

    return train_dataloader, dev_dataloader, test_dataloader



