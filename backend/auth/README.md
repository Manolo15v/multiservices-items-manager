Microservicio de Autenticación (Auth Service)
Este microservicio, desarrollado con Python y FastAPI, es el encargado de gestionar el registro de usuarios, el inicio de sesión y la emisión y validación de JSON Web Tokens (JWT).

Requisitos del Proyecto
Este servicio cumple con los siguientes requisitos funcionales:
Registro de Usuarios: Permite la creación de nuevas cuentas.
Inicio de Sesión (Login): Autentica al usuario y, si es exitoso, genera un token JWT.
Generación de JWT: Crea tokens firmados que el cliente utiliza para acceder a los servicios protegidos (Products e Inventory).
Validación de Token: Ofrece un mecanismo (implícito o explícito) para verificar la validez de un token JWT en endpoints protegidos.

Tecnologías Utilizadas
Lenguaje: Python 3.10+
Framework: FastAPI
Librerías Clave: python-jose (para JWT), passlib (para hashing de contraseñas), uvicorn (servidor ASGI).
Contenedorización: Docker

Configuración y Variables de Entorno
Para ejecutar el servicio veáse .example.env 

Endpoints de la API
El microservicio expone los siguientes endpoints (todos bajo el prefijo principal /auth):

Método    	Ruta          	Descripción	                                                  Seguridad
POST  	/auth/register	  Crea un nuevo usuario.	                                        Pública
POST	  /auth/login	      Autentica al usuario. Retorna un objeto con el token JWT.       Pública
GET	   /auth/users/me	    Retorna los datos del usuario autenticado (basado en el JWT).	  Protegida (Requiere JWT)
