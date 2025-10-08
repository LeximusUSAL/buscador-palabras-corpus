#!/usr/bin/env python3
"""
Buscador de Palabras Clave en Corpus Textual
Análisis de presencia/ausencia y frecuencia de términos personalizados

Este script analiza archivos de texto para encontrar menciones de cualquier palabra clave,
generando estadísticas sobre su presencia y frecuencia en el corpus.

Proyecto: LexiMus - Universidad de Salamanca
Autor: María [Generado con Claude Code]
Licencia: MIT
"""

import os
import re
import json
import sys
from collections import Counter
from datetime import datetime


# ==========================================================================
# ⚙️ CONFIGURACIÓN - MODIFICA AQUÍ TU PALABRA CLAVE
# ==========================================================================

# INSTRUCCIONES:
# 1. Reemplaza "ejemplo" con la palabra EXACTA que quieras buscar
# 2. El script buscará EXACTAMENTE esa palabra (sensible a mayúsculas)
# 3. Solo se permite UNA palabra clave a la vez

PALABRA_CLAVE = "Ejemplo"  # ← Cambia esto por tu palabra clave EXACTA


# ==========================================================================
# CLASE PRINCIPAL DEL BUSCADOR
# ==========================================================================

class BuscadorPalabrasClave:
    def __init__(self, base_directory, palabra_clave):
        """
        Inicializa el buscador de palabra clave

        Args:
            base_directory (str): Ruta al directorio con archivos TXT
            palabra_clave (str): Palabra EXACTA a buscar (sensible a mayúsculas)
        """
        self.base_directory = base_directory
        self.palabra_clave = palabra_clave
        self.resultados = {}
        self.total_archivos = 0
        self.total_palabras = 0

        # Crear patrón regex para la palabra exacta
        # \b = límite de palabra (busca palabras completas, no dentro de otras)
        self.patron = r'\b' + re.escape(palabra_clave) + r'\b'

    def buscar_en_texto(self, contenido):
        """
        Busca todas las apariciones EXACTAS de la palabra clave en un texto

        Args:
            contenido (str): Texto a analizar

        Returns:
            dict: {
                'total_menciones': int,
                'contextos': list (fragmentos de texto donde aparece)
            }
        """
        resultado = {
            'total_menciones': 0,
            'contextos': []
        }

        # Buscar el patrón (sensible a mayúsculas)
        matches = list(re.finditer(self.patron, contenido))

        for match in matches:
            palabra_encontrada = match.group(0)

            # Extraer contexto (100 caracteres antes y después)
            inicio = max(0, match.start() - 100)
            fin = min(len(contenido), match.end() + 100)
            contexto = contenido[inicio:fin].strip()

            # Limpiar saltos de línea múltiples
            contexto = re.sub(r'\s+', ' ', contexto)

            resultado['contextos'].append({
                'texto': contexto,
                'posicion': match.start(),
                'palabra': palabra_encontrada
            })

            resultado['total_menciones'] += 1

        return resultado

    def analizar_archivo(self, filepath):
        """
        Analiza un archivo de texto en busca de la palabra clave

        Args:
            filepath (str): Ruta al archivo

        Returns:
            dict: Resultado del análisis del archivo
        """
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                contenido = f.read()

            # Conteo de palabras
            palabras = len(contenido.split())

            # Buscar palabra clave
            busqueda = self.buscar_en_texto(contenido)

            # Construir resultado
            resultado = {
                'archivo': os.path.basename(filepath),
                'ruta': filepath,
                'palabras': palabras,
                'tiene_palabra_clave': busqueda['total_menciones'] > 0,
                'total_menciones': busqueda['total_menciones'],
                'contextos': busqueda['contextos'][:5]  # Máximo 5 contextos por archivo
            }

            return resultado

        except Exception as e:
            print(f"❌ Error analizando {filepath}: {e}")
            return None

    def analizar_directorio(self, directorio=None):
        """
        Analiza todos los archivos TXT en un directorio

        Args:
            directorio (str): Ruta al directorio (usa base_directory si None)

        Returns:
            dict: Resultados completos del análisis
        """
        if directorio is None:
            directorio = self.base_directory

        print(f"📂 Analizando directorio: {directorio}")

        # Buscar todos los archivos TXT
        archivos_txt = []
        for root, dirs, files in os.walk(directorio):
            for file in files:
                if file.endswith('.txt'):
                    archivos_txt.append(os.path.join(root, file))

        print(f"📄 Encontrados {len(archivos_txt)} archivos TXT")

        if len(archivos_txt) == 0:
            print("❌ No se encontraron archivos TXT en el directorio")
            sys.exit(1)

        # Analizar cada archivo
        resultados_archivos = []
        total_menciones = 0
        archivos_con_palabra = 0
        archivos_sin_palabra = 0
        total_palabras = 0

        for i, filepath in enumerate(archivos_txt, 1):
            print(f"⚙️  Procesando {i}/{len(archivos_txt)}: {os.path.basename(filepath)}")

            resultado = self.analizar_archivo(filepath)
            if resultado:
                resultados_archivos.append(resultado)
                total_menciones += resultado['total_menciones']
                total_palabras += resultado['palabras']

                if resultado['tiene_palabra_clave']:
                    archivos_con_palabra += 1
                else:
                    archivos_sin_palabra += 1

        # Calcular porcentajes
        porcentaje_con_palabra = round(
            (archivos_con_palabra / len(resultados_archivos) * 100)
            if len(resultados_archivos) > 0 else 0, 2
        )

        porcentaje_sin_palabra = round(
            (archivos_sin_palabra / len(resultados_archivos) * 100)
            if len(resultados_archivos) > 0 else 0, 2
        )

        # Frecuencia relativa (menciones por millón de palabras)
        frecuencia_por_millon = round(
            (total_menciones / total_palabras * 1000000)
            if total_palabras > 0 else 0, 2
        )

        # Consolidar resultados
        self.resultados = {
            'metadata': {
                'directorio': directorio,
                'total_archivos': len(resultados_archivos),
                'total_palabras': total_palabras,
                'fecha_analisis': datetime.now().isoformat(),
                'palabra_buscada': self.palabra_clave
            },
            'resumen_general': {
                'total_menciones': total_menciones,
                'archivos_con_palabra': archivos_con_palabra,
                'archivos_sin_palabra': archivos_sin_palabra,
                'porcentaje_con_palabra': porcentaje_con_palabra,
                'porcentaje_sin_palabra': porcentaje_sin_palabra,
                'frecuencia_por_millon_palabras': frecuencia_por_millon
            },
            'archivos': resultados_archivos
        }

        return self.resultados

    def guardar_resultados(self, output_file='resultados_busqueda.json'):
        """
        Guarda los resultados en JSON

        Args:
            output_file (str): Nombre del archivo de salida
        """
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(self.resultados, f, ensure_ascii=False, indent=2)

        print(f"\n✅ Resultados guardados en: {output_file}")
        return output_file

    def generar_web_interactiva(self, output_file='resultados_busqueda.html'):
        """
        Genera una página web interactiva con tabla y gráficos

        Args:
            output_file (str): Nombre del archivo HTML de salida
        """
        resumen = self.resultados['resumen_general']
        meta = self.resultados['metadata']

        # Ordenar archivos: primero con palabra clave, luego sin ella
        archivos_con = sorted(
            [a for a in self.resultados['archivos'] if a['tiene_palabra_clave']],
            key=lambda x: x['total_menciones'],
            reverse=True
        )
        archivos_sin = sorted(
            [a for a in self.resultados['archivos'] if not a['tiene_palabra_clave']],
            key=lambda x: x['archivo']
        )

        html_content = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Análisis de "{meta['palabra_buscada']}" en Corpus Textual</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            min-height: 100vh;
        }}
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            padding: 40px;
        }}
        h1 {{
            text-align: center;
            color: #333;
            margin-bottom: 10px;
            font-size: 2.5em;
        }}
        .subtitle {{
            text-align: center;
            color: #666;
            margin-bottom: 30px;
            font-size: 1.1em;
        }}
        .palabras-buscadas {{
            text-align: center;
            background: #f8f9fa;
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 30px;
            font-size: 0.95em;
        }}
        .palabras-buscadas strong {{
            color: #667eea;
        }}
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
        }}
        .stat-card {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 25px;
            border-radius: 15px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            text-align: center;
            transition: transform 0.3s ease;
        }}
        .stat-card:hover {{
            transform: translateY(-5px);
        }}
        .stat-card h3 {{
            font-size: 0.9em;
            opacity: 0.9;
            margin-bottom: 10px;
        }}
        .stat-card .number {{
            font-size: 2.5em;
            font-weight: bold;
            margin-bottom: 5px;
        }}
        .chart-container {{
            background: #f8f9fa;
            padding: 30px;
            border-radius: 15px;
            margin-bottom: 30px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.05);
        }}
        .chart-container h2 {{
            color: #333;
            margin-bottom: 20px;
            text-align: center;
        }}
        .chart-wrapper {{
            max-width: 600px;
            margin: 0 auto;
        }}
        .table-section {{
            background: #fff;
            padding: 30px;
            border-radius: 15px;
            margin-bottom: 30px;
            border: 1px solid #e0e0e0;
        }}
        .table-section h2 {{
            color: #333;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 3px solid #667eea;
        }}
        .filter-tabs {{
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
            flex-wrap: wrap;
        }}
        .filter-tab {{
            padding: 10px 20px;
            border: none;
            background: #e9ecef;
            border-radius: 8px;
            cursor: pointer;
            font-size: 1em;
            transition: all 0.3s ease;
        }}
        .filter-tab.active {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }}
        .filter-tab:hover {{
            background: #dee2e6;
        }}
        .filter-tab.active:hover {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }}
        th {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px;
            text-align: left;
            font-weight: 600;
            position: sticky;
            top: 0;
            z-index: 10;
        }}
        td {{
            padding: 12px 15px;
            border-bottom: 1px solid #eee;
        }}
        tr:hover {{
            background: #f8f9fa;
        }}
        .badge {{
            display: inline-block;
            padding: 4px 12px;
            border-radius: 20px;
            font-weight: bold;
            font-size: 0.85em;
        }}
        .badge-success {{
            background: #d1fae5;
            color: #065f46;
        }}
        .badge-danger {{
            background: #fee2e2;
            color: #991b1b;
        }}
        .menciones-badge {{
            background: #667eea;
            color: white;
            padding: 4px 10px;
            border-radius: 15px;
            font-weight: bold;
            font-size: 0.9em;
        }}
        .contexto-btn {{
            background: #f3f4f6;
            border: 1px solid #d1d5db;
            padding: 5px 12px;
            border-radius: 6px;
            cursor: pointer;
            font-size: 0.85em;
            transition: all 0.2s ease;
        }}
        .contexto-btn:hover {{
            background: #e5e7eb;
        }}
        .contexto-detalle {{
            display: none;
            margin-top: 10px;
            padding: 15px;
            background: #f9fafb;
            border-left: 4px solid #667eea;
            border-radius: 6px;
            font-size: 0.9em;
            line-height: 1.6;
        }}
        .contexto-detalle.visible {{
            display: block;
        }}
        .contexto-item {{
            margin-bottom: 10px;
            padding: 10px;
            background: white;
            border-radius: 4px;
            border: 1px solid #e5e7eb;
        }}
        .contexto-item strong {{
            color: #667eea;
        }}
        .metadata {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            margin-top: 30px;
            font-size: 0.9em;
            color: #666;
        }}
        footer {{
            text-align: center;
            margin-top: 40px;
            padding-top: 20px;
            border-top: 2px solid #eee;
            color: #666;
        }}
        .search-box {{
            margin-bottom: 20px;
        }}
        .search-box input {{
            width: 100%;
            padding: 12px 20px;
            border: 2px solid #e5e7eb;
            border-radius: 10px;
            font-size: 1em;
            transition: border 0.3s ease;
        }}
        .search-box input:focus {{
            outline: none;
            border-color: #667eea;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🔍 Análisis de "{meta['palabra_buscada']}" en Corpus Textual</h1>
        <p class="subtitle">Proyecto LexiMus - Universidad de Salamanca</p>

        <div class="palabras-buscadas">
            <strong>🔎 Palabra buscada:</strong> "{meta['palabra_buscada']}" (búsqueda EXACTA)
        </div>

        <div class="stats-grid">
            <div class="stat-card">
                <h3>📄 Total Archivos</h3>
                <div class="number">{meta['total_archivos']}</div>
                <div>{meta['total_palabras']:,} palabras</div>
            </div>
            <div class="stat-card">
                <h3>✅ Con "{meta['palabra_buscada']}"</h3>
                <div class="number">{resumen['archivos_con_palabra']}</div>
                <div>{resumen['porcentaje_con_palabra']}% del total</div>
            </div>
            <div class="stat-card">
                <h3>❌ Sin "{meta['palabra_buscada']}"</h3>
                <div class="number">{resumen['archivos_sin_palabra']}</div>
                <div>{resumen['porcentaje_sin_palabra']}% del total</div>
            </div>
            <div class="stat-card">
                <h3>📊 Total Menciones</h3>
                <div class="number">{resumen['total_menciones']}</div>
                <div>{resumen['frecuencia_por_millon_palabras']} por millón</div>
            </div>
        </div>

        <div class="chart-container">
            <h2>Distribución de Archivos por Presencia de "{meta['palabra_buscada']}"</h2>
            <div class="chart-wrapper">
                <canvas id="presenciaChart"></canvas>
            </div>
        </div>

        <div class="chart-container">
            <h2>Frecuencia de Menciones</h2>
            <canvas id="frecuenciaChart"></canvas>
        </div>

        <div class="table-section">
            <h2>📋 Detalle por Archivo</h2>

            <div class="search-box">
                <input type="text" id="searchInput" placeholder="🔍 Buscar por nombre de archivo...">
            </div>

            <div class="filter-tabs">
                <button class="filter-tab active" onclick="filtrarTabla('todos')">
                    Todos ({meta['total_archivos']})
                </button>
                <button class="filter-tab" onclick="filtrarTabla('con')">
                    Con "{meta['palabra_buscada']}" ({resumen['archivos_con_palabra']})
                </button>
                <button class="filter-tab" onclick="filtrarTabla('sin')">
                    Sin "{meta['palabra_buscada']}" ({resumen['archivos_sin_palabra']})
                </button>
            </div>

            <table id="tablaArchivos">
                <thead>
                    <tr>
                        <th style="width: 5%;">#</th>
                        <th style="width: 40%;">Archivo</th>
                        <th style="width: 15%;">Presencia</th>
                        <th style="width: 15%;">Menciones</th>
                        <th style="width: 15%;">Palabras</th>
                        <th style="width: 10%;">Contexto</th>
                    </tr>
                </thead>
                <tbody>
"""

        # Agregar filas de archivos CON palabra clave
        contador = 1
        for archivo in archivos_con:
            contextos_id = f"contexto_{contador}"

            html_content += f"""
                    <tr data-filter="con">
                        <td><strong>{contador}</strong></td>
                        <td>{archivo['archivo']}</td>
                        <td><span class="badge badge-success">✓ SÍ</span></td>
                        <td><span class="menciones-badge">{archivo['total_menciones']}</span></td>
                        <td>{archivo['palabras']:,}</td>
                        <td>
                            <button class="contexto-btn" onclick="toggleContexto('{contextos_id}')">
                                Ver contexto
                            </button>
                            <div id="{contextos_id}" class="contexto-detalle">
"""

            # Agregar contextos
            if archivo['contextos']:
                for i, ctx in enumerate(archivo['contextos'], 1):
                    # Resaltar la palabra buscada
                    texto_resaltado = re.sub(
                        rf'\b({re.escape(meta["palabra_buscada"])})\b',
                        r'<strong>\1</strong>',
                        ctx['texto']
                    )
                    html_content += f"""
                                <div class="contexto-item">
                                    <strong>Mención {i}:</strong><br>
                                    ...{texto_resaltado}...
                                </div>
"""
            else:
                html_content += """
                                <div class="contexto-item">
                                    No hay contextos disponibles.
                                </div>
"""

            html_content += """
                            </div>
                        </td>
                    </tr>
"""
            contador += 1

        # Agregar filas de archivos SIN palabra clave
        for archivo in archivos_sin:
            html_content += f"""
                    <tr data-filter="sin">
                        <td><strong>{contador}</strong></td>
                        <td>{archivo['archivo']}</td>
                        <td><span class="badge badge-danger">✗ NO</span></td>
                        <td><span class="menciones-badge">0</span></td>
                        <td>{archivo['palabras']:,}</td>
                        <td>—</td>
                    </tr>
"""
            contador += 1

        # Top archivos con más menciones
        top_archivos = sorted(archivos_con, key=lambda x: x['total_menciones'], reverse=True)[:10]
        top_labels = [a['archivo'][:30] + '...' if len(a['archivo']) > 30 else a['archivo']
                      for a in top_archivos]
        top_valores = [a['total_menciones'] for a in top_archivos]

        html_content += f"""
                </tbody>
            </table>
        </div>

        <div class="metadata">
            <strong>📂 Directorio analizado:</strong> {meta['directorio']}<br>
            <strong>📅 Fecha de análisis:</strong> {meta['fecha_analisis']}<br>
            <strong>📝 Total palabras procesadas:</strong> {meta['total_palabras']:,}<br>
            <strong>🔍 Palabra buscada:</strong> "{meta['palabra_buscada']}" (búsqueda EXACTA, sensible a mayúsculas)
        </div>

        <footer>
            <p><strong>LexiMus: Léxico y ontología de la música en español</strong></p>
            <p>Universidad de Salamanca | Instituto Complutense de Ciencias Musicales | Universidad de La Rioja</p>
            <p style="margin-top: 10px; font-size: 0.9em;">
                🤖 Generado con <a href="https://claude.com/claude-code" target="_blank">Claude Code</a>
            </p>
        </footer>
    </div>

    <script>
        // Gráfico de Pastel - Presencia/Ausencia
        const ctx1 = document.getElementById('presenciaChart').getContext('2d');
        new Chart(ctx1, {{
            type: 'pie',
            data: {{
                labels: ['Con "{meta['palabra_buscada']}"', 'Sin "{meta['palabra_buscada']}"'],
                datasets: [{{
                    data: [{resumen['archivos_con_palabra']}, {resumen['archivos_sin_palabra']}],
                    backgroundColor: ['#10b981', '#ef4444'],
                    borderWidth: 2,
                    borderColor: '#fff'
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: true,
                plugins: {{
                    legend: {{
                        position: 'bottom',
                        labels: {{
                            font: {{ size: 14 }},
                            padding: 20
                        }}
                    }},
                    tooltip: {{
                        callbacks: {{
                            label: function(context) {{
                                let label = context.label || '';
                                let value = context.parsed || 0;
                                let total = {resumen['archivos_con_palabra'] + resumen['archivos_sin_palabra']};
                                let percentage = ((value / total) * 100).toFixed(1);
                                return label + ': ' + value + ' archivos (' + percentage + '%)';
                            }}
                        }}
                    }}
                }}
            }}
        }});

        // Gráfico de Barras - Top archivos con más menciones
        const ctx2 = document.getElementById('frecuenciaChart').getContext('2d');
        new Chart(ctx2, {{
            type: 'bar',
            data: {{
                labels: {json.dumps(top_labels)},
                datasets: [{{
                    label: 'Menciones de "{meta['palabra_buscada']}"',
                    data: {json.dumps(top_valores)},
                    backgroundColor: '#667eea',
                    borderRadius: 8
                }}]
            }},
            options: {{
                responsive: true,
                indexAxis: 'y',
                scales: {{
                    x: {{
                        beginAtZero: true,
                        ticks: {{
                            stepSize: 1
                        }}
                    }}
                }},
                plugins: {{
                    legend: {{
                        display: false
                    }},
                    tooltip: {{
                        callbacks: {{
                            label: function(context) {{
                                return 'Menciones: ' + context.parsed.x;
                            }}
                        }}
                    }}
                }}
            }}
        }});

        // Función para filtrar tabla
        function filtrarTabla(filtro) {{
            const filas = document.querySelectorAll('#tablaArchivos tbody tr');
            const tabs = document.querySelectorAll('.filter-tab');

            // Actualizar tabs activos
            tabs.forEach(tab => tab.classList.remove('active'));
            event.target.classList.add('active');

            // Filtrar filas
            filas.forEach(fila => {{
                const dataFilter = fila.getAttribute('data-filter');
                if (filtro === 'todos') {{
                    fila.style.display = '';
                }} else if (filtro === dataFilter) {{
                    fila.style.display = '';
                }} else {{
                    fila.style.display = 'none';
                }}
            }});
        }}

        // Función para mostrar/ocultar contexto
        function toggleContexto(id) {{
            const elemento = document.getElementById(id);
            if (elemento.classList.contains('visible')) {{
                elemento.classList.remove('visible');
            }} else {{
                elemento.classList.add('visible');
            }}
        }}

        // Búsqueda en tabla
        document.getElementById('searchInput').addEventListener('keyup', function() {{
            const filtro = this.value.toLowerCase();
            const filas = document.querySelectorAll('#tablaArchivos tbody tr');

            filas.forEach(fila => {{
                const archivo = fila.cells[1].textContent.toLowerCase();
                if (archivo.includes(filtro)) {{
                    fila.style.display = '';
                }} else {{
                    fila.style.display = 'none';
                }}
            }});
        }});
    </script>
</body>
</html>
"""

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)

        print(f"✅ Web interactiva generada: {output_file}")
        return output_file


# ==========================================================================
# FUNCIÓN PRINCIPAL
# ==========================================================================

def main():
    """
    Ejecuta el análisis completo de palabra clave

    Uso:
        python3 buscador_palabras_clave.py /ruta/a/tus/archivos/txt
    """
    # Verificar argumentos de línea de comandos
    if len(sys.argv) < 2:
        print("❌ ERROR: Debes especificar la ruta al directorio con archivos TXT")
        print("\nUso:")
        print("  python3 buscador_palabras_clave.py /ruta/a/tus/archivos/txt")
        print("\nEjemplo:")
        print("  python3 buscador_palabras_clave.py ~/Desktop/MisRevistas")
        print("\n⚠️  IMPORTANTE: No olvides modificar la palabra clave en el archivo")
        print("   Edita la línea 31 del script para cambiar la palabra a buscar")
        sys.exit(1)

    directorio_base = sys.argv[1]

    # Verificar que el directorio existe
    if not os.path.exists(directorio_base):
        print(f"❌ ERROR: El directorio no existe: {directorio_base}")
        sys.exit(1)

    if not os.path.isdir(directorio_base):
        print(f"❌ ERROR: La ruta no es un directorio: {directorio_base}")
        sys.exit(1)

    print("🔍 BUSCADOR DE PALABRA CLAVE EN CORPUS TEXTUAL")
    print("="*80)
    print(f"📂 Directorio: {directorio_base}")
    print(f"🔎 Palabra clave: \"{PALABRA_CLAVE}\" (búsqueda EXACTA)\n")

    # Inicializar buscador
    buscador = BuscadorPalabrasClave(directorio_base, PALABRA_CLAVE)

    # Ejecutar análisis
    resultados = buscador.analizar_directorio()

    # Guardar resultados
    buscador.guardar_resultados('resultados_busqueda.json')
    buscador.generar_web_interactiva('resultados_busqueda.html')

    # Imprimir resumen
    print("\n" + "="*80)
    print("✅ ANÁLISIS COMPLETADO")
    print("="*80)
    resumen = resultados['resumen_general']
    print(f"📄 Total archivos: {resultados['metadata']['total_archivos']}")
    print(f"✅ Archivos con '\"{PALABRA_CLAVE}\"': {resumen['archivos_con_palabra']} ({resumen['porcentaje_con_palabra']}%)")
    print(f"❌ Archivos sin '\"{PALABRA_CLAVE}\"': {resumen['archivos_sin_palabra']} ({resumen['porcentaje_sin_palabra']}%)")
    print(f"📊 Total menciones: {resumen['total_menciones']}")
    print(f"📈 Frecuencia: {resumen['frecuencia_por_millon_palabras']} menciones por millón de palabras")
    print(f"\n📁 Archivos generados:")
    print(f"   - resultados_busqueda.html (🌐 página web interactiva)")
    print(f"   - resultados_busqueda.json (datos completos)")


if __name__ == "__main__":
    main()
