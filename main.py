"""
File : main.py
Author : Harshal Patel
Date : 02-02-2024
"""
import sys
import numpy as np
import random

import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.tag import pos_tag

def file_check():
    """
    Checks if a specified file exists, can be read and is not empty, and returns its contents.

    Args:
        None (takes the file name as a command-line argument)

    Returns:
        str: The raw text content of the file if successful.
    """

    # Ensure the correct number of arguments is provided
    if len(sys.argv) != 2:
        print("Error!! Please pass file name as an argument")
        exit(1)

    # Attempt to open and read the file
    try:
        with open(sys.argv[1], "r") as file:
            raw_text = file.read()
            if len(raw_text) == 0:
                print("Error! file is empty please upload a non-empty file")
                exit(1)
        return raw_text
    # Handle the file not found exception
    except FileNotFoundError:
            print("File not found!")


def lexi_div(raw_text):
    """
    Calculates the lexical diversity of a given raw text.

    Args:
        raw_text (str): The raw text to analyze.

    Returns:
        list: A list of tokenized words from the text.

    Prints:
        Lexical Diversity: The calculated lexical diversity score (rounded to 2 decimal places).
    """

    # Convert all characters to lowercase for consistency
    raw_text = raw_text.lower()

    # Tokenize the text into individual words:
    tokens = word_tokenize(raw_text)

    # Calculate lexical diversity:
    unique_tokens = set(tokens)
    ratio = len(unique_tokens) / len(tokens)
    print("Lexical Diversity :", round(ratio, 2))

    return tokens


def preprocess(raw_text):
    """
    Preprocesses raw text by performing tokenization, filtering, lemmatization,
    stopword removal, part-of-speech tagging, and noun extraction.

    Args:
        raw_text (str): The raw text to be preprocessed.

    Returns:
        tuple: A tuple containing:
            - tokens (list): A list of preprocessed tokens.
            - noun_list (list): A list of nouns extracted from the text.
    """
    raw_tokens = lexi_div(raw_text)

    # Filtering out token with length less than 5 and contains character other than alphabets 
    alpha_tokens = [token for token in raw_tokens if token.isalpha() and len(token) > 5]
    
    # Load the nltk English stopwords list  
    stopWords = nltk.corpus.stopwords.words("english")

    # Removing all the stopwords
    tokens = [token for token in alpha_tokens if token not in stopWords]

    # Lemmatize tokens
    lemmatizer = WordNetLemmatizer()
    lemmas = [lemmatizer.lemmatize(token) for token in tokens]
    unique_lemmas = list(set(lemmas))

    # POS tagging
    tags_list = pos_tag(unique_lemmas)

    # Print the first 20 lemma and the respective pos tag
    for i in range(20):
        print("Lemma :", tags_list[i][0], "Tag :", tags_list[i][1])

    # Making a list of nouns using 
    noun_list = []
    for index in range(len(tags_list)):
        if tags_list[index][1] == "NN":
            noun_list.append(tags_list[index][0])
    
    print("Number of tokens :", len(tokens))
    print("Number of nouns :", len(noun_list))
    
    return tokens, noun_list


def make_dict(tokens, noun_list):
    """
    This function creates a dictionary of nouns and their frequencies in a list of tokens.

    Args:
        tokens (list): A list of tokens (words).
        noun_list (list): A list of nouns.

    Returns:
        list: A list of the 50 most common nouns in the tokens.
    """
    noun_dict = {}

    # Create a dictionary of nouns with a value of 0 for each noun.
    for noun in noun_list:
        noun_dict[noun] = 0
    
    # Increase the value of a noun in the dictionary if it appears in the tokens.
    for token in tokens:
        if token in noun_dict:
            noun_dict[token] += 1

    # Sort the noun dictionary by value in descending order.
    sorted_value_index = np.argsort(list(noun_dict.values()))[::-1]
    noun_dict = {list(noun_dict.keys())[i]: list(noun_dict.values())[i] for i in sorted_value_index}

    # Print the 50 most common nouns
    most_common_words = list(noun_dict.keys())[:50]
    print(most_common_words)

    return most_common_words


def guessing_game(most_common_words):
    """
    This function plays a word guessing game with the user.

    Args:
        most_common_words (list): A list of the most common words to choose from.
    """
    print("Let's play a word guessing game!")
    total_score = 5

    while total_score > 0:
        word = random.choice(most_common_words)

         # Create a list of letters in the word, a list of guessed letters, and a hidden word representation
        word_letters = list(word)
        guessed_letters = []
        hidden_word = ["_ " for _ in word_letters]

        while hidden_word != word_letters and total_score > 0:
            # Display the current state of the hidden word
            print(" ".join(hidden_word))

            guess = input("\nGuess a letter (or '!' to quit): ").lower()

            if guess == "!":
                print("Thanks for playing!")
                return

            # Validate the player's guess
            if len(guess) != 1 or not guess.isalpha():
                print("Invalid guess. Please enter a single letter.")
                continue
            if guess in guessed_letters:
                print("You already guessed that letter.")
                continue

            guessed_letters.append(guess)

            # Check if the guess is correct
            if guess in word_letters:
                for i in range(len(word_letters)):
                    if word_letters[i] == guess:
                        hidden_word[i] = guess
                total_score += 1
                print("Right! Score is ", total_score, "\n")
            else:
                total_score -= 1
                print("Sorry, guess again. Score is ", total_score, "\n")

        # Check if the player has solved the word or run out of points
        if hidden_word == word_letters:
            print(" ".join(hidden_word))
            print("You solved it!")
        else:
            print("Sorry, you ran out of points. The word was:", word)

        print("Current score: ", total_score)

        if total_score > 0:
            guess_again = input("Guess another word? (y/n): ").lower()
            if guess_again != "y":
                break

    print("Thanks for playing!")


def main():
    """
    This function controls the overall execution flow of the program.
    """

    # 1. Handle file processing
    raw_text = file_check()

    # 2. Preprocess text data
    tokens, noun_list = preprocess(raw_text)

    # 3. Create a dictionary of common nouns
    most_common_words = make_dict(tokens, noun_list)

    # 4. Start the word guessing game
    guessing_game(most_common_words)


if __name__ == "__main__":
    main()