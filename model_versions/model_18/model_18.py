import time
start_time = time.time()
import openai
from api_key import OPENAI_API_KEY
import os
import json 
from datetime import datetime 

# Set up OpenAI API key
openai.api_key = OPENAI_API_KEY

######################################################
# Generate outline
######################################################

# Define function to generate outline
def generate_outline(topic):
    # Define prompt
    prompt = f"Please write an outline on {topic}, using roman numerals for section headings and latin letters for sub-headings."
    
    # Call OpenAI API to generate outline
    response = openai.Completion.create(
        model='text-davinci-003',
        prompt=prompt,
        temperature=0.8,
        max_tokens=3800,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.6,
    )
    
    # Extract and return outline
    outline = response.choices[0].text.strip()
    return outline




######################################################
# Split outline into sections 
######################################################

#lists less problematic than RegExs
roman_numerals = ("I.", "II.", "III.", "IV.", "V.", "VI.", "VII.", "VIII.", "IX.", "X.", "XI.", "XII.", "XIII.", "XIV.", "XV.", "XVI.", "XVII.", "XVIII.", "XIX.", "XX.", "XXI.", "XXII.", "XXIII.", "XXIV.", "XXV.", "XXVI.", "XXVII.", "XXVIII.", "XXIX.", "XXX.", "XXXI.", "XXXII.", "XXXIII.", "XXXIV.", "XXXV.", "XXXVI.", "XXXVII.", "XXXVIII.", "XXXIX.", "XL.", "XLI.", "XLII.", "XLIII.", "XLIV.", "XLV.", "XLVI.", "XLVII.", "XLVIII.", "XLIX.", "L.", "LI.", "LII.", "LIII.", "LIV.", "LV.", "LVI.", "LVII.", "LVIII.", "LIX.", "LX.", "LXI.", "LXII.", "LXIII.", "LXIV.", "LXV.", "LXVI.", "LXVII.", "LXVIII.", "LXIX.", "LXX.", "LXXI.", "LXXII.", "LXXIII.", "LXXIV.", "LXXV.", "LXXVI.", "LXXVII.", "LXXVIII.", "LXXIX.", "LXXX.", "LXXXI.", "LXXXII.", "LXXXIII.", "LXXXIV.", "LXXXV.", "LXXXVI.", "LXXXVII.", "LXXXVIII.", "LXXXIX.", "XC.", "XCI.", "XCII.", "XCIII.", "XCIV.", "XCV.", "XCVI.", "XCVII.", "XCVIII.", "XCIX.")
alphabet_sections = ("A.", "B.", "C.", "D.", "E.", "F.", "G.", "H.")


# Define function to split outline into sections for content generation
def split_outline(outline):
    sections = {}
    current_section = None
    
    # Split outline into lines
    lines = outline.split('\n')

    # Loop through lines
    for line in lines:
        # If line is a section header starting with Roman numerals, create a new section key
        if line.strip().startswith(roman_numerals):
            current_section = line.strip()
            sections[current_section] = []
        # If line is a subsection header starting with alphabets, add as a value to the last Roman numeral key
        elif line.strip().startswith(alphabet_sections):
            if current_section is not None:
                sections[current_section].append(line.strip())
        # If line is not a section header, append it to the current section value
        elif current_section is not None:
            # Check if the list exists before trying to append to it
            if sections[current_section]:
                sections[current_section][-1] += ' ' + line.strip()
            else:
                sections[current_section].append(line.strip())
    # Creates empty subsection for keys with no values
    for key in sections.keys():
        if not sections[key]:
            sections[key] = ['']
    
    return sections 


######################################################
# Generate paragraphs 
######################################################

#Define function to generate text for each section given in the outline
def generate_paragraphs(sections):
    generated_text_list = [] 

    # Loop through each section header and subtopics
    for section_header, subtopics in sections.items():
        # Loop through each subtopic within a section
        for subtopic in subtopics:
            # Generate prompt
            prompt = f"Write a few paragraphs on the following thesis paper section: {topic}. {section_header}: {subtopic}."
            print(f"Writing section {section_header}: {subtopic}")
            # Generate text using OpenAI API
            responses = openai.Completion.create(
                model='text-davinci-003',
                prompt=prompt,
                temperature=0.8,
                max_tokens=3800,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0.6,
                best_of = 5
            )
            # Append the generated text to the list
            generated_text_list.append(f"{section_header}: {subtopic} \n\n {responses.choices[0].text} \n")

    # Join the generated text together to create the final string
    generated_text_draft =  '\n\n'.join(generated_text_list)
    # return list of generated text
    return generated_text_list, generated_text_draft



######################################################
# Self assessment
######################################################

# define function for scoring and providing feedback on generated text
def evaluate_sections(generated_text_list):
    evaluations = {} 
    # Loop through each section
    for draft_section in generated_text_list:

        # Evaluate the response using OpenAI API
        prompt = f"Please evaluate the quality of the following section on a scale of 1-100, with 100 being the highest possible score. Evaluate based on the clarity of the writing, the coherence of the arguments, and the use of evidence to support claims;  list the score first, then provide an explanation for the score with specific improvements. Section:{draft_section} "
        print("Evaluating secton")
        response_eval = openai.Completion.create(
            model='text-davinci-003',
            prompt=prompt,
            temperature=1.2,
            max_tokens=500,
            top_p=0.7,
            frequency_penalty=0.5,
            presence_penalty=1.2,
        )

        # Append the generated text to evaluations dictionary
        evaluations[draft_section] = response_eval['choices'][0]['text']
        
    # Rename the dictionary storing sections and their feedback
    evaluations_dict = evaluations 

    # Initialize string version of functionoutput
    evaluations_draft = ""
    
    # Add values to dictionary
    for key, value in evaluations.items():
         evaluations_draft += "\n\n" + key + "\n" + "\n SECTION FEEDBACK: " + value + "\n\n"
    
    return evaluations_dict, evaluations_draft
    
    
# Score parsing
########################

# define function to parse scores from feedback for later calculations
def get_scores(evaluations_dict):
    scores = []
    for feedback in evaluations_dict.values():
        score_str = ""
        for char in feedback:
            if char.isdigit():
                score_str += char
                if len(score_str) == 2:
                    if score_str == "10" and feedback[feedback.index(score_str) + 2] == "0":
                        score_str += "0"
                    break
        scores.append(score_str)

    return scores 



# define functions to add scores to outline foe easy viewing for problem sections
def scored_outline(sections, scores):
    output_string = ""
    
    scores_with_indices = [(score, i) for i, score in enumerate(scores)]
    
    for section_num, (section_title, subsections) in enumerate(sections.items()):
        output_string += f"{section_title}\n"
        
        for subsec_num, subsection_title in enumerate(subsections):
            score, score_index = scores_with_indices[section_num*2 + subsec_num]
            output_string += f"{subsection_title}: {score}/100\n"
        
        output_string += "\n"  # add an empty line after each section
    
    return output_string




######################################################
# SECOND DRAFT - Revise Paragraphs
######################################################

def incorporate_feedback(evaluations_dict, topic):
    revised_draft_list = []
    for section, feedback in evaluations_dict.items():
        prompt = f"The following section is from a thesis paper on {topic}, please rewrite the section to incorporate suggestions from the feedback, but do not provide addtional feedback on the section and maintain the structure of the original section as much as possible. \n Section:{section} \n Feedback: {feedback}"
        print("performing section revisions")


            # Generate text using OpenAI API
        responses = openai.Completion.create(
            model='text-davinci-003',
            prompt=prompt,
            temperature=0.8,
            max_tokens=2800,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0.6,
        )

        # Append the generated text to the list
        revised_draft_list.append(f"\n {responses.choices[0].text} \n")

    # Join the generated text together to create the final string
    revised_draft_text =  '\n\n'.join(revised_draft_list)
    # return list of generated text
    return revised_draft_list, revised_draft_text

    



######################################################
# SECOND Draft Self assessment
######################################################
def evaluate_revised_sections(revised_draft_list):
    second_draft_evaluations = {} # create a new dictionary to store the scores for each section

    # Loop through each section's responses
    for draft_section in revised_draft_list:

        # Loop through each subtopic's response within a section
            # Evaluate the response using OpenAI API
        prompt = f"Please evaluate the quality of the following section on a scale of 1-100, with 100 being the highest possible score. Evaluate based on the clarity of the writing, the coherence of the arguments, and the use of evidence to support claims;  list the score first, then provide an explanation for the score with specific improvements. Section:{draft_section} "
        #prompt = "Please evaluate the quality of the following section on a scale of 1-100, with 100 being the highest possible score. Evaluate based on the clarity of the writing, the coherence of the arguments, and the use of evidence to support claims. Please provide a detailed explanation of the score, including specific examples from the text in the following section. Consider the overall structure and organization of the section, and its place in the paper. Outline: {outline} , {draft_section}"
        print("evaluating revised section")
        response_eval = openai.Completion.create(
            model='text-davinci-003',
            prompt=prompt,
            temperature=1.2,
            max_tokens=500,
            top_p=0.7,
            frequency_penalty=0.5,
            presence_penalty=1.2,
        )

        # Append the generated text to the list
        #evaluations.append(f"DRAFT SECTION: {draft_section} \n \n RESPONSE EVAL: {response_eval['choices'][0]['text']}")
        second_draft_evaluations[draft_section] = response_eval['choices'][0]['text']

    second_draft_evaluations_dict = second_draft_evaluations

    second_draft_evaluations_draft = ""
    
    for key, value in second_draft_evaluations.items():
         second_draft_evaluations_draft += "\n\n" + key + "\n" + "\n SECTION FEEDBACK: " + value + "\n\n"
    
    return second_draft_evaluations_dict, second_draft_evaluations_draft
    




######################################################
# Score revised draft 
######################################################

def get__revised_scores(second_draft_evaluations_dict):
    revised_scores = []
    for feedback in second_draft_evaluations_dict.values():
        score_str = ""
        for char in feedback:
            if char.isdigit():
                score_str += char
                if len(score_str) == 2:
                    if score_str == "10" and feedback[feedback.index(score_str) + 2] == "0":
                        score_str += "0"
                    break
        revised_scores.append(score_str)  
    return revised_scores 



def scored_outline(sections, revised_scores):
    outline_revised_scores = ""
    
    scores_with_indices = [(score, i) for i, score in enumerate(revised_scores)]
    
    for section_num, (section_title, subsections) in enumerate(sections.items()):
        outline_revised_scores += f"{section_title}\n"
        
        for subsec_num, subsection_title in enumerate(subsections):
            score, score_index = scores_with_indices[section_num*2 + subsec_num]
            outline_revised_scores += f"{subsection_title}: {score}/100\n"
        
        outline_revised_scores += "\n"  # add an empty line after each section
    
    return outline_revised_scores





######################################################
# Save 
######################################################
# Create a unique file name
def write_output_to_file(topic, outline, generated_text_draft, evaluations_draft, average_score, scored_outlines,  revised_draft_text, second_draft_evaluations_text, outline_revised_scores, second_draft_average_score):
    # Create a unique file name
    timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    filename = f"generated_paper_{timestamp}.txt"
    filepath = "./code/outputs/model_18/" + filename

    # Compile components to be saved as output
    full_text = f" Topic: {topic} \n\n Score Comparison:\n\n First Draft: \n  {scored_outlines} \n\nFirst Draft Average Score:{average_score} Second Draft: \n {outline_revised_scores} \n\n Second Draft Average Score: {second_draft_average_score} \n First Draft w/ Feedback {evaluations_draft}. \n\n \n\n Above feedback incorporated to generate second draft. \n Second Draft with Feedback:  \n\n {second_draft_evaluations_text} "

    # Save generated text to a new file with unique name
    with open(filepath, 'w', encoding='utf-8') as file:
        file.write(full_text)







######################################################
# RUN FUNCTIONS 
######################################################

# Ask user for topic
topic = input("Please enter a topic: ")


# Make Outline
outline = generate_outline(topic)
print(outline)
print("Outline Complete.")



# Split into sections
sections = split_outline(outline)
print("Sectioning Complete.")


# Generate Paragraphs
generated_text_list, generated_text_draft  = generate_paragraphs(sections)
print("Generate paragraphs complete.")
   


# Evaluate 
evaluations_dict, evaluations_draft = evaluate_sections(generated_text_list)

print ("evaluation complete")


# Parse Scoring 
scores = get_scores(evaluations_dict)
total_score = sum(int(score) for score in scores)
average_score = total_score / len(scores)
print("Average score=", average_score)
scored_outlines =  scored_outline(sections, scores)
print(scored_outlines)
print ("scoring complete")




### SECOND DRAFT 

revised_draft_list, revised_draft_text = incorporate_feedback(evaluations_dict, topic)

print("revised draft list len=", len(revised_draft_list))



second_draft_evaluations_dict, second_draft_evaluations_text = evaluate_revised_sections(revised_draft_list)

revised_scores = get__revised_scores(second_draft_evaluations_dict)

second_draft_total_score = sum(int(score) for score in revised_scores)
second_draft_average_score = second_draft_total_score / len(revised_scores)

outline_revised_scores = scored_outline(sections, revised_scores)



# Write output to file
write_output_to_file(topic, outline, generated_text_draft, evaluations_draft, average_score, scored_outlines,  revised_draft_text, second_draft_evaluations_text, outline_revised_scores, second_draft_average_score)



######################################################
# end timing 
######################################################



end_time = time.time()
#print("Total time taken: {:.2f} seconds".format(end_time - start_time))
total_time = end_time - start_time

minutes, seconds = divmod(total_time, 60)
print("Total time taken: {:.0f} minutes {:.2f} seconds".format(minutes, seconds))
print("Please check output!")
print("model18")