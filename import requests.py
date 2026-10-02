import requests
import json

def dish_fetch(identifier):
    """
    Obtiene los platos típicos desde la API.
    Acepta tanto un ID (entero o string numérico) como un Nombre (string).
    """
    url = "https://api-colombia.com/api/v1/TypicalDish"
    try:
        response = requests.get(url)
        response.raise_for_status()
        dishes = response.json()
        
        # 1. Si el identificador es un número (int o string digito), busca por ID
        if isinstance(identifier, int) or (isinstance(identifier, str) and identifier.isdigit()):
            target_id = int(identifier)
            for dish in dishes:
                if dish.get("id") == target_id:
                    return dish
                    
        # 2. Si el identificador es un texto (nombre), busca por coincidencia en el nombre
        elif isinstance(identifier, str):
            query_name = identifier.strip().lower()
            for dish in dishes:
                dish_name = dish.get("name", "").lower()
                # Coincidencia exacta o parcial
                if query_name in dish_name:
                    return dish

        return None

    except requests.exceptions.RequestException as e:
        return None

def main():
    """
    Herramienta de línea de comandos (CLI) que acepta número o nombre.
    """
    print("=== Consulta de Platos Típicos de Colombia ===")
    
    # 1) Acepta entradas (ID o Nombre)
    user_input = input("Ingresa el ID o el Nombre del plato típico que deseas buscar (ej. '5' o 'Bandeja Paisa'): ").strip()
    
    if not user_input:
        print("Error: Debes ingresar un nombre o un ID.")
        return

    # 3) Conexión a la API y 4) Procesamiento del objeto JSON
    dish = dish_fetch(user_input)
    
    # 2) Muestra la salida
    if dish and isinstance(dish, dict) and "name" in dish:
        print("\n--- ¡Plato Encontrado! ---")
        print(f"ID: {dish.get('id')}")
        print(f"Nombre: {dish.get('name')}")
        if "description" in dish and dish["description"]:
            print(f"Descripción: {dish.get('description')}")
    else:
        print(f"\nNo se encontró ningún plato típico que coincida con '{user_input}'.")

if __name__ == "__main__":
    main()