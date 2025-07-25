from fastapi import FastAPI
from starlette.responses import HTMLResponse
from middleware.logger import logger_middleware
from database import Base, engine
from routers import auth, usuario, libro, prestamo

# Crear las tablas automáticamente
Base.metadata.create_all(bind=engine)

# Instancia principal de la app
app = FastAPI(title="API Biblioteca Final")

# Middleware
app.middleware("http")(logger_middleware)

# Routers
app.include_router(auth.router)
app.include_router(usuario.router)
app.include_router(libro.router)
app.include_router(prestamo.router)

# Ruta de inicio con HTML
@app.get("/", response_class=HTMLResponse)
async def home():
    html_content = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>API Biblioteca</title>
        <style>
            body {
                background-color: #1e1e1e;
                color: #f0f0f0;
                font-family: 'Consolas', 'Courier New', monospace;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                height: 100vh;
                margin: 0;
            }
            h1 {
                font-size: 2.8rem;
                margin-bottom: 0.5rem;
                color: #61dafb;
            }
            p {
                font-size: 1.1rem;
                color: #c0c0c0;
                margin-bottom: 2rem;
            }
            .button {
                background-color: #282c34;
                color: #61dafb;
                border: 2px solid #61dafb;
                padding: 12px 24px;
                margin: 10px;
                border-radius: 6px;
                text-decoration: none;
                font-size: 1rem;
                transition: all 0.3s ease;
            }
            .button:hover {
                background-color: #61dafb;
                color: #1e1e1e;
            }
        </style>
    </head>
    <body>
        <h1>API Biblioteca</h1>
        <p>Bienvenido. Accedé a la documentación interactiva de esta API RESTful.</p>
        <div>
            <a href="/docs" class="button">📘 Swagger UI</a>
            <a href="/redoc" class="button">📕 ReDoc</a>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)
