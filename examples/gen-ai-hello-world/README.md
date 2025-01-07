# GenAI RAGO Example

This is an example of how to use the gllm-pipeline library to build a RAG pipeline.

> [!WARNING]
> The GenAI SDK is in binary version and is currently only available for Linux.

## Prerequisites

1. Python v3.11.
   You can use [Miniconda](http://conda.pydata.org/miniconda.html) to install and manage Python versions.
2. [Poetry](https://python-poetry.org/docs/) v1.8.1 or above.
3. Install [Google Cloud CLI](https://cloud.google.com/sdk/docs/install#linux).
4. You need to have access to the GDP Labs Google Artifact Registry.
   If you don’t have access, please contact the GDP Labs DSO team at infra(at)gdplabs.id.

   Use the following command to verify access:

   ```bash
   gcloud artifacts packages list --repository=gen-ai --location=asia-southeast2 --project=gdp-labs
   ```

5. Environment requirements:
   - **Operating System**: Linux
   - **Architecture**: x86_64
   - **Python Version**: 3.11

> [!NOTE]
> The prerequisites are checked automatically when you run the script.

## Running the code

1. Configure Environment: Copy `.env.example` to `.env` and set up the environment variables.

   ```bash
   cp .env.example .env
   ```

2. Execute the script:

   ```bash
   ./local-start.sh
   ```

The program will then wait for your question:

> Question:

Type your question and press enter. For example, you can try asking:

```
What are the documents?
```

The RAG pipeline will return the following response (more or less):

> _The documents mentioned are referred to as Mock document 1, Mock document 2, and Mock document 3. However, without additional context or content from these documents, I cannot provide specific details about their contents or purposes._

## Known Problem

The following error is currently expected. If you can see the response, it means the pipeline is working as expected.

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
