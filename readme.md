# Planti-Server
AI 기반 식물 생장 모니터링 IoT 플랫폼 "플랜티"
- Release note for v1.0.0

## Connection link
<http://43.200.105.74/home/>

## Features
### 식물 관리
- 전용 단말기를 연동하여 내 식물을 모니터링 합니다.
- 타임랩스 동영상을 생성합니다.
- 최근 물 준 날짜를 자동으로 업데이트 합니다.
- 매 시간 환경 정보를 측정합니다.
### AI 식물박사
- 내 식물의 현재 상태와 환경을 분석하여 맞춤형 재배 솔루션을 제공하는 챗봇입니다.
### 맞춤형 식물찾기
- 내 성향과 잘 맞는 식물 품종을 추천해 드립니다.
### Comming soon...
- 향후 더 많은 기능을 지원할 예정입니다.

## Installation (Server only)
```commandline
pip install -r requirements.txt
```
가상환경 사용을 권장합니다.
(Recommended to use virtual environments)

## Requirements
```
annotated-types==0.7.0
anyio==4.6.2.post1
asgiref==3.7.2
certifi==2024.8.30
distro==1.9.0
Django==4.2.5
djangorestframework==3.14.0
filelock==3.16.1
fsspec==2024.10.0
h11==0.14.0
httpcore==1.0.6
httpx==0.27.2
idna==3.10
Jinja2==3.1.4
jiter==0.7.1
MarkupSafe==3.0.2
mpmath==1.3.0
networkx==3.4.2
numpy==1.26.2
openai==1.54.4
opencv-python==4.8.1.78
pandas==2.2.3
Pillow==10.1.0
pydantic==2.9.2
pydantic_core==2.23.4
python-dateutil==2.9.0.post0
pytz==2023.3.post1
six==1.16.0
sniffio==1.3.1
sqlparse==0.4.4
sympy==1.13.3
torch==2.2.2
tqdm==4.67.0
typing_extensions==4.12.2
tzdata==2024.2
```


## Contributing & Contact
- Chang-in Baek (Server Developer) : qorckddls010@gmail.com
- Seon Heo (Hardware Developer) : tjs1220@naver.com


## License
- BSD 3-Clause "New" or "Revised" License
- Following python django license
- <https://github.com/django/django/blob/main/LICENSE>