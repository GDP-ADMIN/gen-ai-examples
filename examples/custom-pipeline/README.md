# GLLM Plugin Hello World for Custom Pipeline

This is an example of how to use the gllm-plugin library to build a custom pipeline.

> [!WARNING]
> The GenAI SDK binary version is currently only available for Linux, macOS, and Windows.

## Prerequisites

> [!NOTE]
> You need to fulfill the prerequisites to run the script. They will be checked automatically when you execute it.

1. **Python v3.12** (to run `python`)

   - Using Conda (recommended):

     You can use [Miniconda](https://docs.anaconda.com/miniconda/install) to install and manage Python versions.

   - <details>
     <summary>Using Python installer (alternative)</summary>
     
     You can download the Python installer from the link [Python 3.12.8](https://www.python.org/downloads/release/python-3128/), select the version appropriate for your operating system, and run the installer.

     > [!NOTE]
     > For Windows, please make sure to check the `Add python.exe to PATH` option during the installation process.
   </details>

2. **Google Cloud CLI v493.0.0 or above** (to run `gcloud`).

   - You can install it by following [this instruction](https://cloud.google.com/sdk/docs/install).
   - After installing it, sign in to your account using `gcloud auth login` command.
   - If the `gcloud` CLI asks you to enter project ID, enter `gdp-labs`.

3. **Access to the GDP Labs Google Artifact Registry**.
   - If you don’t have access, please make a request to ticket(at)gdplabs.id.


## Running the Code

1. Configure environment variables: copy `.env.example` to `.env` and set up your `OPENAI_API_KEY` and `LANGUAGE_MODEL`.

   - For Linux, macOS, or Windows WSL:

     ```bash
     cp .env.example .env
     ```

   - For Windows Powershell or Command Prompt:

     ```powershell
     copy .env.example .env
     ```

2. Execute the script:

   - For Linux, macOS, or Windows WSL:

     ```bash
     ./local-start.sh
     ```

     > [!NOTE]
     > On Windows, you can either install [WSL (Windows Subsystem for Linux)](https://learn.microsoft.com/en-us/windows/wsl/install) or execute the batch file in Windows Powershell or Command Prompt as described in the next section.

   - For Windows Powershell:

     ```powershell
     .\local-start.bat
     ```

   - For Windows Command Prompt:

     ```cmd
     local-start.bat
     ```

   The program will then wait for your question:

      > Question:

      Type your question and press enter. For example, you can try asking:

      ```
      What is artificial intelligence?
      ```

      The custom pipeline will return the following response (more or less):

      > _Artificial Intelligence (AI) refers to the simulation of human intelligence in machines that are programmed to think, learn, and perform tasks that typically require human cognitive functions. This includes activities like problem-solving, understanding natural language, recognizing patterns, making decisions, and adapting to new information..._