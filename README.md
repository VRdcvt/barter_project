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

🧪 Скриншоты интерфейса

Главная страница
![2025-06-02_06-18-22](https://github.com/user-attachments/assets/0d646fe0-9147-42f1-bd33-d4f792f00e46)
![2025-06-02_06-18-30](https://github.com/user-attachments/assets/2e732cb3-9afe-4683-b4af-9e6b60d2caef)
![2025-06-02_06-18-52](https://github.com/user-attachments/assets/c45817d4-a9a3-454c-8efe-d52be50548f5)
![2025-06-02_06-19-02](https://github.com/user-attachments/assets/42d6527c-bd53-4309-8f31-8cf69172b57f)
![2025-06-02_06-19-19](https://github.com/user-attachments/assets/3ef729fb-8a7b-4081-aa77-de6235c6c8ed)



Объявление
![2025-06-02_06-19-40](https://github.com/user-attachments/assets/6c64484d-f5d8-475c-943e-2a4520bdca33)
![2025-06-02_06-10-57](https://github.com/user-attachments/assets/6227b1d4-3c64-4cc1-93be-94a313cd6955)
![2025-06-02_06-19-57](https://github.com/user-attachments/assets/363eb10b-d172-42e6-b9b4-5c70f5840042)
![2025-06-02_06-20-07](https://github.com/user-attachments/assets/1b30fde0-82e8-4b7e-b3fc-433ad11f341f)
![2025-06-02_06-20-39](https://github.com/user-attachments/assets/88ae1229-1bdb-472e-8b74-7f81753e6ad3)
![2025-06-02_06-20-27](https://github.com/user-attachments/assets/79c5b432-116c-4500-8cc1-bf8e152de36d)



Обмены
![2025-06-02_06-21-22](https://github.com/user-attachments/assets/bdbbf5c1-7bb3-445a-8724-7c700adf3338)
![2025-06-02_06-23-57](https://github.com/user-attachments/assets/353bf2b2-1199-4672-9a18-64463fc796ab)
![2025-06-02_06-23-14](https://github.com/user-attachments/assets/be579cf6-285a-44f3-9785-741d31e0d492)


