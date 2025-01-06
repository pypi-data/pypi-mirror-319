import datetime
import hashlib
import json
import re
import socket
import threading
from openai import OpenAI
from pdfminer.high_level import extract_text
import pdfminer
from itertools import product
import os
import math
import argparse

import evaluator


client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

# Flag to indicate whether the run should be stopped
flags = {
    'stop_run': False,
    'stop_runs': False
}

def listen_for_stop_signal(port, flag_key, flags):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('localhost', port))
        s.listen()
        print(f"listening for {flag_key} signal on port {port}...")
        conn, addr = s.accept()
        with conn:
            print(f"{flag_key} signal received from {addr}.")
            flags[flag_key] = True


def get_pdf_title(pdf_path):
    # Extract text from the PDF
    text = extract_text(pdf_path, page_numbers=[0])
    # Split the text into paragraphs
    title = text.split('\n\n')[0].replace('\n', '')
    return title

def extract_text_from_pdf(pdf_path, line_overlap=0.6, line_margin=0.6, char_margin=3.0, ignore_patterns=[r'^\d+$', r'^\x0c']):
    params = pdfminer.layout.LAParams(line_overlap=line_overlap, line_margin=line_margin, char_margin=char_margin)
    text = extract_text(pdf_path, laparams=params)

    # Split the text into paragraphs
    paragraphs = text.split('\n\n')
    title = get_pdf_title(pdf_path)
    # Clean the paragraphs
    cleaned_paragraphs = clean_paragraphs(paragraphs, ignore_patterns=ignore_patterns)
    cleaned_text = '\n\n'.join(cleaned_paragraphs)
    return title, cleaned_text

def is_complete_sentence(text):
    # Define regex patterns for various sentence-ending formats
    sentence_end_patterns = [
        r'[.!?][\"\')\]]*$',  # Ends with punctuation followed by optional quotes, parentheses, or brackets
        r'[.!?][\"\')\]]*\s*\(\d+\)$',  # Ends with punctuation followed by optional quotes, parentheses, or brackets and a citation
        r'[.!?][\"\')\]]*\s*\[\d+\]$',  # Ends with punctuation followed by optional quotes, parentheses, or brackets and a footnote
        r'[.!?][\"\')\]]*$',  # Ends with punctuation followed by optional quotes, parentheses, or brackets and space
        r':$',  # Ends with colon (lead up to a block quotation)
    ]

    # Check if the text matches any of the sentence-ending patterns
    for pattern in sentence_end_patterns:
        if re.search(pattern, text.strip()):
            return True

    return False

def split_paragraph_with_punctuation(paragraph):
    # Use re.findall to capture sentences along with punctuation and spaces
    sentences = re.findall(r'.*?.!?\]]*|\s*\(\d+\)|\s*\[\d+\])?(?=\s+|$)', paragraph.strip())
    return sentences

def check_final_sentence(paragraph):
    # Split the paragraph by traditional sentence-ending punctuation
    # sentences = re.split(r'(?<=[.!?]) +', paragraph)
    sentences = split_paragraph_with_punctuation(paragraph)
 
    # If the last sentence is not complete, merge it with the previous one
    # if len(sentences) > 1 and not is_complete_sentence(sentences[-1]):
    #     final_sentence = sentences[-2] + sentences[-1]
    # else:
    #     final_sentence = sentences[-1]
    
    return sentences[-1], is_complete_sentence(sentences[-1])


def find_unintended_breaks_indices(paragraphs, header_re=r'^\x0c', page_number_re=r'^\d+$'):
    unintended_break_indices = []
    header_indices = []
    page_number_indices = []

    first_half, second_half = None

    for i, paragraph in enumerate(paragraphs):
        if re.search(header_re, paragraph):
            header_indices.append(i)
        elif len(re.findall(page_number_re, paragraph)) == 1:
            page_number_indices.append(i)

        elif check_final_sentence(paragraph)[1]:
            if first_half:
                second_half = i
                unintended_break_indices.append((first_half, second_half))
                first_half, second_half = None

            else:
                first_half = i

    return header_indices, page_number_indices, unintended_break_indices


def get_ignore_indices(paragraphs, ignore_patterns: list[str]):
    ignore_indices = []
    for i, paragraph in enumerate(paragraphs):
        for pattern in ignore_patterns:
            if re.search(pattern, paragraph):
                ignore_indices.append(i)
                break
    return ignore_indices

def is_ignored(paragraph, ignore_patterns: list[str]):
    for pattern in ignore_patterns:
        if re.search(pattern, paragraph):
            return True
    return False
           
def remove_line_breaks(lines: list[str]):
    merged_lines = ""
    for line in lines:
        merged_lines += line[:line.rfind("-")] if line.strip()[-1] == "-" else line
    return merged_lines


def clean_paragraphs(paragraphs: list[str], ignore_patterns=[r'^\[\d+\]$', r'^\x0c']):
    cleaned_paragraphs = []
    previous_paragraph_incomplete = False
    for paragraph in paragraphs:
        if not is_ignored(paragraph, ignore_patterns):
            lines = paragraph.splitlines()
            merged_paragraph = remove_line_breaks(lines)

            if previous_paragraph_incomplete:
                cleaned_paragraphs[-1] += (merged_paragraph)
            else:
                cleaned_paragraphs.append(merged_paragraph)
            
            previous_paragraph_incomplete = not is_complete_sentence(lines[-1])

    return cleaned_paragraphs

# Function to add brackets to the regex if they forgot to include them so the page number can be included
def ensure_brackets(s):
    if not s.startswith('('):
        s = '(' + s
    if not s.endswith(')'):
        s = s + ')'
    return s

def merge_adjacent_elements(lst=list, n=1):
    if n < 1:
        raise ValueError("n must be at least 1")
    return [''.join(lst[i:i + n]) for i in range(0, len(lst), n)]

# Function to split text based on regex or default to 8 paragraphs, ignores everything up to the first page number.
def split_text(text: str, regex=None, full_paragraphs=True, n_paragraphs_per_page=3):
    if regex and not full_paragraphs:
        text_chunks = merge_adjacent_elements(re.split(ensure_brackets(regex), text)[1:], n=2)
    elif regex:
        text_chunks=[]
        text_chunk = ''
        paragraphs = text.split('\n\n')
        for i, paragraph in enumerate(paragraphs):
            text_chunk += paragraph + "\n\n"
            if (i > 1) and re.search(regex, paragraph):
                text_chunks.append(text_chunk)
                text_chunk = ''
    else:
        paragraphs = text.split('\n\n')
        text_chunks = ['\n\n'.join(paragraphs[i:i+n_paragraphs_per_page]) for i in range(0, len(paragraphs), n_paragraphs_per_page)]

    return text_chunks

# CREATING ANKI CARDS
def generate_cloze_deletions(text_chunk, system_prompt, min_cloze_deletion_percentage, temperature=0.7, max_completion_tokens=2000, top_p=0.5, frequency_penalty=-0.05, presence_penalty=-0.05):
    if not system_prompt:
        system_prompt = (
            "You are an AI language model tasked with generating a JSON of words or phrases to be cloze deleted for a given text in order to create Anki Cards. Generate according to the following rules:\n"
            "- The output should be of the format {\"c1\": [\"word/phrase1\", \"word/phrase2\", ...], \"c2\": [\"word/phrase1\", \"word/phrase2\", ...], \"c3\": [\"word/phrase1\", \"word/phrase2\", ...]} where the dictionary keys are the cloze deletion tags.\n"
            "- Provide only the JSON; any other text will be ignored.\n"
            f"- Ensure that {min_cloze_deletion_percentage}% of each paragraph is included for cloze deletion.\n"
            "- Ensure all semantically similar instances of a deleted term are listed.\n"
            "- Include all terminology and all definitions. Most subjects and predicates of sentences must be included.\n"
            "- Do not just remove single words for cloze deletion; include larger phrases or clauses as well.\n"
            "- Every single Greek, German, French, and Latin term or phrase should be cloze deleted and tagged with 'c3'. Split other cloze deletions roughly 50/50 per card between 'c1' and 'c2'.\n"
        )
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Based on the given text, generate a JSON of words to cloze delete such cloze deletions. The text:\n{text_chunk}"}
        ],
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty,
        max_tokens=max_completion_tokens,
        temperature=temperature,
        top_p=top_p
    )
    return response.choices[0].message['content'].strip()

def create_anki_cards_json_from_cloze_deletions(cloze_deletions_output, text_chunks):
    anki_cards = []
    cloze_deletions = json.loads(cloze_deletions_output)
    
    for i, text_chunk in enumerate(text_chunks):
        # Split the text chunk into paragraphs
        paragraphs = text_chunk.split('\n\n')
        # The first paragraph is the citation
        citation = paragraphs[0]
        # The rest of the paragraphs form the text
        text = '\n\n'.join(paragraphs[1:])
        
        # Create an anki card with "Text" and "Citation" fields
        anki_card = {
            "Text": apply_cloze_deletions(text, cloze_deletions),
            "Citation": citation
        }
        anki_cards.append(anki_card)
    
    return anki_cards


def apply_cloze_deletions(text, cloze_deletions):
    # Create a list of tuples (cloze_tag, phrase) from the dictionary
    cloze_list = [(cloze_tag, phrase) for cloze_tag, phrases in cloze_deletions.items() for phrase in phrases]
    # Sort the list by phrase length in descending order
    cloze_list = sorted(cloze_list, key=lambda x: len(x[1]), reverse=True)
    
    for cloze_tag, phrase in cloze_list:
        # Use re.IGNORECASE to make the replacement case insensitive
        text = re.sub(re.escape(phrase), f"{{{{{cloze_tag}::{phrase}}}}}", text, flags=re.IGNORECASE)
    
    return text


# Function to create cloze deletion anki cards using OpenAI API
def create_anki_cards(text_chunk, system_prompt, temperature=0.7, max_completion_tokens=2000, top_p=0.5, frequency_penalty=-0.05, presence_penalty=-0.05):
    response = client.chat.completions.create(model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"You are about to be given a section of the text, you will convert these into Anki cards in accordance with the guidelines stipulated in your system prompt. Emphasis here is on trying to have as many cloze deletions per card as you can, leave very few words undeleted. How you are to go about doing this is described in your system message. The text:\n{text_chunk}"}
    ],
    # prediction={"type": "content", "content": text_chunk},
    frequency_penalty=frequency_penalty,
    presence_penalty=presence_penalty,
    max_completion_tokens=max_completion_tokens,
    temperature=temperature,
    top_p=top_p)
    return response.choices[0].message.content.strip()

# FORMATING AS JSON
def format_as_json(output):
    def clean_output(output):
        # Replace unescaped double quotes in the text field with single quotes, excluding keys
        output = re.sub(r'(?<!\{)(?<!\d\])(?<!:\s)(?<!Text)(?<!Citation)((?:\\)?)"(?!,|Citation|Text|\}(?!\}))', "\\\"", output)

        # Find the position of the first '['
        start_index = output.find('[')
        
        # Initialize the counter for brackets
        counter = 0
        outer_scope_start = -1
        
        # Find the outermost open '{' bracket using the counter
        for i in range(len(output) - 1, -1, -1):
            if output[i] == '}':
                counter -= 1
            elif output[i] == '{':
                counter += 1
                if counter == 1:
                    outer_scope_start = i
                    counter = 0 
        print(f"Outer Scope Start: {outer_scope_start}\n")
        # If an outer scope '{' bracket is found, find the first closing '}' bracket that precedes it
        if outer_scope_start != -1:
            end_index = output.rfind('}', 0, outer_scope_start) + 1
            cleaned_output = output[start_index:end_index] + ']'

            remaining_start = output.find('{', end_index)
            remaining_content = output[remaining_start:-1].strip('```').strip()
            print(f"Remaining JSON: {remaining_content}")

        else:
            end_index = len(output)
            cleaned_output = output[start_index:end_index].strip('```')
            remaining_content = None
        
        print(f"Start Index: {start_index}\n")
        print(f"End Index: {end_index}\n")
        return cleaned_output, remaining_content

    def retry_parsing(cleaned_output):
        try:
            # Load the JSON data
            json_output = json.loads(cleaned_output)
            return json_output, None
        except json.JSONDecodeError as e:

            print(f"JSONDecodeError: {str(e)}")
            print(f"Error Position: {e.pos}")
            print(f"Error Line: {e.lineno}")
            print(f"Error Column: {e.colno}")
            print(f"Cleaned Output: {cleaned_output}")
            return None, str(e)

    try:
        cleaned_output, remaining_content = clean_output(output)
        json_output, error = retry_parsing(cleaned_output)
        if error:
            # Provide a mechanism to fix the JSON string and retry
            while error:
                if flags['stop_run'] or flags['stop_runs']:
                    print("Stopping run prematurely...")
                    break
                print("Please fix the JSON string and press Enter to retry:")
                input("Press Enter to retry...")
                cleaned_output = input("Enter the corrected JSON string: ")
                json_output, error = retry_parsing(cleaned_output)
        return (json_output, remaining_content), None
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return None, str(e)
    
def find_remaining_text(input_chunk, remaining_content):
    # Extract the content of the "Text" field from the remaining_content string
    text_start = remaining_content.find('"Text": "') + len('"Text": "')
    text_end = remaining_content.find('",', text_start)
    remaining_text = remaining_content[text_start:text_end]
    
    # Consider only the text up until the first "{"
    search_text = remaining_text.split("{")[0]

    search_text = search_text[:40] if len(search_text) > 40 else search_text
    
    # Find the position of the search_text in the input_chunk
    start_index = input_chunk.find(search_text)
    
    # If the search_text is found, return the section from start_index to the end of input_chunk
    if start_index != -1:
        return input_chunk[start_index:].strip()
    else:
        return None
    
# WRITING TO FILE
def write_json_to_file(output_json_path: str, output: str, args: argparse.ArgumentParser, run_id: str, mode='w+'):
    try:
        with open(output_json_path, mode, encoding='utf8') as output_file:
                output = [{"args": vars(args), "output": output.copy(), "run_id": run_id}]
                if not args.overwrite:
                    try: 
                        output_file.seek(0)
                        existing_content = json.loads(output_file.read())
                        output.extend(existing_content)          
                    except:
                        print("File corrupted, empty or is not a list. Forcing overwrite.")
                    finally:
                        output_file.seek(0)
                        output_file.truncate()
                
                json.dump(output, output_file, indent=4)
    except FileNotFoundError as e:
        return e

import csv

def write_json_to_csv(output_csv_path: str, output: str, args: argparse.ArgumentParser,  run_id: str, mode='w+'):
    # Flatten the nested JSON structure
    flattened_json = flatten_json(output)
    try:
        # Open the CSV file with the specified mode and encoding
        with open(output_csv_path, mode, newline='', encoding='utf8') as output_file:
            # Create a CSV DictWriter object with fieldnames from the first dictionary in the list
            writer = csv.DictWriter(output_file, fieldnames=flattened_json[0].keys())
            
            if not args.overwrite:
                try:
                    # Move the file pointer to the beginning of the file
                    output_file.seek(0)
                    # Read the existing content of the CSV file into a list of dictionaries
                    existing_content = list(csv.DictReader(output_file))
                    # Extend the flattened JSON list with the existing content
                    flattened_json.extend(existing_content)
                except:
                    # Handle cases where the file is corrupted, empty, or not a list
                    print("File corrupted, empty or is not a list. Forcing overwrite.")
                finally:
                    # Move the file pointer to the beginning and truncate the file
                    output_file.seek(0)
                    output_file.truncate()
            
            # Write the header row to the CSV file
            writer.writeheader()
            # Write the rows to the CSV file
            writer.writerows(flattened_json)
    except FileNotFoundError as e:
        return e

def flatten_json(nested_json):
    """
    Flatten a nested JSON structure.
    
    Args:
        nested_json (list): A list of dictionaries, potentially nested.
    
    Returns:
        list: A list of flattened dictionaries.
    """
    def flatten_dict(d, parent_key='', sep='_'):
        items = []
        for k, v in d.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, dict):
                # Recursively flatten nested dictionaries
                items.extend(flatten_dict(v, new_key, sep=sep).items())
            elif isinstance(v, list):
                # Handle lists by creating separate entries for each item
                for i, item in enumerate(v):
                    if isinstance(item, dict):
                        # Recursively flatten nested dictionaries within lists
                        items.extend(flatten_dict(item, f"{new_key}{sep}{i}", sep=sep).items())
                    else:
                        # Add non-dictionary items in lists
                        items.append((f"{new_key}{sep}{i}", item))
            else:
                # Add non-dictionary items
                items.append((new_key, v))
        return dict(items)

    # Flatten each dictionary in the list
    flattened_list = []
    for item in nested_json:
        if 'anki_cards' in item:
            for card in item['anki_cards']:
                flattened_card = flatten_dict(card)
                # Add other top-level keys to each card
                for key in item:
                    if key != 'anki_cards':
                        flattened_card[key] = item[key]
                flattened_list.append(flattened_card)
        else:
            flattened_list.append(flatten_dict(item))
    return flattened_list




def main():
    parser = argparse.ArgumentParser(description='Generate cloze deletion anki cards from an epub file.')
    # I/O
    parser.add_argument('pdf_file', type=str, help='Path to the pdf file')
    parser.add_argument('-o', '--out', type=str, required=True, help='Output JSON file path')
    parser.add_argument('-w', '--overwrite', action='store_true', help='Overwrite what is in the output destination')

    # FOR EXTRACTING TEXT INFORMATION FROM PDF USING PDFMINER.SIX
    parser.add_argument("--ignore_patterns", type=str, nargs='*', help="Regular expression(s) to identify headers and page numbers", default=[r'^\d+$', r'^\x0c'])
    parser.add_argument("--line_overlap", type=float, help="If two characters have more overlap than this they are considered to be on the same line. The overlap is specified relative to the minimum height of both characters.", default=0.6)
    parser.add_argument("--line_margin", type=float, help="If two lines are are close together they are considered to be part of the same paragraph. The margin is specified relative to the height of a line.", default=0.6)
    parser.add_argument("--char_margin", type=float, help="If two characters are closer together than this margin they are considered part of the same line. The margin is specified relative to the width of the character.", default=3.0)

    # FOR TEXT BATCHING AS INPUT TO THE LLM 
    parser.add_argument('-r', '--regex', type=str, help='Regular expression to split the text', default=None)
    parser.add_argument('--pages_per_chunk', type=int, help='Number of pages per text chunk to be inputed to the model', default=1)
    parser.add_argument('--page_range', type=int, nargs=2, help='Number of total pages to be converted', default=[1,0])
    parser.add_argument('--full_paragraphs', action='store_true', help='Whether the chunks should always end on the final sentence of a paragraph')
    parser.add_argument('--n_paragraphs_per_page', type=int, help='The estimated number of paragraphs per page (use only if you don\'t have page # regex)', default=4)


    # FOR OPENAI GPT 4o MINI ANKI CARD GENERATION
    parser.add_argument('--prompt_file', type=str, help='Path to a text file containing system prompt instructions', default=None)
    parser.add_argument('--prompt_text', type=str, help='Prompt instructions as a string', default=None)
    parser.add_argument('-t', '--temperature', type=float, nargs='*', help='What sampling temperature to use, between 0 and 2. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic.', default=[0.7])
    parser.add_argument('--max_completion_tokens', type=int, nargs='*', help='An upper bound for the number of tokens that can be generated for a completion, including visible output tokens and reasoning tokens.', default=[3000])
    parser.add_argument('--top_p', type=float, nargs='*', help='An alternative to sampling with temperature, called nucleus sampling, where the model considers the results of the tokens with top_p probability mass. So 0.1 means only the tokens comprising the top 10% probability mass are considered.', default=[0.5])
    parser.add_argument('--frequency_penalty', type=float, nargs="*", help='Number to reduce the likelihood of selecting previously seen tokens', default=[-0.05])
    parser.add_argument('--presence_penalty', type=float, nargs="*", help='Number to reduce the likelihood of selecting tokens that are already present in the text', default=[-0.05])
    parser.add_argument('--generate_cloze_deletions', action='store_true', help='Generate cloze deletions from the output of the LLM.')

    # FOR EVALUATING OUTPUT
    parser.add_argument('--min_cloze_deletion_percentage', type=int, help='Minimum percentage of cloze deletions in the output', default=15)
    # MISCELLANEOUS
    parser.add_argument('--test', action='store_true', help='Generate Anki cards for the first chunk only and append "_test" to the output filename')
    parser.add_argument('--use_example', action='store_true', help='Use example ANKI cards to test file writing')
    

    args = parser.parse_args()

    # Generate a unique run ID based on the arguments and timestamp
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-4]
    args.timestamp = timestamp
    hash_dict = json.dumps(vars(args), sort_keys=True)
    run_id = hashlib.sha256(hash_dict.encode()).hexdigest()

    if not args.use_example:

        # Extract text from epub file
        params = {"line_overlap": args.line_overlap, "line_margin": args.line_margin, "char_margin": args.char_margin, "ignore_patterns": args.ignore_patterns}
        title, text = extract_text_from_pdf(args.pdf_file, **params)

        # Split text based on regex or default to 8 paragraphs
        text_chunks = merge_adjacent_elements(split_text(text, args.regex, args.full_paragraphs, args.n_paragraphs_per_page), n=args.pages_per_chunk)

        # Load prompt instructions from file or use provided prompt text
        if args.prompt_file:
            with open(args.prompt_file, 'r') as file:
                system_prompt = file.read()
        elif args.prompt_text:
            system_prompt = args.prompt_text
        else:
            system_prompt = (
                f"You are a philosophy professor creating Anki flash cards from a given text for self-study purposes. "
                f"You will be given a chunk of text from one of Martin Heidegger's books, to make Anki cloze deletion cards. "
                "Create as many flash cards as needed following these rules:\n"
                "- Do not create duplicates.\n"
                "- You must turn the entirety of the input text into flash cards.\n"
                "- Provide only the JSON for the flash cards; any other text will be ignored.\n"
                "- Format the cards with cloze deletion for the front. \n"
                "- Aim to cloze delete between 35 and 50% of the input text. Don't go over 55%. \n"
                "- Keep the number of deletions consistent between cards, no huge variations.\n"
                "- Include the text citation with the page number under the field 'Citation'.\n"
                "- Do not invent anything; use only the given text.\n"
                "- Do not just remove single words for cloze deletion; include larger phrases or clauses as well.\n"
                "- The 'Text' field should contain at least a 5-6 sentences with at least 25% of the text cloze deleted but max 3 clozes (c1, c2, c3). Multiple 'c1's, 'c2's, and possibly 'c3's should be thematically related.\n"
                "- Write in English (unless there are German, Latin, or Greek terms).\n"
                "- Do not create so many cards that some have less than 5 sentences. It's okay for some cards to have up to 8-10 sentences.\n"
                "- Cloze delete significant nouns, verbs, words, and phrases.\n"
                "- Every single Greek, German, French, and Latin term should be cloze deleted and tagged with 'c3'. Split other cloze deletions roughly 50/50 per card between 'c1' and 'c2'.\n"
                "- Ensure each card is self-complete with enough context to recognize and understand its meaning vaguely on its own. If part of the passage includes a quote from another philosopher, provide enough context prior to the quote.\n"
                "- Ensure all instances and semantically similar instances of a deleted term are clozed."
                "- Cloze delete all of Heidegger's terminology and all of his definitions. Most subjects and predicates of sentences must be cloze deleted."
                "- All hyphenated words must be cloze deleted (e.g. Being-in-the-world, within-the-world, Being-in, reference-relations, existential-ontological, ontico-existentiell etc.)."
                "- Example format for 'Text' field, please match the number and density of cloze deletions for your own cards: \"The full {{c1::essence of truth}}, including its most proper {{c1::nonessence}}, keeps {{c2::Dasein}} in need by this perpetual {{c1::turning to and fro}}. {{c2::Dasein}} is a {{c1::turning into need}}. From the {{c2::Da-sein}} of human beings and from it alone arises the disclosure of {{c1::necessity}} and, as a result, the {{c1::possibility of being transposed}} into what is {{c2::inevitable}}. The disclosure of beings as such is {{c1::simultaneously}} and {{c1::intrinsically}} the {{c2::concealing of beings}}.\"\n"
            )

        if args.regex:
            system_prompt += f"Include the title '{title}' along with the page number in the citation. You can locate the page numbers using the regex '{args.regex}'. Make sure to keep track of when you cross page numbers and cite accordingly. Every text chunk starts with a page number and there should be a total of {str(args.pages_per_chunk)} pages per text chunk."
       
        args.prompt_text = system_prompt
        output_json_path = args.out
        output_csv_path = os.path.splitext(output_json_path)[0] + ".csv"


        if args.test:
            # output_json_path = os.path.splitext(output_json_path)[0] + "_test_t{}_tp{}_mct{}.json".format(str(args.temperature).translate(str.maketrans('', '',string.punctuation)), str(args.top_p).translate(str.maketrans('', '',string.punctuation)), args.max_completion_tokens)
            output_json_path = os.path.splitext(output_json_path)[0] + "_test.json"
            output_csv_path = os.path.splitext(output_csv_path)[0] + "_test.csv"
            input_json_path = os.path.splitext(output_json_path)[0] + "_input.txt"

        error_log_path = os.path.splitext(output_json_path)[0] + "_errors.txt"
        remaining_text_path =  os.path.splitext(output_json_path)[0] + "_remaining.txt"

        all_outputs = []
        all_error_logs = []
        all_remaining_text = []


        # Limit chunks if test flag is set
        text_chunks = text_chunks[math.ceil(args.page_range[0]/args.pages_per_chunk) - 1: math.ceil(args.page_range[1]/args.pages_per_chunk) - 1]

        if args.test:
            text_chunks = text_chunks[:1] if len(text_chunks) > 1 else text_chunks
            print(f"No. of Text Chunks: {len(text_chunks)}\n")
            print("Writing inputs to file...")
            try:
                write_json_to_file(output_json_path=input_json_path, output=text_chunks, args=args, run_id=run_id, mode='a+')
            except FileNotFoundError:
                write_json_to_file(output_json_path=input_json_path, output=text_chunks, args=args, run_id=run_id, mode='w+')


        stop_signal_port_run = 65432
        stop_signal_port_runs = 65433

        # Start the key press listener in a separate thread
        listener_thread_1 = threading.Thread(target=listen_for_stop_signal, args=(stop_signal_port_run, 'stop_run', flags))
        listener_thread_2 = threading.Thread(target=listen_for_stop_signal, args=(stop_signal_port_runs, 'stop_runs', flags))

        listener_thread_1.start()
        listener_thread_2.start()

        
        for (temperature, max_completion_tokens, top_p, frequency_penalty, presence_penalty) in product(args.temperature, args.max_completion_tokens, args.top_p, args.frequency_penalty, args.presence_penalty):
            
            if flags['stop_runs']:
                print("Stopping all runs prematurely...")
                break
            
            # For a given set of parameters, create anki cards for each chunk and handle errors
            variables = {"temperature": temperature, "max_completion_tokens": max_completion_tokens, "top_p": top_p, "frequency_penalty": frequency_penalty, "presence_penalty": presence_penalty}

            all_anki_cards = []
            error_log = []

            error_count = 0
            consecutive_errors = 0
            min_cloze_deletion_percentage_failures = 0
            consecutive_min_cloze_deletion_percentage_failures = 0
            total_cloze_deletion_percentage = 0
            total_length_of_cards = 0
            total_number_of_cards = 0

            for i, chunk in enumerate(text_chunks):

                if flags['stop_run'] or flags['stop_runs']:
                    print("Stopping run prematurely...")
                    break

                if generate_cloze_deletions:
                    cloze_deletions_output = generate_cloze_deletions(chunk, system_prompt, args.min_cloze_deletion_percentage, **variables)
                    anki_cards_json = (create_anki_cards_json_from_cloze_deletions(cloze_deletions_output, text_chunks), None)
                    error = None
                else:
                    anki_cards_output = create_anki_cards(chunk, system_prompt, **variables)
                    anki_cards_json, error = format_as_json(anki_cards_output)

                
                if flags['stop_run'] or flags['stop_runs']:
                    print("Stopping run prematurely...")
                    break


                if anki_cards_json:
                    anki_cards_json_cleaned, anki_cards_json_remaining = anki_cards_json
                    all_anki_cards.extend(anki_cards_json_cleaned)
                    consecutive_errors = 0 # reset the counter because we didn't encounter an error in generating cards nor formatting as json

 # Calculate the percentage of cloze deletions in the output
                    percentage_cloze_deletions = evaluator.calculate_total_cloze_deletion_percentage(anki_cards_json_cleaned)
                    total_cloze_deletion_percentage += percentage_cloze_deletions
                    print(f"Chunk #{i + int(args.page_range[0] / args.pages_per_chunk)} Percentage Cloze Deletions: {percentage_cloze_deletions}%\n")
                    print(f"Cloze Deletion Percentage per Card: {[evaluator.calculate_total_cloze_deletion_percentage([card]) for card in anki_cards_json_cleaned]}\n")
                    average_cloze_deletion_percentage = total_cloze_deletion_percentage/(i+1)
                    print(f"Average Cloze Deletion Percentage: {average_cloze_deletion_percentage}%\n")
                    card_lengths = [len(re.sub(r'{{c\d::|}}', '', card['Text'])) for card in anki_cards_json_cleaned]
                    length_of_cards = sum(card_lengths)
                    number_of_cards = len(anki_cards_json_cleaned)
                    total_length_of_cards += length_of_cards
                    total_number_of_cards += number_of_cards
                    print(f"Chunk Length: {len(chunk)}\n")
                    print(f"Card Lengths: {card_lengths}\n")
                    print(f"Average Length of Cards: {length_of_cards/number_of_cards}\n")
                    print(f"Number of Cards: {number_of_cards}\n")
                    print(f"Overall Average Length of Cards: {total_length_of_cards/total_number_of_cards}\n")
                    print(f"Last Bit of Chunk: {chunk[-60:]}\n")
                    print(f"Last Bit of Last Card: {anki_cards_json_cleaned[-1]['Text'][-70:]}\n")

                    if percentage_cloze_deletions < args.min_cloze_deletion_percentage:
                        error_log.append({"error": f"Percentage of cloze deletions is less than {args.min_cloze_deletion_percentage}%", "chunk": chunk, "output": anki_cards_output, "terminal": False})
                        min_cloze_deletion_percentage_failures += 1
                        consecutive_min_cloze_deletion_percentage_failures += 1
                    else:
                        consecutive_min_cloze_deletion_percentage_failures = 0

                    if consecutive_min_cloze_deletion_percentage_failures >= 3 or (min_cloze_deletion_percentage_failures >= len(text_chunks) * 0.1 and average_cloze_deletion_percentage < args.min_cloze_deletion_percentage) or (min_cloze_deletion_percentage_failures >= len(text_chunks) * 0.2):
                        error_log[-1]["Terminal"] = True
                        print("Too many failures to meet the minimum cloze deletion percentage. Stopping execution.\n")
                        break


                    # check if there is any content remaining from an output that was incomplete i.e. with a card that didn't fully generate
                    if anki_cards_json_remaining:
                        # print(f"Output: {i}\nRemaining JSON: {anki_cards_json_remaining}\n")
                        remaining_text = find_remaining_text(chunk, anki_cards_json_remaining)

                        # TODO: if it cuts off at the field name and there is no text to go off of to search for where it cut off in the input, use the last couple of words from the last good card to search
                        if remaining_text:
                            print(f"Remaining Text: {remaining_text}\n")
                            if i < len(text_chunks) - 1:
                                text_chunks[i+1] = remaining_text + text_chunks[i+1]
                            else:
                                all_remaining_text.append({"remaining_text": remaining_text, "variables": variables})
                        else:
                            message = f"Output #{i} was incomplete but there was no remaining text."
                            print(message + "\nRemaining JSON: {anki_cards_json_remaining}\n")
                            error_log.append({"error": message , "chunk": chunk, "output": anki_cards_output, "remaining_json": anki_cards_json_remaining})
                
                else:
                    error_count += 1
                    consecutive_errors += 1
                    error_log.append({"error": error , "chunk": chunk, "output": anki_cards_output, "terminal": False})

                if consecutive_errors >= 3 or error_count >= len(text_chunks) * 0.2:
                    print("Too many errors encountered. Stopping execution.")
                    error_log[-1]["Terminal"] = True
                    break

            print(f"Variables: {variables}\n")
            # append the outputs and error logs for this set of variables to the total list
            all_outputs.append({"anki_cards": all_anki_cards, "variables": variables, "run_id": run_id})
            if error_log:
                all_error_logs.append({"error_log": error_log, "variables": variables, "run_id": run_id})

        # write the outputs and the error logs to file    
        print("Writing outputs to file...")
        try:
            write_json_to_file(output_json_path=output_json_path, output=all_outputs, args=args, run_id=run_id, mode='a+')
            write_json_to_csv(output_csv_path=output_csv_path, output=all_outputs, args=args, run_id=run_id, mode='a+')
        except FileNotFoundError:
            write_json_to_file(output_json_path=output_json_path, output=all_outputs, args=args, run_id=run_id, mode="w+")
            write_json_to_csv(output_csv_path=output_csv_path, output=all_outputs, args=args, run_id=run_id, mode='w+')


        if all_remaining_text:
            print("Writing remaining text to file...")
            try:
                write_json_to_file(output_json_path=remaining_text_path, output=all_remaining_text, args=args, run_id=run_id, mode="a+")
            except FileNotFoundError:
                write_json_to_file(output_json_path=remaining_text_path, output=all_remaining_text, args=args, run_id=run_id, mode="w+")


        if all_error_logs:
            print("Writing error logs to file...")
            try:
                write_json_to_file(output_json_path=error_log_path, output=all_error_logs, args=args, run_id=run_id, mode='a+')
            except FileNotFoundError:
                write_json_to_file(output_json_path=error_log_path, output=all_error_logs, args=args, run_id=run_id, mode='w+')


    else:
        output_json_path = os.path.dirname(__file__) + "/examples/example_output.json"
        example_json_path = os.path.dirname(__file__) + "/examples/example01.json"
        with open(example_json_path, 'r') as example_json:
            all_anki_cards = json.load(example_json)
        write_json_to_file(output_json_path, all_anki_cards, args, run_id=run_id)

if __name__ == "__main__":
    main()