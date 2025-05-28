"""Tools for the InformationCompilerAgent Agent.

This module contains tools for reading, writing, and creating markdown files.

Authors:
    Generated for InformationCompilerAgent
"""

import os
from pathlib import Path
from typing import Optional
from pydantic import BaseModel, Field
from langchain_core.tools import tool

from gllm_agents.utils.logger_manager import LoggerManager

logger = LoggerManager().get_logger(__name__)


class ReadMarkdownToolInputSchema(BaseModel):
    """Schema for read markdown tool input."""
    
    file_path: str = Field(description="The path to the markdown file to read")


class WriteMarkdownToolInputSchema(BaseModel):
    """Schema for write markdown tool input."""
    
    file_path: str = Field(description="The path to the markdown file to write")
    content: str = Field(description="The content to write to the markdown file")
    append: bool = Field(default=True, description="Whether to append to the file or overwrite it")


class CreateMarkdownToolInputSchema(BaseModel):
    """Schema for create markdown tool input."""
    
    folder_path: str = Field(description="The folder path where to create the markdown file")
    file_name: str = Field(description="The name of the markdown file (with or without .md extension)")
    initial_content: str = Field(default="", description="Initial content for the new markdown file")


@tool(args_schema=ReadMarkdownToolInputSchema)
def read_markdown_file(file_path: str) -> str:
    """Reads content from a markdown file.

    Args:
        file_path: The path to the markdown file to read.

    Returns:
        A string containing the file content or an error message.
    """
    try:
        # Ensure the file path is absolute and safe
        file_path = os.path.abspath(file_path)
        
        # Check if file exists
        if not os.path.exists(file_path):
            message = f"File not found: {file_path}"
            logger.warning(message)
            return message
        
        # Check if it's a file (not a directory)
        if not os.path.isfile(file_path):
            message = f"Path is not a file: {file_path}"
            logger.warning(message)
            return message
        
        # Read the file content
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        logger.info(f"Successfully read markdown file: {file_path}")
        return content
        
    except PermissionError:
        message = f"Permission denied reading file: {file_path}"
        logger.error(message)
        return message
    except UnicodeDecodeError:
        message = f"Unable to decode file as UTF-8: {file_path}"
        logger.error(message)
        return message
    except Exception as e:
        message = f"Error reading file {file_path}: {str(e)}"
        logger.error(message)
        return message


@tool(args_schema=WriteMarkdownToolInputSchema)
def write_markdown_file(file_path: str, content: str, append: bool = False) -> str:
    """Writes content to a markdown file.

    Args:
        file_path: The path to the markdown file to write.
        content: The content to write to the file.
        append: Whether to append to the file or overwrite it.

    Returns:
        A string indicating success or failure.
    """
    try:
        # Ensure the file path is absolute
        file_path = os.path.abspath(file_path)
        
        # Create directory if it doesn't exist
        directory = os.path.dirname(file_path)
        os.makedirs(directory, exist_ok=True)
        
        # Determine write mode
        mode = 'a' if append else 'w'
        
        # Write the content
        with open(file_path, mode, encoding='utf-8') as file:
            file.write(content)
        
        action = "appended to" if append else "written to"
        message = f"Successfully {action} markdown file: {file_path}"
        logger.info(message)
        return message
        
    except PermissionError:
        message = f"Permission denied writing to file: {file_path}"
        logger.error(message)
        return message
    except Exception as e:
        message = f"Error writing to file {file_path}: {str(e)}"
        logger.error(message)
        return message


@tool(args_schema=CreateMarkdownToolInputSchema)
def create_markdown_file(folder_path: str, file_name: str, initial_content: str = "") -> str:
    """Creates a new markdown file in the specified folder if it doesn't exist.

    Args:
        folder_path: The folder path where to create the markdown file.
        file_name: The name of the markdown file (with or without .md extension).
        initial_content: Initial content for the new markdown file.

    Returns:
        A string indicating success or failure.
    """
    try:
        # Ensure folder path is absolute
        folder_path = os.path.abspath(folder_path)
        
        # Add .md extension if not present
        if not file_name.endswith('.md'):
            file_name += '.md'
        
        # Create full file path
        file_path = os.path.join(folder_path, file_name)
        
        # Check if file already exists
        if os.path.exists(file_path):
            message = f"Markdown file already exists: {file_path}"
            logger.info(message)
            return message
        
        # Create directory if it doesn't exist
        os.makedirs(folder_path, exist_ok=True)
        
        # Create the file with initial content
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(initial_content)
        
        message = f"Successfully created markdown file: {file_path}"
        logger.info(message)
        return message
        
    except PermissionError:
        message = f"Permission denied creating file in folder: {folder_path}"
        logger.error(message)
        return message
    except Exception as e:
        message = f"Error creating markdown file in {folder_path}: {str(e)}"
        logger.error(message)
        return message
