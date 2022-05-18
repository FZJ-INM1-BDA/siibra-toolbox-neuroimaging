
trap terminate SIGINT
terminate(){
    pkill -SIGINT -P $$
    exit
}

celery -A http_wrapper.scheduling.worker worker -l INFO &
uvicorn http_wrapper.server:app --port 6001 &
wait
