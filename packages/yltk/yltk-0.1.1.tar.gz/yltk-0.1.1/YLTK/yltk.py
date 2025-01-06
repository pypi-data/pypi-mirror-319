from concurrent.futures import ThreadPoolExecutor, as_completed
import openai
from collections import Counter
import os
import re

# Load the API key from the environment variable
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("OPENAI_API_KEY environment variable not set!")

# Replace with your OpenAI API key
openai.api_key = api_key

class YLTK:
    def __init__():
        return 1
    
    # Extract all yoruba text in a word
    def extract_yoruba_words(text, max_tokens=2000, max_workers=5):
        """
        Extract Yoruba words from the given text using OpenAI GPT model in parallel batches.

        :param text: The full text to process.
        :param max_tokens: Maximum number of tokens per batch (default: 127,000).
        :param max_workers: Maximum number of parallel workers (default: 5).
        :return: Extracted Yoruba words across all batches.
        """
        # Function to split text into batches of approximately max_tokens
        def split_text_into_batches(text, max_tokens):
            words = text.split()  # Split the text into words
            batches = []
            current_batch = []
            current_tokens = 0

            for word in words:
                word_length = len(word) + 1  # Estimate token count for the word (+1 for space/punctuation)
                if current_tokens + word_length > max_tokens:
                    batches.append(" ".join(current_batch))  # Add current batch to batches
                    current_batch = []  # Reset for new batch
                    current_tokens = 0
                current_batch.append(word)
                current_tokens += word_length

            # Add the last batch if it has content
            if current_batch:
                batches.append(" ".join(current_batch))

            return batches

        # Function to process a single batch
        def process_batch(batch, batch_index, total_batches):
            prompt = f"""
            Extract all Yoruba words from the following text:
            {batch}

            Output only the Yoruba words and remove all special characters. No additional commas after each word if they were not there.
            """
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-4-turbo",  # Use gpt-3.5-turbo for a cheaper option
                    messages=[
                        {"role": "system", "content": "You are a Yoruba language expert."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0  # Ensures deterministic output
                )
                # Extract and return the content of the assistant's response
                yoruba_words = response["choices"][0]["message"]["content"].strip()
                print(f"Batch {batch_index + 1}/{total_batches} processed successfully.")
                return yoruba_words
            except Exception as e:
                print(f"Error processing batch {batch_index + 1}/{total_batches}: {e}")
                return ""  # Return an empty string for failed batches

        # Split the input text into batches
        batches = split_text_into_batches(text, max_tokens)
        total_batches = len(batches)  # Calculate the total number of batches
        print(f"Total number of batches: {total_batches}")

        yoruba_words = []

        # Use ThreadPoolExecutor for parallel processing
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit all batches to the executor
            future_to_batch = {executor.submit(process_batch, batch, i, total_batches): i for i, batch in enumerate(batches)}

            # Collect results as they are completed
            for future in as_completed(future_to_batch):
                batch_index = future_to_batch[future]
                try:
                    yoruba_words_batch = future.result()
                    yoruba_words.append(yoruba_words_batch)
                except Exception as e:
                    print(f"Error retrieving result for batch {batch_index + 1}: {e}")

        # Combine all Yoruba words from batches
        return " ".join(yoruba_words)

    
    # Getting the frequecy of words
    def word_frequency_count(text):

        # Helper function to count word frequencies for a chunk of text
        def count_words(text_chunk):
            # Preprocess the text: remove punctuation, convert to lowercase
            cleaned_text = re.sub(r'[^\w\s]', '', text_chunk).lower()

            # Split the text into words
            words = cleaned_text.split()

            # Use Counter to count occurrences of each word
            return Counter(words)

        # Split the text into smaller chunks for parallel processing
        chunk_size = len(text) // 4  # Adjust the number of chunks as needed
        chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]

        # Use ThreadPoolExecutor to process the chunks in parallel
        with ThreadPoolExecutor() as executor:
            results = list(executor.map(count_words, chunks))

        # Combine all word counts from each chunk
        total_word_counts = Counter()
        for result in results:
            total_word_counts.update(result)

        return dict(total_word_counts)

    # Generating the list of stop words
    def stop_words(file: dict):
        # Helper function to check if a word's frequency is greater than or equal to 5
        def check_word(word_item):
            word, count = word_item
            if count >= 5:
                return word
            return None

        # Get the maximum number of workers (CPU cores)
        max_workers = os.cpu_count()

        # Use ThreadPoolExecutor to process the word count items in parallel
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            results = list(executor.map(check_word, file.items()))

        # Filter out the None values (words that don't meet the condition)
        list_of_stopWords = [word for word in results if word is not None]

        return list_of_stopWords
    
    def remove_stopwords(list_a, document_b):
        """
        Removes any text in list_a from document_b and returns the remaining text in document_b.

        :param list_a: List of strings to be removed
        :param document_b: The document (string) from which the text will be removed
        :return: The remaining text in document_b as a string
        """
        # Convert document_b into a list of words
        document_b_words = document_b.split()

        # Create a set from list_a for efficient lookup
        list_a_set = set(list_a)

        # Filter words in document_b that are not in list_a
        remaining_words = [word for word in document_b_words if word not in list_a_set]

        # Join the remaining words back into a single string
        return " ".join(remaining_words)
    

