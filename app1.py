from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import psycopg2
from psycopg2 import sql
from datetime import datetime
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import bcrypt

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta_aqui'

# Configuración del servidor SMTP (ajusta según tu proveedor)
SMTP_SERVER = "smtp.gmail.com"  # Para Gmail, cambia si usas otro
SMTP_PORT = 587
SMTP_USERNAME = "andresdevbod@gmail.com"  # Cambia esto
SMTP_PASSWORD = "lkrx ciua qxsl maqo"  # Cambia esto (usa contraseña de aplicación para Gmail)
EMAIL_FROM = "MiBoletínAdmin.com <andresdevbod@gmail.com>"

def get_db_connection():
    return psycopg2.connect(
        host="localhost",
        database="miboletin",
        user="postgres",
        password="123456"
    )

def enviar_correo_admin(destinatario, asunto, cuerpo_html, cuerpo_texto=""):
    """
    Función para enviar correos electrónicos
    """
    try:
        # Crear mensaje
        mensaje = MIMEMultipart('alternative')
        mensaje['Subject'] = asunto
        mensaje['From'] = SMTP_USERNAME
        mensaje['To'] = destinatario
        
        # Crear versiones del mensaje
        parte_texto = MIMEText(cuerpo_texto, 'plain')
        parte_html = MIMEText(cuerpo_html, 'html')
        
        # Adjuntar ambas versiones
        mensaje.attach(parte_texto)
        mensaje.attach(parte_html)
        
        # Conectar y enviar
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()  # Encriptar conexión
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.send_message(mensaje)
            
        print(f"Correo enviado exitosamente a {destinatario}")
        return True
        
    except Exception as e:
        print(f"Error al enviar correo: {str(e)}")
        return False

@app.route('/')
def index():
    return render_template('loginuser.html')

# Modificar la ruta loginuser para manejar POST
@app.route('/loginuser', methods=['GET', 'POST'])
def loginuser():
    if request.method == 'GET':
        return render_template('loginuser.html')
    
    elif request.method == 'POST':
        # Obtener datos del formulario
        user_identifier = request.form.get('userIdentifier')
        user_email = request.form.get('correo')
        password = request.form.get('contraseña')
        
        # Validar que todos los campos estén presentes
        if not all([user_identifier, user_email, password]):
            return render_template('loginuser.html', 
                                 error='Todos los campos son requeridos')
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        try:
            # Buscar primero como estudiante
            cur.execute(
                'SELECT id_estudiante, nombre_completo, codigo_estudiante, contrasena FROM estudiantes WHERE codigo_estudiante = %s AND correo_electronico = %s;',
                (user_identifier, user_email)
            )
            estudiante = cur.fetchone()
            
            if estudiante:
                # Verificar contraseña (asumiendo que está hasheada con bcrypt)
                if bcrypt.checkpw(password.encode('utf-8'), estudiante[3].encode('utf-8')):
                    session['user_info'] = {
                        'tipo': 'estudiante',
                        'id': estudiante[0],
                        'nombre': estudiante[1],
                        'codigo': estudiante[2]
                    }
                    cur.close()
                    conn.close()
                    return redirect(url_for('estudiante_dashboard'))
                else:
                    return render_template('loginuser.html', 
                                         error='Contraseña incorrecta')
            
            # Si no es estudiante, buscar como profesor
            cur.execute(
                'SELECT id_profesor, nombre_completo, codigo_profesor, contrasena FROM profesores WHERE codigo_profesor = %s AND correo_electronico = %s;',
                (user_identifier, user_email)
            )
            profesor = cur.fetchone()
            
            if profesor:
                # Verificar contraseña
                if bcrypt.checkpw(password.encode('utf-8'), profesor[3].encode('utf-8')):
                    session['user_info'] = {
                        'tipo': 'profesor',
                        'id': profesor[0],
                        'nombre': profesor[1],
                        'codigo': profesor[2]
                    }
                    cur.close()
                    conn.close()
                    return redirect(url_for('profesor_dashboard'))
                else:
                    return render_template('loginuser.html', 
                                         error='Contraseña incorrecta')
            
            # Si no se encontró en ninguna tabla
            return render_template('loginuser.html', 
                                 error='Usuario no encontrado. Verifica tu identificador y correo electrónico.')
            
        except Exception as e:
            print(f"Error en login: {str(e)}")
            return render_template('loginuser.html', 
                                 error='Error en el servidor. Intenta más tarde.')
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()

# Agregar rutas para los dashboards
@app.route('/estudiante')
def estudiante_dashboard():
    # Verificar que el usuario esté logueado y sea estudiante
    user_info = session.get('user_info')
    
    if not user_info or user_info.get('tipo') != 'estudiante':
        return redirect(url_for('loginuser'))
    
    return render_template('estudiante.html', 
                         nombre=user_info['nombre'],
                         codigo=user_info['codigo'])

@app.route('/profesor')
def profesor_dashboard():
    # Verificar que el usuario esté logueado y sea profesor
    user_info = session.get('user_info')
    
    if not user_info or user_info.get('tipo') != 'profesor':
        return redirect(url_for('loginuser'))
    
    return render_template('profesor.html', 
                         nombre=user_info['nombre'],
                         codigo=user_info['codigo'])

# Ruta para cerrar sesión
@app.route('/logout')
def logout():
    session.pop('user_info', None)
    return redirect(url_for('loginuser'))

@app.route('/solicitud_user')
def solicitud_user():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT id_admin, nombre_completo, correo_electronico FROM administradores LIMIT 1;')
    admin = cur.fetchone()
    cur.close()
    conn.close()
    
    if admin:
        admin_id, admin_name, admin_email = admin
    else:
        admin_id, admin_name, admin_email = 'ADM001', 'Administrador del Sistema', 'admin@sistema.com'
    
    return render_template('solicitud.html', 
                         admin_id=admin_id, 
                         admin_name=admin_name, 
                         admin_email=admin_email)

@app.route('/verificar_usuario', methods=['POST'])
def verificar_usuario():
    data = request.json
    user_identifier = data.get('userIdentifier')
    user_email = data.get('userEmail')
    
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute(
        'SELECT id_estudiante, nombre_completo, codigo_estudiante FROM estudiantes WHERE codigo_estudiante = %s AND correo_electronico = %s;',
        (user_identifier, user_email)
    )
    estudiante = cur.fetchone()
    
    if estudiante:
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
    
    cur.execute(
        'SELECT id_profesor, nombre_completo, codigo_profesor FROM profesores WHERE codigo_profesor = %s AND correo_electronico = %s;',
        (user_identifier, user_email)
    )
    profesor = cur.fetchone()
    
    if profesor:
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
    user_email = data.get('userEmail')
    
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
             user_email,
             motivo,
             admin_id,
             'pendiente')
        )
        
        resultado = cur.fetchone()
        id_solicitud = resultado[0]
        fecha_solicitud = resultado[1]
        
        # Obtener información del administrador
        cur.execute(
            'SELECT nombre_completo, correo_electronico FROM administradores WHERE id_admin = %s;',
            (admin_id,)
        )
        admin_info = cur.fetchone()
        
        conn.commit()
        
        # Preparar datos para el correo
        admin_email = admin_info[1] if admin_info else 'admin@sistema.com'
        admin_name = admin_info[0] if admin_info else 'Administrador del Sistema'
        
        # Enviar correo al administrador (en segundo plano para no bloquear la respuesta)
        try:
            asunto = f"Solicitud de Cambio de Contraseña - #{id_solicitud}"
            
            # Cuerpo HTML del correo
            cuerpo_html = f"""
            <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 10px;">
                    <div style="background-color: #003366; color: white; padding: 15px; border-radius: 10px 10px 0 0; text-align: center;">
                        <h2 style="margin: 0;">Sistema de Gestión de Contraseñas</h2>
                    </div>
                    
                    <div style="padding: 20px;">
                        <h3 style="color: #003366;">Nueva Solicitud de Cambio de Contraseña</h3>
                        
                        <div style="background-color: #f5f5f5; padding: 15px; border-radius: 5px; margin: 15px 0;">
                            <p><strong>ID de Solicitud:</strong> {id_solicitud}</p>
                            <p><strong>Fecha y Hora:</strong> {fecha_solicitud.strftime('%d/%m/%Y %H:%M:%S')}</p>
                        </div>
                        
                        <h4 style="color: #003366;">Información del Usuario:</h4>
                        <table style="width: 100%; border-collapse: collapse; margin-bottom: 20px;">
                            <tr>
                                <td style="padding: 8px; border-bottom: 1px solid #ddd;"><strong>Tipo de Usuario:</strong></td>
                                <td style="padding: 8px; border-bottom: 1px solid #ddd;">{user_info['tipo'].capitalize()}</td>
                            </tr>
                            <tr>
                                <td style="padding: 8px; border-bottom: 1px solid #ddd;"><strong>Código:</strong></td>
                                <td style="padding: 8px; border-bottom: 1px solid #ddd;">{user_info['codigo']}</td>
                            </tr>
                            <tr>
                                <td style="padding: 8px; border-bottom: 1px solid #ddd;"><strong>Nombre:</strong></td>
                                <td style="padding: 8px; border-bottom: 1px solid #ddd;">{user_info['nombre']}</td>
                            </tr>
                            <tr>
                                <td style="padding: 8px; border-bottom: 1px solid #ddd;"><strong>Correo Electrónico:</strong></td>
                                <td style="padding: 8px; border-bottom: 1px solid #ddd;">{user_email}</td>
                            </tr>
                        </table>
                        
                        <h4 style="color: #003366;">Motivo de la Solicitud:</h4>
                        <div style="background-color: #f9f9f9; padding: 15px; border-left: 4px solid #003366; margin: 10px 0;">
                            <p style="margin: 0; font-style: italic;">{motivo}</p>
                        </div>
                        
                        <div style="margin-top: 25px; padding: 15px; background-color: #e8f4fd; border-radius: 5px; border-left: 4px solid #4A90E2;">
                            <p style="margin: 0;"><strong>Acción requerida:</strong> Por favor, revisa esta solicitud en el panel de administración y contáctate con el usuario para proceder con el cambio de contraseña.</p>
                        </div>
                        
                        <div style="margin-top: 30px; padding-top: 15px; border-top: 1px solid #ddd; text-align: center; color: #666; font-size: 12px;">
                            <p>Este es un mensaje automático del Sistema de Gestión de Contraseñas. Por favor, no respondas a este correo.</p>
                        </div>
                    </div>
                </div>
            </body>
            </html>
            """
            
            # Cuerpo en texto plano para clientes que no soportan HTML
            cuerpo_texto = f"""
            SOLICITUD DE CAMBIO DE CONTRASEÑA
            
            ID de Solicitud: {id_solicitud}
            Fecha y Hora: {fecha_solicitud.strftime('%d/%m/%Y %H:%M:%S')}
            
            INFORMACIÓN DEL USUARIO:
            -------------------------
            Tipo de Usuario: {user_info['tipo'].capitalize()}
            Código: {user_info['codigo']}
            Nombre: {user_info['nombre']}
            Correo Electrónico: {user_email}
            
            MOTIVO DE LA SOLICITUD:
            -----------------------
            {motivo}
            
            ---
            
            Acción requerida: Por favor, revisa esta solicitud en el panel de administración y contáctate con el usuario para proceder con el cambio de contraseña.
            
            Este es un mensaje automático del Sistema de Gestión de Contraseñas.
            """
            
            # Enviar correo
            enviar_correo_admin(admin_email, asunto, cuerpo_html, cuerpo_texto)
            
        except Exception as email_error:
            print(f"Error al enviar correo (continuando sin interrumpir): {str(email_error)}")
            # No interrumpimos el flujo si falla el correo
        
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
            'admin_name': admin_name,
            'admin_email': admin_email
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