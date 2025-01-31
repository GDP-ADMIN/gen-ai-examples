# GenAI RAGO Example

This is an example of how to use the gllm-pipeline library to build a simple RAG pipeline using binary version of SDK.

See other examples in [gen-ai-hello-world](https://github.com/GDP-ADMIN/gen-ai-examples).

> [!WARNING]
> The GenAI SDK binary version is currently only available for Linux, macOS, and Windows.

## Prerequisites

> [!NOTE]
> You need to fulfill the prerequisites to run the script. They will be checked automatically when you execute it.

1. **Python v3.12** (to run `python`).

   - Using Conda (recommended):

     You can use [Miniconda](https://docs.anaconda.com/miniconda/install) to install and manage Python versions.

   - Using Python installer (alternative):

     You can download the Python installer from the link [Python 3.12.8](https://www.python.org/downloads/release/python-3128/), select the version appropriate for your operating system, and run the installer.

     > [!NOTE]
     > For Windows, please make sure to check the `Add python.exe to PATH` option during the installation process.

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
What are the documents?
```

The RAG pipeline will return the following response (more or less):

> _The documents mentioned are referred to as Mock document 1, Mock document 2, and Mock document 3. However, without additional context or content from these documents, I cannot provide specific details about their contents or purposes._

## FAQs

### 1. I got error `Error executing component StuffResponseSynthesizer__user_query_response_synthesis_bundle`. How do I fix it?

Check `.env` file (if you already run `local-start.sh`, it is auto generated). You might have provided invalid `OPENAI_API_KEY` and/or `LANGUAGE_MODEL`.

```txt
# GDP Labs Gen AI Hello World Example
# Please edit the following variables with your own values.

OPENAI_API_KEY =<YOUR_OPENAI_API_KEY> # Get your OpenAI API key from https://platform.openai.com/api-keys
LANGUAGE_MODEL =<VALID_OPENAI_LANGUAGE_MODEL_NAME> # e.g. "gpt-3.5-turbo", "gpt-4o-mini", "gpt-4o"
```

### 2. I got error `OSError: could not get source code`. How do I fix it?

This error is currently expected. If you can see the response, it means the pipeline is working as expected.

Here is an example of the error.

```
Question: who are you?
/home/resti/glair/gen-ai/testing/gen-ai-examples/examples/gen-ai-hello-world/.venv/lib/python3.11/site-packages/gllm_core/schema/component.py:150: RuntimeWarning: Failed to analyze the _run method: could not get source code.
Traceback (most recent call last):
  File "/home/resti/glair/gen-ai/testing/gen-ai-examples/examples/gen-ai-hello-world/.venv/lib/python3.11/site-packages/gllm_core/schema/component.py", line 168, in _analyze_run_method
  File "/home/resti/anaconda3/envs/gen-ai-internal-test/lib/python3.11/inspect.py", line 1270, in getsource
    lines, lnum = getsourcelines(object)
                  ^^^^^^^^^^^^^^^^^^^^^^
  File "/home/resti/anaconda3/envs/gen-ai-internal-test/lib/python3.11/inspect.py", line 1252, in getsourcelines
    lines, lnum = findsource(object)
                  ^^^^^^^^^^^^^^^^^^
  File "/home/resti/anaconda3/envs/gen-ai-internal-test/lib/python3.11/inspect.py", line 1081, in findsource
    raise OSError('could not get source code')
OSError: could not get source code

Response:
I am an AI assistant here to help you with your questions and provide information. How can I assist you today?
```

### 3. I got error `ImportError: failed to find libmagic`. How do I fix it?

This typically happens if you use macOS or Windows.

#### Install `libmagic` in macOS

For macOS, there two alternatives:

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

### 4. I got error `Unable to find installation candidates`. How do I fix it?

Our binary SDK can only be run on specific OSes:

1. **Linux / WSL**: x86_64 architecture.

2. **macOS**: x86_64 (Intel) or arm64 (Apple Silicon) architecture.

   1. macOS version 13 or newer for x86_64 (Intel).
   2. macOS version 14 or newer for arm64 (Apple Silicon).

3. **Windows**: 64bit architecture.
