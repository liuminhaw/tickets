#!/bin/bash


echo ${*}

SYSTEM_RELEASE=$(uname -a)
case ${SYSTEM_RELEASE} in
  *el7.x86_64*)
    echo "Detected CentOS7"
    TARGET=$(date --date="${*}" +%s)
    ;;
  *Darwin*)
    echo "Detected Darwin"
    TARGET=$(date -j -f "%Y-%m-%d %H:%M:%S" "${*}" +%s)
    ;;
  *)
    echo "Not supported distribution"
    exit 3
  esac

  TARGET_ERROR=$((TARGET+10))


while [[ $(date +%s) -le ${TARGET_ERROR} ]]
do
  if [[ $(date +%s) -ge ${TARGET} ]]; then
    python3 ${HOME}/GitHub/tickets/tickets.py
  fi
  sleep 1
done



exit 0
