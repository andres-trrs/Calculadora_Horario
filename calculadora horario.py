import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkcalendar import Calendar
from datetime import datetime
import csv
import calendar
import babel.numbers

datos_dias = {}

def formatear_hora(var):
    texto = var.get()
    texto = texto.replace(":", "")
    if len(texto) == 4:
        texto = texto[:2] + ":" + texto[2:]
        var.set(texto)

def seleccionar_fecha(event):
    fecha = cal.get_date()
    fecha_label.config(text=f"Fecha seleccionada: {fecha}")
    
    datos = datos_dias.get(fecha, {
        "entrada": "", "salida": "", "colacion": "", 
        "entrada_extra": "", "salida_extra": ""
    })
    entrada_var.set(datos["entrada"])
    salida_var.set(datos["salida"])
    colacion_var.set(datos["colacion"])
    entrada_extra_var.set(datos.get("entrada_extra", ""))
    salida_extra_var.set(datos.get("salida_extra", ""))
    
    # Mostrar u ocultar botón de eliminar según si hay datos
    if fecha in datos_dias and any([datos["entrada"], datos["salida"], datos["colacion"], 
                                datos.get("entrada_extra", ""), datos.get("salida_extra", "")]):
        boton_eliminar.grid(row=11, column=1, columnspan=2, pady=5)
    else:
        boton_eliminar.grid_remove()

def guardar_datos():
    fecha = cal.get_date()
    datos_dias[fecha] = {
        "entrada": entrada_var.get(),
        "salida": salida_var.get(),
        "colacion": colacion_var.get(),
        "entrada_extra": entrada_extra_var.get(),
        "salida_extra": salida_extra_var.get(),
    }
    estado_label.config(text=f"Datos guardados para {fecha}", foreground="green")
    colorear_fechas()
    # Mostrar botón eliminar después de guardar
    boton_eliminar.grid(row=11, column=1, columnspan=2, pady=5)

def eliminar_dia_trabajado():
    """Elimina todos los datos del día seleccionado"""
    fecha = cal.get_date()
    if fecha in datos_dias:
        # Confirmar eliminación
        respuesta = messagebox.askyesno("Confirmar eliminación", 
                                    f"¿Estás seguro de que quieres eliminar todos los datos del {fecha}?")
        if respuesta:
            # Eliminar datos
            del datos_dias[fecha]
            
            # Limpiar campos
            entrada_var.set("")
            salida_var.set("")
            colacion_var.set("")
            entrada_extra_var.set("")
            salida_extra_var.set("")
            
            # Actualizar interfaz
            estado_label.config(text=f"Datos eliminados para {fecha}", foreground="red")
            colorear_fechas()  # Actualizar colores del calendario
            boton_eliminar.grid_remove()  # Ocultar botón eliminar

def calcular_sueldo():
    total_min_trabajados = 0
    total_min_extras = 0
    
    for fecha, datos in datos_dias.items():
        try:
            entrada = datetime.strptime(datos["entrada"], "%H:%M")
            salida = datetime.strptime(datos["salida"], "%H:%M")
            colacion = int(datos["colacion"]) if datos["colacion"].isdigit() else 0

            minutos_trabajados = (salida - entrada).seconds // 60 - colacion
            total_min_trabajados += max(0, minutos_trabajados)

            if datos["entrada_extra"] and datos["salida_extra"]:
                entrada_extra = datetime.strptime(datos["entrada_extra"], "%H:%M")
                salida_extra = datetime.strptime(datos["salida_extra"], "%H:%M")
                minutos_extras = (salida_extra - entrada_extra).seconds // 60
                total_min_extras += max(0, minutos_extras)
        except Exception:
            continue

    horas_trabajadas = total_min_trabajados / 60
    horas_extras = total_min_extras / 60

    try:
        pago_hora = float(pago_var.get())
        porcentaje_extra = float(porcentaje_var.get())
    except:
        resumen_label.config(text="⚠️ Verifica el pago por hora y el porcentaje.", foreground="red")
        return

    sueldo_base = horas_trabajadas * pago_hora
    pago_extras = horas_extras * pago_hora * (1 + porcentaje_extra / 100)
    sueldo_total = sueldo_base + pago_extras

    resumen_label.config(
        text=f"""
Total horas trabajadas: {horas_trabajadas:.2f} h
Horas extra: {horas_extras:.2f} h
Sueldo base: ${sueldo_base:.2f}
Pago por extras: ${pago_extras:.2f}
💰 Sueldo total estimado: ${sueldo_total:.2f}
""", foreground="blue"
    )

def colorear_fechas():
    cal.calevent_remove('all')
    for fecha_str in datos_dias.keys():
        try:
            fecha_obj = datetime.strptime(fecha_str, "%Y-%m-%d").date()
            cal.calevent_create(fecha_obj, 'Guardado', 'guardado')
        except:
            continue
    cal.tag_config('guardado', background='green', foreground='white')

def exportar_csv():
    if not datos_dias:
        messagebox.showinfo("Exportar CSV", "No hay datos para exportar.")
        return

    file_path = filedialog.asksaveasfilename(defaultextension=".csv",
                                            filetypes=[("Archivo CSV", "*.csv")],
                                            title="Guardar archivo CSV")
    if not file_path:
        return
    
    try:
        with open(file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(["Fecha", "Hora Entrada", "Hora Salida", "Colacion (min)", "Horas Trabajadas", "Horas Extras"])
            
            # Variables para totales
            total_horas_trabajadas = 0
            total_horas_extras = 0
            
            for fecha, datos in sorted(datos_dias.items()):
                # Inicializar valores por defecto
                horas_trabajadas = ""
                horas_extras = ""
                
                try:
                    # Función auxiliar para validar formato de hora
                    def es_hora_valida(hora_str):
                        if not hora_str or hora_str.strip() == "" or hora_str == "0":
                            return False
                        try:
                            datetime.strptime(hora_str, "%H:%M")
                            return True
                        except:
                            return False
                    
                    # Calcular horas trabajadas
                    if es_hora_valida(datos.get("entrada")) and es_hora_valida(datos.get("salida")):
                        entrada = datetime.strptime(datos["entrada"], "%H:%M")
                        salida = datetime.strptime(datos["salida"], "%H:%M")
                        colacion = int(datos["colacion"]) if datos["colacion"].isdigit() else 0
                        minutos_trabajados = (salida - entrada).seconds // 60 - colacion
                        horas_trabajadas_calc = max(0, minutos_trabajados) / 60
                        horas_trabajadas = horas_trabajadas_calc
                        total_horas_trabajadas += horas_trabajadas_calc

                    # Calcular horas extras
                    if es_hora_valida(datos.get("entrada_extra")) and es_hora_valida(datos.get("salida_extra")):
                        entrada_extra = datetime.strptime(datos["entrada_extra"], "%H:%M")
                        salida_extra = datetime.strptime(datos["salida_extra"], "%H:%M")
                        minutos_extras = (salida_extra - entrada_extra).seconds // 60
                        horas_extras_calc = max(0, minutos_extras) / 60
                        horas_extras = horas_extras_calc
                        total_horas_extras += horas_extras_calc
                    else:
                        horas_extras = 0
                        
                except Exception as e:
                    # Si hay error en el cálculo, mantener valores vacíos
                    print(f"Error calculando horas para {fecha}: {e}")
                    horas_trabajadas = ""
                    horas_extras = ""

                def dec_a_coma(valor):
                    if valor == "" or valor is None:
                        return ""
                    # Usar truncamiento manual para evitar aproximación
                    valor_truncado = int(valor * 100) / 100  # Truncar a 2 decimales sin aproximar
                    return f"{valor_truncado:.2f}".replace('.', ',')

                writer.writerow([
                    fecha,
                    datos.get("entrada", ""),
                    datos.get("salida", ""),
                    datos.get("colacion", ""),
                    dec_a_coma(horas_trabajadas),
                    dec_a_coma(horas_extras)
                ])
            
            # Agregar fila de totales
            writer.writerow([
                "TOTAL",
                "",
                "",
                "",
                dec_a_coma(total_horas_trabajadas),
                dec_a_coma(total_horas_extras)
            ])

        messagebox.showinfo("Exportar CSV", f"Datos exportados correctamente a:\n{file_path}")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo exportar el archivo.\n{e}")

def abrir_plantilla_semanal():
    """Abre ventana para configurar plantilla de horarios de lunes a domingo"""
    ventana_plantilla = tk.Toplevel(root)
    ventana_plantilla.title("Plantilla Semanal - Lunes a Domingo")
    ventana_plantilla.geometry("550x600")  # Aumenté el alto para acomodar todos los días
    ventana_plantilla.resizable(False, False)
    
    # Variables para almacenar los datos de la plantilla
    plantilla_datos = {}
    dias_semana = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
    
    # Crear variables para cada día
    for dia in dias_semana:
        plantilla_datos[dia] = {
            'entrada': tk.StringVar(),
            'salida': tk.StringVar(),
            'colacion': tk.StringVar()
        }
    
    # Función para formatear hora en la ventana de plantilla
    def formatear_hora_plantilla(var):
        texto = var.get()
        texto = texto.replace(":", "")
        if len(texto) == 4:
            texto = texto[:2] + ":" + texto[2:]
            var.set(texto)
    
    # Título principal
    ttk.Label(ventana_plantilla, text="Configurar Horarios Base", 
            font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=4, pady=10)
    
    ttk.Label(ventana_plantilla, text="Estos horarios se aplicarán a todos los días del mes correspondiente", 
            font=("Arial", 9)).grid(row=1, column=0, columnspan=4, pady=(0,20))
    
    # Encabezados
    ttk.Label(ventana_plantilla, text="Día", font=("Arial", 10, "bold")).grid(row=2, column=0, padx=10, pady=5)
    ttk.Label(ventana_plantilla, text="Entrada", font=("Arial", 10, "bold")).grid(row=2, column=1, padx=10, pady=5)
    ttk.Label(ventana_plantilla, text="Salida", font=("Arial", 10, "bold")).grid(row=2, column=2, padx=10, pady=5)
    ttk.Label(ventana_plantilla, text="Colación (min)", font=("Arial", 10, "bold")).grid(row=2, column=3, padx=10, pady=5)
    
    # Crear campos para cada día
    for i, dia in enumerate(dias_semana, start=3):
        ttk.Label(ventana_plantilla, text=dia).grid(row=i, column=0, padx=10, pady=5, sticky='w')
        
        # Entry para entrada
        entry_entrada = ttk.Entry(ventana_plantilla, textvariable=plantilla_datos[dia]['entrada'], width=10)
        entry_entrada.grid(row=i, column=1, padx=10, pady=5)
        plantilla_datos[dia]['entrada'].trace_add("write", 
            lambda *args, v=plantilla_datos[dia]['entrada']: formatear_hora_plantilla(v))
        
        # Entry para salida
        entry_salida = ttk.Entry(ventana_plantilla, textvariable=plantilla_datos[dia]['salida'], width=10)
        entry_salida.grid(row=i, column=2, padx=10, pady=5)
        plantilla_datos[dia]['salida'].trace_add("write", 
            lambda *args, v=plantilla_datos[dia]['salida']: formatear_hora_plantilla(v))
        
        # Entry para colación
        entry_colacion = ttk.Entry(ventana_plantilla, textvariable=plantilla_datos[dia]['colacion'], width=10)
        entry_colacion.grid(row=i, column=3, padx=10, pady=5)
    
    # Frame para selección de mes/año
    frame_fecha = ttk.LabelFrame(ventana_plantilla, text="Aplicar a mes/año específico", padding=10)
    frame_fecha.grid(row=10, column=0, columnspan=4, padx=20, pady=15, sticky='ew')  # Ajusté la fila
    
    # Variables para mes y año
    mes_var = tk.StringVar(value=str(datetime.now().month))
    año_var = tk.StringVar(value=str(datetime.now().year))
    
    ttk.Label(frame_fecha, text="Mes:").grid(row=0, column=0, padx=5)
    mes_combo = ttk.Combobox(frame_fecha, textvariable=mes_var, width=10, state="readonly")
    mes_combo['values'] = tuple(f"{i:02d}" for i in range(1, 13))
    mes_combo.grid(row=0, column=1, padx=5)
    
    ttk.Label(frame_fecha, text="Año:").grid(row=0, column=2, padx=5)
    año_entry = ttk.Entry(frame_fecha, textvariable=año_var, width=10)
    año_entry.grid(row=0, column=3, padx=5)
    
    def aplicar_plantilla():
        """Aplica la plantilla a todos los días del mes seleccionado"""
        try:
            mes = int(mes_var.get())
            año = int(año_var.get())
            
            # Verificar que hay al menos algunos datos en la plantilla
            hay_datos = False
            for dia in dias_semana:
                if (plantilla_datos[dia]['entrada'].get().strip() or 
                    plantilla_datos[dia]['salida'].get().strip() or 
                    plantilla_datos[dia]['colacion'].get().strip()):
                    hay_datos = True
                    break
            
            if not hay_datos:
                messagebox.showwarning("Advertencia", "Por favor ingresa al menos algunos horarios en la plantilla")
                return
            
            # Mapeo de días de la semana (0=lunes, 6=domingo)
            mapeo_dias = {0: "Lunes", 1: "Martes", 2: "Miércoles", 3: "Jueves", 4: "Viernes", 5: "Sábado", 6: "Domingo"}
            
            # Obtener todos los días del mes
            dias_del_mes = calendar.monthrange(año, mes)[1]
            
            contador_aplicados = 0
            
            for dia in range(1, dias_del_mes + 1):
                fecha_obj = datetime(año, mes, dia)
                dia_semana = fecha_obj.weekday()  # 0=lunes, 6=domingo
                
                # Aplicar a todos los días de la semana (lunes a domingo)
                if dia_semana in mapeo_dias:
                    nombre_dia = mapeo_dias[dia_semana]
                    fecha_str = fecha_obj.strftime("%Y-%m-%d")
                    
                    # Obtener los datos de la plantilla para este día
                    entrada_plantilla = plantilla_datos[nombre_dia]['entrada'].get().strip()
                    salida_plantilla = plantilla_datos[nombre_dia]['salida'].get().strip()
                    colacion_plantilla = plantilla_datos[nombre_dia]['colacion'].get().strip()
                    
                    # Solo aplicar si hay datos válidos para este día de la semana
                    if entrada_plantilla or salida_plantilla or colacion_plantilla:
                        # Obtener datos existentes o crear nuevos
                        datos_existentes = datos_dias.get(fecha_str, {
                            "entrada": "", "salida": "", "colacion": "", 
                            "entrada_extra": "", "salida_extra": ""
                        })
                        
                        # Aplicar solo los datos de la plantilla, conservando las horas extra
                        datos_dias[fecha_str] = {
                            "entrada": entrada_plantilla,
                            "salida": salida_plantilla,
                            "colacion": colacion_plantilla,
                            "entrada_extra": datos_existentes.get("entrada_extra", ""),
                            "salida_extra": datos_existentes.get("salida_extra", "")
                        }
                        contador_aplicados += 1
            
            # Actualizar el calendario y mostrar confirmación
            colorear_fechas()
            messagebox.showinfo("Plantilla Aplicada", 
                f"Plantilla aplicada a {contador_aplicados} días del mes {mes:02d}/{año}")
            ventana_plantilla.destroy()
            
        except ValueError:
            messagebox.showerror("Error", "Por favor ingresa un mes y año válidos")
        except Exception as e:
            messagebox.showerror("Error", f"Error al aplicar plantilla: {e}")
    
    # Botones
    frame_botones = ttk.Frame(ventana_plantilla)
    frame_botones.grid(row=11, column=0, columnspan=4, pady=15)  # Ajusté la fila
    
    ttk.Button(frame_botones, text="Aplicar Plantilla", command=aplicar_plantilla).pack(side=tk.LEFT, padx=10)
    ttk.Button(frame_botones, text="Cancelar", command=ventana_plantilla.destroy).pack(side=tk.LEFT, padx=10)
    
    # Centrar la ventana
    ventana_plantilla.transient(root)
    ventana_plantilla.grab_set()


# Ventana principal
root = tk.Tk()
root.title("Registro de Horas")

cal = Calendar(root, selectmode='day', date_pattern='yyyy-mm-dd', locale='es')
cal.grid(row=0, column=0, padx=10, pady=10, rowspan=15)
cal.bind("<<CalendarSelected>>", seleccionar_fecha)

entrada_var = tk.StringVar()
salida_var = tk.StringVar()
colacion_var = tk.StringVar()
entrada_extra_var = tk.StringVar()
salida_extra_var = tk.StringVar()

# ✅ Aplicar formateo solo cuando el usuario ingresa 4 dígitos
for var in [entrada_var, salida_var, entrada_extra_var, salida_extra_var]:
    var.trace_add("write", lambda *args, v=var: formatear_hora(v))

ttk.Label(root, text="Hora de entrada (HH:MM):").grid(row=0, column=1, sticky='w')
ttk.Entry(root, textvariable=entrada_var, width=10).grid(row=0, column=2)

ttk.Label(root, text="Hora de salida (HH:MM):").grid(row=1, column=1, sticky='w')
ttk.Entry(root, textvariable=salida_var, width=10).grid(row=1, column=2)

ttk.Label(root, text="Colación (min):").grid(row=2, column=1, sticky='w')
ttk.Entry(root, textvariable=colacion_var, width=10).grid(row=2, column=2)

ttk.Label(root, text="Hora entrada extra (HH:MM):").grid(row=3, column=1, sticky='w')
ttk.Entry(root, textvariable=entrada_extra_var, width=10).grid(row=3, column=2)

ttk.Label(root, text="Hora salida extra (HH:MM):").grid(row=4, column=1, sticky='w')
ttk.Entry(root, textvariable=salida_extra_var, width=10).grid(row=4, column=2)

ttk.Button(root, text="Guardar", command=guardar_datos).grid(row=5, column=1, columnspan=2, pady=10)
ttk.Label(root, text="Hecho por Andrés 😊", font=("Arial", 12), foreground="gray").grid(row=999, column=0, columnspan=10, pady=5)


pago_var = tk.StringVar(value="1000")
porcentaje_var = tk.StringVar(value="50")

ttk.Label(root, text="Pago por hora ($):").grid(row=6, column=1, sticky='w')
ttk.Entry(root, textvariable=pago_var, width=10).grid(row=6, column=2)

ttk.Label(root, text="Porcentaje extra (%):").grid(row=7, column=1, sticky='w')
ttk.Entry(root, textvariable=porcentaje_var, width=10).grid(row=7, column=2)

ttk.Button(root, text="Calcular resumen", command=calcular_sueldo).grid(row=8, column=1, columnspan=2, pady=10)

ttk.Button(root, text="Exportar a CSV", command=exportar_csv).grid(row=9, column=1, columnspan=2, pady=10)

ttk.Button(root, text="Configurar Plantilla Semanal", command=abrir_plantilla_semanal).grid(row=10, column=1, columnspan=2, pady=5)

# Botón eliminar (inicialmente oculto)
boton_eliminar = ttk.Button(root, text="Eliminar día trabajado", command=eliminar_dia_trabajado)
boton_eliminar.grid_remove()  # Inicialmente oculto

fecha_label = ttk.Label(root, text="Seleccione una fecha")
fecha_label.grid(row=12, column=1, columnspan=2)  # Cambié de row=11 a row=12

estado_label = ttk.Label(root, text="")
estado_label.grid(row=13, column=0, columnspan=3)  # Cambié de row=12 a row=13

resumen_label = ttk.Label(root, text="", justify="left")
resumen_label.grid(row=14, column=0, columnspan=3, pady=10)  # Cambié de row=13 a row=14

colorear_fechas()

root.mainloop()