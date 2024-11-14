# poll/views.py
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
import torch
import os


# Model 클래스 선언
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


def mainpage(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('home:index'))

    return render(request, 'poll/main.html')


def survey(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('home:index'))

    questions = {
        'Survey': [
            {
                'question': {'number': 'q1', 'question': '당신은 식물을 키워본 경험이 있나요?'},
                'answer': ['6개월 미만', '1년 미만', '1년 ~ 2년', '2년 ~ 3년', '4년 이상']
            },
            {
                'question': {'number': 'q2', 'question': '식물을 어떤 목적으로 키우고 싶나요?'},
                'answer': ['100% 실내 공기정화', '실내 공기정화', '중간', '관상용', '100% 관상용']
            },
            {
                'question': {'number': 'q3', 'question': '식물 관리를 얼마나 자주 할 수 있나요?'},
                'answer': ['월 1회 미만', '월 1~2회', '월 3~4회', '주 1~2회', '주 3회 이상']
            },
            {
                'question': {'number': 'q4', 'question': '하루 중 채광 시간은?'},
                'answer': ['2시간 미만', '4시간', '6시간', '8시간', '10시간 이상']
            },
            {
                'question': {'number': 'q5', 'question': '환기는 얼마나 잘 되나요?'},
                'answer': ['통풍 매우 안됨', '통풍 안됨', '보통', '통풍 잘됨', '통풍 매우 잘됨']
            },
            {
                'question': {'number': 'q6', 'question': '원하는 화분의 크기는?'},
                'answer': ['미니 화분(10cm 이하)', '소형 화분(10~20cm)', '중형 화분(20~30cm)', '대형 화분 (30~40cm)', '40cm 이상']
            },
        ]
    }

    context = {
        'questions': questions,
    }
    return render(request, 'poll/polls.html', context)


def result(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('home:index'))
    
    if request.method == 'POST':
        responses = {key: request.POST[key] for key in request.POST if key.startswith('q')}
        res = calculateRecommend(responses)

        context = {
            'responses': res
        }

        return render(request, 'poll/result.html', context)  # get 방식 요청 응답

    return render(request, 'poll/main.html')


def calculateRecommend(responses):
    # 불러오기
    path = os.getcwd() + '/poll/model.pt'
    classes = ['금사철', '꽃기린', '다육', '대파', '몬스테라', '선인장', '스킨답서스', '스투키', '아스파라거스나누스', '아이비', '알로카시아', '애플민트', '염좌',
               '올리브나무', '장미허브', '제나두살렘', '콩나물', '테라리움', '하월시아', '해피트리', '행운목', '홍콩야자']
    # print(PATH)
    model = Net()
    model.load_state_dict(torch.load(path))
    model.eval()

    # 불러온 모델 테스트
    ans = []
    for k, v in responses.items():
        ans.append(float(v))

    x_test1 = torch.tensor(ans)
    z_test1 = model(x_test1)
    yhat_test = torch.softmax(z_test1, dim=0)
    val, ind = torch.sort(yhat_test, dim=0)

    res = []
    res.append((f'{val[-1].item() * 100:0.2f}%', classes[ind[-1].item()]))
    res.append((f'{val[-2].item() * 100:0.2f}%', classes[ind[-2].item()]))
    res.append((f'{val[-3].item() * 100:0.2f}%', classes[ind[-3].item()]))
    res.append((f'{val[-4].item() * 100:0.2f}%', classes[ind[-4].item()]))
    
    return res
