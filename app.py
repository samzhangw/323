from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")
canvas_data = ""

@app.route('/')
def index():
    return render_template('write.html')

@app.route('/display')
def display():
    return render_template('display.html')

@socketio.on('draw_event')
def handle_draw_event(json):
    emit('draw_event', json, broadcast=True)

@socketio.on('submit_event')
def handle_submit_event(json):
    global canvas_data
    canvas_data = json['image']
    emit('submit_event', json, broadcast=True)

@socketio.on('clear_event')
def handle_clear_event():
    global canvas_data
    canvas_data = ""
    emit('clear_event', broadcast=True)

@socketio.on('unlock_event')
def handle_unlock_event():
    emit('unlock_event', broadcast=True)

@socketio.on('request_canvas')
def handle_request_canvas():
    emit('submit_event', {'type': 'submit', 'image': canvas_data})

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
