cat > app.py << 'EOF'
from flask import Flask, render_template, request, send_file
from weasyprint import HTML
from datetime import datetime
import io

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generar', methods=['POST'])
def generar():
    nombre = request.form['nombre']
    curso = request.form['curso']
    fecha = request.form.get('fecha', datetime.now().strftime('%d/%m/%Y'))
    
    html_string = render_template(
        'moderna.html',
        nombre=nombre,
        curso=curso,
        fecha=fecha,
        folio=f"CONST-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    )
    
    pdf = HTML(string=html_string).write_pdf()
    
    return send_file(
        io.BytesIO(pdf),
        download_name=f'constancia_{nombre.replace(" ", "_")}.pdf',
        as_attachment=True,
        mimetype='application/pdf'
    )

if __name__ == '__main__':
    app.run(debug=True)
EOF
