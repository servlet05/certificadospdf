from flask import Flask, render_template, request, send_file
from weasyprint import HTML
import os
from datetime import datetime

app = Flask(__name__)

# Plantillas disponibles
PLANTILLAS = {
    'moderna': 'moderna.html',
    'clasica': 'clasica.html',
    'minimalista': 'minimalista.html'
}

@app.route('/')
def index():
    return render_template('index.html', plantillas=PLANTILLAS.keys())

@app.route('/generar', methods=['POST'])
def generar():
    # 1. Recibir datos del formulario
    nombre = request.form['nombre']
    curso = request.form['curso']
    fecha = request.form.get('fecha', datetime.now().strftime('%d/%m/%Y'))
    plantilla_id = request.form['plantilla']
    
    # 2. Renderizar HTML con los datos
    html_string = render_template(
        PLANTILLAS[plantilla_id],
        nombre=nombre,
        curso=curso,
        fecha=fecha,
        folio=f"CONST-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    )
    
    # 3. Convertir HTML a PDF (MAGIA!)
    pdf = HTML(string=html_string).write_pdf()
    
    # 4. Enviar PDF al usuario
    return send_file(
        io.BytesIO(pdf),
        download_name=f'constancia_{nombre.replace(" ", "_")}.pdf',
        as_attachment=True,
        mimetype='application/pdf'
    )

if __name__ == '__main__':
    import io  # Necesario para BytesIO
    app.run(debug=True)
