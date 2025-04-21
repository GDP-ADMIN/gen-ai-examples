# Frequently Asked Questions (FAQ)

This document contains common questions and troubleshooting tips for the GenAI Examples repository.

## API Key Issues

### 1. I got error `Error executing component StuffResponseSynthesizer__user_query_response_synthesis_bundle`. How do I fix it?

Check your `.env` file (if you already ran `local-start.sh`, it is auto-generated). You might have provided invalid `OPENAI_API_KEY` and/or `LANGUAGE_MODEL`.

```txt
# GDP Labs Gen AI Hello World Example
# Please edit the following variables with your own values.

OPENAI_API_KEY =<YOUR_OPENAI_API_KEY> # Get your OpenAI API key from https://platform.openai.com/api-keys
LANGUAGE_MODEL =<VALID_OPENAI_LANGUAGE_MODEL_NAME> # e.g. "gpt-3.5-turbo", "gpt-4o-mini", "gpt-4o"
```

## Source Code Access Issues (on Source Code Version of SDK Library)

### 1. I got error `Unable to access repository GDP-ADMIN/gen-ai-internal. Please check your GitHub credentials and repository permissions.`. How do I fix it?

You need to have access to the repository. If you don't have access, please make a request to ticket(at)gdplabs.id.

If you haven't set up your SSH key, you might get errors like:
- `HangupException. The remote server unexpectedly closed the connection.`
- `Permission denied (publickey)`
- `Cannot install gllm-core`

To fix this, you need to add your SSH key to your GitHub account. Please follow this instruction by GitHub: [Adding a new SSH key to your GitHub account](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account).

## Source Code Access Issues (on Binary Version of SDK Library)

### 1. I got error `OSError: could not get source code`. How do I fix it?

This error is currently expected. If you can see the response, it means the pipeline is working as expected.

Here is an example of the error:

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

## IDE and Development Issues

### 1. I got `Unable to import 'gllm_generation.response_synthesizer'` error in VSCode IDE. How do I fix it?

You need to change the Python interpreter path in your IDE. Follow these steps:

1. Run `./local-start.sh` first
2. Look for the log `Getting python interpreter path for use in IDE...` in the console
3. Copy the path in the next line
4. Open command palette (`⌘+Shift+P` for Mac or `Ctrl+Shift+P` for Linux/Windows) 
5. Type `> Python: Select Interpreter` and press enter
6. Select `Enter interpreter path...`
7. Paste the previously copied path and press enter

## Platform-Specific Issues

### 1. I got error `ImportError: failed to find libmagic`. How do I fix it?

For detailed solutions to this issue, please refer to the [macOS Requirements](prerequisites.md#macos-requirements) section in the prerequisites document.

### 2. I got error `Unable to find installation candidates`. How do I fix it?

For detailed solutions to this issue, please refer to the [Binary SDK Compatibility](prerequisites.md#binary-sdk-compatibility) section in the prerequisites document.