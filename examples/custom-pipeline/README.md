# GLLM Plugin Hello World for Custom Pipeline

This is an example of how to use the gllm-plugin library to build a custom pipeline.

## Prerequisites

> [!NOTE]
> You need to fulfill the prerequisites to run the script.

1. **Python v3.12** (to run `python`)

   - Using Conda (recommended):

     You can use [Miniconda](https://docs.anaconda.com/miniconda/install) to install and manage Python versions.

   - <details>
     <summary>Using Python installer (alternative)</summary>
     
     You can download the Python installer from the link [Python 3.12.8](https://www.python.org/downloads/release/python-3128/), select the version appropriate for your operating system, and run the installer.

     > [!NOTE]
     > For Windows, please make sure to check the `Add python.exe to PATH` option during the installation process.
   </details>

2. **Access to GDP-ADMIN/gen-ai-internal and GDP-ADMIN/gen-ai-external repositories**

   You can try to access the [GDP-ADMIN/gen-ai-internal](https://github.com/GDP-ADMIN/gen-ai-internal)  and [GDP-ADMIN/gen-ai-external](https://github.com/GDP-ADMIN/gen-ai-external) repositories in your browser. If you don’t have access, please make a request to ticket(at)gdplabs.id.

3. **SSH Key in your GitHub Account**

   You must add your SSH key to your GitHub account. Please follow this instruction by GitHub: [Adding a new SSH key to your GitHub account](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account). This is required as this sample has dependency to a private GitHub repository.


## Running the Code

1. Configure environment variables: copy `.env.example` to `.env` and set up your `OPENAI_API_KEY` and `LANGUAGE_MODEL`.

   - For Linux, macOS, or Windows WSL:

     ```bash
     cp .env.example .env
     ```

2. Execute the script:

   - For Linux, macOS, or Windows WSL:
     ```bash
     ./local-start.sh
     ```

