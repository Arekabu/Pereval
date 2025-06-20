# Документация REST API для приложения Pereval

Проект предоставляет REST API для добавления, редактирования и просмотра данных о горных перевалах.

## 🔗 Базовые URL
Для основной версии с PosgreSQL:
```url
http://127.0.0.1:8000/api/submitData/
```
Демонстрационная версия с SQLite:
```url
https://kryakzenpuk.pythonanywhere.com/api/submitData/
```

## 📋 Эндпоинты API
### 1.  Добавление нового перевала (POST)
- **URL:** `/submitData/`
- **Метод:** `POST`
- **Требуемые поля:**
  
  ```json
  {    
    "beauty_title": "string",   
    "title": "string",
    "other_titles": "string (optional)",
    "connect": "string (optional)",
    "user": {
        "email": "string (unique)",
        "fam": "string",
        "name": "string",
        "otc": "string (optional)",
        "phone": "string (optional)"
    },
    "coords": {
        "latitude": "float (-90 to 90)",
        "longitude": "float (-180 to 180)",
        "height": "integer"
    },
    "level": {
        "winter": "string (1A-3C or empty)",
        "summer": "string (1A-3C or empty)",
        "autumn": "string (1A-3C or empty)",
        "spring": "string (1A-3C or empty)"
    },
    "images": [
        {
            "data": "null (в текущей версии не используется)",
            "title": "string"
        }
    ]
  }
  ```
  <br>
  
  **Пример запроса:**
  
  ```json
  {
    "beauty_title": "хребет",
    "title": "Чёрный",
    "other_titles": "Темнолесье",
    "connect": "Соединяет лес с горой",
    "user": {
        "email": "misha@gmail.ru",
        "fam": "Иванов",
        "name": "Михаил",
        "otc": "Борисович",
        "phone": "+7 926 45 67"
    },
    "coords": {
        "latitude": 20.5050,
        "longitude": 20.9999,
        "height": 1122
    },
    "level": {
        "winter": "1A",
        "summer": "2A",
        "autumn": "3A",
        "spring": ""
    },
    "images": [
        {"data": null, "title": "Подножие"},
        {"data": null, "title": "Склон"}
        ]
  }
  ```
  <br>
  
  **Успешный ответ (200 OK):**

  ```json
  {
    "status": 200,
    "message": "Запись успешно создана",
    "id": 1
  }
  ```
  <br>

  **Ошибка (400 Bad Request):**

  ```json
  {
    "status": 400,
    "message": {
        "coords": {"latitude": ["Ensure this value is less than or equal to 90."]}
    },
    "id": null
  }
  ```
  <br>

### 2. Получение данных (GET)

#### 2.1 Получить все перевалы пользователя по email
- URL: `/submitData/?user__email=<email>`
- Метод: `GET`

  **Пример запроса:**
  ```text
  https://kryakzenpuk.pythonanywhere.com/api/submitData/?user__email=misha@gmail.ru
  ```
  <br>

  **Успешный ответ (200 OK):**
  ```json
  [
    {
        "id": 1,
        "beauty_title": "пер.",
        "title": "Нижняя Пхия",
        "other_titles": "Южный Триев",
        "connect": "Соединяет что-то с чем-то",
        "add_time": "2025-06-18T17:20:31.678727Z",
        "status": "new",
        "user": {
            "email": "misha@gmail.ru",
            "fam": "Иванов",
            "name": "Михаил",
            "otc": "Борисович",
            "phone": "+7 926 45 67"
        },
        "coords": {
            "latitude": "19.3842",
            "longitude": "13.1525",
            "height": 1100
        },
        "level": {
            "winter": "1A",
            "summer": "1A",
            "autumn": "1A",
            "spring": "1A"
        },
        "images": [
            {
                "data": null,
                "title": "Спуск"
            },
            {
                "data": null,
                "title": "Подъём"
            }
        ]
    },
    {
        "id": 2,
        "beauty_title": "пер.",
        "title": "Дятлова",
        "other_titles": "Не Триев",
        "connect": "",
        "add_time": "2025-06-18T17:32:34.959319Z",
        "status": "new",
        "user": {
            "email": "misha@gmail.ru",
            "fam": "Иванов",
            "name": "Михаил",
            "otc": "Борисович",
            "phone": "+7 926 45 67"
        },
        "coords": {
            "latitude": "19.3870",
            "longitude": "13.1580",
            "height": 1135
        },
        "level": {
            "winter": "1A",
            "summer": "1А",
            "autumn": "1А",
            "spring": "1A"
        },
        "images": [
            {
                "data": null,
                "title": "Река"
            },
            {
                "data": null,
                "title": "Дерево"
            }
        ]
    }
  ]
  ```
  <br>

  **Ошибка (400 Bad Request):**
  ```json
  {
    "error": "Не указан email пользователя"
  }
  ```
  <br> 
  
#### 2.2 Получить конкретный перевал по ID
- URL: `/submitData/<id>/`
- Метод: `GET`

  **Пример запроса:**
  ```url
  https://kryakzenpuk.pythonanywhere.com/api/submitData/1/
  ```
  <br>

  **Успешный ответ (200 OK):**
  ```json
  {
    "id": 1,
    "beauty_title": "пер.",
    "title": "Нижняя Пхия",
    "other_titles": "Южный Триев",
    "connect": "Соединяет что-то с чем-то",
    "add_time": "2025-06-18T17:20:31.678727Z",
    "status": "new",
    "user": {
        "email": "misha@gmail.ru",
        "fam": "Иванов",
        "name": "Михаил",
        "otc": "Борисович",
        "phone": "+7 926 45 67"
    },
    "coords": {
        "latitude": "19.3842",
        "longitude": "13.1525",
        "height": 1100
    },
    "level": {
        "winter": "1A",
        "summer": "1A",
        "autumn": "1A",
        "spring": "1A"
    },
    "images": [
        {
            "data": null,
            "title": "Спуск"
        },
        {
            "data": null,
            "title": "Подъём"
        }
    ]
  }
  ```
  <br>

  **Ошибка (404 Not Found):**
  ```json
  {
    "message": "Перевал не найден",
    "id": 999
  }
  ```
  <br>

### 3. Редактирование перевала (PATCH)
  - **URL:** `/submitData/<id>/`
  - **Метод:** `PATCH`
  - **Ограничения:**
    - Можно редактировать только перевалы со статусом `"new"`.
    - Запрещено изменять данные пользователя (`fam`, `name`, `otc`, `email`, `phone`).
    <br>
    
    **Пример запроса:**
    ```json
    {
      "title": "Новое название",
      "level": {"winter": "2B"}
    }
    ```
    <br>
  
    **Успешный ответ (200 OK):**
    ```json
    {
      "state": 1,
      "message": "Запись успешно обновлена"
    }
    ```
    <br>
  
    **Ошибка (400 Bad Request):**
    ```json
    {
      "state": 0,
      "message": "Редактирование запрещено: запись не в статусе 'new'"
    }
    ```
    <br>

## 🛠 Технические детали
- **Стек:** Django + Django REST Framework (DRF)
- **Аутентификация:** Отсутствует (доступ без токена)
- **Статусы перевала:**
  - `new` — можно редактировать
  - `pending` , `accepted` , `rejected` — редактирование запрещено
  

  

  
  
