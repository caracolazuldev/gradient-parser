FROM python:3.9-slim

RUN pip install numpy==1.22
RUN pip install colormath

WORKDIR /app

CMD ["sh", "-c", "if [ -f main.py ]; then python main.py; else echo 'No main.py script found'; fi"]
