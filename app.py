import fitz  # PyMuPDF
from flask import Flask, request, send_file
import io

app = Flask(__name__)

# Simulación de asignación (luego lo conectamos a Excel)
asignaciones = {
    "2023001": [9, 10],
    "2023002": [11, 12]
}

@app.route('/')
def home():
    return "Servidor activo"

@app.route('/ver_pdf')
def ver_pdf():
    matricula = request.args.get('matricula')

    if matricula not in asignaciones:
        return "Matrícula no válida", 403

    doc = fitz.open("documento.pdf")
    nuevo_pdf = fitz.open()

    for p in asignaciones[matricula]:
        nuevo_pdf.insert_pdf(doc, from_page=p, to_page=p)

    buffer = io.BytesIO()
    nuevo_pdf.save(buffer)
    buffer.seek(0)

    return send_file(buffer, mimetype='application/pdf')

if __name__ == '__main__':
    app.run()