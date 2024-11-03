# RadarServer
Servidor utilizado para la práctica guiada 3 y la práctica entregable 3 de la 
asignatura Software Avanzado Radar (SARA) del Master de Formación Permanente en 
Radar (MSRA).

## Arranque del servidor
Para arrancar el servidor lo primero que necesitamos es un entorno virtual con 
las dependencias del fichero `requirements.txt` instaladas.

Una vez instaladas las dependencias y dentro del entorno virtual ejecutamos el 
siguiente comando:
```
fastapi dev app/main.py
```

Cuando el servidor está arrancado de forma correcta podemos visitar las 
siguientes direcciones para comprobar el correcto funcionamiento.
- Página raíz: http://127.0.0.1:8000
- Página de documentación API: http://127.0.0.1:8000/docs
