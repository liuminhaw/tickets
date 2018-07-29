#!/bin/bash
#
# Launch tickets.py program at set time
#
# Usage:
#   timer.sh YYYY-MM-DD HH:MM:SS
#
# Exit Code:
#   1 - Command not matching requirement
#   3 - Not a supporting distribution


PATH=/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin
export PATH

USAGE='timer.sh YYYY-MM-DD HH:MM:SS'
MINUS_TIME=45

if [[ ${#} -ne 2 ]]; then
  echo "${USAGE}"
  exit 1
fi

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
  *ARCH*)
    echo "Detected ARCH"
    TARGET=$(date --date="${*}" +%s)
    ;;
  *)
    echo "Not supported distribution"
    exit 3
  esac

  TARGET_ADJUST=$((TARGET-MINUS_TIME))

while [[ $(date +%s) -le ${TARGET_ADJUST} ]]
do
  if [[ $(date +%s) -ge ${TARGET_ADJUST} ]]; then
    EXIT_STATUS=$(python3 ${HOME}/GitHub/tickets/tickets.py ${*})
    exit ${EXIT_STATUS}
  fi
  sleep 1
done



exit 0
