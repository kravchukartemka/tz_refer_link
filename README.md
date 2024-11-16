RESTful API сервис для реферальной системы

Функционал сервиса:
регистрация и аутентификация пользователя (JWT, Oauth 2.0);
аутентифицированный пользователь должен иметь возможность создать или удалить свой реферальный код. Одновременно может быть активен только 1 код. При создании кода обязательно должен быть задан его срок годности;
возможность получения реферального кода по email адресу реферера;
возможность регистрации по реферальному коду в качестве реферала;
получение информации о рефералах по id реферера;
UI документация (Swagger/ReDoc).
Pre-requirements
Параметры представлены в открытом виде(.env отсутствует)

Usage
Для регистрации пользователя необходимо сначала отправить запрос POST на адрес /api/v1/auth/send-validation-code с телом запроса что бы получить OTP код для валидации.
POST http://localhost:8000/api/v1/auth/send-validation-code/user@examle.com
После получения кода, пользователь должен отправить запрос POST на адрес /api/v1/auth/register с параметром otp и с телом запроса:
POST http://localhost:8000/api/v1/auth/register?otp=123456

{
  "first_name": "string",
  "last_name": "string",
  "email": "user@example.com",
  "referral_code": "string",
  "password": "string"
}
После регистрации пользователя должен получить JWT токен для входа:
POST http://localhost:8000/api/v1/auth/login

{
  "username": "user@example.com",
  "password": "****"
}
...
Quick start
Установка зависимостей:

pip install -r requirements.txt
Применение миграций базы данных

alembic upgrade head   

Запуск тестов:

pytest app/tests/tests.py   
Запуск сервиса

uvicorn main:app --reload      
Доступ к UI документациям:

http://localhost:8000/docs
http://localhost:8000/redoc
