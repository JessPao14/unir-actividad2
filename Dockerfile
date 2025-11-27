FROM python:3.6-slim

# Creamos directorio del proyecto
RUN mkdir -p /opt/calc

WORKDIR /opt/calc

# Definir PYTHONPATH para que Python encuentre los módulos de /opt/calc/app
ENV PYTHONPATH=/opt/calc

# Instalar dependencias
COPY requires ./
RUN pip install -r requires

# Copiar TODO el proyecto (app/, tests/, pytest.ini, etc.)
COPY . .

# Comando por defecto (opcional)
CMD ["pytest"]