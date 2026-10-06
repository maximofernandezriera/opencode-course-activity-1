# Reflexión sobre el ejercicio

- **¿Qué información se perdió al empezar una sesión nueva?**  
  Cada sesión tenía su propio contexto. En la primera quedó el diseño inicial de la CLI con Typer; en la otra, la comparación de lenguajes —Rust, Go, Python y C— y la idea de elegir según el proyecto y el entorno. Al cambiar de sesión, no se conservaban automáticamente esas decisiones ni el hilo de la conversación.

- **¿Qué decisiones tomamos juntos?**  
  Para la implementación seguimos con **Python y Typer**. Acordamos una semántica inspirada en `wc`: `-l` para líneas, `-w` para palabras, `-m` para caracteres, `-c` para bytes; por defecto, líneas, palabras y bytes. También definimos lectura de archivos y stdin, totales para varios archivos, manejo de errores y una meta de cobertura de al menos el 90%. Después añadimos `loremipsum.txt` y ejemplos al README.

- **¿Para qué sirvió el modo de planificación?**  
  Para acordar alcance, estructura y pruebas antes de tocar el código. Así quedó claro qué debía hacer la herramienta y qué condiciones usaríamos para considerar terminada la implementación.

- **¿Qué aportó medir la cobertura?**  
  Dio una medida verificable de qué partes del código ejecutaban las pruebas y ayudó a detectar problemas reales: hubo pruebas fallidas de conteo y del CLI que hubo que corregir. La suite terminó con **51 pruebas aprobadas y 100% de cobertura de líneas y ramas**, superando el mínimo solicitado del 90%.
