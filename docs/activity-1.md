# Construir una herramienta en el entorno de OpenCode

Utiliza un agente de IA para construir desde cero una pequeña aplicación de línea de comandos inspirada en Unix `wc`.

La herramienta se llamará `wordcount`.

El objetivo es practicar y evaluar interacciones simples trabajadas en el taller.

### 1. Diseña la aplicación

En una primera sesión, pide al agente que diseñe la aplicación utilizando el modo de planificación.

El diseño debe contemplar:

- Una CLI basada en **Typer** o una biblioteca equivalente.

- Opciones para contar líneas, palabras y caracteres.

- Una semántica de opciones inspirada en `wc`.

- Un comportamiento definido para el caso en que no se especifique ninguna opción.

Antes de implementar, abre **una nueva sesión** y pregunta al agente qué lenguaje utilizaría para desarrollar la aplicación y por qué. Después, vuelve a la sesión original.

### 2. Implementa y prueba

Implementa la aplicación con ayuda del agente.

Pídele que:

- escriba las pruebas necesarias;

- analice la cobertura;

- aumente la cobertura hasta alcanzar **al menos el 90 %**.

No es necesario reproducir todas las funcionalidades de `wc`.

### 3. Documenta la ejecución

Incluye un fichero `loremipsum.txt` en el proyecto y pide al agente que prepare unas instrucciones breves de ejecución.

El `README` debe mostrar ejemplos para contar:

- líneas;

- palabras;

- caracteres;

- varias métricas simultáneamente.

### 4. Reflexiona brevemente

Al terminar, responde:

- ¿Qué información perdió el agente al comenzar una nueva sesión?

- ¿Qué decisiones tomaste junto con el agente?

- ¿Qué utilidad tuvo el modo de planificación?

- ¿Qué aportó el análisis de cobertura?

### Entrega

Repositorio con el código (o un archivo ZIP) y la sesión de OpenCode exportada.
