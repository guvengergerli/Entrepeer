# Entrepeer

The aim of this application is to get startup collabrators of the 25 most active startup customers in the world from https://ranking.glassdollar.com and cluster them using Natural Language Processing methods of vector embeddings.

To build the application go to the root of the project and build the docker image by:

```
docker build -t entrepeer-image .
```

and after that run the docker image by:

```
docker run -p 8000:8000 entrepeer-image
```
