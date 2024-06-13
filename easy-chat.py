import os
from decouple import config
os.environ["OPENAI_API_KEY"] = config('OPENAI_API_KEY')
import uuid
from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, join_room

from llama_index import VectorStoreIndex, SimpleDirectoryReader, ServiceContext, GPTVectorStoreIndex
from llama_index.llms import OpenAI



app = Flask(__name__)
app.static_folder = 'template/src'

socketio = SocketIO(app)

documents = SimpleDirectoryReader('Wiki/data').load_data()


# Изменим модель
llm = OpenAI(temperature=0, model='gpt-3.5-turbo')

service_context = ServiceContext.from_defaults(llm=llm)

index = GPTVectorStoreIndex.from_documents(
	documents,
	service_context=service_context
)



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
    query = "Ответь на русском: " + data.get('query')  # Получаем значение поля 'query' из словаря data
    room_id = request.sid  # Получаем уникальный идентификатор сессии пользователя

    try:
        response = query_engine.query(query)
        response_text = str(response)
        response_text =  response_text
    except Exception as e:
        response_text = f"Error during query processing: {str(e)}"

    # Отправляем ответ только в комнату с уникальным идентификатором сессии пользователя
    socketio.emit('response', response_text, room=room_id)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5111)
