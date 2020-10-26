#! /bin/bash
#
# Program:
#   tickets setup script to deploy and run on gcp
#
# Exit Code:
#   11 - function usage error

# --------------------------------------------------------
# Add ending newline to FILENAME file if not already exist
#
# Usage: file_newline FILENAME
# --------------------------------------------------------
file_newline() {
    if [[ "$#" -ne 1 ]]; then
        echo "file_newline usage error"
        exit 11
    fi

    _file=${1}

    tail -c1 < ${_file} | read
    if [[ "$?" -ne 0 ]]; then
        echo "" >> ${_file}
    fi
}

# TODO: check gcloud configuration setting
echo "Check for the correct gcp configuration"
echo -e "=======================================\n"
gcloud config list
echo -e "=======================================\n"
read -p "Press any key to continue... (Ctrl-c to exit)"


# TODO: startup script substitute config_template and copy into project folder
if [[ -f tmp/gcp-startup.sh ]]; then
    rm tmp/gcp-startup.sh
fi

if [[ -f tmp/gcp-config.ini ]]; then
    rm tmp/gcp-config.ini
fi

# Read env variables
source gcp/env.sh

# Generate startup script function 
file_newline gcp/startup-gen-var.sh
file_newline gcp/startup-gen-function.sh
cat gcp/startup-gen-var.sh >> tmp/gcp-startup.sh
cat gcp/startup-gen-function.sh >> tmp/gcp-startup.sh

# Generate startup script config.ini 
file_newline gcp/startup-gen-config.sh

_ini_files=( \
    gcp/default-section.ini \
    gcp/general-section.ini \
    gcp/driver-section.ini \
    gcp/account-section.ini \
    gcp/daan-sport.ini \
)

for _file in ${_ini_files[@]}; do
    file_newline ${_file}
    echo "$(cat ${_file})" >> tmp/gcp-config.ini
done
sed -e "/__BELOW__/r tmp/gcp-config.ini" -e "/__BELOW__/d" gcp/startup-gen-config.sh >> tmp/gcp-startup.sh

# TODO: startup script generate credential.json file in new created instance 
# Generate startup script credential
file_newline gcp/startup-gen-cred.sh
sed -e "/__BELOW__/r credential.json" -e "/__BELOW__/d" gcp/startup-gen-cred.sh >> tmp/gcp-startup.sh

# Generate startup script file deployment
file_newline gcp/startup-gen-deploy.sh
cat gcp/startup-gen-deploy.sh >> tmp/gcp-startup.sh

# TODO: start booking.py program inside tmux
# tmux command execution reference: 
#   https://unix.stackexchange.com/questions/354762/how-to-execute-a-command-by-default-starting-tmux
file_newline gcp/startup-gen-tmux.sh
cat gcp/startup-gen-tmux.sh >> tmp/gcp-startup.sh

# Create gcp compute engine
gcloud beta compute --project=${_gcp_project} instances create ${_gcp_instance_name} --zone=${_gcp_zone} \
    --machine-type=${_gcp_machine_type} \
    --subnet=default \
    --network-tier=PREMIUM \
    --maintenance-policy=MIGRATE \
    --service-account=${_gcp_service_account} \
    --scopes=https://www.googleapis.com/auth/devstorage.read_only,https://www.googleapis.com/auth/logging.write,https://www.googleapis.com/auth/monitoring.write,https://www.googleapis.com/auth/servicecontrol,https://www.googleapis.com/auth/service.management.readonly,https://www.googleapis.com/auth/trace.append \
    --min-cpu-platform=Automatic \
    --no-shielded-secure-boot \
    --shielded-vtpm \
    --shielded-integrity-monitoring \
    --reservation-affinity=any \
    --source-machine-image=${_gcp_source_machine_image} \
    --metadata-from-file=startup-script=tmp/gcp-startup.sh


echo "Done!"