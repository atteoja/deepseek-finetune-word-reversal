import numpy as np
import argparse
import os
import json

CHARACTERS = "abcdefghijklmnopqrstuvwxyz"

TEMPLATE_INPUT = "Reverse the word '{}'"

TEMPLATE_THINK = "To reverse the word '{}', let's split it into individual characters {}." \
"\n\nNow, let's reverse these characters to get {}. Join each character to produce the reversed word '{}'."

TEMPLATE_FINAL = "The reverse word is '{}'."

def augment_word(word):
    """
    Randomly repeats a small part of a word.
    """

    word_len = len(word)

    # repeat words of length 1
    if word_len == 1:
        return word + word

    n_len = np.random.randint(1, word_len)
    
    i = np.random.randint(0, word_len - n_len)
    part = word[i:i+n_len]

    word = word[:i] + part + word[i:]

    return word

def combine_words(base_word, words):
    """
    Combines two random words to create a compound word.
    """

    word_count = len(words)
    word_2 = words[np.random.randint(0, word_count)]

    return base_word + word_2

def generate_samples(words,
                     characters,
                     num_samples,
                     max_length=45,
                     random_sequence_probability=0.01,
                     augment_probability=0.05,
                     combine_probability=0.05):
    """
    Generates the data samples.
    """

    word_count = len(words)

    samples = []

    for i in range(num_samples):

        sequence_characters = []

        # probability to generate random sequence
        p = np.random.rand(1) if i < word_count else 0.5

        if p < random_sequence_probability:
            sequence_length = np.random.randint(2, max_length)
            sequence_characters = np.random.choice(characters, (sequence_length))

        else:
            # take word by index, or randomly select if iteration exceeds word count
            word = words[i] if i < word_count else words[np.random.randint(0, word_count)]

            # probability to combine the selected base word with another random word
            p = np.random.rand(1) if i < word_count else 0.0

            if p < combine_probability:
                word = combine_words(word, words)

            # probability to augment the word with random repetition
            p = np.random.rand(1) if i < word_count else 0.0

            if p < augment_probability:
                word = augment_word(word)

            sequence_characters = list(word)

        # append sample to dataset
        sequence_string = "".join(sequence_characters)

        sample_x = TEMPLATE_INPUT.format(sequence_string)
        sample_t = TEMPLATE_THINK.format(sequence_string,
                                         list(sequence_string),
                                         list(sequence_string[::-1]),
                                         sequence_string[::-1])
        sample_y = TEMPLATE_FINAL.format(sequence_string[::-1])

        samples.append((sample_x, sample_t, sample_y))

    return samples

def write_dataset(samples, output_path):
    samples_dict = {"data":[]}

    for x, t, y in samples:
        sample = {
            "input":x,
            "think":t,
            "final":y
        }
        samples_dict["data"].append(sample)
    
    with open(output_path, "w") as f:
        f.write(json.dumps(samples_dict, indent=2, ensure_ascii=False))


def main(args):

    # set random seed
    np.random.seed(42)

    # read all arguments
    sample_count = args.num_samples
    max_length = args.max_length
    words_path = args.words_path
    random_sequence_probability = args.random_sequence_probability
    augment_probability = args.augment_probability
    combine_probability = args.combine_probability

    words = []
    with open(words_path, "r") as f:
        for word in f:
            words.append(word.strip())
    
    np.random.shuffle(words)

    characters = np.array(list(CHARACTERS))

    # generate all samples
    samples = generate_samples(
        words,
        characters,
        sample_count,
        max_length,
        random_sequence_probability,
        augment_probability=augment_probability,
        combine_probability=combine_probability
    )

    # write the dataset as .json to the output path
    write_dataset(samples, output_path=args.output_path)



if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--num_samples', '-n', default=10000, type=int)
    parser.add_argument('--max_length', '-ml', default=45, type=int)
    parser.add_argument('--words_path', '-wp', default="data/words.txt", type=str)
    parser.add_argument('--random_sequence_probability', '-rp', default=0.01, type=float)
    parser.add_argument('--augment_probability', '-ap', default=0.05, type=float)
    parser.add_argument('--combine_probability', '-cp', default=0.05, type=float)
    parser.add_argument('--output_path', "-op", default="data/reverse_dataset.json")
    args = parser.parse_args()
    
    main(args)