import os
import json
from llamaapi import LlamaAPI
from langchain_community.llms.ollama import Ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.document_loaders import WebBaseLoader

import re
from langchain_community.embeddings import OllamaEmbeddings
import json
import os
from langchain_core.output_parsers import StrOutputParser


from langchain.prompts import PromptTemplate

# from repository.models import Entrys


# def process_json_project_data(data):
#     """
#     Esta función analiza la estructura del proyecto, las rutas en un JSON y usa LangChain para generar documentación.

#     Args:
#         data: El JSON que contiene la información del proyecto.

#     Returns:
#         None.
#     """

#     # Análisis de la estructura del proyecto
#     file_paths = data.get('file_paths')

#     project_structure = []  # Lista para almacenar información resumida de la estructura

#     for filename, filepath in file_paths.items():
#         # Obtener información del archivo
#         file_info = {
#             "nombre": filename,
#             "ruta": filepath,
#             "extension": os.path.splitext(filename)[1],
#             "directorio": os.path.dirname(filepath),
#         }
#         project_structure.append(file_info)  # Agregar a la descripción del proyecto

#         # Puedes agregar más procesamiento/análisis de cada archivo aquí si es necesario

#     # Uso de LangChain
#     summary_template = """
#     **Resumen del proyecto**

#     **Estructura:**

#     {project_structure} 

#     **Objetivo:** Crear una documentación profesional del proyecto.
#     """

#     summary_prompt_template = PromptTemplate(
#         input_variables=["project_structure"], template=summary_template)

#     llm = Ollama(model="llama2")
#     chain = summary_prompt_template | llm

#     res = chain.invoke(input={"project_structure": project_structure})
#     print(res)




def process_file_info(file_info_json):
    """
    Esta función procesa la información de un archivo.

    Args:
        file_info_json: Un JSON que contiene la información del archivo.

    Returns:
        List: A list containing all the responses generated during processing.
    """
    # Limpiar la cadena JSON de caracteres de control no válidos
    file_info = clean_invalid_control_characters(file_info_json)

    responses = []  # List to store all the responses

    try:
        # Cargar el JSON limpiado
        file_info = json.loads(file_info)
    except json.JSONDecodeError as e:
        print(f"Error al cargar el JSON: {e}")
        return responses
    
    # Obtener la información del archivo
    file_paths = file_info.get("file_paths", {})
    file_contents = file_info.get("file_contents", {})
    processed_files = []

    # Procesar cada archivo en file_paths
    for filename, filepath in file_paths.items():
        extension = filename.split(".")[-1] 
        if filename == "list_files_and_content_cli.py":
            continue
        
        # Clasificar el archivo por tipo
        if extension == 'py':
            file_type = "code"
        elif extension == 'md':
            file_type = "docs"
        else:
            file_type = "other"

        if file_type == "docs":
            # Obtener el contenido del archivo si está disponible
            content = file_contents.get(filename)
            if content:
                # Generar un prompt para la documentación
                prompt_template = PromptTemplate(
                    input_variables=["document_content"],
                    template="Given the document content:\n{document_content}\nGenerate a documentation for the document like a documentation generator. in formal language. like a tecnical writer."
                )
                
                # Ejecutar el prompt utilizando LangChain
                llm = Ollama(model="llama2")
                chain = prompt_template | llm
                res = chain.invoke(input={"document_content": content})
                
                # Append the response to the list
                responses.append(('docs', res))
        
        elif file_type == "other":
            # Almacenar la información del archivo en una base de datos u otra acción
            pass
        
        elif file_type == "code":
            # Obtener el contenido del archivo si está disponible
            content = file_contents.get(filename)
            if content:
                # Analizar el contenido del archivo
                # (Aquí puedes realizar cualquier procesamiento adicional que necesites)
                pass

            # Agregar el archivo a la lista de archivos procesados como código
            processed_files.append(filename)

            # Si ya hemos procesado los primeros dos archivos como código, ahora podemos explicar los componentes del proyecto
            if len(processed_files) >= 1:
                # Generar un prompt para explicar los componentes del proyecto
                prompt_template = PromptTemplate(
                    input_variables=["project_components"], 
                    template="Given the project components:\n{project_components}\nExplain the main components of the project for the documentation. act like a documentation generator and explain the project structure and components."
                )
                
                # Ejecutar el prompt utilizando LangChain
                llm = Ollama(model="llama2")
                chain = prompt_template | llm
                res = chain.invoke(input={"project_components": processed_files})
                
                # Append the response to the list
                responses.append(('code', res))

    return responses

                
def clean_invalid_control_characters(json_str):
    # Expresión regular para encontrar caracteres de control no válidos
    control_chars = ''.join(map(chr, range(0,32)))  # Caracteres ASCII de control
    control_char_pattern = f'[{re.escape(control_chars)}]'
    
    # Reemplazar los caracteres de control no válidos con espacios en blanco
    cleaned_json = re.sub(control_char_pattern, ' ', json_str)
    
    return cleaned_json

