import os
from decouple import config
import uuid
os.environ["OPENAI_API_KEY"] = config('OPENAI_API_KEY')
from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, join_room


from llama_index import VectorStoreIndex, SimpleDirectoryReader

app = Flask(__name__)
app.static_folder = 'template/src'

socketio = SocketIO(app)

documents = SimpleDirectoryReader('Wiki/data').load_data()
index = VectorStoreIndex.from_documents(documents)

query_engine = index.as_query_engine()

@app.route('/')
def index():
    return render_template("index.html")

@socketio.on('connect')
def on_connect():
    room_id = request.sid  # Получаем уникальный идентификатор сессии пользователя
    join_room(room_id)  # Добавляем пользователя в комнату с его идентификатором сессии

@socketio.on('query')
def handle_query(data):
    query = data.get('query')  # Получаем значение поля 'query' из словаря data
    room_id = request.sid  # Получаем уникальный идентификатор сессии пользователя

    response = query_engine.query(query)
    response_text = str(response)

    # Отправляем ответ только в комнату с уникальным идентификатором сессии пользователя
    socketio.emit('response', response_text, room=room_id)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5111)
