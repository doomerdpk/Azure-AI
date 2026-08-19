import argparse
import os

import mlflow
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import root_mean_squared_error
from sklearn.model_selection import train_test_split


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=str, required=True)
    parser.add_argument("--model_output", type=str, required=True)
    args = parser.parse_args()

    mlflow.sklearn.autolog()

    df = pd.read_csv(args.data)
    X = df.drop(columns=["target"])
    y = df["target"]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = LinearRegression()
    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    rmse = root_mean_squared_error(y_test, preds)
    print(f"Test RMSE: {rmse:.2f}")

    os.makedirs(args.model_output, exist_ok=True)
    mlflow.sklearn.save_model(model, args.model_output)


if __name__ == "__main__":
    main()