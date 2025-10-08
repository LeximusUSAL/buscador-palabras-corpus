# 🔍 Buscador de Palabras Clave en Corpus Textual

Herramienta sencilla para buscar palabras clave en **corpus masivos de texto**. Genera estadísticas, gráficos interactivos y análisis de frecuencia automáticamente.

---

## 📋 ¿Qué hace este programa?

Este programa te permite:

✅ **Buscar cualquier palabra** en cientos o miles de archivos de texto
✅ **Contar cuántas veces aparece** la palabra en cada archivo
✅ **Generar estadísticas** automáticas (porcentajes, frecuencias, etc.)
✅ **Crear una página web interactiva** con gráficos y tablas
✅ **Ver el contexto** donde aparece cada palabra (fragmentos de texto)

**Ejemplo de uso:**
- Buscar "Benedito" en 500 revistas musicales
- Buscar "feminismo" en corpus de prensa histórica
- Buscar "covid" en documentos científicos
- Buscar "Mozart" en críticas musicales

---

## 🖥️ Requisitos

Para usar este programa necesitas:

1. **Python 3** instalado en tu computadora
   - [Descargar Python](https://www.python.org/downloads/) (es gratis)
   - Durante la instalación, marca la casilla "Add Python to PATH"

2. **Archivos de texto (.txt)** para analizar
   - Pueden estar en una carpeta o subcarpetas
   - El programa los encontrará automáticamente

---

## 📥 Instalación

### Opción 1: Descarga directa

1. Haz clic en el botón verde **"Code"** → **"Download ZIP"**
2. Descomprime el archivo ZIP en tu computadora
3. Abre la carpeta descomprimida

### Opción 2: Con Git (si lo tienes instalado)

```bash
git clone https://github.com/mariamusical/buscador-palabras-corpus.git
cd buscador-palabras-corpus
```

---

## 🚀 Cómo usar el programa (paso a paso)

### **PASO 1: Configurar las palabras a buscar**

1. Abre el archivo `buscador_palabras_clave.py` con un editor de texto
   (puedes usar el Bloc de notas, TextEdit, Notepad++, etc.)

2. Busca las líneas 23-30 que dicen:

```python
PALABRAS_CLAVE = [
    "ejemplo",           # ← Cambia esto por tu palabra clave
    "ejemplos",          # ← Variante plural (opcional)
]

NOMBRE_BUSQUEDA = "Ejemplo"  # ← Cambia esto por el nombre de tu búsqueda
```

3. **Reemplaza** las palabras de ejemplo con las palabras que quieres buscar:

**Ejemplo 1: Buscar "Benedito"**
```python
PALABRAS_CLAVE = [
    "Benedito",
    "Beneditto",
]

NOMBRE_BUSQUEDA = "Benedito"
```

**Ejemplo 2: Buscar "feminismo"**
```python
PALABRAS_CLAVE = [
    "feminismo",
    "feminista",
    "feministas",
]

NOMBRE_BUSQUEDA = "Feminismo"
```

**Ejemplo 3: Buscar "Mozart"**
```python
PALABRAS_CLAVE = [
    "Mozart",
    "mozartiano",
]

NOMBRE_BUSQUEDA = "Mozart"
```

4. **Guarda el archivo** después de hacer los cambios

---

### **PASO 2: Ejecutar el programa**

#### En **Windows**:

1. Abre **PowerShell** o **Símbolo del sistema** (CMD)
2. Navega hasta la carpeta donde está el programa:
   ```bash
   cd C:\Users\TuNombre\Downloads\buscador-palabras-corpus
   ```
3. Ejecuta el programa indicando la ruta a tus archivos:
   ```bash
   python buscador_palabras_clave.py "C:\Mis Documentos\Corpus"
   ```

#### En **Mac/Linux**:

1. Abre la **Terminal**
2. Navega hasta la carpeta del programa:
   ```bash
   cd ~/Downloads/buscador-palabras-corpus
   ```
3. Ejecuta el programa indicando la ruta a tus archivos:
   ```bash
   python3 buscador_palabras_clave.py ~/Desktop/Corpus
   ```

---

### **PASO 3: Ver los resultados**

El programa genera **dos archivos**:

1. **`resultados_busqueda.html`** → Página web interactiva con:
   - Gráficos de distribución
   - Tabla con todos los archivos analizados
   - Contextos donde aparece la palabra
   - Filtros y búsqueda

2. **`resultados_busqueda.json`** → Datos completos en formato JSON
   (para análisis avanzados)

**¡Abre el archivo HTML con tu navegador para ver los resultados!**

---

## 📊 Ejemplo de salida

### Estadísticas generadas:

```
🔍 ANÁLISIS COMPLETADO
================================================================================
📄 Total archivos: 250
✅ Archivos con 'Benedito': 45 (18%)
❌ Archivos sin 'Benedito': 205 (82%)
📊 Total menciones: 127
📈 Frecuencia: 12.5 menciones por millón de palabras

📁 Archivos generados:
   - resultados_busqueda.html (🌐 página web interactiva)
   - resultados_busqueda.json (datos completos)
```

### Visualización web:

La página HTML incluye:

- 📊 **Gráfico de pastel**: Archivos con/sin la palabra
- 📈 **Gráfico de barras**: Top 10 archivos con más menciones
- 📋 **Tabla interactiva**: Listado completo de archivos
- 🔍 **Búsqueda**: Filtrar archivos por nombre
- 📝 **Contextos**: Ver fragmentos donde aparece la palabra

---

## 🛠️ Solución de problemas

### ❌ Error: "python: command not found"

**Solución**: Python no está instalado o no está en el PATH

1. Descarga Python desde [python.org](https://www.python.org/downloads/)
2. Durante la instalación, marca "Add Python to PATH"
3. Reinicia tu computadora

---

### ❌ Error: "No se encontraron archivos TXT"

**Solución**: Verifica que:

1. La ruta al directorio es correcta
2. Los archivos tienen extensión `.txt`
3. Usas comillas si la ruta tiene espacios: `"C:\Mis Documentos\Corpus"`

---

### ❌ Error: "ModuleNotFoundError"

**Solución**: Algunos módulos de Python no están instalados

```bash
# En Windows
python -m pip install --upgrade pip

# En Mac/Linux
python3 -m pip install --upgrade pip
```

---

## 💡 Consejos

1. **Variantes de palabras**: Puedes incluir plurales, formas verbales, etc.
   ```python
   PALABRAS_CLAVE = [
       "componer",
       "compuso",
       "compuesto",
       "compositor",
       "compositora",
   ]
   ```

2. **Palabras compuestas**: Usa guiones o espacios según aparezcan en tus textos
   ```python
   PALABRAS_CLAVE = [
       "avant-garde",
       "avant garde",
   ]
   ```

3. **No distingue mayúsculas**: "Mozart", "mozart" y "MOZART" se consideran iguales

4. **Busca palabras completas**: "arte" NO coincidirá con "artefacto"

---

## 📚 Casos de uso académicos

Este programa fue creado para el proyecto **LexiMus** (Universidad de Salamanca) y se ha usado para:

- ✅ Análisis de presencia/ausencia de compositores en revistas musicales
- ✅ Estudio de frecuencia de términos musicales en prensa histórica
- ✅ Investigación de sesgo de género en crítica musical
- ✅ Análisis de diversidad cultural en publicaciones especializadas

---

## 📝 Licencia

MIT License - Uso libre para fines académicos y comerciales

---

## 👩‍💻 Créditos

**Proyecto**: LexiMus - Léxico y ontología de la música en español
**Instituciones**: Universidad de Salamanca | Instituto Complutense de Ciencias Musicales | Universidad de La Rioja
**Desarrollado con**: Claude Code (Anthropic)

---

## 🆘 ¿Necesitas ayuda?

Si tienes problemas usando el programa:

1. Lee la sección **"Solución de problemas"** arriba
2. Verifica que seguiste todos los pasos correctamente
3. Abre un **Issue** en GitHub describiendo tu problema

---

## 🎯 Próximas características

- [ ] Búsqueda de expresiones regulares (regex)
- [ ] Exportación a Excel/CSV
- [ ] Análisis de colocaciones (palabras cercanas)
- [ ] Gráficos de tendencias temporales
- [ ] Interfaz gráfica (sin línea de comandos)

---

**¡Feliz análisis de corpus!** 📊📚
