import concurrent.futures
from YLTK import YLTK

def process_1(data_batch):
    return YLTK.extract_yoruba_words(data_batch)

def process_2(word_batch):
    return YLTK.word_frequency_count(word_batch)

def process_3(word_count_batch):
    return YLTK.stop_words(word_count_batch)

def pipeline(data):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_1 = executor.submit(process_1, data)
        result_1 = future_1.result()  # Get the result of process 1
        future_2 = executor.submit(process_2, result_1)  # Process 2 starts as soon as process 1 is done
        result_2 = future_2.result()  # Get the result of process 2
        future_3 = executor.submit(process_3, result_2)  # Process 3 starts as soon as process 2 is done
        result_3 = future_3.result()  # Get the final result
        
    # Write the list to a text file
    with open('stop_words.txt', 'w', encoding='utf-8') as file:
        file.write(str(result_3))  # Converts the list to a string and writes it to the file
        

        
    return 'Processes successful!'