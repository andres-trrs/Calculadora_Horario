# 📊 Registro de Horas de Trabajo

> Una aplicación de escritorio completa para el registro y cálculo automático de horas de trabajo, diseñada para freelancers, trabajadores por horas y cualquier persona que necesite un control preciso de su tiempo laboral.

![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 🌟 Características Principales

- **📅 Calendario Interactivo**: Selección visual de fechas con marcado de días trabajados
- **⏰ Registro de Horarios**: Entrada, salida y tiempo de colación con formato automático
- **⏱️ Horas Extras**: Registro separado de horas adicionales
- **🚀 Plantilla Semanal**: Configuración rápida de horarios recurrentes
- **💰 Cálculo Automático**: Sueldo base y horas extras con porcentajes personalizables
- **📊 Exportación CSV**: Reportes detallados para análisis externo
- **🎨 Interfaz Amigable**: Diseño limpio y fácil de usar

## 📸 Vista Previa

```
┌─────────────────────────────────────────────┐
│  📅 CALENDARIO        │  ⏰ REGISTRO DIARIO  │
│                       │                      │
│  [Calendario visual]  │  Entrada: [09:30]    │
│                       │  Salida:  [18:00]    │
│                       │  Colación: [60] min  │
│                       │                      │
│                       │  🚀 [Plantilla Sem.] │
│                       │  💰 [Calcular]       │
└─────────────────────────────────────────────┘
```

## 🚀 Instalación

### Requisitos Previos

- Python 3.7 o superior
- pip (incluido con Python)

### Dependencias

Instala las librerías necesarias:

```bash
pip install tkinter tkcalendar
```

> **Nota**: `tkinter` viene incluido con Python en la mayoría de instalaciones.

### Ejecución

1. Descarga o clona el archivo `registro_horas.py`
2. Ejecuta desde la terminal:

```bash
python registro_horas.py
```

## 📖 Guía de Uso

### 🎯 Registro Básico

1. **Seleccionar Fecha**: Haz clic en cualquier día del calendario
2. **Ingresar Horarios**: 
   - Entrada: Formato HH:MM (ej: 09:30)
   - Salida: Formato HH:MM (ej: 18:00)  
   - Colación: Minutos de descanso (ej: 60)
3. **Guardar**: Clic en "💾 Guardar"

### ⚡ Plantilla Semanal (¡NUEVO!)

Esta característica te permitirá ahorrar tiempo configurando horarios recurrentes:

#### Paso 1: Configurar la Plantilla
1. Haz clic en "📅 Plantilla Semanal"
2. Completa los horarios típicos para cada día de la semana:
   ```
   Lunes    : 09:00 - 18:00 (60 min colación)
   Martes   : 09:00 - 18:00 (60 min colación)
   Miércoles: 09:00 - 17:00 (60 min colación)
   Jueves   : 09:00 - 18:00 (60 min colación)
   Viernes  : 09:00 - 16:00 (60 min colación)
   Sábado   : [vacío - día libre]
   Domingo  : [vacío - día libre]
   ```

#### Paso 2: Aplicar al Mes
1. Asegúrate de estar viendo el mes correcto en el calendario
2. Haz clic en "📅 Aplicar al Mes Actual"
3. ¡Todos los días del mes quedan configurados automáticamente!

#### Paso 3: Ajustes Individuales
- Las horas extras se pueden agregar día por día
- Puedes modificar horarios específicos cuando sea necesario
- Los días aplicados aparecerán marcados en verde

### 💰 Cálculo de Sueldo

1. **Configurar Tarifas**:
   - Pago por hora: Valor en pesos (ej: 1000)
   - Porcentaje extra: % adicional para horas extras (ej: 50%)

2. **Calcular**: Haz clic en "💰 Calcular resumen"

3. **Resultado**: Verás un resumen como:
   ```
   Total horas trabajadas: 168.50 h
   Horas extra: 12.00 h
   Sueldo base: $168,500
   Pago por extras: $18,000
   💰 Sueldo total estimado: $186,500
   ```

### 📊 Exportar Datos

1. Haz clic en "📊 Exportar a CSV"
2. Elige la ubicación del archivo
3. El archivo incluirá:
   - Fecha
   - Horarios de entrada y salida
   - Minutos de colación
   - Horas trabajadas calculadas
   - Horas extras

## 🔧 Características Técnicas

### Formateo Automático
- **Entrada de Horas**: Escribe "0930" → se convierte a "09:30"
- **Validación**: Controles automáticos para evitar errores
- **Persistencia Visual**: Los días con datos aparecen marcados en verde

### Cálculos Precisos
- **Minutos Exactos**: Cálculo en minutos, luego conversión a horas
- **Descansos**: Resta automática del tiempo de colación
- **Horas Extras**: Cálculo separado con porcentaje adicional

### Compatibilidad
- **Formato CSV**: Separador punto y coma (;) para Excel
- **Encoding UTF-8**: Soporte completo para caracteres especiales
- **Fechas**: Formato ISO (YYYY-MM-DD) para ordenamiento automático

## 📁 Estructura del Proyecto

```
registro-horas/
│
├── registro_horas.py          # Aplicación principal
├── README.md                  # Este archivo
└── datos_exportados/          # Carpeta para archivos CSV (se crea automáticamente)
```

## 🛠️ Personalización

### Modificar Configuración por Defecto

En el código, puedes cambiar los valores iniciales:

```python
# Líneas 200-201
pago_var = tk.StringVar(value="1000")      # Tu tarifa por hora
porcentaje_var = tk.StringVar(value="50")  # Tu porcentaje de horas extra
```

### Agregar Nuevos Campos

La estructura de datos es flexible y permite agregar nuevos campos:

```python
datos_dias[fecha] = {
    "entrada": entrada_var.get(),
    "salida": salida_var.get(),
    "colacion": colacion_var.get(),
    "entrada_extra": entrada_extra_var.get(),
    "salida_extra": salida_extra_var.get(),
    # Aquí puedes agregar nuevos campos
    "proyecto": proyecto_var.get(),
    "notas": notas_var.get(),
}
```

## 🐛 Solución de Problemas

### Problemas Comunes

**❌ Error al abrir la aplicación**
```
ModuleNotFoundError: No module named 'tkcalendar'
```
**✅ Solución:**
```bash
pip install tkcalendar
```

**❌ Las horas no se formatean correctamente**
- Asegúrate de ingresar exactamente 4 dígitos (ej: 0930, 1800)
- El formato se aplica automáticamente al completar 4 dígitos

**❌ La plantilla no se aplica**
- Verifica que hayas configurado horarios en la plantilla
- Asegúrate de estar viendo el mes correcto en el calendario

### Contacto y Soporte

Si encuentras algún problema o tienes sugerencias:

1. 🔍 Revisa la sección de problemas comunes
2. 📝 Verifica que todos los campos estén correctamente llenados
3. 💡 Consulta los ejemplos de uso

## 🚀 Ideas futuras

- [ ] 🏢 Múltiples proyectos/clientes
- [ ] 📅 Integración con calendarios externos
- [ ] 💸 Facturación automática
- [ ] 📊 Dashboard de estadísticas
- [ ] ☁️ Sincronización en la nube

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo `LICENSE` para más detalles.

## 🤝 Contribuciones

¡Las contribuciones son bienvenidas! Si tienes ideas para mejorar la aplicación:

1. 🍴 Fork el proyecto
2. 🌿 Crea una rama para tu característica (`git checkout -b feature/nueva-caracteristica`)
3. 📝 Commit tus cambios (`git commit -am 'Agregar nueva característica'`)
4. 📤 Push a la rama (`git push origin feature/nueva-caracteristica`)
5. 🔄 Abre un Pull Request

## ⭐ ¿Te Gustó?

Si esta aplicación te resultó útil:
- ⭐ Dale una estrella al repositorio
- 🔄 Compártela con otros freelancers
- 💡 Sugiere nuevas características

---

<div align="center">

**Desarrollado con ❤️ para freelancers y trabajadores independientes**

</div>
