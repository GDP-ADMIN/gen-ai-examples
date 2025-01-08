@echo off
setlocal EnableDelayedExpansion

:: Set Variables
set "PYTHON_VERSION=3.11"
set "POETRY_VERSION=1.8.1"
set "GCLOUD_VERSION=493.0.0"

set "PYTHON_CMD=python"
set PYTHON_PATH=""

:: Main Section
call :log "Checking gen-ai-hello-world example requirements..."
call :get_python_path
call :check_requirements
call :deactivate_conda
call :check_gcloud_login
call :check_artifact_access
call :log "Setting up gen-ai-hello-world example..."
call :copy_env_file
call :setup_poetry_http_basic
call :install_dependencies
call :log "Running gen-ai-hello-world example..."
poetry run python gen_ai_hello_world/main.py || (
    call :handle_error "Failed to run the application"
    exit /b 1
)
exit /b

:get_python_path
where python3 >nul 2>&1
if %errorlevel% equ 0 ( 
    set "PYTHON_CMD=python3"
) else (
    call :log "python3 command not found, using python instead..."
    where python >nul 2>&1
    if %errorlevel% equ 0 (
        set "PYTHON_CMD=python"
    ) else (
        call :handle_error "Python not found. Please install Python %PYTHON_VERSION%"
    )
)
for /f "delims=" %%i in ('where %PYTHON_CMD%') do (
    set "PYTHON_PATH=%%i"
)
call :log "PYTHON_PATH will be set to: !PYTHON_PATH!"
exit /b

:: Check command version function
:check_command_version
set "cmd=%~1"
set "required_version=%~2"
set "version_flag=%~3"
where !cmd! >nul 2>&1
if %errorlevel% neq 0 (
    call :handle_error "!cmd! is not installed. Please install !cmd! version !required_version! or above."
    exit /b 1
)
:: Execute the command and capture the output
for /f "tokens=* usebackq" %%i in (`!cmd! !%version_flag! 2^>^&1`) do (
    set "version_output=%%i"   
    :: Extract version number using a regular expression
    for /f "tokens=* usebackq" %%v in (`powershell -Command "$version='!version_output!'; if($version -match '\d+\.\d+\.\d+') { $matches[0] }"`) do (
        set "current_version=%%v"
    )
    goto :break
)
:break
if "!current_version!"=="" (
    call :handle_error "Could not determine !cmd! version. Please ensure it is installed correctly."
    exit /b 1
)
:: Compare versions using powershell
powershell -Command "$current='!current_version!'; $required='!required_version!'; if([version]$current -lt [version]$required) { exit 1 } else { exit 0 }" >nul 2>&1
if %errorlevel% neq 0 (
    call :handle_error "!cmd! version !required_version! or above is required. You have version !current_version!."
    exit /b 1
)
call :log "!cmd! is installed and meets the required version (!required_version!). Current version: !current_version!"
exit /b

:check_requirements
call :log "Checking system requirements..."
:: Check command version
call :check_command_version "python" "%PYTHON_VERSION%" "--version"
call :check_command_version "poetry" "%POETRY_VERSION%" "--version"
call :check_command_version "gcloud" "%GCLOUD_VERSION%" "--version"
call :log "System requirements are satisfied."
exit /b

:: Deactivate conda function
:deactivate_conda
where conda >nul 2>&1
if %errorlevel% equ 0 (
    for /f "tokens=* usebackq" %%i in (`conda info --base`) do (
        set "CONDA_BASE=%%i"
    )
    
    if defined CONDA_DEFAULT_ENV (
        call :log "Conda environment '%CONDA_DEFAULT_ENV%' is active. Deactivating..."
        call conda deactivate
    )
    call :log "All Conda environments have been deactivated."
) else (
    call :log "Conda is not installed. Skipping conda deactivation."
)
exit /b

:check_gcloud_login
for /f "tokens=*" %%i in ('gcloud auth list --filter=status:ACTIVE --format="value(account)" 2^>nul') do (
    set "active_account=%%i"
)
if not defined active_account (
    call :handle_error "No active gcloud account found. Please log in using 'gcloud auth login'."
) else (
    call :log "User is successfully logged into gcloud with the active account: !ACTIVE_ACCOUNT!"
)
exit /b

:check_artifact_access
cmd /c gcloud artifacts packages list --repository=gen-ai --location=asia-southeast2 --project=gdp-labs >nul 2>&1
if %errorlevel% neq 0 (
    call :handle_error "User does not have access to the GDP Labs Google Artifact Registry. Please contact the GDP Labs DSO team at infra(at)gdplabs.id."
)
call :log "User has access to the GDP Labs Google Artifact Registry."
exit /b

:copy_env_file
if not exist ".env" (
    copy .env.example .env >nul 2>&1
    call :log "Successfully copied '.env.example' to '.env'."
    call :log "Please change the values in the .env file with your own values and then run './local-start.sh' again."
    call :exit_application
)
call :log ".env file exists. Continuing..."
exit /b

:setup_poetry_http_basic
call :log "Setting up POETRY_HTTP_BASIC_GEN_AI_USERNAME and POETRY_HTTP_BASIC_GEN_AI_PASSWORD..."
set "POETRY_HTTP_BASIC_GEN_AI_USERNAME=oauth2accesstoken"
for /f "tokens=* usebackq" %%i in (`gcloud auth print-access-token`) do (
    set "POETRY_HTTP_BASIC_GEN_AI_PASSWORD=%%i"
)
exit /b

:install_dependencies
call :log "Installing dependencies..."
poetry install || call :handle_error "Failed to install dependencies."
exit /b

:: Logging function
:log
echo [%date:~10,4%-%date:~4,2%-%date:~7,2% %time:~0,8%] - %~1
exit /b

:: Error handling function
:handle_error
call :log "An error occurred: %~1"
call :exit_application
exit /b

:: Exit application function
:exit_application
call :log "Exiting..."
call :exit_batch

:exit_batch
if not exist "%temp%\ExitBatchYes.txt" call :build_yes
call :CtrlC <"%temp%\ExitBatchYes.txt" 1>nul 2>&1

:: Error code terminated by user
:CtrlC
cmd /c exit -1073741510

:: To give yes reponse when exit
:build_yes
pushd "%temp%"
set "yes="
copy nul ExitBatchYes.txt >nul
for /f "delims=(/ tokens=2" %%Y in (
  '"copy /-y nul ExitBatchYes.txt <nul"'
) do if not defined yes set "yes=%%Y"
echo %yes%>ExitBatchYes.txt
popd
exit /b
