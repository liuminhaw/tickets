for _dest in ${_DESTINATIONS[@]}; do
    run_as ${_USER} "cp ${_CREDENTIAL} ${_PROJECT_PATH}/${_dest}"
    run_as ${_USER} "cp ${_CONFIG_TEMPLATE} ${_PROJECT_PATH}/${_dest}"
done
