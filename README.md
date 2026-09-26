Aplicación web interactiva diseñada para el análisis de rendimiento académico a nivel medio superior y la evaluación de algoritmos de procesamiento de datos. Construido con un enfoque en Ciencia de Datos, el sistema incluye un módulo de Cómputo de Alto Desempeño (CAD) que mide y compara la eficiencia de la limpieza y normalización de grandes volúmenes de datos (más de 230,000 registros) utilizando métodos iterativos manuales frente a implementaciones vectorizadas.

## Características Principales
- Diagnóstico y Normalización de Datos
- Métricas de Rendimiento (CAD)
- Visualización Interactiva

## Tecnologías Utilizadas
- Python 3.14
- Streamlit
- Pandas
- Plotly
- Time

## Instalación y Ejecución
1. Clonar el repositorio
    git clone https://github.com/jmendez-git/clean-data-app.git

2. Crear y activar un entorno virtual
    python -m venv venv
    - En Windows:
        venv\Scripts\activate
    - En macOS/Linux:
        source venv/bin/activate

3. Instalar las dependencias
    pip install -r requirements.txt

4. Ejecutar la aplicación
    streamlit run app.py

## Flujo de Uso
    1. Cargar Datos: Subir el archivo CSV crudo desde el panel lateral.

    2. Normalización: Revisar el reporte de limpieza, valores faltantes y el    justificado de decisiones metodológicas.

    3. Análisis CAD: Navegar a "Rendimiento", definir el número de repeticiones y ejecutar la prueba de estrés para observar las métricas comparativas.

    4. Salud Académica: Explorar los gráficos interactivos de desempeño estudiantil e institucional.