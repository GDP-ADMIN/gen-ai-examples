# Prerequisites for GenAI Examples

This document contains all prerequisites needed to run the examples in the GenAI Examples repository.

## Python Environment

1. **Python v3.12**

   - Using Conda (recommended):
     You can use [Miniconda](https://docs.anaconda.com/miniconda/install) to install and manage Python versions.

   - Using Python installer (alternative):
     You can download the Python installer from [Python 3.12.8](https://www.python.org/downloads/release/python-3128/), select the version appropriate for your operating system, and run the installer.
     
     > [!NOTE]
     > For Windows, please make sure to check the `Add python.exe to PATH` option during the installation process.

## Google Cloud Requirements

1. **Google Cloud CLI v493.0.0 or above**

   - You can install it by following [this instruction](https://cloud.google.com/sdk/docs/install).
   - After installing it, sign in to your account using `gcloud auth login` command.
   - If the `gcloud` CLI asks you to enter project ID, enter `gdp-labs`.

2. **Access to the GDP Labs Google Artifact Registry**
   - This is required for some examples to download necessary dependencies.
   - If you don't have access, please make a request to ticket(at)gdplabs.id.

## Repository Access Requirements

1. **Access to GDP-ADMIN/gen-ai-internal repository**
   - You can try to access the [GDP-ADMIN/gen-ai-internal](https://github.com/GDP-ADMIN/gen-ai-internal) repository in your browser.
   - If you don't have access, please make a request to ticket(at)gdplabs.id.

2. **Access to GDP-ADMIN/gen-ai-external repository**
   - For some examples, you need access to [GDP-ADMIN/gen-ai-external](https://github.com/GDP-ADMIN/gen-ai-external).
   - If you don't have access, please make a request to ticket(at)gdplabs.id.

3. **SSH Key in your GitHub Account**
   - You must add your SSH key to your GitHub account for accessing private repositories.
   - Please follow this instruction by GitHub: [Adding a new SSH key to your GitHub account](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account).

## Development Environment

1. **VSCode IDE**
   - Go to [VSCode](https://code.visualstudio.com/download) to download VSCode IDE.


## Platform-Specific Requirements

### macOS Requirements

If you encounter `ImportError: failed to find libmagic` on macOS, you can resolve it by:

1. If you have [conda](https://docs.anaconda.com/miniconda/install/) installed:
   ```
   conda install libmagic
   cd /usr/local/lib
   sudo ln -s /opt/miniconda3/pkgs/libmagic-5.39-h6ba3021_1/lib/libmagic.dylib libmagic.dylib
   ```
   > [!WARNING]
   > Please adjust the path of your Conda installation if it differs. In the example above, the path is `/opt/miniconda3/`.

2. If you have [brew](https://brew.sh/) installed:
   ```
   brew install libmagic
   ```

### Binary SDK Compatibility

The GenAI SDK binary version is currently only available for:

1. **Linux / WSL**: x86_64 architecture.
2. **macOS**:
   - x86_64 (Intel) - macOS version 13 or newer
   - arm64 (Apple Silicon) - macOS version 14 or newer
3. **Windows**: 64bit architecture. 