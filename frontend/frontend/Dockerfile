FROM node:23.5.0-alpine

WORKDIR /usr/src/app

COPY ./package.json ./package.json
COPY ./package-lock.json ./package-lock.json
RUN npm install 
COPY . . 
RUN npm run build
EXPOSE 5173
CMD  ["npm", "run", "dev"]



