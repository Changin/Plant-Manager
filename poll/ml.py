# Planti 성향에 따른 추천 식물 분류 모델 학습코드
import pandas as pd
import torch
# import matplotlib.pyplot as plt

dataset = pd.read_csv('planti.csv').to_numpy()
x = torch.Tensor(dataset[:, 0:-2])   # 특성
y = torch.LongTensor(dataset[:, -2])  # 정답 레이블


class Net(torch.nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.fc1 = torch.nn.Linear(6, 32)
        self.fc2 = torch.nn.Linear(32, 64)
        self.fc3 = torch.nn.Linear(64, 32)
        self.fc4 = torch.nn.Linear(32, 22)
        self.relu = torch.nn.ReLU()

    def forward(self, x):
        x = self.relu(self.fc1(x))
        x = self.relu(self.fc2(x))
        x = self.relu(self.fc3(x))
        z = self.fc4(x)

        return z


net = Net()
cel = torch.nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(net.parameters(), lr=0.01)

loss_lst = []
EPOCH = 10000

for epoch in range(EPOCH):
    z = net(x)

    loss = cel(z, y)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    loss_lst.append(loss.item())

    if epoch % 100 == 0:
        print(f'epoch={epoch}, loss={loss.item():0.5f}')

'''
plt.plot(range(EPOCH), loss_lst)
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.grid(True)
plt.show()
'''

z = net(x)
y_hat = torch.argmax(torch.softmax(z,dim=1),dim=1)
correct = torch.sum(y==y_hat)
accuracy = correct / len(y)*100

print(f'Accuracy={accuracy:0.2f}%')

# 검증
classes = ['금사철', '꽃기린', '다육', '대파', '몬스테라', '선인장', '스킨답서스', '스투키', '아스파라거스나누스', '아이비', '알로카시아', '애플민트', '염좌', '올리브나무', '장미허브', '제나두살렘', '콩나물', '테라리움', '하월시아', '해피트리', '행운목', '홍콩야자']
test_index = 12
x_test = x[test_index]
print(x_test)
y_test = y[test_index]
z_test = net(x_test)
yhat_test = torch.softmax(z_test, dim=0)
val, ind = torch.sort(yhat_test, dim=0)
# print(val)
# val, ind = torch.max(yhat_test,dim=0)
print(f'경력, 목적, 관리빈도, 채광, 환기, 크기 : {x_test}의 추천 결과')
print(f'1위 : {val[-1].item()*100:0.2f}% - {classes[ind[-1].item()]}')
print(f'2위 : {val[-2].item()*100:0.2f}% - {classes[ind[-2].item()]}')
print(f'3위 : {val[-3].item()*100:0.2f}% - {classes[ind[-3].item()]}')
print(f'4위 : {val[-4].item()*100:0.2f}% - {classes[ind[-4].item()]}')
print(f'정답은 {classes[y_test]}이다.')


# 저장
PATH = './model.pt'
torch.save(net.state_dict(), PATH)

