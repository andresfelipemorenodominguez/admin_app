from flask import Flask, render_template

app = Flask(__name__)

# Ruta principal que renderiza loginuser.html
@app.route('/')
def index():
    return render_template('loginuser.html')

# Ruta para loginuser (mismo que la principal)
@app.route('/loginuser')
def loginuser():
    return render_template('loginuser.html')

# Ruta para forgot_password (simplemente para evitar error 404)
@app.route('/forgot_password')
def forgot_password():
    return render_template('f-password.html')

if __name__ == '__main__':
    app.run(debug=True)