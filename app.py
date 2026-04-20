import fitz  # PyMuPDF
from flask import Flask, request, send_file
import pandas as pd
import io

app = Flask(__name__)

# Cargar archivo Excel
df = pd.read_excel("asignaciones.xlsx")

def obtener_paginas(matricula):
    # Buscar la matrícula en el Excel
    fila = df[df['matricula'].astype(str) == str(matricula)]

    if fila.empty:
        return None

    # Obtener rango de páginas (ej: "10-11")
    paginas_str = str(fila.iloc[0]['paginas'])
    
    try:
        inicio, fin = map(int, paginas_str.split('-'))
    except:
        return None

    # Ajustar índice (PDF empieza en 0)
    return list(range(inicio - 1, fin))


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/ver_pdf')
def ver_pdf():
    matricula = request.args.get('matricula')

    if not matricula:
        return "Debe proporcionar una matrícula", 400

    paginas = obtener_paginas(matricula)

    if paginas is None:
        return "Matrícula no válida", 403

    try:
        doc = fitz.open("documento.pdf")
    except:
        return "Error al abrir el documento PDF", 500

    nuevo_pdf = fitz.open()

    try:
        for p in paginas:
            if p < len(doc):
                nuevo_pdf.insert_pdf(doc, from_page=p, to_page=p)
            else:
                return "Número de página fuera de rango", 400

        buffer = io.BytesIO()
        nuevo_pdf.save(buffer)
        buffer.seek(0)

        return send_file(buffer, mimetype='application/pdf')

    except Exception as e:
        return f"Error procesando el PDF: {str(e)}", 500

from flask import Flask, request, send_file, render_template


if __name__ == '__main__':
    app.run()