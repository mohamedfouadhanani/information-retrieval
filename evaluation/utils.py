import numpy as np
from matplotlib import pyplot as plt

def precision_interpolation(precision_recall):
    if not precision_recall:
        return []
        
    recall_range = np.arange(start=0, stop=1.1, step=0.1)
    i_precision = []

    for r_r in recall_range:
        sublist = [precision for precision, recall in precision_recall if recall >= r_r]
        i_precision.append((r_r, max(sublist, default=0)))

    return i_precision

def recall_at(index, selected_documents, relevent_documents):
    if not relevent_documents:
        return []
    
    n_relevent_documents = len(relevent_documents)
    
    selected_documents = selected_documents[:index]
    boolean_list = [selected_document in relevent_documents for selected_document in selected_documents]

    recall = []
    for index in range(len(boolean_list)):
        element = boolean_list[index]
        sub_boolean_list = boolean_list[:index + 1]

        if not element:
            continue

        n_true_elements = sum(sub_boolean_list)
        recall.append(n_true_elements / n_relevent_documents)
    
    return recall

def precision_at(index, selected_documents, relevent_documents):
    if not relevent_documents:
        return []
    
    selected_documents = selected_documents[:index]
    boolean_list = [selected_document in relevent_documents for selected_document in selected_documents]

    precision = []
    for index in range(len(boolean_list)):
        element = boolean_list[index]
        sub_boolean_list = boolean_list[:index + 1]

        if not element:
            continue

        n_true_elements = sum(sub_boolean_list)
        precision.append(n_true_elements / len(sub_boolean_list))
    
    return precision

def precision(selected_documents, relevent_documents):
    if not relevent_documents:
        return 0
    
    boolean_list = [selected_document in relevent_documents for selected_document in selected_documents]

    precision = 0
    for index in range(len(boolean_list)):
        element = boolean_list[index]
        sub_boolean_list = boolean_list[:index + 1]

        if not element:
            continue

        n_true_elements = sum(sub_boolean_list)
        precision += n_true_elements / len(sub_boolean_list)
    
    precision /= len(relevent_documents)
    
    return precision

def recall(selected_documents, relevent_documents):
    if not relevent_documents:
        return 0

    counter = 0

    for relevent_document in relevent_documents:
        if relevent_document in selected_documents:
            counter += 1
    
    score = counter / len(relevent_documents)
    return score

def f_measure(recall, precision):
    try:
        score = 2 * precision * recall / (precision + recall)
    except:
        return 0
        
    return score

if __name__ == "__main__":
    # precision = precision_at(5, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], [1, 2, 4, 6])
    # print(precision)

    # precision = precision_at(10, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], [1, 2, 4, 6])
    # print(precision)

    precision = precision_at(14, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14], [1, 2, 4, 6, 13, 97, 98, 99])
    # print(precision)

    recall_value = recall_at(14, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14], [1, 2, 4, 6, 13, 22])
    # print(recall_value)

    precision_recall = list(zip(precision, recall_value))
    # print(precision_recall)
    
    precision = [1, 1, 0.75, 0.667, 0.38]
    recall_value = [0.167, 0.333, 0.5, 0.667, 0.833]

    precision_recall = list(zip(precision, recall_value))

    interpolated = precision_interpolation(precision_recall)
    for recall_value, precision in interpolated:
        print(f"{recall_value} = {precision}")