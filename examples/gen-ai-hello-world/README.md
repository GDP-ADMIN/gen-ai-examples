# GenAI RAGO Example

This is an example of how to use the gllm-pipeline library to build a RAG pipeline.

## Prerequisites

1. Python v3.11 or above.
2. [Poetry](https://python-poetry.org/docs/) v1.8.1 or above.
3. Install [Google Cloud CLI](https://cloud.google.com/sdk/docs/install#linux).
4. You need to have access to the GDP Labs Google Artifact Registry.
   
   Use the following command to verify access:
   ```bash
   gcloud artifacts packages list --repository=gen-ai-internal --location=asia-southeast2 --project=glair01
   ```
5. Environment requirements:
   - **Operating System**: Linux
   - **Architecture**: x86_64
   - **Python Version**: 3.11

> [!NOTE]
> The prerequisites are checked automatically when you run the script.

## Running the code

1. Configure Environment: Copy `.env.example` to `.env` and set up the environment variables.
2. Execute the script:

```bash
local-start.sh
```

The program will then wait for your question:

> Question:

Type your question and press enter. For example you can try asking:

```
What are the documents?
```

The RAG pipeline will return the following response (more or less):

> _The documents mentioned are referred to as Mock document 1, Mock document 2, and Mock document 3. However, without additional context or content from these documents, I cannot provide specific details about their contents or purposes._

## MacOS Problem

If you are using MacOS, you might encounter an error related to the `libmagic` library:

> _ImportError: failed to find libmagic. Check your installation_

To fix this, there are two alternatives:

1. If you have [conda](https://docs.anaconda.com/miniconda/install/) installed:

```
conda install libmagic
cd /usr/local/lib
sudo ln -s /opt/miniconda3/pkgs/libmagic-5.39-h6ba3021_1/lib/libmagic.dylib libmagic.dylib
```

> [!WARNING]
> Please adjust the path of your conda installation if it is different. In the above example, the path is `/opt/miniconda3/`.

2. If you have [brew](https://brew.sh/) installed:

```
brew install libmagic
```

Then [run the code again](#running-the-code).
