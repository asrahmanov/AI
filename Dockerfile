# базовый образ Python
FROM python:3.9.0-slim

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем всю текущую директорию в контейнер
COPY . .

# Устанавливаем зависимости из файла requirements.txt
RUN pip install -r requirements.txt

# Определяем порт, на котором будет работать
EXPOSE 5111

# Запускаем ваше приложение Flask
CMD ["python", "easy-chat.py"]
