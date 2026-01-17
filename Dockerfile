FROM ubuntu:latest

WORKDIR app/

RUN pip install poetry

COPY poetry.lock pyproject.toml ./
RUN poetry install --no-root

COPY . .

EXPOSE 8000

# Определяем команду для запуска приложения
ENTRYPOINT ["poetry", "run"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
