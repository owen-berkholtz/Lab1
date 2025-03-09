from collections import Counter 

import numpy as np 

  
letters = "abcdefghijklmnopqrstuvwxyz"
# Function to calculate the Index of Coincidence 

def index_of_coincidence(text): 
    N = len(text) #Length of the ciphertext
    n = 26 # count of all the letters in the English alphabet
    char_count = {char : 0 for char in letters} # Initializes a dictionary where the keys are the letters of the alphabet in order a-z and the values are their count in the ciphertext

    #Fills the dictionary 'char_count' with the count of each letter in the cihpertext
    for char in range(N):
        char_count[text[char]] +=1
    

    ic = 0 #IC value 

    #Use IC formula
    for freq in char_count.values():
        ic += freq * (freq - 1)
    ic /= (N * (N - 1))

    return ic #Return the IC

# Function to calculate the average IC for different key lengths 

def average_ic(ciphertext, max_key_length): 
    avg_ics = [] 
    for key_length in range(1, max_key_length+1): 
        ics = [] 
        for i in range(key_length): 
            nth_letters = ciphertext[i: : key_length]
            ic = index_of_coincidence(nth_letters) 
            ics.append(ic) 
        avg_ic = np.mean(ics) 
        avg_ics.append((key_length, avg_ic)) 
    return avg_ics 

def key_finder(list, keylength, i): 
    smallest_x2 = float('inf') 
    best_c = ' ' 
    N = 0 
    expected_freq = [ 

        0.08167, 0.01492, 0.02782, 0.04253, 0.12702, 0.02228, 0.02015, 

        0.06094, 0.06966, 0.00153, 0.00772, 0.04025, 0.02406, 0.06749, 

        0.07507, 0.01929, 0.00095, 0.05987, 0.06327, 0.09056, 0.02758, 

        0.00978, 0.0236, 0.0015, 0.01974, 0.00074 

    ] 
    observed_freq = [0] * 26 
    freq = [0] * 26 
    for j in range(i, len(list), keylength):
        freq[ord(list[j]) - ord('a')] += 1 
    N = sum(freq) 
    for j in range(26): 
        observed_freq[j] = freq[j] / N 
    for j in range(26): 
        x2 = 0 
        for k in range(26): 
             x2 += ((observed_freq[(j + k) % 26] - expected_freq[k]) ** 2) / expected_freq[k] 
        if x2 < smallest_x2: 
            smallest_x2 = x2 
            best_c = chr(ord('a') + j) 
    return best_c 


#Task 2: step 1
#ciphertext 
ciphertext = "usojlbxpkieoiqmwucdyiaxamvknplbeaxcfjmvsjmvsfzblxstgrbbmfxgwyvhjgkamvknpaxacjbachvqnvkmggrqztwfnmxgljglrwquuelgclaqlbaypgqcnkivikfagrtbaaswmrkmmjwvbrbfyqvgmltmgfypulbamjmbyuqgdgvoukqhlvmuwcwlsjivbvnmmxstxrutewxqbrzwusvgmfnmusvgiiltrseuqvteykjtidbacvmullxmggrqldqlbavgwkqhlgjvbvaxpnmeyjbacqttimqwc" 

# Calculate and display the average IC for key lengths up to 10 (you can adjust this value) 
max_key_length = 10 
avg_ics = average_ic(ciphertext, max_key_length) 
# Print the average ICs for each key length 
for key_length, ic in avg_ics: 
    print(f"Key Length: {key_length}, Average IC: {ic:.4f}") 
# Identify the key length with the IC closest to the expected IC for the language (0.065 for English) 
expected_ic = 0.065 
closest_key_length = min(avg_ics, key=lambda x: abs(x[1] - expected_ic))[0] 
print(f"\nClosest key length to expected IC is: {closest_key_length}")

#Task 2: step 2
key = ''
for i in range(closest_key_length):
    key += key_finder(ciphertext, closest_key_length, i)
print(key)


def decrypt(ciphertext, key):
    plaintext = '' # Where the final plaintext will be stored

    #Loop through both the key and the ciphertext
    for key_i, char in enumerate(ciphertext):
        cur_key_val = key[key_i % len(key)] #Get the current character in the key

        shift_amt = ord(cur_key_val) - ord('a') #Get the integer amount to shift the ciphertext by.

        decrypted_char = (ord(char) - ord('a') - shift_amt + 26) # Shift the current character by shift_amt

        plaintext += chr(decrypted_char  % 26 + ord('a')) # Add the character to the plaintext

    return plaintext #Return plaintext

# Now test the decryption
print("Decrypted Message:", decrypt(ciphertext, key))



print("Decrypted Message:",decrypt(ciphertext, key))