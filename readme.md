# Small Language Model Demo: Python Workshop

## Overview

Welcome to our GitHub repository, designed for the Roanoke College computer science department [Living Code Workshop (slides)](https://docs.google.com/presentation/d/1hfrdh9199eMF9oS6MK48R66j5xw0d74otIhO8MdIZv0/edit#slide=id.g2b3b54bbaba_0_5)! This repository showcases the capabilities of small language models, demonstrating how they can be effectively used in various applications. Our Python script we wrote in the workshop provides a glimpse into the world of AI-driven text generation, parsing, and interaction.

## Features
- **Language Model Integration**: Utilizes small language models for generating text, answering questions, and more.
- **Customizable Grammars**: Implements Llama grammars for constrained outputs, ensuring relevance and precision.
- **Real-time Demonstrations**: Includes live examples to illustrate the use of language models in practical scenarios.

## Prerequisites
To run the script, you will need to install the `llama-cpp-python` library. You can do this using pip:

```bash
python3 -m pip install --user llama-cpp-python
```

## Installation
Clone this repository to your local machine using the following command:

```bash
git clone https://github.com/tchlux/roanoke-slm-workshop
```

Then download your favorite small language model (examples below) and put it into this directory for easy access.

## Usage
The script allows you to interact with pre-trained language models. To run the script, navigate to the cloned repository's directory and execute:

```bash
python3 slm.py
```

## Example Models
For optimal performance, we recommend using one of the following models:

1. **Mistral Instruct**: A versatile model suitable for various instructional tasks. [Model Link](https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.1-GGUF)
2. **StableLM Zephyr**: A smaller, more efficient model for quick and compact responses. [Model Link](https://huggingface.co/TheBloke/stablelm-zephyr-3b-GGUF)

## Resources
- **LM Studio**: For a selection of local language models, visit [lmstudio.ai](https://lmstudio.ai).
- **Hugging Face**: Explore a wide range of models published on [huggingface.com](https://huggingface.com).

## Contributing
Feel free to fork this repository and contribute by submitting a pull request. We appreciate any input!
