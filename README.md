# file: README.md

# DemeArizOil Backend — FastAPI + PostgreSQL + Railway

Backend listo para producción siguiendo mejores prácticas:
- FastAPI (Python 3.12)
- SQLAlchemy 2.x
- PostgreSQL
- Alembic
- Dockerfile multi-stage
- Railway con PostgreSQL Add-on

---

# 1. Desarrollo local

## 1.1 Crear entorno `.env`
Copiar el archivo:

cp .env.example .env

shell
Copiar código

Modificar valores si hace falta.

## 1.2 Levantar entorno local (backend + PostgreSQL)

docker-compose up --build

yaml
Copiar código

El backend quedará disponible en:

http://localhost:8000

powershell
Copiar código

## 1.3 Aplicar migraciones

Dentro del contenedor backend:

docker exec -it demearizoil_backend alembic upgrade head

yaml
Copiar código

---

# 2. Subir a GitHub

Crear un nuevo repositorio y subir:

git init
git add .
git commit -m "v1.0 PostgreSQL ready"
git remote add origin <URL_REPO>
git push -u origin main

yaml
Copiar código

---

# 3. Despliegue en Railway (producción)

## 3.1 Crear proyecto
1. Entrar a Railway
2. Crear nuevo proyecto → "Deploy from GitHub"
3. Seleccionar este repositorio

## 3.2 Añadir PostgreSQL
1. En el proyecto → Add → Database → PostgreSQL
2. Railway generará `DATABASE_URL` automáticamente

## 3.3 Configurar variables de entorno del servicio backend

Railway → Service backend → Variables:

SECRET_KEY=<tu clave aleatoria de 30 caracteres>

yaml
Copiar código

NO pongas DB_USER, DB_PASSWORD, DB_HOST. Railway pasa `DATABASE_URL` directamente.

## 3.4 Desplegar (Deploy)

Railway detectará el Dockerfile y construirá la imagen.

---

# 4. Aplicar migraciones en Railway

En el servicio backend → Shell:

alembic upgrade head

yaml
Copiar código

Las tablas se crearán en el PostgreSQL de Railway.

---

# 5. Backend operativo

Railway te dará una URL pública similar a:

https://demearizoil-backend-production.up.railway.app

yaml
Copiar código

Tu API está lista para consumir desde el frontend.

---

# end file: README.md