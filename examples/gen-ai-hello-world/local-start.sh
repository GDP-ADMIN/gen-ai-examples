#!/bin/bash

PYTHON_VERSION="3.11"
POETRY_VERSION="1.8.1"
GCLOUD_VERSION="493.0.0"

LOG_FILE="./deploy.log"

# Write console output to both console and a file, so users can review the output in case the console is accidentally closed.
PIPE=$(mktemp -u) # Create a unique temporary filename and store it in $PIPE
mkfifo "$PIPE"    # Create a named pipe (FIFO) using the filename in $PIPE
tee -a "$LOG_FILE" < "$PIPE" & # Append output from $PIPE to $LOG_FILE in the background
exec >"$PIPE" 2>&1 # Redirect both stdout and stderr to $PIPE

cleanup() {
  rm -f "$PIPE" # Remove the temporary file $PIPE to clean up resources
  exit_application # Call a function to exit the application gracefully
}
trap cleanup INT TERM EXIT # Ensure cleanup is called on script exit or when receiving INT, TERM, or EXIT signals

log() {
    # Logs a message with a timestamp to the console.
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1"
}

exit_application() {
    # Handles script termination, logging a shutdown message and exiting with code 1.
    echo -e "\033[31m"
    log "Exiting..."
    echo -e "\033[0m"

    exit 1
}

handle_error() {
    # Logs an error message and shuts down the application.
    echo -e "\033[31m"
    log "An error occurred: $1"
    echo -e "\033[0m"
    exit_application
}

trap handle_error ERR

check_command_version() {
    # Checks if a command is installed and meets the required version.
    # Arguments:
    #   $1 - Command name
    #   $2 - Required version
    #   $3 - Version flag (e.g., --version)
    local cmd=$1
    local required_version=$2
    local version_flag=$3
    local current_version

    if ! command -v "$cmd" >/dev/null 2>&1; then
        handle_error "$cmd is not installed. Please install $cmd version $required_version or above."
    else
        current_version=$("$cmd" "$version_flag" 2>&1 | grep -m 1 -Eo '[0-9]+(\.[0-9]+)+')
        if [[ -z "$current_version" ]]; then
            handle_error "Could not determine $cmd version. Please ensure it is installed correctly."
        fi
        if [[ "$(printf '%s\n' "$required_version" "$current_version" | sort -V | head -n1)" != "$required_version" ]]; then
            handle_error "$cmd version $required_version or above is required. You have version $current_version."
        fi
    fi

    log "$cmd is installed and meets the required version ($required_version). Current version: $current_version."
}




check_requirements() {
    # Checks system requirements, ensuring Python and Poetry are installed and meet version requirements.
    log "Checking system requirements..."
    check_command_version "python" "$PYTHON_VERSION" "--version"
    check_command_version "poetry" "$POETRY_VERSION" "--version"
    check_command_version "gcloud" "$GCLOUD_VERSION" "--version"

    # check if .env file exists
    if [[ ! -f ".env" ]]; then
        handle_error ".env file not found. Please create a .env file and supply the required environment variables."
    fi

    log "System requirements are satisfied."
}

deactivate_conda() {
    # Deactivates any active Conda environment.
    if command -v conda >/dev/null 2>&1; then
        # shellcheck disable=SC1091
        CONDA_BASE=$(conda info --base 2>/dev/null)

        if [ -n "$CONDA_BASE" ] && [ -f "$CONDA_BASE/etc/profile.d/conda.sh" ]; then
            # shellcheck source=/dev/null
            . "$CONDA_BASE/etc/profile.d/conda.sh" || {
                handle_error "Warning: Unable to source conda.sh from $CONDA_BASE/etc/profile.d"
            }

            while [ -n "$CONDA_DEFAULT_ENV" ]; do
                log "Conda environment '$CONDA_DEFAULT_ENV' is active. Deactivating..."
                conda deactivate
            done
            log "All Conda environments have been deactivated."
        else
            log "Warning: conda.sh not found in $CONDA_BASE/etc/profile.d. Conda cannot be deactivated."
        fi
    else
        log "Conda is not installed. Skipping conda deactivation."
    fi
}

check_gcloud_login() {
    # Checks if the user is logged into gcloud.
    if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" | grep -q .; then
        handle_error "No active gcloud account found. Please log in using 'gcloud auth login'."
    fi
    
    log "User is logged into gcloud."
}

check_artifact_access() {
    if ! gcloud artifacts packages list --repository=gen-ai --location=asia-southeast2 --project=gdp-labs; then
        handle_error "User does not have access to the GDP Labs Google Artifact Registry. Please contact the GDP Labs DSO team at infra(at)gdplabs.id."
    fi
    
    log "User has access to the GDP Labs Google Artifact Registry."
}

main() {
    # Main function to orchestrate the deployment script.
    log "Checking gen-ai-hello-world example requirements..."
    check_requirements
    check_gcloud_login
    check_artifact_access
    deactivate_conda

    log "Running gen-ai-hello-world example..."
    export POETRY_HTTP_BASIC_GEN_AI_USERNAME=oauth2accesstoken
    export POETRY_HTTP_BASIC_GEN_AI_PASSWORD=$(gcloud auth print-access-token)
    poetry install
    poetry run python gen_ai_hello_world/main.py
}

main
