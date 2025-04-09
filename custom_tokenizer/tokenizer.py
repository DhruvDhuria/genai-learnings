# Tokenizer

char = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z','a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

tokens = {}

for i in range(len(char)):
    tokens[char[i]] = ((i + 1) * 2) + i

# print(tokens)

input_text = input("Provide some text to convert into tokens: ")

tokenized_sentance = []

if isinstance(input_text, str):
    splitted_text = input_text.split()
    divided_text = list(splitted_text)

    for text in divided_text:
        tokenized_text = 0
        for char in text:
            tokenized_text += tokens[char]
        tokenized_sentance += [tokenized_text]


print(tokenized_sentance)
