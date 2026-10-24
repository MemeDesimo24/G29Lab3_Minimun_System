import os

def get_file(filename: str) -> str:
    # Calcola il percorso assoluto partendo dalla cartella in cui si trova resources.py
    base_dir = os.path.dirname(os.path.abspath(__file__))
    # Modifica "assets" o "data" in base alla cartella in cui hai salvato i JSON
    file_path = os.path.join(base_dir,"src","g29lab3_minimum_system", "assets", "Data", filename)
    return file_path