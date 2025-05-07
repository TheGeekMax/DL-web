@echo off

:: Stop and remove the 'ia' container
docker stop ia
docker rm ia

:: Build the 'ia' Docker image
cd ia
docker build --rm -t ia .
cd ..

:: Stop and remove the 'nn' container
docker stop nn
docker rm nn

:: Build the 'nn' Docker image
cd nn
docker build --rm -t nn .
cd ..

:: Start the services using docker-compose
docker-compose -f docker-compose.yml up

:: j'ai généré cette merde avec cette merde de ChatGPT