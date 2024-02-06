# csv_to_mysql_stadium 🏟️

csv_to_mysql_stadium 프로젝트는 CSV 파일로부터 경기장 정보를 읽어 해당 데이터를 MySQL 데이터베이스에 저장하는 파이썬 스크립트입니다. 이 스크립트는 축구장 및 간이운동장 데이터를 분석하여 지역별로 분류한 뒤, 이를 데이터베이스에 구조화된 형태로 저장합니다.

# 설치 및 실행 가이드 🚀

## 필요 조건
이 프로젝트를 실행하기 전에 다음 요구사항을 충족해야 합니다:

* Python 3.6 이상
* pandas
* mysql-connector-python
* python-dotenv

## 설치 방법 📂
필요한 파이썬 패키지 설치

```bash
pip install pandas mysql-connector-python python-dotenv
```

## .env 파일 설정 📋

```.env
DB_HOST=localhost
DB_USER=my_username
DB_PASSWORD=my_password
DB_DATABASE=my_database
```

## 실행 방법 🏃
위의 설치 방법에 따라 필요한 조건을 충족시킵니다.
메인 스크립트를 실행합니다.

```python
python index.py
```
