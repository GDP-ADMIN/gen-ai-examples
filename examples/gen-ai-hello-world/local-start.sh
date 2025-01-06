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
    echo "[LOG][$(date '+%Y-%m-%d %H:%M:%S')] $1"
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

get_conda_python_path() {
    if ! CONDA_BASE=$(conda info --base); then
        handle_error "Failed to retrieve Conda base path."
    fi

    if ! conda list | grep -q "python "; then
        handle_error "Python is not installed in the Conda environment. Please install it inside the Conda environment."
    fi

    # Set the python on the global to point to this python inside the miniconda
    PYTHON_PATH="$CONDA_BASE/bin"

    log "Successfully retrieved the Conda environment with Python version '$PYTHON_VERSION'."
}

export_python_path() {
    log "Using Python on $PYTHON_PATH"
    export PATH="$PYTHON_PATH:$PATH"
    hash -r
}

update_shell_path() {
    local shell_rc=$1
    local poetry_path="$HOME/.local/bin"

    if ! grep -q "$poetry_path" "$shell_rc" 2>/dev/null; then
        echo "export PATH=\"$poetry_path:\$PATH\"" >> "$shell_rc"
        log "Added Poetry to PATH in $shell_rc"
    fi

    # Source the shell configuration file to update the current session
    if [ -f "$shell_rc" ]; then
        case "$SHELL" in
            */zsh)
                # shellcheck disable=SC1090
                source "$shell_rc" || log "Failed to source $shell_rc in Zsh."
                ;;
            */bash)
                # shellcheck disable=SC1090
                source "$shell_rc" || log "Failed to source $shell_rc in Bash."
                ;;
            *)
                log "Unsupported shell for sourcing $shell_rc."
                ;;
        esac
        log "Sourced $shell_rc to update PATH for the current session."
    fi
}

update_fish_path() {
    local fish_config="$HOME/.config/fish/config.fish"
    local poetry_path="$HOME/.local/bin"

    if ! grep -q "$poetry_path" "$fish_config" 2>/dev/null; then
        echo "set -U fish_user_paths $poetry_path \$fish_user_paths" >> "$fish_config"
        log "Added Poetry to PATH in $fish_config"
    fi

    # Source the fish configuration file to update the current session
    fish -c "source $fish_config"
    log "Sourced $fish_config to update PATH for the current session."
}

update_tcsh_path() {
    local tcsh_rc="$HOME/.tcshrc"
    local poetry_path="$HOME/.local/bin"

    if ! grep -q "$poetry_path" "$tcsh_rc" 2>/dev/null; then
        echo "setenv PATH \"$poetry_path:\$PATH\"" >> "$tcsh_rc"
        log "Added Poetry to PATH in $tcsh_rc"
    fi

    # Source the tcsh configuration file to update the current session
    source "$tcsh_rc"
    log "Sourced $tcsh_rc to update PATH for the current session."
}

detect_and_update_shell_path() {
    case "$SHELL" in
        */bash)
            update_shell_path ~/.bashrc
            ;;
        */zsh)
            update_shell_path ~/.zshrc
            ;;
        */fish)
            update_fish_path
            ;;
        */tcsh)
            update_tcsh_path
            ;;
        *)
            log "Unsupported shell. Please update your PATH manually."
            ;;
    esac

    # Clear the command hash table to ensure the shell recognizes the updated PATH
    hash -r
}

install_command() {
    local cmd=$1
    local required_version=$2

    if [[ "$cmd" == "poetry" ]]; then
        log "Attempting to install the latest version of $cmd..."

        # If the installed poetry is detected, remove it before reinstalling
        if [ -d ~/.local/share/pypoetry ] || [ -f ~/.local/bin/poetry ]; then
            log "Removing existing Poetry installation..."
            if ! curl -sSL https://install.python-poetry.org | python3 - --uninstall; then
                handle_error "Failed to remove existing Poetry installation. Please remove it manually."
            fi
        fi

        # Install the latest version of Poetry
        if ! curl -sSL https://install.python-poetry.org | python3 -; then
            handle_error "Failed to install $cmd version $required_version."
        fi

        # Update PATH in both .bashrc and .zshrc for future interactive sessions
        detect_and_update_shell_path

        log "$cmd version $required_version installed successfully."
    else
        handle_error "Please install $cmd version $required_version or above manually."
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
    current_version=$("$cmd" "$version_flag" 2>&1 | grep -Eo '[0-9]+(\.[0-9]+)+')
    if [[ -z "$current_version" ]]; then
        handle_error "Could not determine $cmd version. Please ensure it is installed correctly."
    fi

    # Compare versions (lexicographically sorted)
    if [[ "$(printf '%s\n' "$required_version" "$current_version" | sort -V | head -n1)" != "$required_version" ]]; then
        log "$cmd version $required_version or above is required. You have version $current_version."
        install_command "$cmd" "$required_version"
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


copy_env_file() {
    # Copies the .env.example file to .env.
    if [[ ! -f ".env" ]]; then
        cp .env.example .env
        
        # Prompt user to edit the .env file
        log "Please edit the .env file with your own values."
        nano .env
    fi
}

main() {
    # Main function to orchestrate the deployment script.
    log "Checking gen-ai-hello-world example requirements..."
    check_requirements
    deactivate_conda
    check_gcloud_login
    check_artifact_access
    copy_env_file

    log "Running gen-ai-hello-world example..."
    export POETRY_HTTP_BASIC_GEN_AI_USERNAME=oauth2accesstoken
    export POETRY_HTTP_BASIC_GEN_AI_PASSWORD=$(gcloud auth print-access-token)
    poetry install
    poetry run python gen_ai_hello_world/main.py
}

main
