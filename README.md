# QnA API

REST API-сервис, позволяющий создавать вопросы и ответы на них. Реализован на FastAPI + SQLAlchemy + Alembic + PostgreSQL, обёрнут в Docker.

## ⚙️ Как запустить проект

> Требования: установлен [Docker](https://www.docker.com/) и [Docker Compose](https://docs.docker.com/compose/)

```bash
git clone https://github.com/den13boec/hitalent_test
cd hitalent_test
```

Перед запуском необходимо создать .env файл в корне проекта для подключения к БД:

```env
# Вариант 1 (одной строкой)
DATABASE_URL=postgresql+psycopg2://qna:secret@db:5432/qna

# Вариант 2 (по частям; DATABASE_URL соберётся автоматически)
POSTGRES_HOST=db
POSTGRES_PORT=5432
POSTGRES_DB=qna
POSTGRES_USER=qna
POSTGRES_PASSWORD=secret
```

>POSTGRES_HOST=db — это имя сервиса базы данных в docker-compose.yml

Затем:

```bash
docker compose up --build
```

## Эндпойнты

### Вопросы (questions)

|  Метод | URL               | Описание                             |
|:------:|-------------------|--------------------------------------|
| GET    | `/questions/`     | Список всех вопросов                 |
| POST   | `/questions/`     | Создать новый вопрос                 |
| GET    | `/questions/{id}` | Получить вопрос и все ответы на него |
| DELETE | `/questions/{id}` | Удалить вопрос (вместе с ответами)   |

### Ответы (answers)

У каждого ответа должен быть id пользователя. Если не указывается - генерируется uuid.

|  Метод | URL                        | Описание                  |
|:------:|----------------------------|---------------------------|
| POST   | `/questions/{id}/answers/` | Добавить ответ к вопросу  |
| GET    | `/answers/{id}`            | Получить конкретный ответ |
| DELETE | `/answers/{id}`            | Удалить ответ             |

>Можно протестировать эндпойнты через [SwaggerUI](http://127.0.0.1:8000/docs) или [Redoc](http://127.0.0.1:8000/redoc)

## Тесты

Тесты написаны на Pytest, работают на **in-memory SQLite**.  
Контейнеры сервиса можно **не поднимать** - команда ниже сама создаст одноразовый контейнер.

Для запуска тестов:

```bash
docker compose run --rm -w /app -v "${PWD}:/app" api sh -lc "PIP_ROOT_USER_ACTION=ignore pip install -r requirements-dev.txt && pytest -q"
```

Покрытие:

- Questions: create/list/get/delete, валидация пустых строк, каскадное удаление ответов.

- Answers: create/get/delete, 400 на несуществующий вопрос, тримминг строк, авто-UUID для user_id
