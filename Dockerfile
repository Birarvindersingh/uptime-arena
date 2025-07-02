FROM node:20-alpine AS frontend-builder

WORKDIR /app/client

COPY client/package*.json ./
RUN npm install

COPY client/ ./
RUN npm run build

FROM python:3.9-slim-buster AS backend-base

ENV PYTHONUNBUFFERED=1

RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser
USER appuser

ENV PATH="/home/appuser/.local/bin:${PATH}"

WORKDIR /app/server

COPY server/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY server/ ./

FROM backend-base AS final-image

COPY --from=frontend-builder /app/client/dist /app/server/static

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]