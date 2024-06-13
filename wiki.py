s    join_room(room_id)  # Добавляем пользователя в комнату с его идентификатором сессии

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
