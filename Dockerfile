FROM node:18 AS frontend-build
WORKDIR /app
COPY ./frontend/package*.json ./
RUN npm install
COPY ./frontend .
RUN npm run build

FROM python:3.11-slim AS backend
WORKDIR /app
COPY ./backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY ./backend .
EXPOSE 5050
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5050"]

FROM nginx:alpine AS frontend
COPY --from=frontend-build /app/dist /usr/share/nginx/html
COPY ./frontend/nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80

FROM node:18-alpine AS frontend-dev
WORKDIR /app
COPY ./frontend/package*.json ./
RUN npm install
COPY ./frontend .
EXPOSE 3535
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]