# ----
# Run command as other user
# 
# Usage: run_as USER COMMAND...
# ---
run_as() {
    local _user=${1}

    shift
    su - ${_user} -c "${@}"
}
