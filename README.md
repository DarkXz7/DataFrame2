# 📊 Proyecto Django: Carga y Procesamiento de Archivos Excel/CSV

Este proyecto permite a los usuarios **subir archivos Excel o CSV**, procesarlos automáticamente y visualizar una **vista previa limpia de los datos** antes de guardarlos.  
Es ideal para trabajar con **tablas financieras de interés compuesto**, especialmente aquellas que incluyen **celdas fusionadas o formatos complejos**.

---

## 🚀 Estructura del Proyecto

- **`models.py`** → Define el modelo `ArchivoCargado` para registrar metadatos de los archivos subidos.  
- **`views.py`** → Contiene la lógica para subir, limpiar, previsualizar y guardar archivos.  
- **`archivos/templates/archivos/`** → Plantillas HTML para carga, vista previa y confirmación de guardado.  
- **`uploads/`** → Carpeta donde se almacenan los archivos procesados localmente.  

---

## ⚙️ Funcionamiento

### 1. Subida de archivo
El usuario selecciona un archivo **Excel (.xlsx) o CSV** y lo carga mediante un formulario web.

### 2. Procesamiento y limpieza
El sistema:
- Lee el archivo y detecta los **encabezados y columnas relevantes**.  
- Propaga valores de **celdas fusionadas** (por ejemplo, semestres).  
- Elimina filas **vacías o irrelevantes**.  
- Muestra solo la **primera aparición de cada grupo** (ejemplo: solo la primera fila de cada semestre incluye el número de semestre).  
- Genera una **vista previa limpia y ordenada**.  

### 3. Vista previa y confirmación
El usuario revisa la tabla procesada y decide si desea guardar el archivo.

### 4. Guardado local y registro
Al confirmar:
- El archivo procesado se guarda en la carpeta **`uploads/`**.  
- Se registra en la **base de datos** con su información principal.  

---

## 🖥️ ¿Cómo usarlo?

1. Clona el repositorio y navega al directorio del proyecto:  
   ```bash
   git clone <url-del-repositorio>
   cd <nombre-del-proyecto>

2. Instala las dependencias:
   	pip install -r requirements.txt
   
3. Ejecuta las migraciones de la base de datos
	python manage.py migrate

3. Inicia el servidor de desarrollo:
	python manage.py runserver

4. Accede en tu navegador a:
	http://localhost:8000/subir/




💡 Características destacadas

✅ Soporte para archivos Excel y CSV.
✅ Limpieza automática de filas vacías y propagación de celdas fusionadas.
✅ Vista previa antes de guardar.
✅ Guardado local y en base de datos.
✅ Interfaz web amigable con mensajes claros para el usuario.


📂 Ejemplo de uso
🔹 Subida del archivo

El usuario selecciona un archivo .xlsx o .csv desde el formulario de carga:
[Seleccionar archivo]  [Subir]



🔹 Vista previa procesada

Una vez cargado, se muestra una tabla limpia y ordenada con los datos listos para revisar:

Semestre	Capital Inicial	Interés 		(%)	Capital Final
1			1,000,000						5%	1,050,000
			1,050,000						5%	1,102,500
2			1,102,500						5%	1,157,625
			1,157,625						5%	1,215,506


🔹 Confirmación

El usuario hace clic en "Guardar" para almacenar el archivo procesado.
El sistema guarda:

📁 Una copia del archivo en la carpeta uploads/.

🗂️ Un registro en la base de datos con información básica (nombre, fecha de carga, etc.).



📌 Notas

Este proyecto está diseñado como base o plantilla, adaptable fácilmente a otros casos de procesamiento de datos.
Compatible con Django 4.x o superior.
Requiere pandas y openpyxl para manejar archivos Excel.


⚙️ Requerimientos principales
En el archivo requirements.txt encontrarás las dependencias necesarias. Ejemplo:

Django>=4.0 

pandas

openpyxl
