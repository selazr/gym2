# 🏋️‍♂️ Cesar's Gym

Es un proyecto de ejemplo para la gestión de un gimnasio, desarrollado con [Django](https://www.djangoproject.com/) y [Djongo](https://www.djongomapper.com/) (una herramienta que permite usar MongoDB como base de datos en proyectos Django).

---

## ⚙️ Requisitos

- Python **3.10** (recomendado para compatibilidad con Djongo)
- MongoDB en ejecución (local o remoto)
- Node.js y npm (para dependencias frontend, si se usan)
- pip (gestor de paquetes de Python)

---

## 🧪 Instalación

Sigue estos pasos para configurar el entorno de desarrollo:

### 1. Clona el repositorio

```bash
git clone https://github.com/tu_usuario/djongo_gym.git
cd djongo_gym
```

### 2. Crea y activa un entorno virtual

```bash
python3.10 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### 3. Instala las dependencias de Python

```bash
pip install -r requirements.txt
```

### 4. Instala las dependencias de JavaScript (si el proyecto usa assets frontend)

```bash
npm install
```

---

## 🚀 Uso

### Inicia el servidor de desarrollo

```bash
python manage.py runserver
```

Abre tu navegador y accede a:

```
http://localhost:8000
```

---

## 🧰 Herramientas y Tecnologías

- Django (framework backend)
- Djongo (conexión MongoDB)
- MongoDB (base de datos NoSQL)
- Bootstrap / Tailwind (opcional para frontend)
- npm / Node.js (para manejar assets si se usan)

---

## 📌 Notas

- Asegúrate de tener **MongoDB** corriendo antes de iniciar el servidor.
- Puedes configurar la conexión a MongoDB en `settings.py`, en la sección `DATABASES`.
- Si encuentras errores con Djongo, revisa que estés usando Python 3.10, ya que versiones más recientes pueden presentar incompatibilidades.
