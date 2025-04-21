# GLLM Plugin Hello World for Custom Pipeline

This is an example of how to use the gllm-plugin library to build a custom pipeline.

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
      What is artificial intelligence?
      ```

      The custom pipeline will return the following response (more or less):

      > _Artificial Intelligence (AI) refers to the simulation of human intelligence in machines that are programmed to think, learn, and perform tasks that typically require human cognitive functions. This includes activities like problem-solving, understanding natural language, recognizing patterns, making decisions, and adapting to new information..._
      
## Troubleshooting

For common issues and their solutions, please refer to the centralized [FAQ document](../../faq.md).