# GLLM Plugin Hello World for Custom Pipeline

This is an example of how to use the gllm-plugin library to build a custom pipeline.

## For Simple Pipeline

1. Install the required libraries

```bash
pip install gllm-core-binary gllm-generation-binary gllm-pipeline-binary gllm-rag-binary python-dotenv gllm-inference-binary gllm-plugin-binary langchain-mcp-adapters
```

2. Create `simple_pipeline/.env` file based on `simple_pipeline/.env.example` and set your LLM API Key. You can also change the Language Model of your preference.

```bash
cp simple_pipeline/.env.example simple_pipeline/.env
```

3. Run the example

```bash
python main.py
```

---

The program will then wait for your question:

> Question:

Type your question and press enter. For example, you can try asking:

```
What is artificial intelligence?
```

The custom pipeline will return the following response (more or less):

> _Artificial Intelligence (AI) refers to the simulation of human intelligence in machines that are programmed to think, learn, and perform tasks that typically require human cognitive functions. This includes activities like problem-solving, understanding natural language, recognizing patterns, making decisions, and adapting to new information..._

## For MCP Pipelines

1. Install the required libraries

```bash
pip install gllm-core-binary gllm-generation-binary gllm-pipeline-binary gllm-rag-binary python-dotenv gllm-inference-binary gllm-plugin-binary langchain-mcp-adapters
```

2. Create `mcp_pipeline/.env` file based on `mcp_pipeline/.env.example` and set your LLM API Key and MCP Server URL. You can also change the Language Model of your preference. By default it's set to GPT 4.1.

```bash
cp mcp_pipeline/.env.example mcp_pipeline/.env
```

If you want to use GDP Labs' MCP Server, you can ask GDP Labs' MCP Team to get the value of `MCP_SERVER_URL`. Remember that GDP VPN is required to access the MCP Server.

3. Run the example

```bash
python main_mcp.py
```

---

The program will then wait for your question:

> Question:

Type your question and press enter. For example, you can try asking something that requires tool calling. For GDP Labs' MCP, it has a Github tool that you can try:

```
How many open PRs are in bosa-sdk as of now?
```

The MCP pipeline will return the following response (more or less):

```
Response:

As of now (2025-05-27 15:39 Asia/Jakarta), there are 12 open pull requests in the GDP-ADMIN/bosa-sdk repository. If you need a list or details about these PRs, let me know!
```

There will be a lot more logging for the MCP Call. However, the most important bit should be the `Response:` section.

<details>
<summary><h2>Steps Using Poetry</h2></summary>

## Prerequisites

Please refer to the centralized [prerequisites.md](../../prerequisites.md) file for detailed requirements to run this example.

This example specifically requires:

- Python Environment

You need to fulfill the prerequisites to run the script. They will be checked automatically when you execute it.

## Running the Code

1.  Configure environment variables: copy `.env.example` to `.env` and set up your `SIMPLE_PIPELINE_LLM_API_KEY` and `SIMPLE_PIPELINE_LANGUAGE_MODEL`.

    - For Linux, macOS, or Windows WSL:

      ```bash
      cp simple_pipeline/.env.example simple_pipeline/.env
      ```

    - For Windows Powershell or Command Prompt:

      ```powershell
      copy simple_pipeline/.env.example simple_pipeline/.env
      ```

2.  Execute the script:

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

</details>

## Additional Resources

For detailed instructions on creating, testing, and registering a custom pipeline, please refer to the [GL Chat Custom Pipeline Guide](./guide.md).

<details><summary><h2>Troubleshooting</h2></summary>

For common issues and their solutions, please refer to the centralized [FAQ document](../../faq.md).

</details>
