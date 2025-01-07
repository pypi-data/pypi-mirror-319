<p align="center">
  <img src="dagent_llm.png" alt="DCheck Logo" width="250">
</p>

# DAgent: Command Line Interface for Language Model Operations
[中文](README_zh.md) | English
## Overview
The LLM Package is a Python-based command-line interface (CLI) that provides an easy way to interact with Large Language Models (LLMs). It allows users to chat with the model, make choices based on given options, and more. This package is designed to be simple, intuitive, and extendable for various LLM operations.
## Features
- Chat with the LLM and receive responses.
- Present options to the LLM and get a choice.
- Choose an option and provide arguments for further processing.
- Few-shot learning capabilities for better context understanding.
- Logging of conversation history for future reference.
## Installation
To install the LLM Package, run the following command:
```bash
pip install dagent_llm
```
Ensure that you have Python 3.6 or later installed on your system.
## Help
To view the available commands and options, use the `help` flag:
```bash
dagent_llm help
```
This will display the list of available commands and their descriptions.
> Note : Dagent_llm assumes that you have configured the environment variables through [dsqlenv](https://pypi.org/project/dsqlenv/), and the system will read the necessary information from [dsqlenv](https://pypi.org/project/dsqlenv/).
```
D-Agent LLM Command Line Interface

Usage: dagent_llm 

Available Commands:
  chat             Send a message to the LLM and get a response.
  choose           Present options to the LLM and get a choice.
  choose_with_args Choose an option and provide arguments.

Options for 'chat' command:
  --message         The message to send to the LLM.
  --llm_server      Specify the LLM server to use.
  --role            Specify the role of the message sender (default: 'human').

Options for 'choose' command:
  --options         List of options to choose from.
  --prompt          The prompt for choosing.
  --need-reason     Ask the LLM to provide reasons for the choice.
  --multiple        Allow the LLM to select multiple options.
  --notes           Additional notes to add to the prompt.
  --examples        Few-shot learning examples to guide the choice.

Options for 'choose_with_args' command:
  --options         List of options to choose from.
  --prompt          The prompt for choosing.
  --option-type     The type of options being chosen.
  --need-reason     Provide reasons for the choice.
  --multiple        Allow multiple selections.
  --notes           Additional notes to add to the prompt.
  --examples        Few-shot learning examples to guide the choice.

Version: 0.1.0 | 2024-10-18
Copyright: © 2024 VoiceCodeAI, Singapore
```

## Dependencies
- Python 3.6+
- dsqlenv
- langchain_core
- langchain_openai

## Usage
### Chatting with the LLM
To send a message to the LLM and receive a response, use the `chat` command:
```bash
dagent_llm chat --message "Hello, how are you?" --role human
```
The `--role` flag can be set to `human`, `ai`, or `system` depending on the context of the message.
### Making a Choice
To present options to the LLM and get a choice, use the `choose` command:
```bash
dagent_llm choose --options "Option 1" "Option 2" "Option 3" --prompt "Choose an option" --need-reason --multiple
```
The `--need-reason` flag will ask the LLM to provide reasons for the choice, and the `--multiple` flag allows the selection of multiple options.
### Choosing with Arguments
To choose an option and provide arguments, use the `choose_with_args` command:
```bash
dagent_llm choose_with_args --options "Option 1" "Option 2" "Option 3" --prompt "Choose an option and provide arguments" --option-type "type" --need-reason --multiple
```
The `--option-type` flag describes the type of options being chosen.
### Providing Few-Shot Examples
You can provide few-shot examples to guide the LLM using the `examples` argument:
```bash
dagent_llm choose --options ... --prompt ... --examples "Example 1" "Example 2"
```
### Adding Notes
Additional notes can be added to the prompt using the `notes` argument:
```bash
dagent_llm choose --options ... --prompt ... --notes "Note 1" "Note 2"
```
## Demo
Here's a simple demo to demonstrate chatting with the LLM:
```bash
# Chat with the LLM
dagent_llm chat --message "What's the weather like today?" --role human
# Output:
# LLM response: The weather is sunny with a few clouds.
```

## Python API
The LLM Package can also be used as a Python library. Here's an example of how to chat with the LLM using the Python API:
```python
from dagent_llm import LLM
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

# Initialize the LLM model with a specific engine
model = LLM("deepseek")  # 'deepseek' is the engine being used for LLM
# Note: Directly starting with llm_server requires you to have installed dsqlenv and configured it.
# For example: {llm_server}_api_key, {llm_server}_base_url, {llm_server}_model, etc.
# Please refer to [dsqlenv](https://pypi.org/project/dsqlenv/) for specific configuration methods.

# Or you can specify the complete engine information
model = LLM(
    llm_server="deepseek",
    max_retries=3, # Max retry times
    ###################################
    # OpenAI API parameters
    temperature=0.7,
    api_key="your_api_key",
    base_url="https://api.deepseek.com",
    model_name="deepseek-chat", 
    ###################################
    history=[] # Same as langchain_core.messages
)


# Simple interaction with the model
r = model.chat("Tell me about yourself")
print(r.content)  # Outputs the response from the model

# Define a list of functions with their names and inputs
functions_info = [
    {"name": "get_data", "input": ["id"], "example_input": "a"},
    {"name": "insert_data", "input": ["id", "data"], "example_input": ["a", "b"]},
    {"name": "update_data", "input": ["id", "data"], "example_input": ["a", "b"]},
    {"name": "delete_data", "input": ["id"], "example_input": "a"},
]

# Example 1: Selecting a function based on user input, including reasons for choice
# Here, the model will be asked to select a function and provide the necessary arguments.
r = model.function_choose(
    functions_info,                      # List of functions to choose from
    "Add a record with key-value pair abc and 123",  # The prompt asking what to do
    need_reason=True,                    # Model must provide a reason for its choice
    multiple=False,                      # Single function selection allowed
    add_to_history=True                  # Add this interaction to the conversation history
)
# r["choice"], r["reason"] will contain the selected function and reason
print(r)  # Outputs the selected function and arguments

r = model.function_choose(
    functions_info,                      # List of functions to choose from
    "Add a record with key-value pair abc and 123",  # The prompt asking what to do
    need_reason=False,                    # No need for a reason
    multiple=False,                      # Single function selection allowed
    add_to_history=True                  # Add this interaction to the conversation history
)
print(r)  # Outputs the selected function and arguments


# Example 2: Function selection with additional context such as examples and notes
# This provides the model with extra guidance on how to make its decision
r2 = model.function_choose(
    functions_info,
    "Delete record with key abc",        # Instruction for deletion operation
    need_reason=True,                    # Model must provide reasoning
    multiple=False,                      # Only one function can be selected
    add_to_history=True,                 # Record this interaction
    examples=[                           # Example to guide the model
        "Add a record with key-value pair abc and 123 -> insert_data('abc', '123')"
    ],
    notes=[                              # Important notes for the operation
        "Delete operation is irreversible",  
        "This will delete all records with key 'abc'"
    ]
)
print(r2)  # Outputs the selected function and explanation


# Example 3: Simple selection scenario for choosing from a list of food options
# Multiple selections are allowed in this case, and the model needs to justify its choice
foods = ["Snail noodles", "Rice noodles", "Beef noodles", "Egg noodles", "Vegetable salad", "Boiled beef"]
r = model.choose(
    foods,                               # List of options to choose from
    "What can I eat while on a diet?",   # The question or prompt
    "Food name",                         # Type of options being chosen
    need_reason=True,                    # Model must provide reasons for its choices
    multiple=True,                       # Multiple choices allowed (diet-friendly foods)
    add_to_history=True                  # Record the conversation
)
# r["choice"], r["reason"] will contain the selected food(s) and reason(s)
print(r)  # Outputs the selected food(s) and reason(s)

# Review conversation history to see how previous interactions were logged
print(model.history)

# If token information is needed (optional debugging for developers):
# print(model.input_tokens)

# KeyWord Class Usage
from dagent_llm import KeyWord
# Pass in the folder path to save the keywords
# In the csv file under the keywords folder, each line is a keyword, with the first column as the keyword category and the second column as the keyword
# For example, a typical keyword file is as follows:
# --keywords
#   --keywords.csv
#   --keywords2.csv
# The content of the keywords.csv file is as follows:
# fraud,scam
# ad,offer
kw = KeyWord("./keywords")
text = "scam offer"
print(kw.match(text))
# The result is a two-dimensional list, with each element being a list of keywords under a keyword category and the file name
# [['faurd', 'scam', 'keywords'], ['ad', 'offer', 'keywords']]
```
## APP: Telephone Customer Service Quality Inspection System: Combining `dagent_llm`, `dguard`, and `dspeech`

This demo showcases how to build a quality inspection system for telephone customer service using the following components:
- **`dagent_llm`**: A large language model (LLM) used for evaluating the dialogue content, identifying emotions, solving user problems, and ensuring compliance with customer service standards.
- **`dguard`**: A diarization model used to identify speakers and segment audio files by speaker turns.
- **`dspeech`**: A speech-to-text (STT) model used for transcribing audio content and classifying emotions.

### Demo Features
This system processes recorded customer service calls, providing:
1. **Speaker diarization**: Identifies different speakers from the audio.
2. **Emotion analysis**: Assesses emotions for both customer service agents and customers.
3. **Service quality evaluation**: Determines whether customer problems are solved and evaluates if the agent followed proper procedures.

### Requirements
- Python 3.8+
- `dagent_llm`, `dguard`, and `dspeech` installed
- Additional Python libraries: `rich`, `os`, `csv`, `subprocess`

### System Workflow
1. **Input WAV Files**: The system takes in audio files (WAV format) from the customer service call recordings.
2. **Audio Preprocessing**: The audio is downsampled to a single channel (16 kHz) using `ffmpeg`.
3. **Speaker Diarization**: The `dguard` model identifies different speakers in the audio and segments it based on speaker turns.
4. **Speech Transcription**: The `dspeech` model transcribes each speaker’s segment into text.
5. **Emotion Classification**: For segments longer than a set threshold (e.g., 2 seconds), the system classifies emotions using the `dspeech` model.
6. **Dialogue Evaluation**: The system uses `dagent_llm` to assess:
   - Agent's emotions: Whether they exhibit negative emotions.
   - Customer's emotions: Whether they are satisfied or dissatisfied with the service.
   - Problem resolution: Whether the customer’s issue was solved.
   - Procedural compliance: Whether the agent followed proper service procedures.
7. **Results**: The system outputs a CSV file summarizing the evaluation results, along with individual text files for each conversation.

### Code Overview

Below is a breakdown of the main functions and their roles:

#### 1. **rich_print**
This function uses the `rich` library to color-code and format output. It highlights speaker turns and emotions.

```python
def rich_print(content):
    colors = ["red", "green", "blue", "yellow", "magenta", "cyan"]
    for idx, line in enumerate(content.split("\n")):
        if ":" not in line:
            continue
        spk_id = line.split(":")[0].split(" ")[-1]
        console.print(f"[{colors[int(spk_id) % 6]}]{line}")
```

#### 2. **get_diarization_content**
This function processes a WAV file to generate speaker-diarized transcriptions. For each speaker, it transcribes the speech and classifies emotions if the speaking duration exceeds the `emotion_time_threshold`.

```python
def get_diarization_content(file_path, emotion_time_threshold=2):
    try:
        r = dm_model.diarize(file_path)
        all_content = ""
        last_spk = ""
        for data in r:
            spk_label = data[3]
            start_time = data[1]
            end_time = data[2]
            generate_text = stt_model.transcribe_file(file_path, start=start_time, end=end_time)
            if end_time - start_time > emotion_time_threshold:
                emotion = stt_model.emo_classify_file(file_path, start=start_time, end=end_time)
                emotion_label = emotion["labels"][emotion["scores"].index(max(emotion["scores"]))]
                emotion_score = max(emotion["scores"])
                emotion_text = f"(emotion：{emotion_label} with score: {emotion_score:.2f})"
            else:
                emotion_text = ""
            if spk_label != last_spk:
                all_content += f"\nSpeaker {spk_label}: {generate_text} " + emotion_text
                last_spk = spk_label
            else:
                all_content += f" {generate_text}"
        return all_content
    except Exception as e:
        console.print(f"[red]Error processing file {file_path}: {str(e)}[/red]")
        return ""
```

#### 3. **evaluate_wav_file**
This function evaluates the quality of the customer service conversation using the `dagent_llm`. It provides:
- Agent emotion evaluation
- Customer satisfaction
- Problem resolution assessment
- Procedural compliance evaluation

```python
def evaluate_wav_file(content):
    try:
        chooses = ["符合要求（无负面情绪）", "不符合要求（有负面情绪）"]
        prompt = f"<对话内容>\n{content}<对话内容>\n请你根据对话内容评估客服人员的情绪是否符合要求..."
        r = dagent_llm.choose(chooses, prompt, "情绪是否符合要求", need_reason=True)
        emo_of_agent = r[0]
        reason_of_agent = dagent_llm.history[-1].reason

        # Similar blocks for evaluating user emotions, problem resolution, and process compliance...
        
        return {
            "客服情绪评估": emo_of_agent,
            "客服情绪原因": reason_of_agent,
            "用户情绪评估": emo_of_user,
            "用户情绪原因": reason_of_user,
            "用户问题解决评估": is_user_problem_solved,
            "用户问题解决原因": reason_of_user_problem_solved,
            "解答流程规范评估": is_answer_process_standard,
            "解答流程规范原因": reason_of_answer_process_standard
        }
    except Exception as e:
        console.print(f"[red]Error evaluating content: {str(e)}[/red]")
        return {}
```

#### 4. **Main Script**
The main script processes a directory of WAV files, converts them to the required format, runs speaker diarization, performs transcriptions, and evaluates the conversations based on the criteria listed.

```python
if __name__ == "__main__":
    input_dir = "/datasets_hdd/customer_downloadwavs/20241014/"
    output_dir = "outputs/"
    txt_dir = os.path.join(output_dir, "txt")
    os.makedirs(txt_dir, exist_ok=True)

    csv_file = os.path.join(output_dir, "output.csv")
    with open(csv_file, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["ID", "客服情绪评估", "客服情绪原因", "用户情绪评估", "用户情绪原因", 
                         "用户问题解决评估", "用户问题解决原因", "解答流程规范评估", "解答流程规范原因"])

        for filename in os.listdir(input_dir):
            if filename.endswith(".wav") and "channel" not in filename:
                try:
                    file_path = os.path.join(input_dir, filename)
                    file_id = os.path.splitext(filename)[0]
                    
                    # Audio preprocessing using ffmpeg
                    file_path_new = os.path.join(output_dir, 'tmp_wav', f"{file_id}.wav")
                    subprocess.run(f"ffmpeg -y -i  {file_path} -ac 1 -ar 16000 {file_path_new}", shell=True)
                    
                    # Diarization and transcription
                    content = get_diarization_content(file_path_new)
                    
                    # Evaluate the conversation
                    results = evaluate_wav_file(content)
                    if results:
                        writer.writerow([file_id] + list(results.values()))

                except Exception as e:
                    console.print(f"[red]Error processing file {filename}: {str(e)}[/red]")

    console.print(f"[bold green]Process completed! Results are saved in {output_dir}[/bold green]")
```

### Conclusion
This demo illustrates how to integrate speaker diarization, speech transcription, emotion analysis, and dialogue evaluation into a single system for inspecting the quality of customer service interactions. The combination of `dagent_llm`, `dguard`, and `dspeech` ensures comprehensive analysis of both speech content and emotions, providing valuable insights for customer service improvement.


## Contributing
Contributions to the LLM Package are welcome! Please fork the repository, make your changes, and submit a pull request.
## License
This project is licensed under the MIT License - see the LICENSE file for details.
## Contact
For any questions or suggestions, please email Zhao Sheng at zhaosheng@nuaa.edu.cn.
