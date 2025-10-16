import base64
from flask import jsonify, request
from __init__ import APP
import src.process as process
import src.verify as verify


@APP.route("/", methods = ["GET"])
def main():
    return "hello", 200

@APP.route("/procesar_pdf", methods=["POST"])
def procesar():
    data = request.json
    pdf_b64 = data.get("pdf_b64")

    if not pdf_b64:
        return jsonify({"error": "No se recibió PDF en base64"}), 400

    try:
        pdf_bytes = base64.b64decode(pdf_b64)
        resultado = process.procesar_pdf(pdf_bytes)
        return jsonify(resultado)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
     
@APP.route("/verificar_pdf", methods=["POST"])
def verificar():
    data = request.json
    pdf_b64 = data.get("pdf_b64")

    if not pdf_b64:
        return jsonify({"error": "No se recibió PDF en base64"}), 400

    try:
        pdf_bytes = base64.b64decode(pdf_b64)
        resultado = verify.verificar_pdf(pdf_bytes)
        return jsonify(resultado)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    APP.run(debug=True, host="0.0.0.0")