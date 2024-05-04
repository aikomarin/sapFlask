from flask import Flask, render_template, request, url_for
from flask_migrate import Migrate
from werkzeug.utils import redirect

from database import db
from forms import PersonaForm
from models import Persona

app = Flask(__name__)

# Configuración de la DB
USER_DB = 'postgres'
PASS_DB = 'admin'
URL_DB = 'localhost'
NAME_DB = 'sapersonas_flask_db'
FULL_URL_DB = f'postgresql://{USER_DB}:{PASS_DB}@{URL_DB}/{NAME_DB}'

app.config['SQLALCHEMY_DATABASE_URI'] = FULL_URL_DB
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Configurar flask-migrate
migrate = Migrate()
migrate.init_app(app, db)

# Configurar flask-wtf
app.config['SECRET_KEY'] = 'llave_secreta'


@app.route('/')  # Procesar múltiples rutas
@app.route('/index')  # Procesar múltiples rutas
@app.route('/index.html')  # Procesar múltiples rutas
def inicio():
    # personas = Persona.query.all()
    personas = Persona.query.order_by('id')
    total_personas = Persona.query.count()
    app.logger.debug(f'Listado Personas: {personas}')
    app.logger.debug(f'Total Personas: {total_personas}')
    return render_template('index.html', personas=personas, total_personas=total_personas)


@app.route('/ver/<int:id>')
def ver_detalle(id):
    persona = Persona.query.get_or_404(id)
    app.logger.debug(f'Ver persona: {persona}')
    return render_template('detalle.html', persona=persona)


@app.route('/agregar', methods=['GET', 'POST'])
def agregar():
    persona = Persona()
    persona_form = PersonaForm(obj=persona)
    if request.method == 'POST':
        if persona_form.validate_on_submit():  # Validar información del formulario
            persona_form.populate_obj(persona)  # Se llenen los datos del objeto persona
            app.logger.debug(f'Persona a insertar: {persona}')
            db.session.add(persona)  # Insertar registro en DB
            db.session.commit()  # Guardar registro en DB
            return redirect(url_for('inicio'))
    return render_template('agregar.html', persona_form=persona_form)


@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    persona = Persona.query.get_or_404(id)
    persona_form = PersonaForm(obj=persona)
    if request.method == 'POST':
        if persona_form.validate_on_submit():
            persona_form.populate_obj(persona)
            app.logger.debug(f'Persona a actualizar: {persona}')
            db.session.commit()
            return redirect(url_for('inicio'))
    return render_template('editar.html', persona_form=persona_form)


@app.route('/eliminar/<int:id>')
def eliminar(id):
    persona = Persona.query.get_or_404(id)
    app.logger.debug(f'Persona a eliminar: {persona}')
    db.session.delete(persona)
    db.session.commit()
    return redirect(url_for('inicio'))
