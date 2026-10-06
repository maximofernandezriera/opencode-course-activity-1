# Actividad 1 — CLI `wordcount` con OpenCode

> **Para la corrección:** [leer las respuestas de reflexión en `RESPUESTAS.md`](RESPUESTAS.md).

Este repositorio contiene la entrega completa del ejercicio: la aplicación CLI
`wordcount`, sus pruebas, la consigna y rúbrica, y los registros de las dos
sesiones usadas durante el trabajo.

## Contenido

- [`RESPUESTAS.md`](RESPUESTAS.md): respuestas a las preguntas de reflexión.
- [`wordcount/`](wordcount/): aplicación Python con Typer, datos de ejemplo y
  suite de pruebas.
- [`docs/activity-1.md`](docs/activity-1.md): consigna del ejercicio.
- [`docs/rubrica_ Actividad de la sesión 1 _ fweib.pdf`](docs/rubrica_%20Actividad%20de%20la%20sesi%C3%B3n%201%20_%20fweib.pdf): rúbrica de evaluación.
- [`docs/sessions/`](docs/sessions/): exportaciones Markdown de las dos
  sesiones de OpenCode.

## Ejecutar la aplicación

Desde la carpeta de la aplicación, instala el proyecto y ejecútalo:

```sh
cd wordcount
python -m pip install '.[dev]'
wordcount -l loremipsum.txt
wordcount -w loremipsum.txt
wordcount -m loremipsum.txt
wordcount -l -w -m loremipsum.txt
```

La CLI también acepta `-c` para contar bytes. Sin opciones muestra líneas,
palabras y bytes por defecto. Encontrarás más ejemplos en
[`wordcount/README.md`](wordcount/README.md).

## Pruebas y cobertura

```sh
cd wordcount
pytest
```

La configuración de pytest exige al menos un 90 % de cobertura. La suite
verificada para esta entrega reportó **51 pruebas aprobadas y 100 % de
cobertura de líneas y ramas**.
