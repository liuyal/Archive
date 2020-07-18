import os
import time
import sys
import stat
import shutil
import csv
import copy
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import metrics
from sklearn.cluster import KMeans


def delete_folder(path):
    for root, dirs, files in os.walk(path):
        for dir in dirs:
            os.chmod(os.path.join(root, dir), stat.S_IRWXU)
        for file in files:
            os.chmod(os.path.join(root, file), stat.S_IRWXU)
    shutil.rmtree(path, ignore_errors=True)


def load_csv_data(file_path):
    data_output = []
    file = open(file_path, "r+", encoding="utf-8")
    data = csv.reader(file)
    for row in data: data_output.append(row)
    file.close()
    header = data_output.pop(0)
    return header, data_output


# _kmeans.py line 435
def calculate_k_means_Q1(training_data_frame):
    print("Q1")
    copy_frame = copy.deepcopy(training_data_frame)
    df = copy_frame.drop(training_data_frame.columns[0], axis=1)
    kmeans = KMeans(n_init=1, n_clusters=10, max_iter=100, verbose=True)
    cluster = kmeans.fit(df)


def calculate_k_means_Q2(training_data_frame):
    print("\nQ2")
    k_range = [2, 5, 10, 20]
    copy_frame = copy.deepcopy(training_data_frame)
    df = copy_frame.drop(training_data_frame.columns[0], axis=1)
    for k in k_range:
        print("\n****************** Number of Clusters: " + str(k) + " ******************")
        kmeans = KMeans(n_init=10, n_clusters=k, max_iter=100, verbose=True)
        cluster = kmeans.fit(df)


def calculate_k_means_Q3(training_data_frame):
    print("\nQ3")

    k_range = [10, 20, 30, 50]
    copy_frame = copy.deepcopy(training_data_frame)
    df = copy_frame.drop(training_data_frame.columns[0], axis=1)

    for k in k_range:
        print("\n****************** Number of Clusters: " + str(k) + " ******************")
        kmeans = KMeans(n_init=10, n_clusters=k, max_iter=100, verbose=True)
        cluster = kmeans.fit(df)

    return 0


def calculate_k_means_Q4(training_data_frame):
    print("\nQ4")
    return 0


def find_min_sse(folder_path):
    for file in os.listdir(folder_path):
        if "Q2" in file:
            f = open(folder_path + os.sep + file, "r")
            text = f.readlines()
            f.close()

            values = []

            print(file)

            for i in range(0, len(text)):
                if "Converged at" in text[i]:
                    values.append(float(text[i - 1].replace('\n', '').split(' ')[-1]))
                    print(text[i - 1].replace('\n', ''))
            print("Min: ", min(values))


if __name__ == "__main__":
    training_header, training_data = load_csv_data(os.getcwd() + os.sep + "training.csv")
    test_header, test_data = load_csv_data(os.getcwd() + os.sep + "testing.csv")

    training_data_frame = pd.DataFrame(training_data, columns=training_header)
    test_data_frame = pd.DataFrame(test_data, columns=test_header)

    # calculate_k_means_Q1(training_data_frame)
    # calculate_k_means_Q2(training_data_frame)
    # calculate_k_means_Q3(training_data_frame)
    # calculate_k_means_Q4(training_data_frame)

    find_min_sse(os.getcwd() + os.sep + "results")