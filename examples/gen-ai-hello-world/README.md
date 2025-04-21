# GenAI RAGO Example Using Binary Version of SDK

This is an example of how to use the gllm-pipeline library to build a simple RAG pipeline using binary version of SDK.

See other examples in [gen-ai-examples](https://github.com/GDP-ADMIN/gen-ai-examples).

> [!WARNING]
> The GenAI SDK binary version is currently only available for Linux, macOS, and Windows.

<details><summary><h2>Prerequisites</h2></summary>

> Please refer to the centralized [prerequisites.md](../../prerequisites.md) file for detailed requirements to run this example.
>
> This example specifically requires:
> - Python Environment
> - Access to Private Binary Version of SDK Library
>
> You need to fulfill the prerequisites to run the script. They will be checked automatically when you execute it.
</details>


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

## Troubleshooting

For common issues and their solutions, please refer to the centralized [FAQ document](../../faq.md).
