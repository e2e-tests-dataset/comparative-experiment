# BUGSJS Experiment

To build Docker images (necessary to perform the experiment):

```sh
    ./downloadAndBuild.sh
```

This commmand generates the image `bugsjs:quatic-2020`. You should re-tag this image to push it to DockerHub:

```
    docker tag bugsjs:quatic-2020 <my_user>/bugsjs:quatic-2020
```

You can use the image generated in this experiment (in DockerHub): `maes95/bugsjs:quatic-2020`.