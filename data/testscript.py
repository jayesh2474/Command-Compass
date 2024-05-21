import os
from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from tqdm import tqdm


# Read text from file
def read_text_from_file(file_path):
    with open(file_path, "r") as file:
        return file.read()


# Write text to file
def write_text_into_file(file_path, text):
    with open(file_path, "w") as file:
        file.write(text)


# LangChain model setup
llm = ChatOllama(model="phi3")
prompt = ChatPromptTemplate.from_template('{Prompt} "{text}"')

# Using LangChain Expressive Language chain syntax
chain = prompt | llm | StrOutputParser()

# Paths to the input and output directories
input_directory = "test"
output_directory = "test_output"

# Ensure the output directory exists
os.makedirs(output_directory, exist_ok=True)

# List all text files in the input directory
input_files = [f for f in os.listdir(input_directory) if f.endswith(".txt")]

# Process each file in the input directory with a progress bar
for file_name in tqdm(input_files, desc="Processing files"):
    input_file_path = os.path.join(input_directory, file_name)

    if os.path.isfile(input_file_path):
        # Read text from the file
        text = read_text_from_file(input_file_path)

        # Print the input text (optional)
        print(f"Input Text from {file_name}:\n", text)

        # Invoke LangChain model with the text twice for two different responses
        response1 = chain.invoke({"Prompt": "Explain in detail", "text": text})
        response2 = chain.invoke(
            {"Prompt": "Give examples for every argument", "text": text}
        )

        # Paths to the output files
        output_file_path1 = os.path.join(output_directory, f"{file_name}_response1.txt")
        output_file_path2 = os.path.join(output_directory, f"{file_name}_response2.txt")

        # Write the responses to the output files
        write_text_into_file(output_file_path1, response1)
        write_text_into_file(output_file_path2, response2)

        # Print the responses (optional)
        print(f"Formatted Text for {file_name} Response 1:\n", response1)
        print(f"Formatted Text for {file_name} Response 2:\n", response2)
