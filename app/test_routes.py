from flask import Blueprint, request, jsonify
from app.models import db, Evento

#verificar endpoints de eventos sin requerir login
main = Blueprint('main', __name__)

@main.route('/')
@main.route('/dashboard')
def index():
    """
    Home page when running in test mode.
    """
    return '<h1>Running in Test Mode.</h1>'

@main.route('/eventos', methods=['GET'])
def listar_eventos():
    """
    Returns a list of all events (JSON).
    """
    eventos = Evento.query.all()
    data = [
        {
            'id': evento.id,
            'nombre': evento.nombre,
            'ubicacion': evento.ubicacion,
            'fecha_hora': evento.fecha_hora.strftime('%Y-%m-%d %H:%M'),
            'capacidad': evento.capacidad,
            'descripcion': evento.descripcion,
            'organizador_id': evento.organizador_id
        }
        for evento in eventos
    ]
    return jsonify(data), 200

@main.route('/eventos/<int:id>', methods=['GET'])
def listar_un_evento(id):
    """
    Returns a single event by its ID (JSON).
    """
    evento = Evento.query.get_or_404(id)
    data = {
        'id': evento.id,
        'nombre': evento.nombre,
        'ubicacion': evento.ubicacion,
        'fecha_hora': evento.fecha_hora.strftime('%Y-%m-%d %H:%M'),
        'capacidad': evento.capacidad,
        'descripcion': evento.descripcion,
        'organizador_id': evento.organizador_id
    }
    return jsonify(data), 200

@main.route('/eventos', methods=['POST'])
def crear_evento():
    """
    Creates a new event without authentication.
    Expects JSON with: nombre, ubicacion, fecha_hora, capacidad, descripcion, organizador_id.
    """
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No input data provided'}), 400

    from datetime import datetime
    evento = Evento(
        nombre=data.get('nombre'),
        ubicacion=data.get('ubicacion'),
        fecha_hora=datetime.strptime(data.get('fecha_hora'), '%Y-%m-%d %H:%M'),
        capacidad=data.get('capacidad'),
        descripcion=data.get('descripcion'),
        organizador_id=data.get('organizador_id')
    )
    db.session.add(evento)
    db.session.commit()
    return jsonify({'message': 'Event created', 'id': evento.id}), 201

@main.route('/eventos/<int:id>', methods=['PUT'])
def actualizar_evento(id):
    """
    Updates an existing event without authentication.
    """
    evento = Evento.query.get_or_404(id)
    data = request.get_json()

    from datetime import datetime
    evento.nombre = data.get('nombre', evento.nombre)
    evento.ubicacion = data.get('ubicacion', evento.ubicacion)
    if data.get('fecha_hora'):
        evento.fecha_hora = datetime.strptime(data.get('fecha_hora'), '%Y-%m-%d %H:%M')
    evento.capacidad = data.get('capacidad', evento.capacidad)
    evento.descripcion = data.get('descripcion', evento.descripcion)
    evento.organizador_id = data.get('organizador_id', evento.organizador_id)

    db.session.commit()
    return jsonify({'message': 'Event updated', 'id': evento.id}), 200

@main.route('/eventos/<int:id>', methods=['DELETE'])
def eliminar_evento(id):
    """
    Deletes an event without authentication.
    """
    evento = Evento.query.get_or_404(id)
    db.session.delete(evento)
    db.session.commit()
    return jsonify({'message': 'Event deleted', 'id': evento.id}), 200
