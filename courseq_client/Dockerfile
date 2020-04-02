FROM node

# Create app directory
WORKDIR /usr/src/app
COPY package*.json ./

RUN npm install

COPY . .

RUN echo | ls
RUN npm run build
RUN echo | ls
RUN env

EXPOSE 3000

# CMD [ "node", "server.js" ]
CMD [ "npm" ,"run", "serve" ]
# CMD [ "npm", "run" ,"start:dev" ]

