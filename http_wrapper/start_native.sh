
trap terminate SIGINT
terminate(){
    pkill -SIGINT -P $$
    exit
}

cd http_wrapper && celery -A scheduling.worker worker -l INFO &
cd http_wrapper && uvicorn server:app --port 6006 &
wait
