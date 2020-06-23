#!/bin/bash
#
# Program:
#   tickets setup script
#
# Exit Code:
#   1 - Calling syntax error
#   3 - Destination directory does not exist
#
#   11 - Copy file failed
#   13 - Change file permission failed
#   15 - Make directory failed
#   17 - Download file failed


# Check exit code function
# USAGE:
#   checkCode EXITCODE MESSAGE
function checkCode() {
  if [[ ${?} -ne 0 ]]; then
    echo ${2}
    exit ${1}
  fi
}

# Install execution
function Installation() {
    DESTDIR=${1}

    # Setup process
    cp README.md ${DESTDIR}
    checkCode 11 "Copy README.md failed." > /dev/null

    cp booking.py ${DESTDIR}
    checkCode 11 "Copy booking.py failed." > /dev/null

    #cp requirements.txt ${DESTDIR}
    #checkCode 11 "Copy requirements.txt failed." > /dev/null

    cp -r general_pkg ${DESTDIR}
    checkCode 11 "Copy general_pkg directory failed." > /dev/null

    cp -r module_pkg ${DESTDIR}
    checkCode 11 "Copy module_pkg directory failed." > /dev/null

    if [[ ! -f "${DESTDIR}/config.ini" ]]; then
      cp config_template.ini ${DESTDIR}/config.ini
      checkCode 11 "Copy config_template.ini failed." > /dev/null
    fi

    if [[ ! -d "${DESTDIR}/log" ]]; then
      mkdir "${DESTDIR}/log"
      checkCode 15 "Make log directory failed." > /dev/null
    fi
}


# Calling setup format check
USAGE="setup.sh DESTINATION"

if [[ ${#} -ne 1 ]];  then
    echo -e "USAGE:\n    ${USAGE}"
    exit 1
fi

if [[ ! -d ${1} ]]; then
    echo "ERROR: Destination directory does not exist"
    exit 3
fi


# System checking
SYSTEM_RELEASE=$(uname -a)
case ${SYSTEM_RELEASE} in
  *Linux*)
    echo "Linux detected"
    echo ""
    Installation ${1}
    ;;
  *)
    echo "OS Not supported."
    exit 1
esac

echo "booking setup success."
exit 0
