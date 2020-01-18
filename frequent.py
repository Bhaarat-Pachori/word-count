import multiprocessing
from collections import Counter
from functools import reduce
import logging, re, itertools, os
#from memory_profiler import profile

logging.basicConfig(level=logging.DEBUG)


def count_words(data_part):
    """
    this method counts the words frequency
    :param data_part: string containing the words
    :return: returns the dictionary with frequency
    """
    counts = Counter(data_part)
    return counts


def merge_dicts(proc1_counts, proc2_counts):
    """
    this is a supporting method to merge the two
    count values.
    proc1_counts: the dictionary one with k-v pairs
    proc2_counts: the dictionary two with k-v pairs
    return: the merged dictionary
    """
    for word, count in proc2_counts.items():
        if word not in proc1_counts:
          proc1_counts[word] = 0
        proc1_counts[word] += proc2_counts[word]
    return proc1_counts


#@profile
def get_frequency(filename):
    """
    this method cleans the text, separate the words
     and use helper methods to get the counts of words
     and also merging the results from the different
     running processes.
    :param filename: the name of the file
    :return: it returns the count frequencies in sorted order
    """
    if not os.stat(filename).st_size:
        return "Empty File"
    sentences = list()
    with open(filename, 'r') as ot:
        sentences = [word.strip().lower() for word in ot.readlines() if word.strip()]

    # Regex to strip special characters from the text
    # except for the apostrophes in words
    rgx = re.compile(r"(?<!\w)\'|\'(?!\w)")

    for index, item in enumerate(sentences):
        sentences[index] = rgx.sub('', item)

    sentences = [word.split() for word in sentences]
    sentences = [item.split("_") for word in sentences for item in word]

    # flattening the list
    sentences = list(itertools.chain(*sentences))

    # Keeping the apostrophes in sentences
    sentences = [re.split(r'[^\w\']', word) for word in sentences]

    # flattening the list
    sentences = list(itertools.chain(*sentences))

    # removing None values from flattened list
    sentences = list(filter(None, sentences))

    # getting the number of processors the machine supports
    available_processors = multiprocessing.cpu_count()

    print("Total Processors: ", available_processors)

    parts = len(sentences) // available_processors

    # creating processes from pools
    pool = multiprocessing.Pool(processes=available_processors)

    # map method which takes the function as an input and the list to work
    # upon
    word_counts_per_process = pool.map(count_words, [sentences[pos: pos + parts]\
                                   for pos in range(0, len(sentences), parts)])

    # merging the dictionaries with values as frequency count from
    # different processes
    counts = reduce(merge_dicts, word_counts_per_process)

    #logging.debug(len(counts))
    #logging.debug(Counter(counts).most_common(len(counts)))
    #logging.debug(type(Counter(counts).most_common(len(counts))))
    return Counter(counts).most_common(len(counts))

#get_frequency('./test.txt')