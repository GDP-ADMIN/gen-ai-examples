#!/bin/bash

PYTHON_VERSIONS=("3.11" "3.12") # acceptable versions
POETRY_VERSION="1.8.1"
GCLOUD_VERSION="493.0.0"

PYTHON_CMD="python"
LOG_FILE="./deploy.log"

PYTHON_PATH=""
POETRY_PATH=""

# colors for logging
COLOR_ERROR="\033[31m"
COLOR_WARNING="\033[33m"
COLOR_INFO="\033[34m"
COLOR_SUCCESS="\033[32m"
COLOR_RESET="\033[0m"

> "$LOG_FILE" # Clear the log file

# Write console output to both console and a file, so users can review the output in case the console is accidentally closed.
PIPE=$(mktemp -u) # Create a unique temporary filename and store it in $PIPE
mkfifo "$PIPE"    # Create a named pipe (FIFO) using the filename in $PIPE
tee -a "$LOG_FILE" < "$PIPE" & # Append output from $PIPE to $LOG_FILE in the background
exec >"$PIPE" 2>&1 # Redirect both stdout and stderr to $PIPE

cleanup() {
  rm -f "$PIPE" # Remove the temporary file $PIPE to clean up resources
  exit_application # Call a function to exit the application gracefully
}
trap cleanup INT # Ensure cleanup is called on script exit or when receiving INT signal

get_timestamp() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')]"
}

log() {
    # Logs a message with a timestamp to the console.
    echo -e "${COLOR_INFO}$(get_timestamp)$COLOR_RESET" "$1"
}

exit_application() {
    # Handles script termination, logging a shutdown message and exiting with code 1.
    log "${COLOR_WARNING}Exiting...$COLOR_RESET"
    exit 1
}

handle_error() {
    # Logs an error message and shuts down the application.
    echo -e "${COLOR_ERROR}$(get_timestamp) An error occurred\n $1$COLOR_RESET"

    exit_application
}

trap handle_error ERR INT TERM

get_python_path() {
    # Get the full path to the Python executable
    if command -v python3 >/dev/null 2>&1; then
        PYTHON_PATH=$(command -v python3)
        PYTHON_CMD="python3"    
    elif command -v python >/dev/null 2>&1; then
        PYTHON_PATH=$(command -v python)
        PYTHON_CMD="python"
    else
        handle_error "Python not found. Please install Python $PYTHON_VERSION"
    fi

    log "PYTHON_PATH will be set to: $PYTHON_PATH"
}

get_poetry_path() {
    # Determine the poetry path based on the operating system
    if [[ "$OSTYPE" == "darwin"* ]]; then
        POETRY_PATH="$HOME/Library/Application Support/pypoetry/venv/bin/poetry" # macOS
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        if grep -q "microsoft" /proc/version 2>/dev/null; then
            POETRY_PATH="$HOME/.local/bin/poetry" # WSL
        else
            POETRY_PATH="$HOME/.local/share/pypoetry/venv/bin/poetry" # Linux/Unix
        fi
    elif [[ "$OSTYPE" == "cygwin" || "$OSTYPE" == "msys" ]]; then
        POETRY_PATH="%APPDATA%\\pypoetry\\venv\\Scripts\\poetry" # Windows
    elif [[ -n "$POETRY_HOME" ]]; then
        POETRY_PATH="$POETRY_HOME/venv/bin/poetry" # If $POETRY_HOME is set
    else
        handle_error "Unsupported operating system or POETRY_HOME not set."
    fi

    log "Detected Poetry path: $POETRY_PATH"
}

install_command() {
    local cmd=$1
    local required_version=$2

    if [[ "$cmd" == "poetry" ]]; then
        log "Attempting to install the latest version of $cmd..."

        # Install the latest version of Poetry
        log "Installing Poetry via curl..."
        if ! curl -sSL https://install.python-poetry.org | $PYTHON_CMD -; then
            handle_error "Failed to install $cmd version $required_version."
        fi

        get_poetry_path
    else
        if [[ "$cmd" == "$PYTHON_CMD" ]]; then
            handle_error "Please use Python version ${PYTHON_VERSIONS[*]}."
        else
            handle_error "Please install $cmd version $required_version or above."
        fi
    fi
}

compare_versions() {
    # Compare two version strings $1 and $2
    local IFS=.
    local i ver1=($1) ver2=($2)

    # Fill empty fields in ver1 with zeros
    for ((i=${#ver1[@]}; i<${#ver2[@]}; i++)); do
        ver1[i]=0
    done

    # Fill empty fields in ver2 with zeros
    for ((i=${#ver2[@]}; i<${#ver1[@]}; i++)); do
        ver2[i]=0
    done

    for ((i=0; i<${#ver1[@]}; i++)); do
        if ((10#${ver1[i]} > 10#${ver2[i]})); then
            return 1 # The current version is greater than the required version
        fi
        if ((10#${ver1[i]} < 10#${ver2[i]})); then
            return 0 # The current version is less than the required version
        fi
    done

    return 1 # The current version is equal to the required version
}

check_version_array() {
    local current_version=$1
    local command_name=$2
    local version_array=("${@:3}")
    local version_matched=false

    for version in "${version_array[@]}"; do
        if [[ "$current_version" =~ ^$version\.[0-9]+$ ]]; then
            version_matched=true
            break
        fi
    done

    if [[ "$version_matched" == false ]]; then
        handle_error "$command_name version must be either (${version_array[*]}). Current version: $current_version."
    fi
}

check_command_version() {
    # Checks if a command is installed and meets the required version.
    # Arguments:
    #   $1 - Command name
    #   $2 - Required version
    #   $3 - Version flag (e.g., --version)
    local cmd=$1
    local required_version=$2
    local version_flag=$3

    if ! command -v "$cmd" >/dev/null 2>&1; then
        log "$cmd is not installed. Required version: $required_version."
        install_command "$cmd" "$required_version"
    fi

    local current_version
    current_version=$("$cmd" "$version_flag" 2>&1 | grep -Eo '[0-9]+(\.[0-9]+)+' | head -n 1)

    if [[ -z "$current_version" ]]; then
        handle_error "Could not determine $cmd version. Please ensure it is installed correctly."
    fi

    # Modify the check_command_version function to handle exact version check for Python
    if [[ "$cmd" == "$PYTHON_CMD" ]]; then
        if ! check_version_array "$current_version" "$PYTHON_CMD" "${PYTHON_VERSIONS[@]}"; then
            handle_error "$PYTHON_CMD version must be one of (${PYTHON_VERSIONS[*]}). Current version: $current_version."
        fi
    else
        # Use the compare_versions function
        compare_versions "$current_version" "$required_version"
        if [[ $? == 0 ]]; then
            log "$cmd version $required_version or above is required. You have version $current_version."
            install_command "$cmd" "$required_version"
        fi
    fi
    log "$cmd is installed and meets the required version. Current version: $current_version."
}

check_requirements() {
    # Checks system requirements, ensuring Python and Poetry are installed and meet version requirements.
    log "Checking system requirements..."

    check_command_version "$PYTHON_CMD" "$PYTHON_VERSION" "--version"
    check_command_version "gcloud" "$GCLOUD_VERSION" "--version"

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

copy_env_file() {
    # Copies the .env.example file to .env.
    if [[ ! -f ".env" ]]; then
        if [[ -f ".env.example" ]]; then
            cp .env.example .env
            log "Successfully copied '.env.example' to '.env'."
            log "${COLOR_WARNING}Please change the values in the .env file with your own values and then run './local-start.sh' again.$COLOR_RESET"
            exit_application
        else
            log ".env.example file not found. Continuing without creating .env file."
        fi
    else
        log ".env file exists. Continuing..."
    fi
}

check_gcloud_login() {
    # Checks if the user is logged into gcloud.
    if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" | grep -q .; then
        handle_error "No active gcloud account found. Please log in using 'gcloud auth login'."
    fi
    
    log "User is successfully logged into gcloud with the active account: $(gcloud auth list --filter=status:ACTIVE --format="value(account)")."
}

check_artifact_access() {
    # Checks if the user has access to the GDP Labs Google Artifact Registry.
    if ! gcloud artifacts packages list --repository=gen-ai --location=asia-southeast2 --project=gdp-labs; then
        handle_error "User does not have access to the GDP Labs Google Artifact Registry. Please contact the GDP Labs DSO team at infra(at)gdplabs.id."
    fi
    
    log "User has access to the GDP Labs Google Artifact Registry."
}

configure_poetry_python_path() {
    log "Configuring Poetry to use Python $PYTHON_PATH..."
    
    if ! "$POETRY_PATH" env use "$PYTHON_PATH"; then
        handle_error "Failed to configure Poetry to use Python $PYTHON_PATH. Please try again."
    fi
}

setup_poetry_http_basic() {
    log "Setting up POETRY_HTTP_BASIC_GEN_AI_USERNAME and POETRY_HTTP_BASIC_GEN_AI_PASSWORD..."
    export POETRY_HTTP_BASIC_GEN_AI_USERNAME=oauth2accesstoken
    export POETRY_HTTP_BASIC_GEN_AI_PASSWORD=$(gcloud auth print-access-token)
}

install_dependencies() {
    log "Installing dependencies..."

    if ! "$POETRY_PATH" install; then
        handle_error "Failed to install dependencies. Please try again."
    fi
}

show_poetry_python_interpreter_path() {
    log "Getting Python interpreter path for use in IDE..."
    
    if ! "$POETRY_PATH" env info --executable; then
        handle_error "Failed to get Python interpreter path. Please try again."
    fi
}

main() {
    # Main function to orchestrate the deployment script.
    log "${COLOR_INFO}Checking custom-tool-and-agent example requirements...$COLOR_RESET"
    get_python_path
    check_requirements
    install_command "poetry" "$POETRY_VERSION"

    deactivate_conda
    check_gcloud_login
    check_artifact_access
    log "${COLOR_SUCCESS}All requirements are satisfied.$COLOR_RESET"

    log "${COLOR_INFO}Setting up custom-tool-and-agent example...$COLOR_RESET"
    copy_env_file
    setup_poetry_http_basic
    configure_poetry_python_path
    install_dependencies
    log "${COLOR_SUCCESS}custom-tool-and-agent example ready to run.$COLOR_RESET"

    show_poetry_python_interpreter_path
    log "${COLOR_SUCCESS}custom-tool-and-agent example finished running.$COLOR_RESET"
}

main
