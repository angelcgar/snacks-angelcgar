# Utilidades comunes para la aplicación

def format_platforms(platforms_list):
    """Formatea la lista de plataformas para salida"""
    return " ".join(platforms_list) if platforms_list else ""

def validate_text_length(text, max_length=280):
    """Valida la longitud del texto"""
    if len(text) > max_length:
        raise ValueError(f"El texto excede los {max_length} caracteres")
    return True
