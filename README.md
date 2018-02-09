# Crypto Notifier

A small bot able to send you an email when your crypto is falling down 
too fast.

Build on Django & Django Rest Framework

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

Fill .env file with the required parameters

## Launch
```
python3 manage.py runserver & python3 manage.py process_tasks
```

