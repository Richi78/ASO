# Administrador Hosting Web - ASO
Proyecto de aplicación de sistemas operativos

## Descargar Python

1. Descargar e instalar Python de la página oficial

[Descargar Python 3.12](https://www.python.org/downloads/release/python-3127/)

2. Verificar versión de python
```
python --version
```

## Instalar las dependencias
```
pip3 install -r requirements.txt
```
Tambien puede utilizar un entorno virtual de python, instalación de las dependencias es lo mismo.
## Ejecutar el programa
Se lo debe realizar en modo root (con privilegios).
1. En el directorio donde se encuentra el proyecto ejecutar. 
  ```
  python3 singleton.py
  ```
2. Otra alternativa.
Dar permisos de ejecución al file singleton.py.
```
chmod 777 singleton.py
```
Ejecutar el archivo singleton.py como si fuera un binario.
```
./singleton.py
```
## Otros
En caso de que el host sea una nueva máquina y no tiene instalado las dependencias necesarias, puede realizarlo con los botones en la parte superior.

![image](https://github.com/user-attachments/assets/95f3a523-b460-4614-a043-433deca8323b)
