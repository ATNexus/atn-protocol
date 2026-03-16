# ATN Marketplace UI Dockerfile
FROM node:18-alpine

WORKDIR /app

# 复制package文件
COPY package*.json ./

# 安装依赖
RUN npm ci

# 复制代码
COPY . .

# 构建
RUN npm run build

# 暴露端口
EXPOSE 3000

# 启动
CMD ["npm", "start"]
