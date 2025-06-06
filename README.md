# QRKot - Благотворительный фонд поддержки котиков

QRKot — это приложение для управления благотворительными проектами, направленными на помощь кошачьей популяции. Фонд собирает пожертвования на различные целевые проекты, такие как медицинское обслуживание, обустройство кошачьей колонии и поддержка бездомных кошек.

## Описание

Проект позволяет создать несколько целевых проектов, в которые пользователи могут делать пожертвования. Все пожертвования поступают в проекты по принципу **First In, First Out (FIFO)**. Как только проект набирает необходимую сумму, он закрывается, и пожертвования направляются на следующий открытый проект.

### Возможности проекта:

- Создание целевых проектов.
- Просмотр информации о проектах (название, описание, сумма).
- Совершение пожертвований пользователями.
- Принцип FIFO для распределения пожертвований.
- Просмотр списка своих пожертвований.
- Автоматическое распределение пожертвований по проектам.

## Структура проекта

### Проекты

- Каждый проект имеет название, описание и цель по сбору средств.
- Проекты могут быть открыты или закрыты в зависимости от того, собрана ли нужная сумма.
- Когда проект закрывается, пожертвования поступают в следующий проект.

### Пожертвования

- Пожертвования вносятся в фонд и автоматически распределяются по проектам.
- Пожертвования можно сопровождать комментариями.
- Если проект закрыт или если текущая сумма пожертвования превышает нужную сумму, оставшиеся средства направляются в следующий проект.

### Пользователи

- Администраторы могут создавать проекты.
- Все пользователи могут просматривать список проектов, включая собранные и требуемые суммы.
- Зарегистрированные пользователи могут отправлять пожертвования и видеть список своих пожертвований.

## Установка

1. Клонируйте репозиторий:
    ```
    git clone git@github.com:turbonyasha/QRkot_spreadsheets.git
    ```
2. Перейдите в каталог проекта:
    ```
    cd QRkot_spreadsheets
    ```
3. Установите зависимости:
    ```
    pip install -r requirements.txt
    ```
4. Настройте базу данных и выполните миграции:
    ```
    alembic upgrade head
    ```

## Запуск проекта

Для запуска приложения на локальном сервере используйте команду:

```
uvicorn app.main:app --reload
```

Теперь приложение доступно по адресу: [http://127.0.0.1:8000](http://127.0.0.1:8000)

## Структура каталога проекта.
- app/: Основной каталог проекта.
- app/models/: Модели для базы данных.
- app/schemas/: Схемы для сериализации данных.
- app/crud/: Логика работы с базой данных.
- app/api/: Роутеры и эндпоинты для API.
- app/core/: Основные утилиты и настройки.
- alembic/versions/: Миграции проекта. 

## Документация проекта

Документация API проекта в формате Swagger доступна после запуска проекта на локальном сервере на эндпоинте [/docs](http://127.0.0.1:8000/docs)

В формате ReDoc документация для проекта доступна на эндпоинте [/redoc](http://127.0.0.1:8000/redoc).


## Автор проекта
[Женя Скуратова]
- github [turbonyasha](https://github.com/turbonyasha)
- telegram [@janedoel](https://t.me/janedoel)