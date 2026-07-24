FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml LICENSE README.md /tmp/pkg/
COPY src /tmp/pkg/src
RUN pip install --no-cache-dir /tmp/pkg fastapi "uvicorn[standard]" pydantic \
    && rm -rf /tmp/pkg

COPY samples/clinical-intel/ /app/

ENV PORT=8080
EXPOSE 8080

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]
