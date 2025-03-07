#!/bin/bash

PYTHON_VERSIONS=("3.11" "3.12") # acceptable versions
POETRY_VERSION="1.8.1"

PYTHON_CMD="python"
LOG_FILE="./deploy.log"

PYTHON_PATH=""
POETRY_PATH=""

PROJECT_NAME="simple-pipeline"

# colors for logging
COLOR_ERROR="\033[31m"
COLOR_WARNING="\033[33m"
COLOR_INFO="\033[34m"
COLOR_SUCCESS="\033[32m"
COLOR_RESET="\033[0m"

> "$LOG_FILE" # Clear the log file

# Write console output to both console and a file
PIPE=$(mktemp -u)
mkfifo "$PIPE"
tee -a "$LOG_FILE" < "$PIPE" &
exec >"$PIPE" 2>&1

cleanup() {
    rm -f "$PIPE"
    exit_application
}
trap cleanup INT

get_timestamp() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')]"
}

log() {
    echo -e "${COLOR_INFO}$(get_timestamp)$COLOR_RESET" "$1"
}

exit_application() {
    log "${COLOR_WARNING}Exiting...$COLOR_RESET"
    exit 1
}

handle_error() {
    echo -e "${COLOR_ERROR}$(get_timestamp) An error occurred\n $1$COLOR_RESET"
    exit_application
}

trap handle_error ERR INT TERM

get_python_path() {
    if command -v python3 >/dev/null 2>&1; then
        PYTHON_PATH=$(command -v python3)
        PYTHON_CMD="python3"    
    elif command -v python >/dev/null 2>&1; then
        PYTHON_PATH=$(command -v python)
        PYTHON_CMD="python"
    else
        handle_error "Python not found. Please install Python version ${PYTHON_VERSIONS[*]}"
    fi

    log "PYTHON_PATH will be set to: $PYTHON_PATH"
}

get_poetry_path() {
    if [[ "$OSTYPE" == "darwin"* ]]; then
        POETRY_PATH="$HOME/Library/Application Support/pypoetry/venv/bin/poetry"
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        if grep -q "microsoft" /proc/version 2>/dev/null; then
            POETRY_PATH="$HOME/.local/bin/poetry"
        else
            POETRY_PATH="$HOME/.local/share/pypoetry/venv/bin/poetry"
        fi
    elif [[ "$OSTYPE" == "cygwin" || "$OSTYPE" == "msys" ]]; then
        POETRY_PATH="%APPDATA%\\pypoetry\\venv\\Scripts\\poetry"
    elif [[ -n "$POETRY_HOME" ]]; then
        POETRY_PATH="$POETRY_HOME/venv/bin/poetry"
    else
        handle_error "Unsupported operating system or POETRY_HOME not set."
    fi

    log "Detected Poetry path: $POETRY_PATH"
}

install_command() {
    local cmd=$1
    local required_version=$2

    if [[ "$cmd" == "poetry" ]]; then
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

    if [[ "$cmd" == "$PYTHON_CMD" ]]; then
        check_version_array "$current_version" "$PYTHON_CMD" "${PYTHON_VERSIONS[@]}"
    fi
    
    log "$cmd is installed with version: $current_version"
}

deactivate_conda() {
    if command -v conda >/dev/null 2>&1; then
        CONDA_BASE=$(conda info --base 2>/dev/null)

        if [ -n "$CONDA_BASE" ] && [ -f "$CONDA_BASE/etc/profile.d/conda.sh" ]; then
            . "$CONDA_BASE/etc/profile.d/conda.sh" || {
                handle_error "Warning: Unable to source conda.sh"
            }

            while [ -n "$CONDA_DEFAULT_ENV" ]; do
                log "Deactivating Conda environment '$CONDA_DEFAULT_ENV'..."
                conda deactivate
            done
            log "All Conda environments have been deactivated."
        fi
    fi
}

configure_poetry_python_path() {
    log "Configuring Poetry to use Python $PYTHON_PATH..."
    
    if ! "$POETRY_PATH" env use "$PYTHON_PATH"; then
        handle_error "Failed to configure Poetry to use Python $PYTHON_PATH"
    fi
}

install_dependencies() {
    log "Installing dependencies..."

    if ! "$POETRY_PATH" install; then
        handle_error "Failed to install dependencies"
    fi
}

show_poetry_python_interpreter_path() {
    log "Python interpreter path for IDE configuration:"
    "$POETRY_PATH" env info --executable
}

main() {
    log "${COLOR_INFO}Starting local setup...$COLOR_RESET"
    get_python_path
    check_command_version "$PYTHON_CMD" "" "--version"
    install_command "poetry" "$POETRY_VERSION"
    deactivate_conda
    
    log "${COLOR_INFO}Setting up project...$COLOR_RESET"
    configure_poetry_python_path
    install_dependencies
    
    log "${COLOR_SUCCESS}$PROJECT_NAME example ready to run.$COLOR_RESET"
    
    log "${COLOR_INFO}Running $PROJECT_NAME example...$COLOR_RESET"
    "$POETRY_PATH" run $PYTHON_CMD main.py

    show_poetry_python_interpreter_path
    log "${COLOR_SUCCESS}$PROJECT_NAME example finished running.$COLOR_RESET"
}

main 