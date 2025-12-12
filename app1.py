from flask import Flask, render_template, request, jsonify, session
import psycopg2
from psycopg2 import sql
from datetime import datetime
import json

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta_aqui'  # Necesaria para usar sesiones

def get_db_connection():
    return psycopg2.connect(
        host="localhost",
        database="miboletin",
        user="postgres",
        password="123456"
    )

# Ruta principal
@app.route('/')
def index():
    return render_template('loginuser.html')

# Ruta para loginuser
@app.route('/loginuser')
def loginuser():
    return render_template('loginuser.html')

# Ruta para solicitud_user con datos del administrador
@app.route('/solicitud_user')
def solicitud_user():
    # Obtener un administrador de la base de datos
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT id_admin, nombre_completo, correo_electronico FROM administradores LIMIT 1;')
    admin = cur.fetchone()
    cur.close()
    conn.close()
    
    # Si no hay administrador, usar valores por defecto
    if admin:
        admin_id, admin_name, admin_email = admin
    else:
        admin_id, admin_name, admin_email = 'ADM001', 'Administrador del Sistema', 'admin@sistema.com'
    
    return render_template('solicitud.html', 
                         admin_id=admin_id, 
                         admin_name=admin_name, 
                         admin_email=admin_email)

# Ruta para verificar usuario
@app.route('/verificar_usuario', methods=['POST'])
def verificar_usuario():
    data = request.json
    user_identifier = data.get('userIdentifier')
    user_email = data.get('userEmail')
    
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Buscar en estudiantes
    cur.execute(
        'SELECT id_estudiante, nombre_completo, codigo_estudiante FROM estudiantes WHERE codigo_estudiante = %s AND correo_electronico = %s;',
        (user_identifier, user_email)
    )
    estudiante = cur.fetchone()
    
    if estudiante:
        # Guardar información del usuario en sesión
        session['user_info'] = {
            'tipo': 'estudiante',
            'id': estudiante[0],
            'nombre': estudiante[1],
            'codigo': estudiante[2]
        }
        cur.close()
        conn.close()
        return jsonify({
            'status': 'success',
            'tipo': 'estudiante',
            'id': estudiante[0],
            'nombre': estudiante[1],
            'codigo': estudiante[2]
        })
    
    # Buscar en profesores
    cur.execute(
        'SELECT id_profesor, nombre_completo, codigo_profesor FROM profesores WHERE codigo_profesor = %s AND correo_electronico = %s;',
        (user_identifier, user_email)
    )
    profesor = cur.fetchone()
    
    if profesor:
        # Guardar información del usuario en sesión
        session['user_info'] = {
            'tipo': 'profesor',
            'id': profesor[0],
            'nombre': profesor[1],
            'codigo': profesor[2]
        }
        cur.close()
        conn.close()
        return jsonify({
            'status': 'success',
            'tipo': 'profesor',
            'id': profesor[0],
            'nombre': profesor[1],
            'codigo': profesor[2]
        })
    
    cur.close()
    conn.close()
    return jsonify({
        'status': 'error',
        'message': 'Usuario no encontrado. Verifica tu identificador y correo electrónico.'
    }), 404

# Ruta para guardar la solicitud en la base de datos
@app.route('/guardar_solicitud', methods=['POST'])
def guardar_solicitud():
    data = request.json
    
    # Obtener información del usuario desde la sesión
    user_info = session.get('user_info')
    
    if not user_info:
        return jsonify({
            'status': 'error',
            'message': 'Información de usuario no encontrada. Por favor, verifica tu identidad primero.'
        }), 400
    
    # Extraer datos del JSON
    motivo = data.get('requestReason')
    admin_id = data.get('adminId')
    
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        # Insertar la solicitud en la tabla
        cur.execute(
            """
            INSERT INTO solicitudes_cambio_contrasena 
            (tipo_usuario, id_usuario, codigo_usuario, correo_usuario, motivo, id_admin, estado)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING id_solicitud, fecha_solicitud;
            """,
            (user_info['tipo'],
             user_info['id'],
             user_info['codigo'],
             data.get('userEmail'),
             motivo,
             admin_id,
             'pendiente')
        )
        
        resultado = cur.fetchone()
        id_solicitud = resultado[0]
        fecha_solicitud = resultado[1]
        
        conn.commit()
        
        # Obtener información del administrador
        cur.execute(
            'SELECT nombre_completo, correo_electronico FROM administradores WHERE id_admin = %s;',
            (admin_id,)
        )
        admin_info = cur.fetchone()
        
        cur.close()
        conn.close()
        
        # Limpiar la sesión después de guardar
        session.pop('user_info', None)
        
        return jsonify({
            'status': 'success',
            'message': 'Solicitud guardada correctamente',
            'id_solicitud': id_solicitud,
            'fecha_solicitud': fecha_solicitud.strftime('%d/%m/%Y %H:%M:%S'),
            'tipo_usuario': user_info['tipo'],
            'nombre_usuario': user_info['nombre'],
            'admin_name': admin_info[0] if admin_info else 'Administrador del Sistema',
            'admin_email': admin_info[1] if admin_info else 'admin@sistema.com'
        })
        
    except Exception as e:
        if conn:
            conn.rollback()
        cur.close()
        conn.close()
        return jsonify({
            'status': 'error',
            'message': f'Error al guardar la solicitud: {str(e)}'
        }), 500

@app.route('/limpiar_sesion', methods=['POST'])
def limpiar_sesion():
    session.pop('user_info', None)
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    app.run(debug=True)