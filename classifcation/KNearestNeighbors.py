import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from classes.League import attributes
from classes.League import classificationField
from classifcation.helperFunctions import csvProcessedDataReadPath


def kNearestNeighborsClassification():
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csvProcessedDataReadPath + 'processedGames.csv')

    # Select the features
    X = df[attributes]

    # Select the target
    y = df[classificationField]

    # Split the data into a training set and a test set
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Create a KNeighborsClassifier
    model = KNeighborsClassifier()

    # Train the model on the training data
    model.fit(X_train, y_train)

    # Evaluate the model on the test data
    accuracy = model.score(X_test, y_test)
    print(' KNN Accuracy:', accuracy)
