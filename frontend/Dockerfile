FROM node:16-alpine

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY . .

ENV WATCHPACK_POLLING=true
ENV REACT_APP_API_URL=http://api_gateway:5000/api

EXPOSE 3000

CMD ["npm", "start"]
