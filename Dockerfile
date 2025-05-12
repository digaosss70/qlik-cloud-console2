FROM python:3.12-slim

# Instala o Poetry
RUN pip install poetry

# Copia os arquivos do projeto
COPY . /src
WORKDIR /src

# Instala dependências (ignora o projeto atual)
RUN poetry install --no-root

# Expõe a porta e roda o Streamlit
EXPOSE 8502
ENTRYPOINT ["poetry", "run", "streamlit", "run", "app.py", "--server.port=8502", "--server.address=0.0.0.0"]