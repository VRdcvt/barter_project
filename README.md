# 📦 Barter Project

Приложение на Django для размещения и обмена объявлениями между пользователями.

---

## 🚀 Установка

1. **Клонируйте репозиторий**

```bash
git clone https://github.com/VRdcvt/barter_project.git
cd barter_project
```

2. **Создайте и активируйте виртуальное окружение**

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate    # Windows
```

3. **Установите зависимости**

```bash
pip install -r requirements.txt
```

4. **Создайте .env файл (опционально)**

> Если используется настройка через переменные среды

---

## 🔧 Миграции и запуск сервера

1. **Выполните миграции базы данных**

```bash
python manage.py makemigrations ads
python manage.py migrate
```

2. **Создайте суперпользователя (по желанию)**

```bash
python manage.py createsuperuser
```

3. **Запустите сервер разработки**

```bash
python manage.py runserver
```

4. Перейдите в браузере по адресу:

```
http://127.0.0.1:8000/
```

---

## 🧪 Запуск тестов

Приложение использует встроенную систему тестирования Django.

```bash
python manage.py test
```

Все ключевые функции (создание, редактирование, удаление объявлений, обработка предложений) покрыты модульными тестами.

---

## 📁 Структура проекта

```
barter_project/
├── ads/                  # Основное приложение с моделями, views и шаблонами
│   ├── templates/        # Общие шаблоны
├── barter_project/       # Конфигурация проекта
├── manage.py             # Точка входа
├── requirements.txt      # Зависимости
```

---

## ✨ Дополнительно

* Bootstrap используется для стилизации.
* Django messages выводятся через модальные окна.
* Доступны фильтры по категории, состоянию, ключевым словам, пользователям и статусам обменов.

---

## 📬 Обратная связь

Если у вас есть предложения или проблемы, откройте issue или отправьте pull request.

Скриншоты:
![2025-06-02_06-10-57](https://github.com/user-attachments/assets/56fcd074-37df-42d4-8dbf-5cf9daff9154)
![2025-06-02_06-18-22](https://github.com/user-attachments/assets/39439493-c59a-46a3-8682-26099b61e08e)
![2025-06-02_06-18-30](https://github.com/user-attachments/assets/26b228e7-a9cb-45c1-811f-712a1f5fcb73)
![2025-06-02_06-18-52](https://github.com/user-attachments/assets/8e947a76-437a-4b5f-bce1-207128c04e05)
![2025-06-02_06-19-02](https://github.com/user-attachments/assets/973e384a-c538-4570-a7bd-33a15b8ebee3)
![2025-06-02_06-19-19](https://github.com/user-attachments/assets/43463a1b-703a-4e60-a328-2ead562200fe)
![2025-06-02_06-19-40](https://github.com/user-attachments/assets/a067d638-2bc4-4b73-bf98-3cd76b4a19bc)
![2025-06-02_06-19-57](https://github.com/user-attachments/assets/d0083649-6264-4477-bbd8-be1e3746f406)
![2025-06-02_06-20-07](https://github.com/user-attachments/assets/8ea58329-1988-4de0-83ab-a0d1a9a8e257)
![2025-06-02_06-20-27](https://github.com/user-attachments/assets/1f1b7873-8271-41dd-a5b9-ace506aa57d2)
![2025-06-02_06-20-39](https://github.com/user-attachments/assets/bf866c74-1f66-425c-b9f3-b0a53dec9cd6)
![2025-06-02_06-21-22](https://github.com/user-attachments/assets/ae8894fc-0e90-4671-8976-317a17a17208)
![2025-06-02_06-23-14](https://github.com/user-attachments/assets/ff231826-d7c3-4903-a6c9-00ffccd93dd8)
![2025-06-02_06-23-57](https://github.com/user-attachments/assets/9a7d8e67-3da3-4901-95c3-1a8ebe7b397d)

