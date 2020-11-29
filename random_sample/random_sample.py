import os
import random
import math


# path to the folder with text files
# pdfs_path = os.getcwd() + '/pdfs/'
# file_list = os.listdir(pdfs_path)

# dictionary with sorted text files
# files = {
#     "A_files_list": [i for i in file_list if "A" in i],
#     "B_files_list": [i for i in file_list if "B" in i],
#     "C_files_list": [i for i in file_list if "C" in i],
#     "D_files_list": [i for i in file_list if "D" in i],
#     "E_files_list": [i for i in file_list if "E" in i]}

files = {
    "A": ["A%d" % i for i in range(1090)],
    "B": ["B%d" % i for i in range(400)],
    "C": ["C%d" % i for i in range(11)],
    "D": ["D%d" % i for i in range(7)],
    "E": ["E%d" % i for i in range(5)],
}

# sample file number
SAMPLE_SIZE = 50

# dictionary with the number of files for each type of document
totals = {k: len(files[k]) for k in files}

# tuple with the number of files sorted for each type of document
sorted_files = sorted(totals.items(), key=lambda x: x[1])

# dictionary to store the count of occurrences for each type of file
groups = {}

# average number of selected files for each type of document
avg = SAMPLE_SIZE / len(files)

# variable with the current sample size
total_selected = 0

# loop for file types whose number is less than the starting average.
# When there are more, the starting average is added.
# The total_selected variable is updated.
for k, v in sorted_files:
    if v < avg:
        groups[k] = v
    else:
        groups[k] = avg
    total_selected += groups[k]

# file types with more than average amount + sorted
candidates = {k: len(v) for k, v in files.items() if len(v) > avg}
sorted_candidates = sorted(candidates.items(), key=lambda x: x[1])

# the amount by which to increase avg
add_to_avg = int((SAMPLE_SIZE - total_selected) / (len(candidates) or 1))

# the types of files that have already been selected
selected_keys = set(files) - set(candidates)

# file types that have already been selected along with the quantity
selected = {k: len(files[k]) for k in selected_keys}

for k, v in sorted_candidates:
    # loop for file types whose number is less than the new average.
    # The add_to_avg variable is updated.
    if v <= avg + add_to_avg:
        groups[k] = v
        selected[k] = v

        add_to_avg = int(math.ceil((SAMPLE_SIZE - sum(groups.values())) / (
            (len(files) - len(selected)) or 1)
        ))

    else:
        # if the total number of files is above the maximum then subtract
        if (sum(selected.values()) + (avg + add_to_avg)) > SAMPLE_SIZE:
            total_files = sum(selected.values()) + (avg + add_to_avg)
            diff = total_files % SAMPLE_SIZE
            max_to_select = avg + add_to_avg - diff
            selected[k] = max_to_select
            groups[k] = max_to_select
        else:
            selected[k] = avg + add_to_avg
            groups[k] = avg + add_to_avg

# randomize the selected number of files
for c, n in selected.items():
    print(sorted(random.sample(files[c], int(n))))
