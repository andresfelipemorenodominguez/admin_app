from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import psycopg2
import psycopg2.extras
from psycopg2 import sql
import bcrypt
import random
import string
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta_aqui'  # Necesaria para sesiones

# -------------------------
# 🔧 CONFIGURACIÓN EMAIL (GMAIL)
# -------------------------
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USER = "miboletin5@gmail.com"
EMAIL_PASSWORD = "oshx qaxu ugdo baql"
EMAIL_FROM = "MiBoletínAdmin.com <miboletin5@gmail.com>"

# -------------------------
# 🔌 CONFIGURACIÓN DATABASE
# -------------------------
def get_db_connection():
    return psycopg2.connect(
        host="localhost",
        database="miboletin",
        user="postgres",
        password="123456"
    )

# 📧 FUNCIÓN PARA ENVIAR EMAIL DE VERIFICACIÓN (ACTUALIZADA)
def send_verification_email(to_email, verification_code):
    """Envía un email con el código de verificación"""
    try:
        subject = "Verifica tu cuenta en MiBoletín.com"
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                * {{
                    margin: 0;
                    padding: 0;
                    box-sizing: border-box;
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                }}
                
                body {{
                    background: linear-gradient(135deg, #f0f7ff 0%, #e6f0ff 100%);
                    color: #333;
                    line-height: 1.6;
                    min-height: 100vh;
                    padding: 20px;
                }}
                
                .email-container {{
                    max-width: 600px;
                    margin: 0 auto;
                    background: #FFFFFF;
                    border-radius: 10px;
                    overflow: hidden;
                    box-shadow: 0 8px 25px rgba(0, 51, 102, 0.15);
                    border: 1px solid #CCCCCC;
                }}
                
                .email-header {{
                    background-color: #003366;
                    color: #FFFFFF;
                    padding: 30px 20px;
                    text-align: center;
                    box-shadow: 0 2px 15px rgba(0, 51, 102, 0.2);
                }}
                
                .email-header h1 {{
                    font-size: 1.8rem;
                    font-weight: 700;
                    letter-spacing: 0.5px;
                    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
                    margin: 0;
                }}
                
                .email-content {{
                    padding: 2.5rem;
                }}
                
                .welcome-section {{
                    text-align: center;
                    margin-bottom: 2rem;
                }}
                
                .welcome-section h2 {{
                    color: #003366;
                    font-size: 1.6rem;
                    margin-bottom: 1rem;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    gap: 10px;
                }}
                
                .welcome-section p {{
                    color: #666;
                    font-size: 0.95rem;
                    margin-bottom: 1.5rem;
                }}
                
                .verification-code {{
                    background: #f8fafc;
                    border-radius: 8px;
                    padding: 2rem;
                    text-align: center;
                    margin: 2rem 0;
                    border-left: 4px solid #003366;
                }}
                
                .code-display {{
                    display: inline-block;
                    padding: 20px 40px;
                    background-color: #003366;
                    color: #FFFFFF;
                    font-size: 28px;
                    font-weight: 700;
                    letter-spacing: 8px;
                    border-radius: 6px;
                    margin: 15px 0;
                    font-family: monospace;
                    box-shadow: 0 4px 12px rgba(0, 51, 102, 0.2);
                    border: 2px solid #4A90E2;
                }}
                
                .instructions {{
                    background: rgba(74, 144, 226, 0.1);
                    padding: 1.5rem;
                    border-radius: 6px;
                    margin: 2rem 0;
                    border: 1px solid rgba(74, 144, 226, 0.3);
                }}
                
                .instructions h3 {{
                    color: #003366;
                    margin-bottom: 1rem;
                    font-size: 1.1rem;
                    display: flex;
                    align-items: center;
                    gap: 10px;
                }}
                
                .instructions ul {{
                    list-style: none;
                    padding-left: 0;
                }}
                
                .instructions li {{
                    margin-bottom: 0.8rem;
                    padding-left: 24px;
                    position: relative;
                    color: #555;
                }}
                
                .instructions li:before {{
                    content: "✓";
                    color: #4A90E2;
                    position: absolute;
                    left: 0;
                    font-weight: bold;
                }}
                
                .cta-button {{
                    text-align: center;
                    margin: 2.5rem 0;
                }}
                
                .button {{
                    display: inline-block;
                    background-color: #4A90E2;
                    color: #FFFFFF;
                    text-decoration: none;
                    padding: 16px 32px;
                    border-radius: 6px;
                    font-weight: 600;
                    font-size: 1rem;
                    border: none;
                    cursor: pointer;
                    transition: all 0.3s;
                    box-shadow: 0 4px 12px rgba(74, 144, 226, 0.3);
                }}
                
                .button:hover {{
                    background-color: #003366;
                    transform: translateY(-2px);
                    box-shadow: 0 6px 16px rgba(0, 51, 102, 0.2);
                }}
                
                .warning-note {{
                    background-color: #fff8e1;
                    border-left: 4px solid #ffb900;
                    padding: 1rem 1.25rem;
                    margin: 1.5rem 0;
                    border-radius: 4px;
                    color: #333;
                }}
                
                .email-footer {{
                    background-color: #003366;
                    color: #FFFFFF;
                    padding: 2rem;
                    margin-top: 2rem;
                    text-align: center;
                }}
                
                .footer-content {{
                    max-width: 500px;
                    margin: 0 auto;
                }}
                
                .footer-logo {{
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    gap: 12px;
                    margin-bottom: 1.5rem;
                }}
                
                .footer-logo-text {{
                    color: #FFFFFF;
                    font-size: 1.4rem;
                    font-weight: 700;
                    letter-spacing: 0.5px;
                }}
                
                .social-links {{
                    display: flex;
                    justify-content: center;
                    gap: 15px;
                    margin: 1.5rem 0;
                }}
                
                .social-icon {{
                    display: inline-flex;
                    align-items: center;
                    justify-content: center;
                    width: 36px;
                    height: 36px;
                    background: rgba(255, 255, 255, 0.1);
                    border-radius: 50%;
                    color: #FFFFFF;
                    text-decoration: none;
                    transition: all 0.3s ease;
                }}
                
                .social-icon:hover {{
                    background: #4A90E2;
                    transform: translateY(-2px);
                }}
                
                .footer-bottom {{
                    border-top: 1px solid rgba(255, 255, 255, 0.1);
                    padding-top: 1.5rem;
                    margin-top: 1.5rem;
                    color: #CCCCCC;
                    font-size: 0.85rem;
                }}
                
                @media (max-width: 600px) {{
                    .email-content {{
                        padding: 1.5rem;
                    }}
                    
                    .code-display {{
                        padding: 15px 25px;
                        font-size: 22px;
                        letter-spacing: 6px;
                    }}
                    
                    .button {{
                        padding: 14px 28px;
                        width: 100%;
                    }}
                }}
            </style>
        </head>
        <body>
            <div class="email-container">
                <div class="email-header">
                    <h1>MiBoletín.com</h1>
                </div>
                
                <div class="email-content">
                    <div class="welcome-section">
                        <h2>¡Bienvenido a MiBoletín.com! 👋</h2>
                        <p>Gracias por registrarte en nuestra plataforma. Estamos emocionados de tenerte con nosotros.</p>
                    </div>
                    
                    <div class="verification-code">
                        <h3 style="color: #003366; margin-bottom: 1rem;">Código de Verificación</h3>
                        <p style="color: #666; margin-bottom: 1rem;">Usa este código para completar tu registro:</p>
                        <div class="code-display">{verification_code}</div>
                        <p style="color: #666; font-size: 0.9rem; margin-top: 1rem;">Este código es válido por 5 minutos</p>
                    </div>
                    
                    <div class="instructions">
                        <h3>📋 Instrucciones para verificar tu cuenta:</h3>
                        <ul>
                            <li>Regresa a la página de verificación de MiBoletín.com</li>
                            <li>Ingresa el código mostrado arriba</li>
                            <li>Haz clic en "Verificar Cuenta"</li>
                            <li>¡Y listo! Podrás acceder a todas las funciones</li>
                        </ul>
                    </div>
                    
                    <div class="warning-note">
                        <p><strong>⚠️ Importante:</strong> Si no solicitaste este registro, por favor ignora este email. Tu información no será utilizada.</p>
                    </div>
                    
                    <div class="cta-button">
                        <a href="#" class="button">Ir a MiBoletín.com</a>
                    </div>
                </div>
                
                <div class="email-footer">
                    <div class="footer-content">
                        <div class="footer-logo">
                            <div class="footer-logo-text">MiBoletín.com</div>
                        </div>
                        
                        <p style="color: #CCCCCC; margin-bottom: 1.5rem;">
                            La plataforma líder para la gestión de boletines y comunicación digital.
                        </p>
                        
                        <div class="social-links">
                            <a href="#" class="social-icon">📘</a>
                            <a href="#" class="social-icon">🐦</a>
                            <a href="#" class="social-icon">📸</a>
                            <a href="#" class="social-icon">💼</a>
                        </div>
                        
                        <div class="footer-bottom">
                            <p>© {datetime.now().year} MiBoletín.com. Todos los derechos reservados.</p>
                            <p>Este es un email automático, por favor no respondas a este mensaje.</p>
                            <p><a href="#" style="color: #4A90E2; text-decoration: none;">Política de Privacidad</a> | <a href="#" style="color: #4A90E2; text-decoration: none;">Términos de Servicio</a></p>
                        </div>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """
        
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = EMAIL_FROM
        msg['To'] = to_email
        
        msg.attach(MIMEText(html_content, 'html'))
        
        server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()
        
        print(f"Email enviado exitosamente a {to_email}")
        return True
        
    except Exception as e:
        print(f"Error enviando email a {to_email}: {str(e)}")
        return False

# 🔑 FUNCIÓN PARA GENERAR CÓDIGO
def generate_verification_code(length=6):
    """Genera un código de verificación aleatorio"""
    # Para tokens largos, usar letras y números
    if length > 10:
        characters = string.ascii_letters + string.digits
        return ''.join(random.choices(characters, k=length))
    else:
        return ''.join(random.choices(string.digits, k=length))

# -------------------------
# 📌 RUTAS HTML
# -------------------------
@app.route("/")
def register():
    return render_template("register.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/forgot-password")
def forgot_password():
    return render_template("f-password.html")

@app.route("/email-verification")
def email_verification():
    return render_template("e-verification.html")

@app.route("/request-password")
def request_password():
    return render_template("r-password.html")

# -------------------------
# 📌 RUTA PARA EL DASHBOARD (PROTEGIDA)
# -------------------------
@app.route("/dashboard")
def dashboard():
    # Verificar si el usuario está logueado
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    return render_template("dashboard.html")

# -------------------------
# 📌 RUTA PARA CERRAR SESIÓN
# -------------------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('login'))

# -------------------------
# 📌 RUTA PARA REGISTRO (POST)
# -------------------------
@app.route("/register", methods=["POST"])
def register_user():
    data = request.get_json()

    fullname = data.get("fullname")
    email = data.get("email")
    password = data.get("password")

    if not all([fullname, email, password]):
        return jsonify({"status": "error", "message": "All fields are required."})

    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    
    verification_code = generate_verification_code()
    verification_expires = datetime.now() + timedelta(minutes=5)

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        insert_query = """
            INSERT INTO administradores 
            (nombre_completo, correo_electronico, contrasena, verification_code, verification_code_expires)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id_admin;
        """
        cur.execute(insert_query, (fullname, email, hashed_password, verification_code, verification_expires))
        new_id = cur.fetchone()[0]

        conn.commit()
        cur.close()
        conn.close()

        email_sent = send_verification_email(email, verification_code)
        
        if not email_sent:
            return jsonify({
                "status": "warning", 
                "message": "User registered but verification email could not be sent. Please try resending.",
                "id": new_id,
                "redirect": "/email-verification"
            })

        return jsonify({
            "status": "success", 
            "message": "User registered successfully! Verification email sent.", 
            "id": new_id,
            "redirect": "/email-verification"
        })

    except psycopg2.Error as e:
        error_message = str(e).lower()
        
        if "unique constraint" in error_message:
            return jsonify({"status": "error", "message": "Email already registered."})
        elif "not null" in error_message:
            return jsonify({"status": "error", "message": "All fields are required."})
        elif "foreign key" in error_message:
            return jsonify({"status": "error", "message": "Referential integrity error."})
        else:
            print(f"Database error: {e}")
            return jsonify({"status": "error", "message": "Database error occurred. Please try again later."})

    except Exception as e:
        print(f"Unexpected error: {e}")
        return jsonify({"status": "error", "message": "An unexpected error occurred. Please try again."})

# -------------------------
# 📌 RUTA PARA INICIAR SESIÓN (POST)
# -------------------------
@app.route("/login", methods=["POST"])
def login_user():
    data = request.get_json()
    
    username = data.get("username")
    password = data.get("password")
    
    if not username or not password:
        return jsonify({
            "status": "error", 
            "message": "Todos los campos son requeridos.",
            "field": "general"
        })
    
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        
        query = """
            SELECT id_admin, nombre_completo, correo_electronico, contrasena, email_verified 
            FROM administradores 
            WHERE nombre_completo = %s OR correo_electronico = %s
        """
        cur.execute(query, (username, username))
        user = cur.fetchone()
        
        cur.close()
        conn.close()
        
        if not user:
            return jsonify({
                "status": "error", 
                "message": "Nombre de usuario o correo electrónico no encontrado.",
                "field": "username"
            })
        
        if not user['email_verified']:
            return jsonify({
                "status": "error", 
                "message": "Por favor, verifica tu email antes de iniciar sesión.",
                "field": "email"
            })
        
        if bcrypt.checkpw(password.encode('utf-8'), user['contrasena'].encode('utf-8')):
            # Crear sesión
            session['user_id'] = user['id_admin']
            session['user_name'] = user['nombre_completo']
            session['user_email'] = user['correo_electronico']
            
            return jsonify({
                "status": "success", 
                "message": "Inicio de sesión exitoso.",
                "redirect": "/dashboard",
                "user": {
                    "id": user['id_admin'],
                    "name": user['nombre_completo'],
                    "email": user['correo_electronico']
                }
            })
        else:
            return jsonify({
                "status": "error", 
                "message": "Contraseña incorrecta.",
                "field": "password"
            })
            
    except Exception as e:
        print(f"Login error: {e}")
        return jsonify({
            "status": "error", 
            "message": "Error al iniciar sesión. Por favor, intenta nuevamente.",
            "field": "general"
        })

# -------------------------
# 📌 RUTA PARA VERIFICAR CÓDIGO (POST)
# -------------------------
# En la función verify_code de app.py
@app.route("/verify-code", methods=["POST"])
def verify_code():
    data = request.get_json()
    
    email = data.get("email")
    code = data.get("code")
    
    if not email or not code:
        return jsonify({"status": "error", "message": "Email and code are required."})
    
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        query = """
            SELECT id_admin, verification_code, verification_code_expires 
            FROM administradores 
            WHERE correo_electronico = %s
        """
        cur.execute(query, (email,))
        result = cur.fetchone()
        
        if not result:
            return jsonify({"status": "error", "message": "Email not found."})
        
        user_id, stored_code, expires = result
        
        if datetime.now() > expires:
            return jsonify({"status": "error", "message": "Verification code has expired. Please request a new one."})
        
        if stored_code != code:
            return jsonify({"status": "error", "message": "Invalid verification code."})
        
        update_query = """
            UPDATE administradores 
            SET email_verified = TRUE, 
                verification_code = NULL,
                verification_code_expires = NULL
            WHERE correo_electronico = %s
        """
        cur.execute(update_query, (email,))
        conn.commit()
        
        # ✅ CREAR SESIÓN AUTOMÁTICAMENTE
        session['user_id'] = user_id
        session['user_email'] = email
        
        # Obtener nombre del usuario
        cur.execute("SELECT nombre_completo FROM administradores WHERE id_admin = %s", (user_id,))
        user_name = cur.fetchone()[0]
        session['user_name'] = user_name
        
        cur.close()
        conn.close()
        
        return jsonify({
            "status": "success", 
            "message": "Email verified successfully!",
            "user_id": user_id,
            "user_email": email,
            "user_name": user_name
        })
        
    except Exception as e:
        print(f"Verification error: {e}")
        return jsonify({"status": "error", "message": "Verification failed. Please try again."})

# -------------------------
# 📌 RUTA PARA REENVIAR CÓDIGO (POST)
# -------------------------
@app.route("/resend-code", methods=["POST"])
def resend_code():
    data = request.get_json()
    
    email = data.get("email")
    
    if not email:
        return jsonify({"status": "error", "message": "Email is required."})
    
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        query = "SELECT id_admin FROM administradores WHERE correo_electronico = %s"
        cur.execute(query, (email,))
        result = cur.fetchone()
        
        if not result:
            return jsonify({"status": "error", "message": "Email not found."})
        
        new_code = generate_verification_code()
        new_expires = datetime.now() + timedelta(minutes=5)
        
        update_query = """
            UPDATE administradores 
            SET verification_code = %s,
                verification_code_expires = %s
            WHERE correo_electronico = %s
        """
        cur.execute(update_query, (new_code, new_expires, email))
        conn.commit()
        
        cur.close()
        conn.close()
        
        email_sent = send_verification_email(email, new_code)
        
        if email_sent:
            return jsonify({
                "status": "success", 
                "message": f"New verification code sent to {email}"
            })
        else:
            return jsonify({
                "status": "error", 
                "message": "Failed to send verification email. Please try again."
            })
        
    except Exception as e:
        print(f"Resend error: {e}")
        return jsonify({"status": "error", "message": "Failed to resend code. Please try again."})

# -------------------------
# 📌 RUTA PARA ACTUALIZAR EMAIL (POST)
# -------------------------
@app.route("/update-email", methods=["POST"])
def update_email():
    data = request.get_json()
    
    old_email = data.get("old_email")
    new_email = data.get("new_email")
    
    if not old_email or not new_email:
        return jsonify({"status": "error", "message": "Both old and new email are required."})
    
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        check_query = "SELECT id_admin FROM administradores WHERE correo_electronico = %s"
        cur.execute(check_query, (new_email,))
        if cur.fetchone():
            return jsonify({"status": "error", "message": "New email is already registered."})
        
        cur.execute(check_query, (old_email,))
        if not cur.fetchone():
            return jsonify({"status": "error", "message": "Old email not found."})
        
        new_code = generate_verification_code()
        new_expires = datetime.now() + timedelta(minutes=5)
        
        update_query = """
            UPDATE administradores 
            SET correo_electronico = %s,
                verification_code = %s,
                verification_code_expires = %s,
                email_verified = FALSE
            WHERE correo_electronico = %s
        """
        cur.execute(update_query, (new_email, new_code, new_expires, old_email))
        conn.commit()
        
        email_sent = send_verification_email(new_email, new_code)
        
        cur.close()
        conn.close()
        
        if email_sent:
            return jsonify({
                "status": "success", 
                "message": f"Email updated. New verification code sent to {new_email}"
            })
        else:
            return jsonify({
                "status": "error", 
                "message": "Email updated but failed to send verification email."
            })
        
    except Exception as e:
        print(f"Update email error: {e}")
        return jsonify({"status": "error", "message": "Failed to update email. Please try again."})

# 📌 RUTA PARA SOLICITUD DE RECUPERACIÓN DE CONTRASEÑA (POST)
@app.route("/request-password", methods=["POST"])
def request_password_post():  # Cambia el nombre aquí
    data = request.get_json()
    
    email = data.get("email")
    
    if not email:
        return jsonify({"status": "error", "message": "Email is required."})
    
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Verificar si el email existe en la base de datos
        query = "SELECT id_admin, nombre_completo FROM administradores WHERE correo_electronico = %s"
        cur.execute(query, (email,))
        user = cur.fetchone()
        
        if not user:
            # Por seguridad, no revelamos si el email existe o no
            return jsonify({
                "status": "success", 
                "message": "Si el email está registrado, recibirás un enlace para restablecer tu contraseña."
            })
        
        # Generar token de recuperación (puedes usar un código o token único)
        recovery_code = generate_verification_code(32)  # Generar código más largo
        recovery_expires = datetime.now() + timedelta(hours=24)
        
        # Guardar el token en la base de datos
        update_query = """
            UPDATE administradores 
            SET recovery_token = %s,
                recovery_token_expires = %s
            WHERE correo_electronico = %s
        """
        cur.execute(update_query, (recovery_code, recovery_expires, email))
        conn.commit()
        
        cur.close()
        conn.close()
        
        # Generar enlace de recuperación
        recovery_link = f"http://localhost:5000/f-password?token={recovery_code}"
        
        # Enviar email con el enlace
        email_sent = send_recovery_email(email, recovery_link, user[1])
        
        if email_sent:
            return jsonify({
                "status": "success", 
                "message": f"Enlace de recuperación enviado a {email}"
            })
        else:
            return jsonify({
                "status": "error", 
                "message": "Error al enviar el email. Por favor, intenta nuevamente."
            })
        
    except Exception as e:
        print(f"Request password error: {e}")
        return jsonify({"status": "error", "message": "Error en el servidor. Por favor, intenta más tarde."})

# 📧 FUNCIÓN PARA ENVIAR EMAIL DE RECUPERACIÓN (ACTUALIZADA)
def send_recovery_email(to_email, recovery_link, user_name):
    """Envía un email con el enlace de recuperación de contraseña"""
    try:
        subject = "Restablece tu contraseña en MiBoletín.com"
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                * {{
                    margin: 0;
                    padding: 0;
                    box-sizing: border-box;
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                }}
                
                body {{
                    background: linear-gradient(135deg, #f0f7ff 0%, #e6f0ff 100%);
                    color: #333;
                    line-height: 1.6;
                    min-height: 100vh;
                    padding: 20px;
                }}
                
                .email-container {{
                    max-width: 600px;
                    margin: 0 auto;
                    background: #FFFFFF;
                    border-radius: 10px;
                    overflow: hidden;
                    box-shadow: 0 8px 25px rgba(0, 51, 102, 0.15);
                    border: 1px solid #CCCCCC;
                }}
                
                .email-header {{
                    background-color: #003366;
                    color: #FFFFFF;
                    padding: 30px 20px;
                    text-align: center;
                    box-shadow: 0 2px 15px rgba(0, 51, 102, 0.2);
                }}
                
                .email-header h1 {{
                    font-size: 1.8rem;
                    font-weight: 700;
                    letter-spacing: 0.5px;
                    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
                    margin: 0;
                }}
                
                .email-content {{
                    padding: 2.5rem;
                }}
                
                .greeting-section {{
                    text-align: center;
                    margin-bottom: 2rem;
                }}
                
                .greeting-section h2 {{
                    color: #003366;
                    font-size: 1.6rem;
                    margin-bottom: 0.5rem;
                }}
                
                .greeting-section p {{
                    color: #666;
                    font-size: 0.95rem;
                }}
                
                .user-greeting {{
                    color: #4A90E2;
                    font-weight: 600;
                    font-size: 1.1rem;
                    margin-bottom: 1rem;
                }}
                
                .request-info {{
                    background: #f8fafc;
                    padding: 1.5rem;
                    border-radius: 8px;
                    margin: 2rem 0;
                    border-left: 4px solid #4A90E2;
                }}
                
                .request-info p {{
                    color: #555;
                    margin-bottom: 1rem;
                }}
                
                .reset-section {{
                    background: rgba(74, 144, 226, 0.05);
                    border: 2px solid #e6f0ff;
                    border-radius: 8px;
                    padding: 2rem;
                    margin: 2rem 0;
                    text-align: center;
                }}
                
                .reset-section h3 {{
                    color: #003366;
                    margin-bottom: 1.5rem;
                    font-size: 1.2rem;
                }}
                
                .cta-button {{
                    text-align: center;
                    margin: 2rem 0;
                }}
                
                .button {{
                    display: inline-block;
                    background-color: #4A90E2;
                    color: #FFFFFF;
                    text-decoration: none;
                    padding: 16px 40px;
                    border-radius: 6px;
                    font-weight: 600;
                    font-size: 1rem;
                    border: none;
                    cursor: pointer;
                    transition: all 0.3s;
                    box-shadow: 0 4px 12px rgba(74, 144, 226, 0.3);
                    margin-bottom: 1.5rem;
                }}
                
                .button:hover {{
                    background-color: #003366;
                    transform: translateY(-2px);
                    box-shadow: 0 6px 16px rgba(0, 51, 102, 0.2);
                }}
                
                .link-alternative {{
                    background: #f8fafc;
                    padding: 1.25rem;
                    border-radius: 6px;
                    margin: 1.5rem 0;
                    word-break: break-all;
                    border: 1px solid #e9ecef;
                }}
                
                .link-alternative p {{
                    color: #666;
                    font-size: 0.9rem;
                    margin-bottom: 0.5rem;
                }}
                
                .link-display {{
                    font-family: monospace;
                    color: #003366;
                    background: white;
                    padding: 10px;
                    border-radius: 4px;
                    font-size: 0.85rem;
                    border: 1px solid #ddd;
                }}
                
                .warning-section {{
                    background-color: #fff8e1;
                    border-left: 4px solid #ffb900;
                    padding: 1.25rem;
                    margin: 2rem 0;
                    border-radius: 6px;
                }}
                
                .warning-section h4 {{
                    color: #333;
                    margin-bottom: 0.75rem;
                    display: flex;
                    align-items: center;
                    gap: 8px;
                }}
                
                .warning-section ul {{
                    list-style: none;
                    padding-left: 0;
                }}
                
                .warning-section li {{
                    margin-bottom: 0.5rem;
                    padding-left: 24px;
                    position: relative;
                    color: #333;
                }}
                
                .warning-section li:before {{
                    content: "⚠️";
                    position: absolute;
                    left: 0;
                }}
                
                .email-footer {{
                    background-color: #003366;
                    color: #FFFFFF;
                    padding: 2rem;
                    margin-top: 2rem;
                    text-align: center;
                }}
                
                .footer-content {{
                    max-width: 500px;
                    margin: 0 auto;
                }}
                
                .footer-logo {{
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    gap: 12px;
                    margin-bottom: 1.5rem;
                }}
                
                .footer-logo-text {{
                    color: #FFFFFF;
                    font-size: 1.4rem;
                    font-weight: 700;
                    letter-spacing: 0.5px;
                }}
                
                .security-info {{
                    background: rgba(0, 0, 0, 0.1);
                    padding: 1rem;
                    border-radius: 4px;
                    margin: 1.5rem 0;
                    font-size: 0.85rem;
                }}
                
                .footer-bottom {{
                    border-top: 1px solid rgba(255, 255, 255, 0.1);
                    padding-top: 1.5rem;
                    margin-top: 1.5rem;
                    color: #CCCCCC;
                    font-size: 0.85rem;
                }}
                
                @media (max-width: 600px) {{
                    .email-content {{
                        padding: 1.5rem;
                    }}
                    
                    .button {{
                        padding: 14px 28px;
                        width: 100%;
                    }}
                    
                    .reset-section {{
                        padding: 1.5rem;
                    }}
                }}
            </style>
        </head>
        <body>
            <div class="email-container">
                <div class="email-header">
                    <h1>MiBoletín.com</h1>
                </div>
                
                <div class="email-content">
                    <div class="greeting-section">
                        <div class="user-greeting">Hola {user_name},</div>
                        <h2>Restablecimiento de Contraseña 🔒</h2>
                        <p>Recibimos una solicitud para cambiar la contraseña de tu cuenta.</p>
                    </div>
                    
                    <div class="request-info">
                        <p><strong>📋 Detalles de la solicitud:</strong></p>
                        <p>• Solicitado desde: {datetime.now().strftime("%d/%m/%Y %H:%M")}</p>
                        <p>• Dirección IP: [Protegida por privacidad]</p>
                        <p>• Navegador: [Información no disponible]</p>
                    </div>
                    
                    <div class="reset-section">
                        <h3>Haz clic en el botón para restablecer tu contraseña:</h3>
                        
                        <div class="cta-button">
                            <a href="{recovery_link}" class="button">Restablecer Contraseña</a>
                        </div>
                        
                        <p style="color: #666; font-size: 0.9rem;">Este enlace expirará en 24 horas.</p>
                    </div>
                    
                    <div class="link-alternative">
                        <p><strong>O copia y pega este enlace en tu navegador:</strong></p>
                        <div class="link-display">{recovery_link}</div>
                    </div>
                    
                    <div class="warning-section">
                        <h4>⚠️ Importante - Seguridad de tu cuenta:</h4>
                        <ul>
                            <li>Si NO solicitaste este cambio, ignora este email</li>
                            <li>Nunca compartas tu enlace de recuperación</li>
                            <li>El enlace solo es válido por 24 horas</li>
                            <li>Después de restablecer, inicia sesión para verificar</li>
                        </ul>
                    </div>
                    
                    <div style="text-align: center; margin-top: 2rem;">
                        <p style="color: #666; font-size: 0.9rem;">
                            ¿Problemas con el botón? Copia el enlace manualmente o 
                            <a href="#" style="color: #4A90E2; text-decoration: none;">contacta con soporte</a>
                        </p>
                    </div>
                </div>
                
                <div class="email-footer">
                    <div class="footer-content">
                        <div class="footer-logo">
                            <div class="footer-logo-text">MiBoletín.com</div>
                        </div>
                        
                        <p style="color: #CCCCCC; margin-bottom: 1.5rem;">
                            Tu seguridad es nuestra prioridad. Protegemos siempre tus datos.
                        </p>
                        
                        <div class="security-info">
                            <p><strong>🔒 Medidas de seguridad:</strong></p>
                            <p style="font-size: 0.8rem; margin-top: 0.5rem;">
                                Este email fue enviado automáticamente como medida de seguridad. 
                                Ningún miembro de nuestro equipo te pedirá nunca tu contraseña.
                            </p>
                        </div>
                        
                        <div class="footer-bottom">
                            <p>© {datetime.now().year} MiBoletín.com. Todos los derechos reservados.</p>
                            <p>Este es un email automático, por favor no respondas a este mensaje.</p>
                            <p>
                                <a href="#" style="color: #4A90E2; text-decoration: none;">Centro de Ayuda</a> | 
                                <a href="#" style="color: #4A90E2; text-decoration: none;">Política de Privacidad</a>
                            </p>
                        </div>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """
        
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = EMAIL_FROM
        msg['To'] = to_email
        
        msg.attach(MIMEText(html_content, 'html'))
        
        server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()
        
        print(f"Email de recuperación enviado exitosamente a {to_email}")
        return True
        
    except Exception as e:
        print(f"Error enviando email de recuperación a {to_email}: {str(e)}")
        return False

# 📌 RUTA PARA F-PASSWORD CON TOKEN DE VERIFICACIÓN
@app.route("/f-password")
def forgot_password_with_token():
    token = request.args.get('token')
    
    if not token:
        return redirect(url_for('request_password'))
    
    # Verificar si el token es válido
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        query = """
            SELECT id_admin, recovery_token_expires 
            FROM administradores 
            WHERE recovery_token = %s
        """
        cur.execute(query, (token,))
        result = cur.fetchone()
        
        cur.close()
        conn.close()
        
        if result:
            user_id, expires = result
            if datetime.now() <= expires:
                # Token válido, mostrar página para restablecer contraseña
                return render_template("f-password.html", token=token)
        
        # Token inválido o expirado
        return render_template("r-password.html", error="El enlace de recuperación es inválido o ha expirado.")
        
    except Exception as e:
        print(f"Token verification error: {e}")
        return render_template("r-password.html", error="Error al verificar el enlace de recuperación.")

# 📌 RUTA PARA ACTUALIZAR CONTRASEÑA (POST)
@app.route("/reset-password", methods=["POST"])
def reset_password():
    data = request.get_json()
    
    token = data.get("token")
    new_password = data.get("new_password")
    confirm_password = data.get("confirm_password")
    
    if not all([token, new_password, confirm_password]):
        return jsonify({"status": "error", "message": "Todos los campos son requeridos."})
    
    if new_password != confirm_password:
        return jsonify({"status": "error", "message": "Las contraseñas no coinciden."})
    
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Verificar token y expiración
        query = """
            SELECT id_admin, recovery_token_expires 
            FROM administradores 
            WHERE recovery_token = %s
        """
        cur.execute(query, (token,))
        result = cur.fetchone()
        
        if not result:
            return jsonify({"status": "error", "message": "Token de recuperación inválido."})
        
        user_id, expires = result
        if datetime.now() > expires:
            return jsonify({"status": "error", "message": "El token de recuperación ha expirado."})
        
        # Hash de la nueva contraseña
        hashed_password = bcrypt.hashpw(new_password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        
        # Actualizar contraseña y limpiar token
        update_query = """
            UPDATE administradores 
            SET contrasena = %s,
                recovery_token = NULL,
                recovery_token_expires = NULL
            WHERE id_admin = %s
        """
        cur.execute(update_query, (hashed_password, user_id))
        conn.commit()
        
        cur.close()
        conn.close()
        
        return jsonify({
            "status": "success", 
            "message": "Contraseña restablecida exitosamente!",
            "redirect": "/login"
        })
        
    except Exception as e:
        print(f"Reset password error: {e}")
        return jsonify({"status": "error", "message": "Error al restablecer la contraseña."})

if __name__ == "__main__":
    app.run(debug=True)