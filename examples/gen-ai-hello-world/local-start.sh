#!/bin/bash

PYTHON_VERSIONS=("3.11" "3.12") # acceptable versions
POETRY_VERSION="1.8.1"
GCLOUD_VERSION="493.0.0"

PYTHON_CMD="python"
LOG_FILE="./deploy.log"

PYTHON_PATH=""

# colors for logging
COLOR_ERROR="\033[31m"
COLOR_WARNING="\033[33m"
COLOR_INFO="\033[34m"
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
    echo -e "$COLOR_INFO$(get_timestamp)$COLOR_RESET $1"
}

exit_application() {
    # Handles script termination, logging a shutdown message and exiting with code 1.
    echo -e "$COLOR_WARNING"
    log "Exiting..."
    echo -e "$COLOR_RESET"

    exit 1
}

handle_error() {
    # Logs an error message and shuts down the application.
    echo -e "$COLOR_ERROR$(get_timestamp) An error occurred: $1$COLOR_RESET"

    exit_application
}

trap handle_error ERR

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

get_shell_rc() {
    case "$SHELL" in
        */bash)
            echo "$HOME/.bashrc"
            ;;
        */zsh)
            echo "$HOME/.zshrc"
            ;;
        *)
            handle_error "Unsupported shell. Please update your PATH manually and rerun the local-start.sh script again."
            ;;
    esac
}

update_shell_config() {
    local shell_rc=$(get_shell_rc)
    

    # Source the shell configuration file to update the current session
    if [ -f "$shell_rc" ]; then
        # shellcheck disable=SC1090
        source "$shell_rc" || log "Failed to source $shell_rc in ${SHELL##*/}."
        log "Sourced $shell_rc to update PATH for the current session."
    fi
}

update_poetry_path() {
    local shell_rc=$(get_shell_rc)
    local poetry_path

    # Determine the poetry path based on the operating system
    if [[ "$OSTYPE" == "darwin"* ]]; then
        poetry_path="$HOME/Library/Application Support/pypoetry/venv/bin/poetry" # macOS
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        if grep -q "microsoft" /proc/version 2>/dev/null; then
            poetry_path="$HOME/.local/bin/poetry" # WSL
        else
            poetry_path="$HOME/.local/share/pypoetry/venv/bin/poetry" # Linux/Unix
        fi
    elif [[ "$OSTYPE" == "cygwin" || "$OSTYPE" == "msys" ]]; then
        poetry_path="%APPDATA%\\pypoetry\\venv\\Scripts\\poetry" # Windows
    elif [[ -n "$POETRY_HOME" ]]; then
        poetry_path="$POETRY_HOME/venv/bin/poetry" # If $POETRY_HOME is set
    else
        handle_error "Unsupported operating system or POETRY_HOME not set."
    fi

    if [[ -f "$shell_rc" && -w "$shell_rc" ]]; then
        if ! grep -q "$poetry_path" "$shell_rc" 2>/dev/null; then
            echo "export PATH=\"$poetry_path:\$PATH\"" >> "$shell_rc"
            log "Added Poetry to PATH in $shell_rc"
        else
            log "Poetry path already exists in $shell_rc"
        fi
    else
        log "Shell configuration file $shell_rc does not exist or is not writable."
    fi
}

install_command() {
    local cmd=$1
    local required_version=$2

    if [[ "$cmd" == "poetry" ]]; then
        log "Attempting to install the latest version of $cmd..."

        # If the installed poetry is detected, remove it before reinstalling
        if [ -d ~/.local/share/pypoetry ] || [ -f ~/.local/bin/poetry ]; then
            log "Poetry is installed but is not detected. Removing existing Poetry installation..."
            if ! curl -sSL https://install.python-poetry.org | $PYTHON_CMD - --uninstall; then
                handle_error "Failed to remove existing Poetry installation. Please remove it manually."
            fi
        fi

        # Install the latest version of Poetry
        log "Installing Poetry via curl..."
        if ! curl -sSL https://install.python-poetry.org | $PYTHON_CMD -; then
            handle_error "Failed to install $cmd version $required_version."
        fi

        # Update PATH in both .bashrc and .zshrc for future interactive sessions
        update_poetry_path
        update_shell_config

        # Wait for a moment to ensure the system recognizes the new installation
        sleep 2
    else
        if [[ "$cmd" == "$PYTHON_CMD" ]]; then
            handle_error "Please use Python version ${PYTHON_VERSIONS[*]}."
        else
            handle_error "Please install $cmd version $required_version or above manually."
        fi
    fi
}

compare_versions() {
    # Compare two version strings $1 and $2
    # Returns 0 if $1 == $2, 1 if $1 > $2, and 2 if $1 < $2
    if [[ "$1" == "$2" ]]; then
        return 0
    fi

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
            return 0 # The current version is greater than the required version
        fi
        if ((10#${ver1[i]} < 10#${ver2[i]})); then
            return 2 # The current version is less than the required version
        fi
    done

    return 0 # The current version is equal to the required version
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
        if [[ $? == 2 ]]; then
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
    check_command_version "poetry" "$POETRY_VERSION" "--version"
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

copy_env_file() {
    # Copies the .env.example file to .env.
    if [[ ! -f ".env" ]]; then
        cp .env.example .env
        log "Successfully copied '.env.example' to '.env'."
        log "$COLOR_WARNING Please change the values in the .env file with your own values and then run './local-start.sh' again.$COLOR_RESET"
        exit_application
    fi

    log ".env file exists. Continuing..."
}

main() {
    # Main function to orchestrate the deployment script.
    log "$COLOR_GREEN Checking gen-ai-hello-world example requirements...$COLOR_RESET"

    get_python_path
    check_requirements
    deactivate_conda
    check_gcloud_login
    check_artifact_access

    log "$COLOR_GREEN Setting up gen-ai-hello-world example...$COLOR_RESET"
    copy_env_file

    export POETRY_HTTP_BASIC_GEN_AI_USERNAME=oauth2accesstoken
    export POETRY_HTTP_BASIC_GEN_AI_PASSWORD=$(gcloud auth print-access-token)
    poetry install

    log "$COLOR_GREEN Running gen-ai-hello-world example...$COLOR_RESET"
    poetry run $PYTHON_CMD gen_ai_hello_world/main.py
}

main
