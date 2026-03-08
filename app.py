import streamlit as st
import pandas as pd
import pickle

st.set_page_config(page_title="Car Price Predictor", page_icon="🚗", layout="centered")

# load model
model = pickle.load(open("LinearRegressionModel.pkl","rb"))

st.title("🚗 Car Price Prediction")
st.write("Predict the resale value of your car")

# get categories from model
encoder = model.named_steps['columntransformer'].named_transformers_['onehotencoder']

car_models = list(encoder.categories_[0])
companies = list(encoder.categories_[1])
fuels = list(encoder.categories_[2])

# create simple mapping company -> models
car_company_map = {}

for car in car_models:
    for comp in companies:
        if comp.lower() in car.lower():
            car_company_map.setdefault(comp, []).append(car)

# 1️⃣ select company first
company = st.selectbox("Select Car Company", companies)

# 2️⃣ models based on company
models = car_company_map.get(company, car_models)

name = st.selectbox("Select Car Model", models)

# other inputs
year = st.selectbox("Select Year of Purchase", list(range(2000,2025)))

kms = st.number_input("Enter Kilometers Driven", 0, 500000)

fuel = st.selectbox("Select Fuel Type", fuels)

# prediction
if st.button("Predict Price"):

    input_df = pd.DataFrame({
        "name":[name],
        "company":[company],
        "year":[year],
        "kms_driven":[kms],
        "fuel_type":[fuel]
    })

    prediction = model.predict(input_df)

    st.success(f"Predicted Price: ₹ {round(prediction[0],2)}")