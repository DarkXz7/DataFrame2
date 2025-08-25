from django.shortcuts import render, redirect
from .forms import SubidaArchivoForm
from .models import ArchivoCargado
import pandas as pd
from django.http import JsonResponse
import os
from django.conf import settings
from django.contrib import messages

def subir_archivo(request):
    if request.method == 'POST':
        form = SubidaArchivoForm(request.POST, request.FILES)
        if form.is_valid():
            archivo = request.FILES['archivo']
            nombre = archivo.name

            # Detectar tipo
            if nombre.endswith('.xlsx'):
                try:
                    # Primero, leer todo el archivo para debug
                    df_completo = pd.read_excel(archivo)
                    print("Archivo completo:")
                    print(df_completo.head(10))
                    
                    # Ahora leer con los parámetros específicos
                    df = pd.read_excel(archivo, header=4)
                    
                    # Mantener solo las primeras 5 columnas
                    df = df.iloc[:, :5]
                    
                    # PROPAGAR VALORES DE CELDAS FUSIONADAS ANTES DE LIMPIAR
                    # Esto llena hacia abajo los valores de celdas fusionadas
                    df = df.fillna(method='ffill')
                    
                    # LIMPIAR FILAS VACÍAS - Múltiples métodos
                    
                    # 1. Eliminar filas completamente vacías (NaN en todas las columnas)
                    df = df.dropna(how='all')
                    
                    # 2. Eliminar filas donde todas las columnas son 0 o vacías
                    df = df[~((df == 0) | (df.isna()) | (df == '')).all(axis=1)]
                    
                    # 3. Eliminar filas donde las columnas principales están vacías
                    # (por ejemplo, si MES está vacío, probablemente la fila está vacía)
                    df = df[df.iloc[:, 1].notna()]  # Segunda columna (MES) no debe estar vacía
                    
                    # 4. Resetear el índice después de eliminar filas
                    df = df.reset_index(drop=True)
                    
                    # 5. Reemplazar NaN restantes con valores apropiados
                    df = df.fillna(0)
                    
                    # Renombrar columnas
                    df.columns = ['SEMESTRE', 'MES', 'CAPITAL INICIAL', '% INTERES', 'INTERES MES A MES']
                    
                    # LIMPIAR LA COLUMNA SEMESTRE - manejar celdas fusionadas correctamente
                    # En lugar de eliminar duplicados, mantener el valor propagado
                    # Solo limpiar los 0.0 que no deberían estar ahí
                    # LIMPIAR LA COLUMNA SEMESTRE - mostrar solo primera aparición
                    
                    
                    
                    # LIMPIAR LA COLUMNA SEMESTRE - mostrar solo primera aparición
                    # Crear una máscara para identificar cambios de grupo
                    
                    # Renombrar columnas
                    df.columns = ['SEMESTRE', 'MES', 'CAPITAL INICIAL', '% INTERES', 'INTERES MES A MES']
                    
                    # OPCIÓN 1: Mostrar solo la primera fila de cada semestre
                    df = df.drop_duplicates(subset=['SEMESTRE'], keep='first')
                    
                    # Limpiar cualquier 0.0 restante
                    df['SEMESTRE'] = df['SEMESTRE'].replace(0.0, '')
                    
                    # Si se quiere mostrar el semestre solo en la primera fila de cada grupo
                    # df['SEMESTRE'] = df['SEMESTRE'].where(df['SEMESTRE'] != df['SEMESTRE'].shift(), '')
                    
                    tipo = "Excel"
                except Exception as e:
                    messages.error(request, f"Error al leer Excel: {str(e)}")
                    return render(request, "archivos/subir.html", {"form": form})
                    
            elif nombre.endswith('.csv'):
                try:
                    df = pd.read_csv(archivo)
                    
                    # Para CSV también aplicar propagación hacia abajo si es necesario
                    df = df.fillna(method='ffill')
                    
                    # LIMPIAR FILAS VACÍAS PARA CSV
                    # 1. Eliminar filas completamente vacías
                    df = df.dropna(how='all')
                    
                    # 2. Eliminar filas donde todas las columnas son vacías o solo espacios
                    df = df[~df.astype(str).apply(lambda x: x.str.strip()).eq('').all(axis=1)]
                    
                    # 3. Resetear índice
                    df = df.reset_index(drop=True)
                    
                    # 4. Reemplazar valores restantes
                    df = df.fillna('')
                    
                    tipo = "CSV"
                except Exception as e:
                    messages.error(request, f"Error al leer CSV: {str(e)}")
                    return render(request, "archivos/subir.html", {"form": form})
            else:
                messages.error(request, "Formato no soportado. Solo se permiten archivos .xlsx y .csv")
                return render(request, "archivos/subir.html", {"form": form})

            # Verificar que el DataFrame no esté vacío después de la limpieza
            if df.empty:
                messages.error(request, "El archivo no contiene datos válidos o todas las filas estaban vacías")
                return render(request, "archivos/subir.html", {"form": form})

            # Mostrar información de limpieza
            print(f"Filas después de limpieza: {len(df)}")
            
            # Guardar temporalmente los datos en la sesión para el guardado posterior
            request.session['archivo_temporal'] = {
                'nombre': nombre,
                'tipo': tipo,
                'df_html': df.to_html(classes='table table-striped'),
                'columnas': ", ".join(df.columns),
                'filas': len(df)
            }

            # También guardamos el archivo temporalmente
            request.session['archivo_datos'] = df.to_dict('records')

            return render(request, "archivos/vista_previa.html", {
                "nombre": nombre, 
                "df": df.to_html(classes='table table-striped'),
                "filas": len(df),
                "columnas": len(df.columns)
            })
        else:
            # Si el formulario no es válido, mostrar errores
            messages.error(request, "Por favor, selecciona un archivo válido")
            return render(request, "archivos/subir.html", {"form": form})

    else:
        form = SubidaArchivoForm()

    return render(request, "archivos/subir.html", {"form": form})

def guardar_archivo(request):
    if request.method == 'POST':
        # Recuperar datos de la sesión
        archivo_temp = request.session.get('archivo_temporal')
        archivo_datos = request.session.get('archivo_datos')
        
        if not archivo_temp or not archivo_datos:
            messages.error(request, "No hay archivo para guardar. Por favor, sube un archivo primero.")
            return redirect('subir_archivo')
        
        try:
            # Recrear DataFrame
            df = pd.DataFrame(archivo_datos)
            nombre = archivo_temp['nombre']
            tipo = archivo_temp['tipo']
            
            # GUARDAR ARCHIVO LOCALMENTE
            uploads_dir = os.path.join(os.getcwd(), 'uploads')
            if not os.path.exists(uploads_dir):
                os.makedirs(uploads_dir)
            
            # Guardar el DataFrame procesado
            if tipo == "Excel":
                archivo_procesado = os.path.join(uploads_dir, f'procesado_{nombre}')
                df.to_excel(archivo_procesado, index=False)
            else:  # CSV
                archivo_procesado = os.path.join(uploads_dir, f'procesado_{nombre}')
                df.to_csv(archivo_procesado, index=False)
            
            print(f"Archivo procesado guardado en: {archivo_procesado}")
            
            # Guardar metadata en BD
            ArchivoCargado.objects.create(
                nombre=nombre,
                tipo=tipo,
                columnas=archivo_temp['columnas'],
                filas=archivo_temp['filas']
            )
            
            # Limpiar sesión
            del request.session['archivo_temporal']
            del request.session['archivo_datos']
            
            # Mensaje de éxito
            messages.success(request, f"¡Archivo '{nombre}' guardado exitosamente! Se procesaron {archivo_temp['filas']} filas.")
                
            return render(request, "archivos/exito.html", {
                "nombre": nombre, 
                "mensaje": "Archivo guardado exitosamente"
            })
            
        except Exception as e:
            messages.error(request, f"Error al guardar el archivo: {str(e)}")
            return redirect('subir_archivo')
    
    messages.error(request, "Método no permitido")
    return redirect('subir_archivo')