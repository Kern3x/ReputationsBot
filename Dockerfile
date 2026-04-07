FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN addgroup --system app && adduser --system --ingroup app app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN chown -R app:app /app && chmod +x /app/docker/entrypoint.sh

USER app

HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
  CMD python -m app.healthcheck || exit 1

CMD ["/app/docker/entrypoint.sh"]
