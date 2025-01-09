@echo off
setlocal EnableDelayedExpansion

:: Set Variables
set "PYTHON_VERSION=3.11 3.12"
set "POETRY_VERSION=1.8.1"
set "GCLOUD_VERSION=493.0.0"

set "PYTHON_CMD=python"
set PYTHON_PATH=""
set POETRY_PATH=""

(
:: Main Section
call :log "Checking gen-ai-hello-world example requirements..."
call :get_python_path
call :check_requirements
call :install_command "poetry" "%POETRY_VERSION%"
call :deactivate_conda
call :check_gcloud_login
call :check_artifact_access
call :log "All requirements are satisfied."
call :log "Setting up gen-ai-hello-world example..."
call :copy_env_file
call :setup_poetry_http_basic
call :install_dependencies
call :log "gen-ai-hello-world example ready to run."
call :log "Running gen-ai-hello-world example..."
!POETRY_PATH! run python gen_ai_hello_world/main.py || (
    call :handle_error "Failed to run the application"
    exit /b 1
)
call :log "gen-ai-hello-world example finished running."
exit /b
)

:get_python_path
where python >nul 2>&1
if %errorlevel% equ 0 ( 
    set "PYTHON_CMD=python"
) else (
    call :log "python command not found, trying to use python3 instead..."
    where python3 >nul 2>&1
    if %errorlevel% equ 0 (
        set "PYTHON_CMD=python3"
    ) else (
        call :handle_error "Python not found. Please install Python with one of these versions %PYTHON_VERSION%"
    )
)
for /f "delims=" %%i in ('where %PYTHON_CMD%') do (
    set "PYTHON_PATH=%%i"
)
call :log "use python command: !PYTHON_CMD!"
call :log "PYTHON_PATH will be set to: !PYTHON_PATH!"
exit /b

:check_requirements
call :log "Checking system requirements..."
:: Check command version
call :check_command_version "%PYTHON_CMD%" "%PYTHON_VERSION%" "--version"
call :check_command_version "gcloud" "%GCLOUD_VERSION%" "--version"
call :log "System requirements are satisfied."
exit /b

:: Check command version function
:check_command_version
set "cmd=%~1"
set "required_version=%~2"
set "version_flag=%~3"
where !cmd! >nul 2>&1
if %errorlevel% neq 0 (
    call :log "!cmd! is not installed. Required version: !required_version!."
    call :install_command !cmd! !required_version!
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
:: Check for exact Python version
if "!cmd!"=="%PYTHON_CMD%" (
    call :check_version_array !current_version! !cmd! "%PYTHON_VERSION%"
    if !errorlevel! neq 0 exit /b 1
) else (
    call :compare_versions "!current_version!" "!required_version!"
    if !errorlevel! equ 0 (
        call :log "!cmd! version !required_version! or above is required. You have version !current_version!."
        call :install_command !cmd! !required_version!
        exit /b 1
    )
)
call :log "!cmd! is installed and meets the required version (!required_version!). Current version: !current_version!"
exit /b

:check_version_array
set "current_version=%~1"
set "command_name=%~2"
set "version_array=%~3"
set "version_matched=false"
for %%v in (!version_array!) do (
    powershell -Command "$current='%current_version%'; if($current -match '^%%v\.[0-9]+$') { exit 0 } else { exit 1 }" >nul 2>&1
    if !errorlevel! equ 0 (
        set "version_matched=true"
        goto :version_match_end
    )
)
:version_match_end
if "!version_matched!"=="false" (
    call :handle_error "!command_name! version must be one of (!version_array!). Current version: %current_version%."
    exit /b 1
)
exit /b 0

:compare_versions
:: Parameters: %~1 = current version, %~2 = required version
:: Returns: errorlevel 0 if current version is less than required version
::         errorlevel 1 if current version is greater than or equal to required version
powershell -Command "function Compare-Version { param($ver1, $ver2); $v1 = [version]::new($ver1); $v2 = [version]::new($ver2); if ($v1 -lt $v2) { exit 0 } else { exit 1 } }; Compare-Version '%~1' '%~2'" >nul 2>&1
exit /b %errorlevel%

:install_command
set cmd=%~1
set required_version=%~2
if "%cmd%"=="poetry" (
    call :log "Attempting to install the latest version of %cmd%..."
    :: Install the latest version of Poetry
    call :log "Installing Poetry via powershell..."
        powershell -Command "(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | & $env:PYTHON_CMD -" || (
        call :handle_error "Failed to install %cmd% version %required_version%."
    )
    :: Update PATH in
    call :update_poetry_path
    :: Wait for a moment to ensure the system recognizes the new installation
    timeout /t 2 >nul
) else (
    if "%cmd%"=="%PYTHON_CMD%" (
        call :handle_error "Please use Python version %PYTHON_VERSIONS%."
    ) else (
        call :handle_error "Please install %cmd% version %required_version% or above manually."
    )
)
exit /b

:update_poetry_path
for /f "delims=" %%i in ('where poetry') do (
    set "POETRY_PATH=%%i"
)
call :log "POETRY_PATH will be set to: !POETRY_PATH!"
set "poetry_export_path=%POETRY_PATH:~0,-12%"
echo %PATH% | findstr /i /c:"%poetry_export_path%" >nul
if errorlevel 1 (
    set "PATH=%poetry_export_path%;%PATH%"
    setx PATH "%poetry_export_path%;%PATH%"
    call :log "Added Poetry to PATH"
) else (
    call :log "Poetry path already exists in PATH"
)
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
!POETRY_PATH! install || call :handle_error "Failed to install dependencies."
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
