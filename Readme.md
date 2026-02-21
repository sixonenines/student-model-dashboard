



# bachelor-thesis-yasin-studentmodels

Web-based platform for training Item-Response Theory (IRT) models using Python and R

## Requirements

You will need [Docker](https://docs.docker.com/get-docker/) installed on your computer to build and run this application.

## How to use v2 version:

1. Have [Docker](https://docs.docker.com/get-docker/) up and running
2. Clone this repository and move to directory v2 in your terminal
3. Use docker compose to orchestrate the services required
```bash
docker compose up -d
```
4. Open the [application](http://localhost:3000/studentmodelsdashboard)

## How to use v1 version

1. Have [Docker](https://docs.docker.com/get-docker/) up and running
2. Clone this repository and move to the directory in your terminal
3. Build the Docker Image
```bash
docker build . -t studentmodeldash
```
4. Run the Docker Image
```bash
docker run -it -p 8501:8501 studentmodeldash
```
5. Open the [application](http://localhost:8501/)