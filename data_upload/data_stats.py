import numpy as np
import pandas as pd

with open('data.txt', 'r') as f:
    data = f.readlines()


big = np.argmax(map(lambda x: len(x), data))
big_word = np.argmax(map(lambda x: len(x.split()), data))

biggest = data[big]
biggest_word = data[big_word].split()
print(biggest, len(biggest))
print(biggest_word, len(biggest_word))
# 95 chars, 21 words