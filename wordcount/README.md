# wordcount

Una pequeña CLI en Python inspirada en `wc`, implementada con Typer.

## Instalar

```sh
python -m pip install .
```

Para instalar también las dependencias de desarrollo:

```sh
python -m pip install '.[dev]'
```

## Ejemplos de uso

```sh
# Contar líneas
wordcount -l loremipsum.txt

# Contar palabras
wordcount -w loremipsum.txt

# Contar caracteres Unicode
wordcount -m loremipsum.txt

# Contar varias métricas en una sola invocación
wordcount -l -w loremipsum.txt
wordcount -l -w -m loremipsum.txt

# También se pueden contar bytes
wordcount -c loremipsum.txt
wordcount -l -w -m -c loremipsum.txt

# Procesar varios archivos o leer desde stdin
wordcount -l -w archivo1.txt archivo2.txt
cat loremipsum.txt | wordcount
```

Sin opciones de conteo, `wordcount loremipsum.txt` muestra líneas, palabras y
bytes. Si se especifican opciones, muestra únicamente las métricas elegidas.
`-` indica entrada estándar; al procesar varios operandos también se muestra
una fila `total`.

## Pruebas y cobertura

```sh
pytest
```

La configuración exige al menos un 90% de cobertura; la suite actual reporta
cobertura de ramas y líneas.
