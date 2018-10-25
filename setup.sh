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

    cp tickets.py ${DESTDIR}
    checkCode 11 "Copy tickets.py failed." > /dev/null

    cp train_template.ini ${DESTDIR}/train_tickets.ini
    checkCode 11 "Copy train_template.ini failed." > /dev/null

    cp requirements.txt ${DESTDIR}
    checkCode 11 "Copy requirements.txt failed." > /dev/null

    cp -r tickets_pkg ${DESTDIR}
    checkCode 11 "Copy tickets_pkg directory failed." > /dev/null

    if [[ ! -d "${DESTDIR}/log" ]]; then
      mkdir "${DESTDIR}/log"
      checkCode 15 "Make log directory failed." > /dev/null
    fi

    if [[ ! -d "${DESTDIR}/model" ]]; then
      mkdir "${DESTDIR}/model"
      checkCode 15 "Make model directory failed." > /dev/null
    fi

    wget --directory-prefix=${DESTDIR}/model https://storage.googleapis.com/taiwan-railway-220407/model/imitate_5_model.h5 \
    checkCode 17 "Download imitate_5_model failed." > /dev/null

    wget --directory-prefix=${DESTDIR}/model https://storage.googleapis.com/taiwan-railway-220407/model/imitate_6_model.h5 \
    checkCode 17 "wget download imitate_6_model failed." > /dev/null

    wget --directory-prefix=${DESTDIR}/model https://storage.googleapis.com/taiwan-railway-220407/model/imitate_56_model.h5 \
    checkCode 17 "wget download imitate_56_model failed." > /dev/null

    wget --directory-prefix=${DESTDIR}/model https://storage.googleapis.com/taiwan-railway-220407/model/capture.jpg
    checkCode 17 "wget download capture.jpg failed." > /dev/null

    wget --directory-prefix=${DESTDIR}/model https://storage.googleapis.com/taiwan-railway-220407/model/screen.png
    checkCode 17 "wget download screen.png failed." > /dev/null
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
  *Darwin*)
    echo "Darwin detected"
    echo ""
    Installation ${1}
    ;;
  *)
    echo "OS Not supported."
    exit 1
esac


echo "tickets setup success."
exit 0
