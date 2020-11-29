# Defects4JS Experiment

To build Docker images (necessary to perform the experiment):

```sh
    ./downloadAndBuild.sh
```

This commmand generates the image `defects4j:quatic-2020`. You should re-tag this image to push it to DockerHub:

```
    docker tag defects4j:quatic-2020 <my_user>/defects4j:quatic-2020
```

You can use the image generated in this experiment (in DockerHub): `maes95/defects4j:quatic-2020`.