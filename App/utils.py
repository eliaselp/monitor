import uuid    
import qrcode
from io import BytesIO
import base64
import json


def get_tocken():
    # Generar una cadena larga con uuid.uuid4()
    cadena_larga = str(uuid.uuid4())
    # Extraer la primera subsecuencia antes del primer signo '-'
    subsecuencia = cadena_larga.split('-')[0]
    print(subsecuencia)
    return subsecuencia


def generate_qr_code(url):
    qr = qrcode.make(url)
    buffer = BytesIO()
    qr.save(buffer)
    buffer.seek(0)
    img_str = base64.b64encode(buffer.getvalue()).decode('utf-8')
    return img_str




# Método para cifrar en base64
def cifrar_base64(texto):
    texto_bytes = texto.encode('utf-8')
    base64_bytes = base64.b64encode(texto_bytes)
    base64_texto = base64_bytes.decode('utf-8')
    return base64_texto

# Método para descifrar desde base64
def descifrar_base64(base64_texto):
    base64_bytes = base64_texto.encode('utf-8')
    texto_bytes = base64.b64decode(base64_bytes)
    texto = texto_bytes.decode('utf-8')
    return texto



def descifrar_base64_a_dict(base64_str):
    try:
        # Decodificar la cadena base64
        json_str = base64.b64decode(base64_str).decode('utf-8')
        # Convertir la cadena JSON a un diccionario
        data_dict = json.loads(json_str)
        return data_dict
    except Exception as e:
        return None
