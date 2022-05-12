# siibra toolbox template

This repository provides a template for developing a toolbox for the siibra-toolsuite. 

A full-fledged toolbox contains three components:

 1. A python implementation of functionalities or workflows that make use of the [siibra-python](https://github.com/FZJ-INM1-BDA/siibra-python).
 2. An implementation of an asynchronous REST API around the python workflow, which exposes (part of) the functionality to web services.
 3. An implementation of an interactive user interface in the form of a [siibra-explorer](https://github.com/FZJ-INM1-BDA/siibra-explorer) plugin, which connects to the http wrapper.
 
An example of such a toolbox is [siibra-toolbox-jugex](https://github.com/FZJ-INM1-BDA/siibra-toolbox-jugex).

## Get started

### Clone

```sh
git clone https://github.com/fzj-inm1-bda/siibra-toolbox-template my-toolbox
cd my-toolbox
```

### Setup

- edit `.env`
    - `SIIBRA_TOOLBOX_NAME`: name of the python package. It is recommended to be prepend by `siibra_toolbox_`
    - `SIIBRA_TOOLBOX_SRC`: directory relative to root the package resides. It is strongly recommend to be the same as `SIIBRA_TOOLBOX_NAME`
- edit `setup.py`
    - `install_requires`
    - (Optionally) `author`, `author_email`
- rename or create the directory specified by `SIIBRA_TOOLBOX_SRC`

### Develop the python toolbox

<!-- TODO -->

### Develop asynchronous API

> :warning: The following section assumes a MVP of _Develop toolbox_ is present in the directory `{SIIBRA_TOOLBOX_NAME}`

You can choose one of two ways to develop the asynchronous API

#### docker-compose

- requires: `docker` and `docker-commpose` installed on host machine

```sh
docker-compose up
```

#### native

- requires: python3.6+, a redis instance (localhost or otherwise, ran natively or via docker)
    - e.g. `docker run --name redis -p 127.0.0.1:6379:6379 redis:6`

- install dependencies

```sh
pip install -r ./http_wrapper/requirements-server.txt
pip install -r ./http_wrapper/requirements-worker.txt

```
- run the processes

```sh
./http_wrapper/start_native.sh
```

> :info: If you get a maximum callstack reached error, it is likely that celery is not able to connect to redis. Check that redis is running via `docker ps`

## License

This template is licensed under the Apache 2.0 license. 
