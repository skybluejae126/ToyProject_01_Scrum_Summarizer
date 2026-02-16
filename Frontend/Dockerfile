# Stage 1: Build
FROM node:18-alpine AS build-stage
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# Stage 2: Serve with Nginx
FROM nginx:stable-alpine
# 빌드된 파일 복사
COPY --from=build-stage /app/build /usr/share/nginx/html
# [추가] 우리가 만든 설정 파일을 Nginx 설정 폴더에 덮어쓰기
COPY default.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]