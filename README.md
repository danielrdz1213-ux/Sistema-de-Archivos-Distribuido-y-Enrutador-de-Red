# Bitacora

## Mariano


Semana 1:

Mariano: En grupo realizamos una breve llamada grupal para distrubir el trabajo del proyecto.

Semana 2:

Mariano: Una vez con todo ya bien divido se comezó a trabajar en el código, con ayuda de la IA se logró implementar el módulo 2 (la parte del trabajo que me correspondía), se concluyó con creación e implementación de la tabla hash y los nodos de los usuarios que irán dentro de ella, con sus respectivos métodos y la parte más importante, la fórmula de dispersión polinomial de la tabla hash

Semana 3:

Mariano: Una vez con cada módulo concluído se procede a afinar detalles en el código, como acomodar bloques de código y detalles en la consola para mantener ordenado el proyecto, además de eso se procedió a comentar el código para su mayor comprensión.

Pronts:

Ayuda a realizar la tabla hash de este proyecto, mi parte es el modulo 2 (claude) Quiero que cuando el usuario digite la contrasena, solo se muestren asterizcos (cline) Quiero que realizes pruebas de cada menu para ver si funcionan correctamente (cline) Explícame detalladamente la tabla hash, entiendo comofunciona, pero el método para redimensionar y una fórmula que viene ahí no entiendo para que es (claude)
---

## Kendall

## Prompt 1. Creación de la estructura inicial del sistema de archivos

- **Prompt:** "Actúa como un desarrollador experto en Python y Estructuras de Datos. Vamos a construir el Módulo 1 de un Sistema de Archivos Distribuido, el cual simula el disco duro de un servidor usando una estructura de datos de Árbol." Pediste la clase **Nodo** (tipo, nombre, lista de hijos, referencia al padre) y la clase **FileSystem** que en su constructor cree el nodo raíz "/" de tipo Carpeta. "No implementes menús, ni algoritmos de búsqueda o eliminación todavía… Entrega únicamente el código de estas dos clases usando tipado estático (type hints) y buenas prácticas de Python, listo para ser expandido en futuros pasos."

- **Acción del sistema:** Creó el paquete `sistema_archivos/` con `nodo.py` (clase Nodo + enum TipoNodo y type hints), `file_system.py` (FileSystem con raíz "/", `directorio_actual` y `esta_vacio`) e `__init__.py`. Lo validó con un script temporal de pruebas que después eliminó y mostró el código de las dos clases.

- **Observación:** funcionaba pero ocupo tener la simplicidad de python.



## Prompt 2. Simplificación de las clases y eliminación de elementos innecesarios

- **Prompt:** "Necesito refactorizarlo para aprovechar el tipado dinámico y la simplicidad de Python." Cambios exactos: eliminar todas las importaciones de `typing` y los type hints; eliminar el Enum (tipo como string validado con `if tipo not in ["Carpeta", "Archivo"]:` y `ValueError`); eliminar todos los `@property` y convertirlos en métodos tradicionales (`get_cantidad_hijos()`, `es_carpeta()`, etc.); mantener la lógica base intacta.

- **Acción del sistema:** Reescribió `nodo.py`, `file_system.py` y `__init__.py` sin hints, sin Enum y sin decoradores; dejó métodos (`es_carpeta()`, `es_archivo()`, `es_raiz()`, `get_cantidad_hijos()`, `esta_vacio()`), validaciones y `agregar_hijo()`. Verificó con pruebas y con un barrido que no quedara ningún rastro de `typing`/`Enum`/`@property`.

- **Observación:** segui con la siguiente funcionalidad.


## Prompt 3. Creación de nodos y visualización del árbol

- **Prompt:** "Vamos a actualizar únicamente el archivo file_system.py agregando dos métodos": **crear_nodo(ruta_padre, nombre_nuevo, tipo_nuevo)**, que navegue desde la raíz hasta la ruta (ej. "/Documentos/Universidad"), "Separa correctamente los nombres de las carpetas a partir del string de la ruta", cree el nodo con `agregar_hijo` y lance `ValueError` si la ruta no existe o el destino no es Carpeta; y **mostrar_arbol()**, que recorra recursivamente el árbol e imprima con indentación proporcional a la profundidad. "Manteniendo el estilo de tipado dinámico y sin decoradores."

- **Acción del sistema:** Implementó ambos métodos en `file_system.py`: navegación con `split("/")` + bucle por segmentos y recorrido recursivo con la función interna `dibujar()` (sangría de 4 espacios, "/" final en carpetas). Dio el código completo del archivo y lo probó.

- **Observación:** Hubo un error, pero **en la prueba de la IA** (creó "Rock" dentro de "/Musica" sin crear "Musica" antes); la IA lo detectó, corrigió su prueba y aclaró que el error no era del código.


## Prompt 4. Búsqueda recursiva y eliminación de nodos

- **Prompt:** "Ahora vamos a agregar los dos últimos algoritmos principales a la clase FileSystem en file_system.py": **buscar_nodo(nombre_objetivo)** con "búsqueda recursiva por todas las ramas del árbol" guiándose solo por el nombre, devolviendo la ruta completa (ej. '/Documentos/Universidad/nota.txt') o `None`; y **eliminar_nodo(ruta_objetivo)** que navegue hasta la ruta y, si es Carpeta, aplique "eliminación en cascada" con "una función recursiva auxiliar que recorra todo el subárbol de esa carpeta, vaciando la lista de hijos de cada nodo para liberar las referencias antes de eliminar al padre (no dejar nodos huérfanos)", removiendo al final el nodo de la lista de su padre, con validación para impedir eliminar la raíz "/".

- **Acción del sistema:** Implementó ambos en `file_system.py`: la recursiva `buscar()` en preorden y `eliminar_nodo()` con navegación hasta el padre, la auxiliar `vaciar_subarbol()` (postorden) y `padre.hijos.remove()`; además reinició `directorio_actual` si estaba dentro de lo eliminado. Validó que no quedaran huérfanos y dio el código completo.

- **Observación:** Hubo un segundo error **de la IA, también en su prueba** (una aserción esperaba 2 hijos en vez de 1).


## Prompt 5. Sustitución de listas por comprensión por ciclos explícitos

- **Prompt:** "Necesito un pequeño ajuste de legibilidad en el archivo file_system.py": eliminar la comprensión de listas `partes = [parte for parte in ruta.split("/") if parte != ""]` en **crear_nodo** y **eliminar_nodo** y sustituirla por un ciclo for tradicional y explícito con la estructura `partes = []`, `for parte in ruta.split("/"):` , `if parte != "":` , `partes.append(parte)`. "Entrégame únicamente el código actualizado… manteniendo todo lo demás intacto."

- **Acción del sistema:** Reemplazó esas dos líneas por los bucles explícitos, verificó que no quedaran comprensiones, compiló el archivo y repitió las pruebas de rutas.

- **Observación:** Todo bien, faltan las pruebas con un menu.


## Prompt 6. Creación de un menú de pruebas para el sistema de archivos

- **Prompt:** "Para finalizar el Módulo 1, necesito el menú de prueba para demostrar el módulo aislado." Crear un archivo `menu_modulo1.py` que importe `FileSystem` desde el paquete, con un menú interactivo dentro de `if __name__ == '__main__':` usando un ciclo `while`, que instancie un árbol vacío y muestre estrictamente: Crear (pedir ruta padre, nombre y tipo), Buscar (pedir nombre y mostrar la ruta o indicar si no existe), Listar árbol (llamar a `mostrar_arbol()`), Eliminar (pedir la ruta objetivo) y Salir. "Es indispensable que uses bloques try-except ValueError alrededor de las llamadas a crear_nodo y eliminar_nodo… imprimir el mensaje de la excepción de forma amigable, y volver a mostrar el menú sin interrumpir la ejecución." (En la última línea del mensaje lo llamaste "menu_de_pruebas.py".)

- **Acción del sistema:** Creó `menu_modulo1.py` con `mostrar_menu()` y el bucle dentro del guard, probó con 35 entradas simuladas (creaciones, errores controlados, borrado y salida) sin ningún traceback y dio el código completo.

- **Observación:** quedó pendiente el nombre del archivo.


## Prompt 7. Cambio del nombre del menú provisional

- **Prompt:** "No quiero que el archivo ni el código hagan referencia a 'modulo 1'. Aplica estos cambios: El archivo debe llamarse `menu_provisional.py`. En el docstring inicial, actualiza la instrucción de ejecución a `python menu_provisional.py`. En la función mostrar_menu() y en la opción 5 de Salir, elimina cualquier texto que diga 'MÓDULO 1' o 'Módulo 1' y cámbialo por 'Menú Provisional'."

- **Acción del sistema:** Renombró el archivo y cambió las 4 apariciones del texto (primera línea del docstring, instrucción de ejecución, banner y mensaje de salida), verificó que no quedara ninguna referencia y lo ejecutó.

- **Observación:** mejoras de usabilidad sobre ese mismo archivo.


## Prompt 8. Mejora de la selección del tipo de elemento

- **Prompt:** "El menú es muy poco intuitivo para un usuario que no conoce el código. Necesito que mejores la experiencia de usuario en la Opción 1 (Crear)": cambiar el ingreso del 'Tipo' por un submenú numérico rápido ("Ingrese 1 para Carpeta o 2 para Archivo: "), asignando internamente 'Carpeta' o 'Archivo'; "Si digita un número inválido, avísale y usa continue para cancelar la creación y volver a mostrar el menú". Y modificar el texto del input de 'Ruta padre' por el exacto: `input('Ruta de la carpeta padre (esta ruta YA DEBE EXISTIR, ej. /): ')`.

- **Acción del sistema:** Aplicó ambos cambios dentro de la Opción 1, probó el tipo 1, el tipo 2 y dos entradas inválidas ("3" y la palabra "Archivo"), confirmando que las inválidas cancelan con `continue` sin crear nada.

- **Observación:** puliendo la Opción 1.


## Prompt 9. Creación automática del primer elemento en la raíz

- **Prompt:** "El menú sigue siendo frustrante para un usuario sin contexto técnico porque asume que saben usar la raíz '/'. Vamos a hacer la Opción 1 (Crear) verdaderamente intuitiva": usar `fs.esta_vacio()` para decidir. Si el árbol está vacío, no pedir la ruta y imprimir exactamente "💡 Como el disco duro está vacío, este primer elemento se guardará automáticamente en la raíz (/)." y asignar `ruta_padre = '/'`; si no está vacío, pedirla con `input('Ruta de la carpeta padre (Recuerde empezar con / , ej: /hola): ')`.

- **Acción del sistema:** Implementó la decisión con `esta_vacio()`. Además **detectó un problema no pedido**: el emoji provoca `UnicodeEncodeError` cuando la salida se redirige (el programa se caía) y añadió `import sys` + `sys.stdout.reconfigure(encoding="utf-8", errors="replace")`, explicando por qué.

- **Observación:** la salida no tiene el formato esperado


## Prompt 10. Eliminación de emojis y corrección de la codificación de la consola

- **Prompt:** "No quiero usar emojis en la consola porque complican la codificación, prefiero mantenerlo estándar. Aplica estos dos cambios: cambiar el mensaje del bombillo para que empiece con 'Nota: Como el disco duro está vacío, este primer elemento…'. Elimina la importación `import sys` al inicio del archivo y elimina por completo el bloque de `if hasattr(sys.stdout, 'reconfigure'):`…"

- **Acción del sistema:** Cambió el texto a "Nota: …", borró `import sys` y la guarda de codificación, y verificó (cero caracteres fuera de latin-1, ejecución con salida redirigida sin UTF-8 → `EXIT=0`, compilación OK). Entregó el código completo del archivo.

- **Observación:** todo listo


## Greivin 
## Prompt Estructura del grafo. :
"Creame la estructura base de un grafo ponderado con lista de adyacencia
en Python: vértices que son servidores y aristas bidireccionales cuyo peso es
la latencia en milisegundos."
Ajuste manual: le agregué la validación de que la latencia sea un número
mayor que 0 (rechaza cero, negativos y NaN), porque la salida original
aceptaba cualquier valor.

## Prompt Dijkstra :
"Sobre esa clase Grafo, implementá Dijkstra sin librerías, igual al
pseudocódigo del curso, para la ruta de menor latencia entre dos servidores."
Ajuste manual: la salida solo calculaba distancias; le agregué el diccionario
`previos` para reconstruir el camino e imprimirlo salto por salto con su
costo, y el registro de cada cálculo en el log de auditoría.

## Prompt Ping general (BFS). :
"Un ping general que recorra el grafo con BFS y diga si hay
servidores aislados."
Ajustes manuales: la IA usaba `deque` y lo cambié por una lista común con
pop(0) para no usar librerías; y la condición de "aislado" la definí yo:
el que no quedó en `visitados` tras el BFS está aislado.

## Prompt Bug real de la tabla hash. :
"Me sale NameError: name 'true' is not defined al registrar usuarios,
¿por qué?"
La IA me explicó que `true` es de JavaScript, no de Python. El ajuste mío
fue una sola línea: `while actual==true:` → `while actual:` (commit d3fb960),
porque un nodo None ya se evalúa como falso.


