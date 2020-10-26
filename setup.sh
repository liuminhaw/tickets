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

# ----------------------------------------------------------------------------
# Show usage message
#
# Usage: show_help
# ----------------------------------------------------------------------------
show_help() {
cat << EOF
Usage: ${0##*/} [--help] DESTINATION
    --help                      Display this help message and exit
EOF

exit 1
}

# ---------------------------------
# Check exit code function
#
# Usage: checkCode EXITCODE MESSAGE
# ---------------------------------
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

    cp requirements.txt ${DESTDIR}
    checkCode 11 "Copy requirements.txt failed." > /dev/null

    cp -r general_pkg ${DESTDIR}
    checkCode 11 "Copy general_pkg directory failed." > /dev/null

    cp -r module_pkg ${DESTDIR}
    checkCode 11 "Copy module_pkg directory failed." > /dev/null

    cp -r gcp_template ${DESTDIR}/gcp
    checkCode 11 "Copy gcp directory failed."

    if [[ ! -f "${DESTDIR}/config.ini" ]]; then
      cp config_template.ini ${DESTDIR}/config.ini
      checkCode 11 "Copy config_template.ini failed." > /dev/null
    else 
      cp config_template.ini ${DESTDIR}/config_template.ini
      checkCode 11 "Copy config_template.ini failed." > /dev/null
    fi

    if [[ ! -d "${DESTDIR}/tmp" ]]; then
      mkdir "${DESTDIR}/tmp"
      checkCode 15 "Make tmp directory filed." > /dev/null
    fi

    if [[ ! -d "${DESTDIR}/log" ]]; then
      mkdir "${DESTDIR}/log"
      checkCode 15 "Make log directory failed." > /dev/null
    fi
}


# Calling setup format check
if [[ ${#} -ne 1 ]];  then
  show_help
fi

while :; do
    case ${1} in
        --help)
            show_help
            ;;
        -?*)
            echo -e "[WARN] Unknown option (ignored): ${1}" 1>&2
            ;;
        *)  # Default case: no more options
            break
    esac

    shift
done

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
