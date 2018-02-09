# Crypto Notifier

A small bot able to send you an email when your crypto is falling down 
too fast.

Build on Django & Django Rest Framework

## Requirements

* python3 in your path, and python3-virtualenv installed
* A MySQL server with a database in utf8 (utf8mb4 can cause problems at this time)

## Installation
```
python3 -m venv crypto   
```

```
source crypto/bin/activate
```

```
pip3 install -r requirements.txt
```

```
cp .env.example .env
```

```
python3 manage.py migrate
```

Fill .env file with the required parameters

## Launch
```
python3 manage.py runserver & python3 manage.py process_tasks ; fg
```

