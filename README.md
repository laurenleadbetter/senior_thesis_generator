
## Table of Contents

- [Project Description](#Project_Description)
- [Installation](#Installation)
- [Results](#Results)
- [Future Work](#future_work)
- [License](#license)




## Project Description <a name="Project_Description"></a>
This project was completed to fulfil the senior thesis requirement at Claremont McKenna College spring 2023, done under the supervision of Dr. Mike Izbicki

This project is a Python program designed to generate a senior thesis on a user-inputted topic using natural language processing techniques. The program takes in a topic from the user and then uses OpenAI API to deploy text models for text generation and evaluation, such as GPT-3 and Davinci-003. The resulting output is in .tex format and includes a first-draft outline and paper, followed by self-generated assessment, with scoring, revisions, and feedback comments instructing manual revisions.

The goal of this project is to provide a tool for students and researchers to quickly generate high-quality senior theses on a variety of topics, without having to spend months conducting research and writing. The intended audience for this program is undergraduate and graduate students in fields such as computer science, data science, and the social sciences.


The program is built using Python 3 and utiliizes OpenAI API for text generation and evaluation. It can be run on any operating system that supports Python, and installation instructions are provided further in the README.md file. OpenAI's API levarages the power of NLP and deep learning without having to implement all of the complex algorithms and techniques from scratch. Instead, you can use the API and model to handle tasks such as language generation, text classification, sentiment analysis, and more, which can save you time and effort.


The program is designed to be user-friendly and includes detailed documentation on how to use it, as well as a sample input and output file to demonstrate its functionality. The code is also well-commented and organized, making it easy for other developers to understand and contribute to the project.

Overall, this project represents a novel approach to senior thesis writing that combines the power of natural language processing with the structure and rigor of academic research. By providing a tool that streamlines the research and writing process, we hope to enable more students to produce high-quality senior theses and contribute to the advancement of knowledge in their respective fields.



## Installation <a name="Installation"></a>

To run this program, you will need to install Python 3 and several libraries and packages. We recommend using a virtual environment to keep your dependencies separate from other Python projects you may be working on.

### Dependencies

The following dependencies are required to run this program:

- `openai` (version 0.11.2 or higher)
- `json` (included with Python 3)
- `os` (included with Python 3)
- `datetime` (included with Python 3)

You can install the `openai` library using pip:

`pip install openai`



### API Key

To use the OpenAI API, you will need to obtain an API key from OpenAI. You can sign up for an account and obtain an API key on the OpenAI website.

Once you have obtained your API key, create a file named `api_key.py` in the project directory and add the following line:

```python
OPENAI_API_KEY = "your-api-key-goes-here" 
```

Replace "your-api-key-goes-here" with your actual API key.

### Running the Program

To run the program, navigate to the project directory and execute the following command:

```bash 
python3 version_17.py
```
Replace `version_17.py` with your desired version. This will start the program and prompt you for a topic. Once you enter a topic, the program will begin generating your thesis text and feedback. The output will be saved to a .txt file with a timestamped filename. Note that to access the output you will need to specify an output location in the function `write_output_to_file`. Running the program may take some time depending on the length and complexity of the input topic, print statement will signal what function is being completed.


## Results <a name="Results"></a>
The result from running the program will vary from model to model depending on what features you want to be included in the final output. These differences are noted in modlel versions of the readme.md file. 



## Future Work  <a name="future_work"></a>
- Have Output be a latex document formatted for Claremont McKenna College Senior Thesis Submission. 
- Incorporate Plagarism check using Turn-it-in API 
- Make project pip installable



## License
