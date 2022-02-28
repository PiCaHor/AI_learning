class Message:
    def __init__(self, dis, path):
        self.dis = dis
        self.path = path

    def add_Info(self, start, end):
        with open('./log.txt', 'a') as file_object:
            file_object.write('Query node from ' + start + ' to ' + end + '\n')
            file_object.write('Distance is ' + str(self.dis) + '\n')
            file_object.write('Path is ' + self.path + '\n\n')


def init(m, max_dis):
    t = [[] for i in range(m)]
    for i in range(m):
        for j in range(m):
            if i == j:
                t[i].append(0)
            else:
                t[i].append(max_dis)
    return t
