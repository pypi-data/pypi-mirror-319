from .general import save_to_csv, read_csv_file
import re, csv, os, threading, string, requests, random, time
from openai import OpenAI
from tqdm import tqdm
from pandas.errors import EmptyDataError
import pandas as pd
import json

classification_analyses = ["tenses", "relationships_classify"]
extraction_analyses = ["relationships_extract"]
keyword_analyses = ["association", "modal", "speculation"]
all_analyses = classification_analyses + extraction_analyses + keyword_analyses

def api_call_wrapper(system_prompt, prompt, result_container, event):
    
    """Try prompting OpenAI."""

    client = OpenAI(
        api_key=os.environ['OPENAI_API_KEY'],  # this is also the default, it can be omitted
    )

    try:
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            response_format = {"type": "json_object"},
            temperature = 0.5,
            timeout=10
        )
        result_container[0] = response
        event.set()
    except Exception as e:
        result_container[1] = e
        event.set()

def send_to_openai(system_prompt, prompt, analysis_type, max_retries=3, manual_timeout=15):
    
    """Handle time-outs by OpenAI."""
    
    base_delay = 1  # Base delay in seconds
    max_delay = 480  # Max delay in seconds
    retries = 0
    
    while retries < max_retries:
        #print("Making API call...")
        
        result_container = [None, None]
        done_event = threading.Event()
        
        api_thread = threading.Thread(target=api_call_wrapper, args=(system_prompt, prompt, result_container, done_event))
        api_thread.start()
        api_thread.join(timeout=manual_timeout)
        
        if done_event.is_set():
            response, error = result_container
            if response:
                clean_response = response.choices[0].message.content.strip().lower()
                return clean_response
            elif isinstance(error, requests.exceptions.Timeout):
                retries += 1
                delay = base_delay * (2 ** retries)  # Exponential backoff
                delay = min(max_delay, delay) + random.uniform(0, 0.1*base_delay)  # Add some jitter
                time.sleep(delay)
                print("Timeout exception")
            else:
                raise error  # Some other exception occurred
        else:
            # The manual timeout was triggered
            retries += 1
            print(f"Manual timeout triggered after {manual_timeout} seconds")
            
    return None  # Default return value if all retries fail

def contains_whole_words(analysis_type, sentence):
    
    """Check whether the sentence contains any words in a specified list and report the count."""
    
    words_to_check = []

    modal_words = ["can", "could", "will", "would", "shall", "should", "may", "might", "must", "ought"]
    association_words = ['correlation', 'correlated with', 'correlated to', 'association', 'associated with', 'associated to', 'related with', 'related to', 'relates to', 'linkage', 'linked with', 'linked to']
    speculation_words = ['possibly', 'potentially', 'presumably','perhaps','seem', 'seems', 'appear', 'appears', 'suggest', 'suggests','suppose', 'supposedly']
    uncertainty_words = ["probably", "likely", "unlikely"]
    #ambiguity_words = ["often", "involve", ...?]

    if analysis_type == "modal":
        words_to_check == modal_words
    
    elif analysis_type == "association":
        words_to_check == association_words
    
    elif analysis_type == "speculation":
        words_to_check == speculation_words
    
    elif analysis_type == "uncertainty":
        words_to_check == uncertainty_words

    sentence_text = sentence.lower()
    count = 0
    
    for word in words_to_check:
        matches = re.findall(rf'\b{re.escape(word)}\b', sentence_text)
        count += len(matches)
    
    return count

def get_decision_for_sentence(sentence, context_window, analysis_type):
    
    """Get a decision for the current sentence, based on the current type of analysis."""
    
    if analysis_type in classification_analyses:
        with open(f'./FlashQDA/Prompts/{analysis_type}.txt', 'r') as file:
            system_prompt = "You are a helpful assistant that classifies sentences. Follow the user's instructions carefully. Respond using JSON."
            prompt = file.read()
        prompt = prompt.format(sentence=sentence, context_window=context_window)
        decision = send_to_openai(system_prompt, prompt, analysis_type)
    elif analysis_type in extraction_analyses:
        with open(f'./FlashQDA/Prompts/{analysis_type}.txt', 'r') as file:
            system_prompt = "You are a helpful assistant that extracts and lists causal relationships from sentences. Follow the user's instructions carefully. Respond using JSON."
            prompt = file.read()
        prompt = prompt.format(sentence=sentence, context_window=context_window)
        decision = send_to_openai(system_prompt, prompt, analysis_type)
    elif analysis_type == 'modal':
        decision = contains_whole_words(sentence, analysis_type)
    elif analysis_type == 'association':
        decision = contains_whole_words(sentence, analysis_type)
    elif analysis_type == 'speculation':
        decision = contains_whole_words(sentence, analysis_type)
    return decision

def count_decisions_for_sentence(analysis_type, decisions):
    
    """For the current sentence and the current type of analysis, count the number of decisions that match the specified criteria."""
    
    if analysis_type == "tenses":
        decisions_count = "{},{},{},{},{},{},{},{},{},{},{},{}".format(
            decisions.count('simple past'),
            decisions.count('past perfect'),
            decisions.count('past continuous'),
            decisions.count('past perfect continuous'),
            decisions.count('simple present') + decisions.count('present simple'),
            decisions.count('present continuous'),
            decisions.count('present perfect'),
            decisions.count('present perfect continuous'),
            decisions.count('simple future'),
            decisions.count('future perfect'),
            decisions.count('future continuous'),
            decisions.count('future perfect continuous'))
    
    elif analysis_type == "relationships_classify":
        decisions_count = "{},{},{}".format(
            decisions.count('causal'),
            decisions.count('correlational'),
            decisions.count('no relationship'))
    
    elif analysis_type == "relationships_extract":
        decisions_count = decisions

    elif analysis_type in keyword_analyses:
        decisions_count = decisions[0]
    
    return decisions_count

def calculate_subscore_for_sentence(analysis_type, decisions):

    """For the current sentence and the current type of analysis, calculate a subscore."""

    if analysis_type == "tenses":
        subscore = (decisions.count('simple present') + 
                    decisions.count('present simple') + 
                    decisions.count('present continuous')
                    ) / len(decisions)
    
    elif analysis_type == "relationships_classify":
        subscore = decisions.count('causal') / len(decisions)
    
    elif analysis_type == "relationships_extract":
        subscore = None

    elif analysis_type in keyword_analyses:
        subscore = decisions[0] if decisions[0] <= 1 else 1
    
    return subscore

def analyze_the_current_sentence(sentence, context_window, analysis_type, query_count=3):
    
    """Analyze the current sentence based on the specified analysis type."""
    
    decisions = []
    
    # Classify the current sentence by tense or relationship type (causal, correlational, none)
    if analysis_type in classification_analyses:    
        type = "tenses" if analysis_type == "tenses" else "relationships"
        for _ in range(query_count):
            decision = get_decision_for_sentence(sentence["sentence"], context_window, analysis_type)
            data = json.loads(decision)
            for key, value in data[type].items():
                decisions.append(value)
    
    # Extract causal relationships from the current sentence
    elif analysis_type in extraction_analyses:
        decision = get_decision_for_sentence(sentence["sentence"], context_window, analysis_type)
        decisions = decision        
    
    # Detect keywords in the current sentence
    elif analysis_type in keyword_analyses:
        decision = get_decision_for_sentence(sentence["sentence"], context_window, analysis_type)
        decisions.append(decision)
    
    decisions_count = count_decisions_for_sentence(analysis_type, decisions)
    subscore = calculate_subscore_for_sentence(analysis_type, decisions)
    
    return decisions_count, subscore

def initialize_files(save_name, analysis_type):
    base_path = os.path.join('./Results', save_name)
    results_file = os.path.join(base_path, f'{save_name}_sentences.csv')
    temp_file = os.path.join(base_path, f'{save_name}_{analysis_type}_temp.csv')
    log_file = os.path.join(base_path, f'{save_name}_{analysis_type}_log.csv')

    os.makedirs(base_path, exist_ok=True)
    
    # Ensure results file exists or create an empty one
    if not os.path.exists(results_file):
        pd.DataFrame().to_csv(results_file, index=False)
    
    # Ensure log file exists or create with default values
    if not os.path.exists(log_file):
        with open(log_file, 'w') as log:
            writer = csv.writer(log)
            writer.writerow(['last_processed_document', 'last_processed_sentence'])
            writer.writerow([1, -1])

    # Initialize temp file with empty DataFrame if it doesn't exist
    if not os.path.exists(temp_file):
        pd.DataFrame(columns=["document_id", "filename", "sentence_id", "sentence"]).to_csv(temp_file, index=False)

    # Read existing results from temp file if it exists, otherwise initialize as empty list
    try:
        existing_results = pd.read_csv(temp_file).to_dict('records')
    except EmptyDataError:
        existing_results = []

    return results_file, temp_file, log_file, existing_results

def get_start_ids(log_file):
    try:
        with open(log_file, 'r') as log:
            reader = csv.reader(log)
            next(reader)  # Skip header
            start_document_id, start_sentence_id = map(int, next(reader))
    except EmptyDataError:
        start_document_id, start_sentence_id = 1, -1  # Default values

    return start_document_id, start_sentence_id

def update_log(log_file, document_id, sentence_id):
    with open(log_file, 'w') as log:
        writer = csv.writer(log)
        writer.writerow(['last_processed_document', 'last_processed_sentence'])
        writer.writerow([document_id, sentence_id])

def append_to_context(context_window, sentence, context_length):
    if context_length > 0:
        if len(context_window) == context_length:
            context_window.pop(0)
        context_window.append(sentence)
    return context_window

def check_filter_for_analysis(sentence, context_window, analysis_type, filter, filter_key, filter_cutoff):
    decisions_count, subscore = None, None

    if filter:
        success = sentence.get(f'subscore_{filter}', None)
        if success not in ['', 'nan', None]:
            success = float(success)
            if success >= filter_cutoff:
                decisions_count, subscore = analyze_the_current_sentence(sentence, context_window, analysis_type)
    else:
        decisions_count, subscore = analyze_the_current_sentence(sentence, context_window, analysis_type)

    return decisions_count, subscore

def handle_classified_sentence(sentence, analysis_type, decisions_count, subscore, existing_results):
    
    classified_sentence = {}

    for key, value in sentence.items():
        if key not in classified_sentence:
            classified_sentence[key] = value

    if analysis_type != "relationships_extract":
        classified_sentence.update({
            f"decisions_{analysis_type}": decisions_count,
            f"subscore_{analysis_type}": subscore
        })
    else:
        if decisions_count:
            data = json.loads(decisions_count)
            for relationship in data["relationships"]:
                classified_sentence.update({
                    "cause": relationship["cause"],
                    "effect": relationship["effect"]
                })
                existing_results.append(classified_sentence.copy())
            return
        else:
            classified_sentence.update({"cause": None, "effect": None})

    existing_results.append(classified_sentence)

def analyze_all_sentences(sentences, analysis_type, save_name, context_length=0, filter=None, filter_key=0, filter_cutoff=0):
    results_file, temp_file, log_file, existing_results = initialize_files(save_name, analysis_type)
    start_document_id, start_sentence_id = get_start_ids(log_file)
    #existing_results = pd.read_csv(temp_file).to_dict('records') if os.path.exists(temp_file) else []

    print(f"Starting '{analysis_type}' analysis with '{filter}' filter (filter key: {filter_key}, filter cutoff: {filter_cutoff}) at document {start_document_id}, sentence {start_sentence_id}")

    context_window = []
    for sentence in tqdm(sentences):
        document_id = int(sentence["document_id"])
        sentence_id = int(sentence["sentence_id"])

        if document_id < start_document_id or (document_id == start_document_id and sentence_id <= start_sentence_id):
            continue

        context_window = append_to_context(context_window, sentence["sentence"], context_length)
        decisions_count, subscore = check_filter_for_analysis(sentence, context_window, analysis_type, filter, filter_key, filter_cutoff)
        handle_classified_sentence(sentence, analysis_type, decisions_count, subscore, existing_results)

        try:
            pd.DataFrame(existing_results).to_csv(temp_file, index=False)
            update_log(log_file, document_id, sentence_id)
        except KeyboardInterrupt:
            print(f"Saving interrupted at document {document_id}, sentence {sentence_id}. Continuing until saving completed.")
            pd.DataFrame(existing_results).to_csv(temp_file, index=False)
            update_log(log_file, document_id, sentence_id)
            raise

    results_folder = os.path.join('./Results', save_name)
    pd.DataFrame(existing_results).to_csv(os.path.join(results_folder, f'{save_name}_sentences.csv'), index=False)
    
    return existing_results
    
def score_sentences(sentences, subscores, weights, save_name):
    """Calculate score for the list of sentences."""
    TEMP_FILE = os.path.join('./Results/' + save_name + '_scores_temp.csv')

    scored_sentences = []

    for sentence in sentences:
        score = 0
        for i in range(len(subscores)):
            for key in sentence.keys():
                if key == 'subscore_' + subscores[i]:
                    if sentence[key] not in ['', 'nan']:
                        score += float(sentence[key]) * weights[i]
                        break

        scored_sentence = {
            "score": round(score * 100, 2)
        }

        # Dynamically add keys from the CSV file to classified_sentence
        for key, value in sentence.items():
            if key not in scored_sentence:
                scored_sentence[key] = value

        scored_sentences.append(scored_sentence)  # Append modified dictionary to new list

    # Save the list of sentences as a csv file
    with open(TEMP_FILE, 'w') as f:
        pd.DataFrame(scored_sentences).to_csv(f, index=False)
    results_folder = './Results/' + save_name + '/'
    save_to_csv(scored_sentences, results_folder, save_name + '_sentences.csv')
    os.remove(TEMP_FILE)