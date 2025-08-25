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
