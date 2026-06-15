import pandas as pd
import pickle

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error

data=pd.read_csv("data/destination.csv")

features=[
    
    "Type",
    "Entrance Fee in INR",
    "time needed to visit in hrs",
    "DSLR Allowed",
    "Best Time to visit"
]

target="Google review rating"

X=data[features]
y=data[target]

categorical_features=["Type", "DSLR Allowed", "Best Time to visit"]
numerical_features=["Entrance Fee in INR", "time needed to visit in hrs"]

preprocessor=ColumnTransformer(
    transformers=[
        ("num", "passthrough", numerical_features),
        ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features)
    ] 
)

model=Pipeline([
    ("preprocessor", preprocessor),
    ("regressor", RandomForestRegressor(n_estimators=100, random_state=42))         
])

X_train, X_test, y_train, y_test=train_test_split(X, y, test_size=0.2, random_state=42)
model.fit(X_train, y_train)

predictions=model.predict(X_test)
mae=mean_absolute_error(y_test, predictions)
print(f"Mean Absolute Error: {mae}")
with open("travique_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("Model Saved!")