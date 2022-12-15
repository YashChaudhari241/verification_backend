FROM node:14-alpine
COPY utils/package.json /app/package.json
RUN cd /app && npm install 
COPY ./utils/src/utils.js /app/src/utils.js
WORKDIR /app
EXPOSE 3000/tcp
CMD DEBUG=express:* node src/utils.js
