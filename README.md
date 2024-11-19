# Administrador Hosting Web - ASO
Proyecto de aplicación de sistemas operativos

## Descargar Python

1. Descargar e instalar Python de la página oficial

[Descargar Python 3.12](https://www.python.org/downloads/release/python-3127/)

2. Verificar versión de python
```
python3 --version
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
## Guía de uso
En caso de que el host sea una nueva máquina y no tiene instalado las dependencias necesarias, puede realizarlo con los botones en la parte superior.

![image](https://github.com/user-attachments/assets/95f3a523-b460-4614-a043-433deca8323b)

### Crear nuevo usario
Todos los campos son obligatorios.

![image](https://github.com/user-attachments/assets/7b8a1b6b-bfcc-4dd5-a77c-22228fab4b06)

### Listar usuarios
Al presionar el boton Listar usuarios sale una ventana con los usuarios existentes.

![image](https://github.com/user-attachments/assets/36e28825-b355-4eb4-8636-71b55410ef46)

### Editar usuarios
Al presionar Editar usuario sale una ventana donde podrá poner el nombre del usuario que desea editar, presionar el boton Editar y realizar los cambios correspondientes.

![image](https://github.com/user-attachments/assets/128a090e-2bcd-43b5-8518-c36818fb9a4c)

### Eliminar usuario
Al presionar Eliminar usuario sale una ventana donde podrá poner el nombre del usuario que desea eliminar, presiona eliminar y debe confirmar su acción. 

![image](https://github.com/user-attachments/assets/7c64186e-5646-4180-89df-944def6459f2)

