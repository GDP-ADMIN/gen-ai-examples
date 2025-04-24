# GL Chat Custom Pipeline Guide

This guide will help you create, test, and register a custom pipeline in GL Chat.

## Create Custom Pipeline

### 1. Using Provided Example

To prepare your custom pipeline for registration:

1. Compress the entire `custom-pipeline/` directory into a zip file.
2. Name the zip file, e.g., `custom-pipeline.zip`.

   - **Naming Conventions**: The zip file name should only contain alphanumeric characters, hyphens (`-`), and underscores (`_`). Avoid using spaces or special characters to ensure compatibility.

This zip file is needed for registration in GL Chat.

### 2. Using Your Own Pipeline

To create your own pipeline, follow these steps:

1. **Create a New Directory**: Inside the `custom-pipeline/` directory, create a new directory for your custom pipeline. Name it appropriately, e.g., `my_custom_pipeline`.

   - **Naming Conventions**: The directory name should only contain alphanumeric characters and underscores (`_`). Avoid using spaces or special characters to ensure compatibility.

2. **Define the Pipeline State**: In your new directory, create a `state.py` file to define the state for your pipeline. This state will manage data throughout the pipeline's execution.

3. **Define the Pipeline Preset Configuration**: In `preset_config.py`, define the preset configuration for your pipeline, including any initialization parameters.

4. **Implement the Pipeline Builder**: Create a `pipeline.py` file that implements `PipelineBuilderPlugin`. This class will define the steps and interactions within your pipeline.

5. **Define the Pipeline Configurations**: Create a `config.yaml` file to define your pipeline's configuration, including presets and chatbot settings.

6. **Refer to the Example Repository**: Use the [gen-ai-examples/simple-pipeline](https://github.com/GDP-ADMIN/gen-ai-examples/tree/main/examples/simple-pipeline) as a reference for your implementation.

7. **Compress the Pipeline**: Before registration, compress the entire directory containing your pipeline into a zip file. Name it appropriately, e.g., `your-pipeline.zip`.

For detailed instructions on creating a custom pipeline, refer to the [PIPELINE.md](https://github.com/GDP-ADMIN/gen-ai-external/blob/main/libs/gllm-plugin/PIPELINE.md).

## Test Custom Pipeline

### 1. Using Provided Example

To test the provided example, you can run the pipeline locally by following the instructions in the [README.md](./README.md#running-the-code).

### 2. Your Own Pipeline

To test your own pipeline, you will need to adjust the `main.py` file to integrate your custom pipeline logic. Follow these steps:

1. **Modify `main.py`**: Open the `main.py` file and update it to import and use your custom pipeline. Ensure that it initializes and runs your pipeline correctly.

   - **Import Your Pipeline**: Replace the import statement to import your custom pipeline builder. For example:
     ```python
     from my_custom_pipeline.pipeline import MyCustomPipelineBuilder
     ```

   - **Initialize Your Pipeline**: Replace the `SimplePipelineBuilder` with your custom pipeline builder:
     ```python
     pipeline_builder = MyCustomPipelineBuilder()
     ```

   - **Configure Your Pipeline**: Update the `pipeline_config` and `state` initialization to match your pipeline's requirements. You may need to adjust the input parameters and configuration settings based on your pipeline's design.

2. **Run the Pipeline**: To test your pipeline, follow the instructions in the [README.md](./README.md#running-the-code).

3. **Verify Functionality**: Ensure that your pipeline runs as expected and interacts correctly with any configured chatbots or components.

By following these steps, you can test your custom pipeline locally. Adjust `main.py` as needed to fit your specific pipeline logic and requirements.

## Register Pipeline

### Using `config.yaml`

To register your pipeline with the GLChat system, follow these steps:

1. **Create a New User**: 
   - Go to the [GL Chat admin dashboard](https://stag-chat-ui-gdplabs-gen-ai-starter.obrol.id/admin).
   - In the navigation bar, choose **"User Management"**.
   - Click on the **"New User"** button at the top right corner.
   - Fill out the form with the necessary details for the new user.
   - Click the **"Save"** button located on the right corner to save the new user information.
   - **Reminder**: Note the username you created, as it will need to be set in the `config.yaml` file.

2. **Set the New User in `config.yaml`**: Update your `config.yaml` file to include the new user settings.

3. **Include `config.yaml` in the Compressed Pipeline**: Ensure that your `config.yaml` file is included in the zip file of your pipeline.

4. **Register via Endpoint**: Use the API to register your pipeline. Send a request to the GLChat backend with your pipeline's configuration.

   - **Sample API Request**:
     ```sh
     curl -X POST "https://stag-gbe-gdplabs-gen-ai-starter.obrol.id/register-pipeline-plugin" \
     -H 'Content-Type: multipart/form-data' \
     -F zip_file="@/path/to/your-pipeline.zip"
     ```

   Replace `your-domain.com` with the actual domain where your backend is hosted.

5. **Verify Registration**: After registration, verify that your pipeline is active by checking the available chatbots in GLChat. Ensure that a chatbot configured with your new pipeline is listed and functioning as expected.

### Without `config.yaml`

#### Automating Preset Creation via Backend

*Note: Detailed instructions for automating preset creation via the backend will be provided soon.*

#### Setup a Preset from Admin Dashboard

*Note: Detailed instructions for setting up a preset from the admin dashboard will be provided soon.*

