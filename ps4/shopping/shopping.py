import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    
    # empty lists we'll add to
    evidence = []
    labels = []
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'June', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    month_num = enumerate(months) # pair months with ints 0-11
    month = {key: value for value, key in month_num} # swap the key-value pairs so month is key and int is value
    
    with open(filename, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            current_evidence = []
            
            # append to current_evidence
            current_evidence.append(int(row["Administrative"]))
            current_evidence.append(float(row["Administrative_Duration"]))
            current_evidence.append(int(row["Informational"]))
            current_evidence.append(float(row["Informational_Duration"]))
            current_evidence.append(int(row["ProductRelated"]))
            current_evidence.append(float(row["ProductRelated_Duration"]))
            current_evidence.append(float(row["BounceRates"]))
            current_evidence.append(float(row["ExitRates"]))
            current_evidence.append(float(row["PageValues"]))
            current_evidence.append(float(row["SpecialDay"]))
            current_evidence.append(int(month[row["Month"]]))
            current_evidence.append(int(row["OperatingSystems"]))
            current_evidence.append(int(row["Browser"]))
            current_evidence.append(int(row["Region"]))
            current_evidence.append(int(row["TrafficType"]))
            current_evidence.append(int(row["VisitorType"] == 'Returning_Visitor'))
            current_evidence.append(int(row["Weekend"] == 'TRUE'))
            
            # append this to the overarching evidence list
            evidence.append(current_evidence)
            # add last column: revenue to labels
            labels.append(row["Revenue"])
            
        return evidence, labels
    

def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """

    model = KNeighborsClassifier(n_neighbors=1) # knn where n = 1
    
    model.fit(evidence, labels)
    
    return model
    

def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """

    # initialize counter vars
    positive_correct_guesses = 0
    negative_correct_guesses = 0
    positive_total = 0
    negative_total = 0
    
    size = len(labels)

    for guess in range(size):
        if labels[guess] == 1:
            positive_total += 1
            if predictions[guess] == 1:
                positive_correct_guesses += 1
        elif labels[guess] == 0:
            negative_total += 1
            if predictions[guess] == 0:
                negative_correct_guesses += 1
            
    sensitivity = positive_correct_guesses / positive_total
    specificity = negative_correct_guesses / negative_total
    
    return sensitivity, specificity
        

if __name__ == "__main__":
    main()
