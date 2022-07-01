# http-wrapper

## develop


You can choose one of two ways to develop the asynchronous API. In either case, the swagger doc will be available at [http://localhost:6001/docs](http://localhost:6001/docs)

### docker-compose

- requires: `docker` and `docker-commpose` installed on host machine

```sh
docker-compose up
```

### native

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