
#!/bin/sh -ex
# Use tmux to open mutltiple windows for development, each running a different command

tmux new-session -d -s "pullapprove"
tmux send-keys "pipenv run python pullapprove/manage.py migrate && pipenv run python pullapprove/manage.py runserver" "C-m"
tmux split-window -v
tmux send-keys "ngrok http 8000" "C-m"
tmux split-window -h
tmux send-keys "docker run --name pullapprove-postgres ..." "C-m"
tmux attach-session -t "pullapprove"
