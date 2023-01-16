# bachelor-thesis-yasin-studentmodels

Web-based platform for training Item-Response Theory (IRT) models using Python and R

## Requirements

You will need [Docker](https://docs.docker.com/get-docker/) installed on your computer to build and run this application.

## How to Use

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
5. Open the [application] (http://localhost:8501/)