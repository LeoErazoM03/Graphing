import os


def convert_python_to_markdown(directory):
    # Itera sobre los archivos en la carpeta especificada
    for filename in os.listdir(directory):
        # Verifica si el archivo tiene la extensión .py
        if filename.endswith(".py"):
            # Lee el contenido del archivo .py con codificación utf-8
            with open(os.path.join(directory, filename), 'r', encoding="utf-8") as py_file:
                code_lines = py_file.readlines()

            # Formatea el contenido en Markdown
            md_content = "```python\n" + "".join(code_lines) + "\n```"

            # Define el nombre del archivo .md
            md_filename = filename.replace(".py", ".md")
            # Escribe el contenido en un archivo .md con codificación utf-8
            with open(os.path.join(directory, md_filename), 'w', encoding="utf-8") as md_file:
                md_file.write(md_content)

            # Imprime un mensaje de confirmación
            print(f"Convertido: {filename} a {md_filename}")


# Reemplaza la ruta con la ubicación de tus archivos Python
convert_python_to_markdown(
    r"C:\Users\leoda\OneDrive - Instituto Tecnológico de Morelia\Universidad\6to Semestre\Graficación\ProyectoGraficación\ProyectoGraficacion")
