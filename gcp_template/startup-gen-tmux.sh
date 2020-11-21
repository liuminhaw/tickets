
for _dest in ${_DESTINATIONS[@]}; do
    run_as ${_USER} "tmux new -d -s ${_dest}"
    run_as ${_USER} "tmux send-keys -t ${_dest} \"cd ${_PROJECT_PATH}/${_dest}\" Enter"
    run_as ${_USER} "tmux send-keys -t ${_dest} \"source venv/bin/activate\" Enter"
    run_as ${_USER} "tmux send-keys -t ${_dest} \"python3 booking.py ${_BOOKING}\" Enter"
done
