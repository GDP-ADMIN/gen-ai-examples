@echo off
setlocal enabledelayedexpansion

REM Define acceptable Python versions
set "PYTHON_VERSIONS=3.11 3.12"
set "POETRY_VERSION=1.8.1"
set "GCLOUD_VERSION=493.0.0"

set "PYTHON_CMD=python"
set "LOG_FILE=.\deploy.log"

set "PYTHON_PATH="
set "POETRY_PATH="

REM Colors for logging
set "COLOR_ERROR=[91m"
set "COLOR_WARNING=[93m"
set "COLOR_INFO=[94m"
set "COLOR_SUCCESS=[92m"
set "COLOR_RESET=[0m"

REM Clear the log file
type nul > "%LOG_FILE%"

REM Create a log file that we'll append to
echo %DATE% %TIME% - Starting custom-tool-and-agent setup > "%LOG_FILE%"

REM Function to get timestamp
:get_timestamp
set "TIMESTAMP=[%DATE% %TIME%]"
exit /b

REM Function to log messages
:log
call :get_timestamp
echo %COLOR_INFO%%TIMESTAMP%%COLOR_RESET% %~1
echo %TIMESTAMP% %~1 >> "%LOG_FILE%"
exit /b

REM Function to handle errors and exit
:handle_error
call :get_timestamp
echo %COLOR_ERROR%%TIMESTAMP% An error occurred: %~1%COLOR_RESET%
echo %TIMESTAMP% ERROR: %~1 >> "%LOG_FILE%"
call :exit_application
exit /b

REM Function to exit application
:exit_application
call :log "%COLOR_WARNING%Exiting...%COLOR_RESET%"
exit /b 1

REM Function to get Python path
:get_python_path
where python >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    for /f "tokens=*" %%i in ('where python') do (
        set "PYTHON_PATH=%%i"
        set "PYTHON_CMD=python"
    )
) else (
    call :handle_error "Python not found. Please install Python %PYTHON_VERSIONS%"
)

call :log "PYTHON_PATH will be set to: %PYTHON_PATH%"
exit /b

REM Function to get Poetry path
:get_poetry_path
set "POETRY_PATH=%APPDATA%\pypoetry\venv\Scripts\poetry.exe"
if not exist "%POETRY_PATH%" (
    if defined POETRY_HOME (
        set "POETRY_PATH=%POETRY_HOME%\venv\Scripts\poetry.exe"
    ) else (
        call :handle_error "Poetry path not found. Please install Poetry."
    )
)

call :log "Detected Poetry path: %POETRY_PATH%"
exit /b

REM Function to install command
:install_command
set "cmd=%~1"
set "required_version=%~2"

if "%cmd%"=="poetry" (
    call :log "Attempting to install the latest version of %cmd%..."
    
    call :log "Installing Poetry via PowerShell..."
    powershell -NoProfile -ExecutionPolicy Bypass -Command "(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -"
    if %ERRORLEVEL% NEQ 0 (
        call :handle_error "Failed to install %cmd% version %required_version%."
    )
    
    call :get_poetry_path
) else (
    if "%cmd%"=="%PYTHON_CMD%" (
        call :handle_error "Please use Python version %PYTHON_VERSIONS%."
    ) else (
        call :handle_error "Please install %cmd% version %required_version% or above."
    )
)
exit /b

REM Function to extract version number
:extract_version
for /f "tokens=*" %%a in ('%~1 %~2 2^>^&1') do (
    set "VERSION_OUTPUT=%%a"
    call :parse_version "!VERSION_OUTPUT!"
)
exit /b

REM Function to parse version string
:parse_version
set "version_string=%~1"
for /f "tokens=1,2,3 delims=. " %%a in ('echo %version_string%') do (
    set "parsed_version=%%a.%%b.%%c"
)
exit /b

REM Function to check if a version is in allowed array
:check_version_array
set "current_version=%~1"
set "command_name=%~2"
set "version_matched=false"

for %%v in (%PYTHON_VERSIONS%) do (
    echo !current_version! | findstr /r "^%%v\.[0-9]*$" >nul
    if !ERRORLEVEL! EQU 0 (
        set "version_matched=true"
    )
)

if "!version_matched!"=="false" (
    call :handle_error "%command_name% version must be either (%PYTHON_VERSIONS%). Current version: %current_version%."
)
exit /b

REM Function to check command version
:check_command_version
set "cmd=%~1"
set "required_version=%~2"
set "version_flag=%~3"

where %cmd% >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    call :log "%cmd% is not installed. Required version: %required_version%."
    call :install_command "%cmd%" "%required_version%"
    exit /b
)

REM Get current version
for /f "tokens=* usebackq" %%a in (`%cmd% %version_flag% 2^>^&1`) do (
    set "version_output=%%a"
    echo !version_output! | findstr /r "[0-9]\+\.[0-9]\+\.[0-9]\+" >nul
    if !ERRORLEVEL! EQU 0 (
        for /f "tokens=1,2,3 delims=. " %%x in ("!version_output!") do (
            set "current_version=%%x.%%y.%%z"
        )
    )
)

if not defined current_version (
    call :handle_error "Could not determine %cmd% version. Please ensure it is installed correctly."
)

REM Check Python version specifically
if "%cmd%"=="%PYTHON_CMD%" (
    call :check_version_array "!current_version!" "%PYTHON_CMD%"
) else (
    REM Basic version check for other commands (not implementing compare_versions fully)
    echo %current_version% | findstr /r "^[0-9]" >nul
    if !ERRORLEVEL! NEQ 0 (
        call :handle_error "%cmd% version %required_version% or above is required."
    )
)

call :log "%cmd% is installed and meets the required version. Current version: %current_version%."
exit /b

REM Function to check requirements
:check_requirements
call :log "Checking system requirements..."

call :check_command_version "%PYTHON_CMD%" "%PYTHON_VERSION%" "--version"
call :check_command_version "gcloud" "%GCLOUD_VERSION%" "--version"

call :log "System requirements are satisfied."
exit /b

REM Function to deactivate conda
:deactivate_conda
where conda >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    call :log "Checking for active Conda environments..."
    
    if defined CONDA_DEFAULT_ENV (
        call :log "Conda environment '%CONDA_DEFAULT_ENV%' is active. Deactivating..."
        call conda deactivate 2>nul
        call :log "Conda environment has been deactivated."
    ) else (
        call :log "No active Conda environment detected."
    )
) else (
    call :log "Conda is not installed. Skipping conda deactivation."
)
exit /b

REM Function to copy env file
:copy_env_file
if not exist ".env" (
    if exist ".env.example" (
        copy ".env.example" ".env" >nul
        call :log "Successfully copied '.env.example' to '.env'."
        call :log "%COLOR_WARNING%Please change the values in the .env file with your own values and then run 'local-start.bat' again.%COLOR_RESET%"
        call :exit_application
    ) else (
        call :log ".env.example file not found. Continuing without creating .env file."
    )
) else (
    call :log ".env file exists. Continuing..."
)
exit /b

REM Function to check gcloud login
:check_gcloud_login
for /f "tokens=*" %%a in ('gcloud auth list --filter^=status:ACTIVE --format^="value(account)" 2^>^&1') do (
    set "ACTIVE_ACCOUNT=%%a"
)

if not defined ACTIVE_ACCOUNT (
    call :handle_error "No active gcloud account found. Please log in using 'gcloud auth login'."
)

call :log "User is successfully logged into gcloud with the active account: %ACTIVE_ACCOUNT%."
exit /b

REM Function to check artifact access
:check_artifact_access
gcloud artifacts packages list --repository=gen-ai --location=asia-southeast2 --project=gdp-labs >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    call :handle_error "User does not have access to the GDP Labs Google Artifact Registry. Please contact the GDP Labs DSO team at infra(at)gdplabs.id."
)

call :log "User has access to the GDP Labs Google Artifact Registry."
exit /b

REM Function to configure poetry python path
:configure_poetry_python_path
call :log "Configuring Poetry to use Python %PYTHON_PATH%..."

"%POETRY_PATH%" env use "%PYTHON_PATH%" >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    call :handle_error "Failed to configure Poetry to use Python %PYTHON_PATH%. Please try again."
)
exit /b

REM Function to setup poetry http basic
:setup_poetry_http_basic
call :log "Setting up POETRY_HTTP_BASIC_GEN_AI_USERNAME and POETRY_HTTP_BASIC_GEN_AI_PASSWORD..."
set "POETRY_HTTP_BASIC_GEN_AI_USERNAME=oauth2accesstoken"

for /f "tokens=*" %%a in ('gcloud auth print-access-token') do (
    set "POETRY_HTTP_BASIC_GEN_AI_PASSWORD=%%a"
)
exit /b

REM Function to install dependencies
:install_dependencies
call :log "Installing dependencies..."

"%POETRY_PATH%" install
if %ERRORLEVEL% NEQ 0 (
    call :handle_error "Failed to install dependencies. Please try again."
)
exit /b

REM Function to show poetry python interpreter path
:show_poetry_python_interpreter_path
call :log "Getting Python interpreter path for use in IDE..."

"%POETRY_PATH%" env info --executable
if %ERRORLEVEL% NEQ 0 (
    call :handle_error "Failed to get Python interpreter path. Please try again."
)
exit /b

REM Main function
:main
call :log "%COLOR_INFO%Checking custom-tool-and-agent example requirements...%COLOR_RESET%"
call :get_python_path
call :check_requirements
call :install_command "poetry" "%POETRY_VERSION%"

call :deactivate_conda
call :check_gcloud_login
call :check_artifact_access
call :log "%COLOR_SUCCESS%All requirements are satisfied.%COLOR_RESET%"

call :log "%COLOR_INFO%Setting up custom-tool-and-agent example...%COLOR_RESET%"
call :copy_env_file
call :setup_poetry_http_basic
call :configure_poetry_python_path
call :install_dependencies
call :log "%COLOR_SUCCESS%custom-tool-and-agent example ready to run.%COLOR_RESET%"

call :show_poetry_python_interpreter_path
call :log "%COLOR_SUCCESS%custom-tool-and-agent example finished running.%COLOR_RESET%"

exit /b

REM Call main function
call :main
endlocal
