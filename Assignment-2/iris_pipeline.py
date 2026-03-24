import kfp
from kfp import dsl
from typing import NamedTuple, List

@dsl.component(base_image="python:3.9-slim", packages_to_install=["pandas","scikit-learn"])
def load_data() -> NamedTuple("Outputs",[("features",List[List[float]]),("labels",List[int])]):
    from sklearn.datasets import load_iris
    iris = load_iris()
    return (iris.data.tolist(), iris.target.tolist())

@dsl.component(base_image="python:3.9-slim", packages_to_install=["scikit-learn"])
def train_model(features: List[List[float]], labels: List[int]) -> NamedTuple("Output",[("accuracy",float)]):
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import accuracy_score

    X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.2)
    clf = RandomForestClassifier()
    clf.fit(X_train, y_train)
    acc = accuracy_score(y_test, clf.predict(X_test))
    print(f"Accuracy: {acc}")
    return (acc,)

@dsl.pipeline(name="iris-pipeline")
def iris_pipeline():
    data = load_data()
    train_model(features=data.outputs["features"], labels=data.outputs["labels"])

if __name__ == "__main__":
    kfp.compiler.Compiler().compile(iris_pipeline, "iris_pipeline.yaml")