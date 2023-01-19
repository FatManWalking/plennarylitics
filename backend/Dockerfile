# 
FROM python:3.9

# 
WORKDIR /code

# /backend
COPY ./backend/requirements.txt /code/requirements.txt

# 
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# /backend
COPY ./backend/app /code/app

# 
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080", "--reload"]