# Barmen admin panel

Статичная страница `web/index.html` предназначена для размещения на ESP32 и работает с
эндпоинтами в текстовом формате:

- `GET/POST /config` — `ssid;password`
- `GET/POST /ingredients` — многострочный список `short;display`
- `GET/POST /cocktail_recipes` — многострочный список `name;short(weight),short(weight)`
- `GET/POST /pump_assigment` — многострочный список `short;pump_id`

## Мок-сервер

Пока микроконтроллер не готов, страницу можно протестировать с помощью Flask-сервера.

```bash
pip install flask
python mock_server.py
```

После запуска страница будет доступна на `http://127.0.0.1:5000/`, все данные будут
сохраняться в `mock_state.json`.
