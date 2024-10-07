import re
import phonenumbers
from phonenumbers import NumberParseException

class Verificador:
    @staticmethod
    def mayuscula_minuscula_espacio(texto):
        # La expresión regular permite letras mayúsculas, minúsculas y espacios
        patron = re.compile(r'^[A-Za-zÁÉÍÓÚÑáéíóúñ ]+$')
        return bool(patron.match(texto))
    

    @staticmethod
    def mayuscula_minuscula_numeros(texto):
        # La expresión regular permite letras mayúsculas, minúsculas, espacios, números y el carácter '_'
        patron = re.compile(r'^[A-Za-zÁÉÍÓÚÑáéíóúñ0-9_]+$')
        return bool(patron.match(texto))

    @staticmethod
    def validar_correo(correo):
        # La expresión regular para validar correos electrónicos
        patron = re.compile(
            r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        )
        return bool(patron.match(correo))
    

    @staticmethod
    def validar_numero_telefono(numero):
        try:
            parsed_number = phonenumbers.parse(numero)
            return phonenumbers.is_valid_number(parsed_number)
        except NumberParseException:
            return False
        

    @staticmethod
    def validar_password(contrasena, confirmar_contrasena):
        if contrasena != confirmar_contrasena:
            return "Las contraseñas no coinciden"
        # La contraseña debe tener al menos 8 caracteres
        if len(contrasena) < 8:
            return "La contraseña debe tener 8 caracteres o más"
        if not re.search(r'[A-Z]', contrasena) or not re.search(r'[a-z]', contrasena) or not re.search(r'[0-9]', contrasena) or not re.search(r'[\W_]', contrasena):
            return "La contraseña debe contener al menos una letra mayúscula, una letra minúscula, un número y un carácter especial"
        
        return "OK"
    
    
    