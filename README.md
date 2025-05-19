<table style="border-collapse: collapse; width: 100%; border: 1px solid black;">
    <tr>
        <td style="border: 1px solid black; text-align: center;">
            <img src="https://unisallevirtual.lasalle.edu.co/pluginfile.php/1/theme_remui/loaderimage/1740446401/lasalle60a%C3%B1os.png" width="500"/>
        </td>
        <td style="border: 1px solid black; text-align: center;">
            <h2 style="font-size:160%;">Actividad 4: Aplicación web interactiva para el análisis de mortalidad en Colombia</h2>
            <p style="font-size:130%;">Aplicaciones I</p>
            <p style="font-size:130%;">Prof. Cristian Duney Bermudez Quintero</p>
        </td>        
        <td style="border: 1px solid black; text-align: center;">
            <h3 style="font-size:160%;">Estudiantes:</h3>
            <p style="font-size:130%;">Santiago González Cruz</p>
          <p style="font-size:130%;">Ángel Andrés Bonilla Bonilla</p>
        </td>
    </tr>
    <tr>
        <td colspan="3" style="border: 1px solid black; text-align: center; padding: 15px;">
            <h3>Unidad 2: Aplicación web con dashborad interactivo en Python</h3>
        </td>
    </tr>
</table>

# Tabla de Contenido

- [Introducción](#1)
- [Objetivo](#2)
- [Estructura del proyecto](#3)
- [Software](#4)
- [Conceptos](#5)
- [Análisis de mortalidad en Colombia 2019](#6)
- [Conclusiones](#7)
- [Referencias](#8)

<a name="1"></a>
# Introducción

La visualización interactiva de datos se ha convertido en un componente esencial para transformar conjuntos de información complejos en narrativas comprensibles y accionables. Herramientas como Plotly, especializada en la creación de gráficos dinámicos, y Dash, framework que facilita el desarrollo de aplicaciones web interactivas, permiten a científicos de datos y desarrolladores integrar análisis avanzado con experiencias de usuario ricas y accesibles (AI Planet, s. f.; Daniel, 2024). La elección de estas tecnologías se potencia al emplear Python, un lenguaje de propósito general que, gracias a su sintaxis simple y a su vasto ecosistema de bibliotecas, ha escalado hasta el segundo lugar de popularidad entre los programadores (O’Grady, 2021; Staff, 2023). Para llevar estas aplicaciones a producción con agilidad y bajo costo, plataformas en la nube como Render ofrecen flujos de despliegue sin fricciones y un nivel gratuito que resulta especialmente atractivo para estudiantes e investigadores (Manaktala, 2024).

En este contexto, el presente informe emplea un stack basado en Python + Plotly + Dash, desplegado en Render, para analizar la mortalidad registrada en Colombia durante 2019. A través de una serie de visualizaciones gráficos de líneas, barras apiladas, mapas de dispersión y diagramas circulares se exploran patrones temporales, concentraciones geográficas y disparidades territoriales, con el propósito de identificar tendencias clave y generar evidencia que oriente la planificación sanitaria. La combinación de estas herramientas no solo optimiza el procesamiento y la representación de los datos, sino que también democratiza el acceso a los resultados, proporcionando a responsables de políticas y público en general una plataforma interactiva y transparente para la toma de decisiones informadas.

<a name="2"></a>
# Objetivo
El objetivo de este proyecto es desarrollar una aplicación web interactiva de análisis de mortalidad en Colombia para el 2019 utilizando **Dash**. Se utilizarán herramientas de control de versiones como **Git** en Visual Studio Code para gestionar el código de manera eficiente. El proyecto es cargado en **GitHub** para su almacenamiento remoto. Finalmente, la aplicación será desplegada en Render, asegurando su ejecución de manera segura y accesible en la web. 

<a name="3"></a>
# Estructura del proyecto
```bash
project-root/
├── Data/                       # Carpeta que contiene los datos a analizar
├── src/                        # Carpeta que contiene el código fuente
    └── app.py                  # Código principal de la aplicación Dash
        └── server = app.server # Exposición del servidor Flask utilizado por Dash
├── render.yaml                 # Archivo de configuración de Render
├── requirements.txt            # Dependencias necesarias para la aplicación
└── README.md                   # Documentación del proyecto
```
<a name="4"></a>
# Software

**Requisitos**
1. Python 3.11.x
2. Visual Studio Code
3. Bibliotecas necesarias:
   ```
    - asttokens==3.0.0
      └─ executing>=2.2.0,<3.0        
    - attrs==25.3.0
    - blinker==1.9.0
    - certifi==2025.4.26
    - charset-normalizer==3.4.2
    - click==8.2.0
      └─ colorama>=0.4 
    - comm==0.2.2
      └─ traitlets>=4      
    - dash==3.0.4
          ├─ Flask>=1.0.4
          ├─ Jinja2<4
          ├─ Werkzeug<3
          ├─ plotly>=5.0.0
          ├─ dash-core-components==2.0.0
          ├─ dash-html-components==2.0.0
          └─ dash-table==5.0.0
    - debugpy==1.8.14    
    - decorator==5.2.1
    - et_xmlfile==2.0.0
    - executing==2.2.0
    - fastjsonschema==2.21.1
    - Flask==3.0.3
          ├─ Werkzeug>=3.0.0
          ├─ Jinja2>=3.1.2
          ├─ itsdangerous>=2.2.0
          ├─ click>=8.1.3
          ├─ blinker>=1.6.2
    - geopandas==1.0.1
          ├─ pandas>=1.5
          ├─ shapely>=2
          ├─ fiona>=1.9
          ├─ pyproj>=3.1
          └─ packaging
    - gunicorn==23.0.0
          ├─ packaging
    - idna==3.10
    - ipykernel==6.29.5
          ├─ comm>=0.1.1
          ├─ jupyter_client>=7.4.9
          ├─ traitlets>=5.16
          ├─ tornado>=6.4
          ├─ matplotlib-inline>=0.1
          ├─ psutil
          ├─ debugpy>=1.6.5
          ├─ pyzmq>=25
          ├─ nest-asyncio>=1.5.6
          └─ pygments>=2.4.0 
    - ipython==9.2.0
          ├─ jedi>=0.16
          ├─ prompt_toolkit>=3.0.30,<3.1
          ├─ traitlets>=5
          ├─ pygments>=2.4.0
          ├─ decorator
          ├─ backcall
          ├─ matplotlib-inline
          └─ stack-data
    - ipython_pygments_lexers==1.1.1
          └─ Pygments>=2.18
    - itsdangerous==2.2.0
    - jedi==0.19.2
      └─ parso==0.8.4
    - Jinja2==3.1.6
      └─ MarkupSafe>=2.1
    - jsonschema==4.23.0
          ├─ attrs>=22.2.0
          ├─ jsonschema-specifications>=2023.03.6
          ├─ referencing>=0.28.4
          └─ rpds-py>=0.7.1                
    - jsonschema-specifications==2025.4.1
      └─ referencing>=0.35.0
    - jupyter_client==8.6.3
          ├─ python-dateutil>=2.8.2
          ├─ pyzmq>=25
          ├─ tornado>=6.2
          ├─ traitlets>=5.3
          └─ jupyter_core>=5.1.0  
    - jupyter_core==5.7.2
          ├─ platformdirs>=2.5
    - MarkupSafe==3.0.2
    - matplotlib-inline==0.1.7
          └─ traitlets
    - narwhals==1.39.0
          ├─ numpy>=1.18
          ├─ pandas>=1.3
          ├─ pyarrow>=11
          └─ typing_extensions>=4
    - nbformat==5.10.4
          ├─ fastjsonschema
          ├─ jsonschema>=2.6
          ├─ jupyter_core>=5.4
          ├─ traitlets>=5.7
          └─ attrs>=23
    - nest-asyncio==1.6.0
    - numpy==2.2.5
    - openpyxl==3.1.5
          └─ et-xmlfile
    - packaging==25.0
    - pandas==2.2.2
          ├─ numpy>=1.24
          ├─ python-dateutil>=2.8.2
          ├─ pytz>=2020.1
          └─ tzdata>=2022.1
    - parso==0.8.4
    - platformdirs==4.3.8
    - plotly==6.0.1
          └─ tenacity>=6.2
    - prompt_toolkit==3.0.51
      └─ wcwidth
    - psutil==7.0.0
    - pure_eval==0.2.3
    - Pygments==2.19.1 
    - pyogrio==0.11.0
          ├─ numpy>=1.22
          ├─ pandas>=1.4
          ├─ pyarrow>=11
          ├─ shapely>=2
          └─ fsspec>=2021.5
    - pyproj==3.7.1
          ├─ certifi>=2023.1
          └─ numpy    
    - python-dateutil==2.9.0.post0
          └─ six>=1.5
    - pytz==2025.2
    - pywin32==310    
    - pyzmq==26.4.0    
    - referencing==0.36.2
          ├─ attrs>=23.1
          └─ rpds-py>=0.7.1
    -requests==2.32.3
          ├─ charset-normalizer>=2,<4
          ├─ idna>=2.5,<4
          ├─ urllib3>=2.0,<3
          └─ certifi>=2017.4.17
    - retrying==1.3.4
    - rpds-py==0.24.0    
    - shapely==2.1.0
          └─ numpy
    - six==1.17.0    
    - stack-data==0.6.3
          ├─ asttokens>=2.1.0
          ├─ pure_eval
          ├─ executing>=1.2.0
          └─ pygments>=2.4.0
    - tornado==6.4.2    
    - traitlets==5.14.3
          ├─ decorator
          └─ typing_extensions *solo si Python<3.11*
    - typing_extensions==4.13.2    
    - tzdata==2025.2    
    - urllib3==2.4.0    
    - wcwidth==0.2.13    
    - Werkzeug==3.0.6
          └─ MarkupSafe>=2.1.3
    - zipp==3.21.0
   ```
<a name="5"></a>
# Conceptos
Plotly es una biblioteca para visualizar datos, mientras que Dash es un framework para crear aplicaciones web interactivas (Introducción A Plotly y Dash | AI Planet (Formerly DPhi), s. f.). Plotly se centra en la creación de gráficos y visualizaciones, y Dash utiliza Plotly para permitir a los científicos de datos y desarrolladores de Python construir aplicaciones web que integren visualizaciones y lógica de análisis de datos (Daniel, 2024). 

Por otra parte, Python es un lenguaje de programación ampliamente utilizado en el desarrollo de sitios web y software, así como en la automatización de tareas y el análisis de datos. Considerado un lenguaje de propósito general (Staff, 2023), permite la creación de una amplia gama de programas y no se limita a resolver problemas específicos. Esta versatilidad, combinada con su accesibilidad para los principiantes, ha llevado a que Python se convierta en uno de los lenguajes de programación más populares en la actualidad. De hecho, una encuesta realizada por la empresa de análisis del sector RedMonk reveló que en 2021 ocupó el segundo lugar entre los lenguajes de programación preferidos por los desarrolladores (O’Grady, 2021).
Python es una herramienta ampliamente utilizada en el desarrollo de sitios web y software, así como en la automatización de tareas, el análisis de datos y la visualización de información. Su facilidad de aprendizaje ha llevado a que muchos profesionales que no son programadores, como contables y científicos, lo adopten para realizar diversas tareas cotidianas, incluyendo la organización de sus finanzas (Staff, 2023).

Finalmente, Render es una plataforma en la nube orientada a facilitar el paso de las aplicaciones a producción de manera rápida y sencilla. Permite construir, desplegar y escalar proyectos sin fricciones, desde los primeros usuarios hasta escenarios de gran volumen. A diferencia de proveedores como AWS, GCP o Azure, Render dispone de un nivel gratuito que no requiere tarjeta de crédito, lo que la convierte en una alternativa especialmente atractiva para estudiantes y desarrolladores que desean experimentar o lanzar sus ideas sin restricciones económicas (Manaktala, 2024).

<a name="6"></a>
# Análisis de mortalidad en Colombia 2019

## 1. Gráfico de líneas: Total de muertes por mes
La serie temporal mensual revela que los departamentos con mayor carga de mortalidad en 2019 son Santafé de Bogotá, D. C., Antioquia y Valle del Cauca. El comportamiento de las tres curvas es muy similar: tras iniciar el año con valores elevados, se aprecia una caída conjunta en febrero (el punto más bajo del periodo) y, posteriormente, una tendencia ascendente hasta alcanzar el máximo en septiembre. Esta sincronía sugiere que factores estacionales o eventos de alcance nacional influyeron de forma homogénea sobre los tres territorios. En el caso de Santafé de Bogotá, febrero registró 2.850 fallecimientos, mientras que septiembre alcanzó 3.386, lo que representa un incremento cercano al 19 % entre ambos meses.

![Image](https://github.com/user-attachments/assets/e7fa5edd-b811-4878-8c37-a9d8cee00a60)
Figura 1. Muertes por departamento (fuente: https://analisis-de-mortalidad-en-colombia-2019.onrender.com).

![Image](https://github.com/user-attachments/assets/004f4b2b-6c3b-40a8-8367-f30ed724f84e)
Figura 2. Muertes para el departemento de Santafé de Bogotá, D. C (fuente: https://analisis-de-mortalidad-en-colombia-2019.onrender.com).

## 2. Gráfico de barras apiladas: Las cinco ciudades con mayor mortalidad total
El análisis de los cinco municipios con más defunciones muestra que Bogotá D. C. (≈ 38.800), Medellín (≈ 19.100), Cali (≈ 18.000), Cúcuta (≈ 5.700) y Pereira (≈ 5.100) concentran una parte sustancial de las muertes registradas en el país. En los cinco casos la causa predominante es la muerte natural, con valores de 35.295 en Bogotá, 17.451 en Medellín, 15.787 en Cali, 5.095 en Cúcuta y 4.609 en Pereira. Las defunciones por causas externas (accidentales, violentas o indeterminadas) constituyen, por tanto, una fracción menor, pero siguen siendo relevantes para las autoridades sanitarias y de seguridad, sobre todo en las tres primeras ciudades donde la densidad poblacional amplifica el impacto absoluto de estos eventos.

![Image](https://github.com/user-attachments/assets/4b3ac99f-eb73-4c8c-9f7d-6d3841fb0a70)

Figura 3. Top 5 de ciudades con mayor mortalidad total (fuente: https://analisis-de-mortalidad-en-colombia-2019.onrender.com).

## 3. Gráfico de dispersión geográfica: Distribución total de muertes por departamento
La visualización cartográfica confirma la supremacía de Santafé de Bogotá D. C. (38.760 muertes), Antioquia (34.473) y Valle del Cauca (28.443), cuyos círculos sobresalen en tamaño sobre el mapa. La concentración de fallecimientos en estas tres jurisdicciones coincide con lo observado en la serie temporal (Figura 1) y refleja tanto su peso demográfico como la complejidad de sus entornos urbanos. Las diferencias respecto al resto de departamentos son claras: los círculos de segundo orden, aun siendo significativos por ejemplo, Atlántico o Cundinamarca, se encuentran muy por debajo del nivel de los tres líderes.

![Image](https://github.com/user-attachments/assets/406969e4-8404-45d6-8cda-0a100726c097)

Figura 4. Distribución total de muertes por departamento (fuente: https://analisis-de-mortalidad-en-colombia-2019.onrender.com).

## 4. Gráfico de torta: Diez municipios con menor mortalidad
El diagrama circular ilustra que los diez municipios con el índice de mortalidad más bajo Hato, Alto Baudó, Restrepo, Mapiripana, Albán, Margarita, San Fernando, La Tola, Bituima y Jericó registraron una sola muerte cada uno durante 2019. Debido a la igualdad absoluta en el número de casos, cada sector representa exactamente el 10 % del total del gráfico. Este hallazgo pone de relieve la marcada disparidad territorial: mientras que en las grandes capitales se registran decenas de miles de defunciones, en ciertos municipios rurales o de baja densidad poblacional la mortalidad puede reducirse a un solo evento anual, lo que plantea desafíos distintos para la planificación sanitaria y la asignación de recursos.

![Image](https://github.com/user-attachments/assets/5801d1e0-41a1-4e98-a0fe-08b612abbaf8)

Figura 5. Municipios con menor índice de mortalidad (fuente: https://analisis-de-mortalidad-en-colombia-2019.onrender.com).

## 5. Tabla: Listado de las 10 principales causas de muerte en Colombia
El analisis de El análisis de mortalidad en Colombia en 2019 revela que las principales causas de fallecimiento incluyen enfermedades cardiovasculares como infarto agudo del miocardio y hipertensión esencial, enfermedades respiratorias como la EPOC y neumonía, así como varios tipos de cáncer, destacándose los malignos del estómago, pulmón, mama y próstata. Además, las lesiones por violencia, especialmente por arma de fuego, representan una causa significativa de mortalidad en el país.

![image](https://github.com/user-attachments/assets/172ca450-99af-4a1e-97ae-5f81027bb1ba)

## Puntos clave
• Las enfermedades cardiovasculares, particularmente el infarto agudo del miocardio, son una de las principales causas de muerte en Colombia en 2019.
• La hipertensión esencial (primaria) también contribuye significativamente a la mortalidad, indicando una alta prevalencia de riesgos cardiovasculares.
• Las enfermedades respiratorias, como la EPOC y neumonía, representan una carga importante en las muertes del año.
• Los cánceres, específicamente de estómago, pulmón, mama y próstata, lideran las causas oncológicas de mortalidad.
• Lesiones por agresión con armas de fuego son una causa relevante de mortalidad, relacionadas con la violencia en el país.


## 6. Histograma: Distribución de muertes por rango de edad
Se presenta la distribución de muertes agrupadas por rangos de edad de cinco años, desde 0-4 años hasta 85 años o más. Los datos indican cuántas personas fallecieron en cada grupo de edad, con una escala que va desde 0 hasta 120,000 muertes. La tabla muestra cómo varía la cantidad de muertes según la edad, lo que ayuda a entender cuáles grupos etarios tienen mayor mortalidad.




## 7. Gráfico de barras apiladas: Comparación de muertes por sexo y departamento
Se presenta la distribución de muertes en diferentes departamentos del país, diferenciadas por sexo (hombres y mujeres). Los datos muestran cuántas personas fallecieron por sexo en cada departamento, con un rango que llega hasta 40,000 muertes. Esto permite entender en qué regiones y segmentos de sexo se concentran más las muertes, ayudando a identificar posibles desigualdades o áreas de mayor impacto.




<a name="7"></a>
# Conclusiones 
1. La mayor carga de defunciones en 2019 se concentró en tres territorios Santafé de Bogotá D. C., Antioquia y Valle del Cauca que, en conjunto, representaron más de una cuarta parte de las muertes del país. Esta concentración refleja tanto su peso demográfico como la complejidad de sus ambientes urbanos y subraya la necesidad de políticas sanitarias diferenciadas que contemplen la magnitud y especificidad de estos entornos metropolitanos.

2. La caída simultánea de los fallecimientos en febrero, seguida de un aumento sostenido hasta septiembre, indica la existencia de factores estacionales o coyunturales de alcance nacional que afectan de forma homogénea a los principales departamentos. Identificar estos factores permitiría programar intervenciones preventivas en los periodos de mayor riesgo y optimizar la distribución temporal de recursos.

3. En las ciudades con mayor mortalidad, las muertes naturales superan ampliamente a las violentas o accidentales, aunque estas últimas siguen siendo significativas en términos absolutos. Esto sugiere que las estrategias de salud pública deben priorizar la prevención y el manejo de enfermedades crónicas sin descuidar las políticas de seguridad y reducción de riesgos externos.

4. La coexistencia de municipios que registran una sola muerte al año con capitales que superan las 30.000 revela una disparidad sanitaria y demográfica marcada. Mientras que los centros urbanos requieren estrategias de gran escala y alta complejidad, los municipios de baja mortalidad podrían beneficiarse más de acciones focalizadas y programas de vigilancia epidemiológica simplificados.

5. La evidencia sugiere que la asignación de recursos debe considerar tanto la magnitud absoluta de la mortalidad como sus causas principales y su distribución temporal. En los departamentos líderes, se recomienda reforzar la capacidad hospitalaria y los programas de enfermedades crónicas; en los municipios de baja incidencia, garantizar la accesibilidad a servicios básicos y el fortalecimiento de la notificación de eventos de salud.

<a name="8"></a>
# Referencias
* Introducción a Plotly y Dash | AI Planet (formerly DPhi). (s. f.). AI Planet (Formerly DPhi). https://aiplanet.com/learn/data-visualization-with-plotly-and-dash-es/introduccion-a-plotly-y-dash/1806/introduccion-a-plotly-y-dash
* Daniel. (2024, 22 noviembre). Dash para Python: ¿Qué es? ¿Cómo funciona? DataScientest. https://datascientest.com/es/dash-para-python-que-es#:~:text=Dash%20es%20un%20marco%20de,datos%20y%20desarrolladores%20de%20Python.
* Manaktala, P. (2024, 29 noviembre). Deploying a Spring Boot Application on Render - Parth Manaktala - Medium. Medium. https://medium.com/@pmanaktala/deploying-a-spring-boot-application-on-render-4e757dfe92ed
* O’Grady, S. (2021, 5 agosto). The RedMonk Programming Language rankings: June 2021. Tecosystems. https://redmonk.com/sogrady/2021/08/05/language-rankings-6-21/ 
* Staff, C. (2023, 29 noviembre). ¿Qué es Python y para qué se usa? Guía para principiantes. Coursera. https://www.coursera.org/mx/articles/what-is-python-used-for-a-beginners-guide-to-using-python 

