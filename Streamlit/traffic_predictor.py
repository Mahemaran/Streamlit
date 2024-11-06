import streamlit as st
import numpy as np
import pickle

# Load the trained model
with open("C:\\Users\\DELL\\PycharmProjects\\pythonProject\\Streamlit\\Traffic_prediction.pickle", 'rb') as f:
    model = pickle.load(f)

# Streamlit app layout
st.set_page_config(page_title="Traffic Prediction", page_icon="🚦", layout="centered")
st.title("Traffic Prediction App")
st.write("Enter the input features below to predict whether the traffic is low or high.")

# Collect user input for the counts
car_count = st.number_input("**Car Count**", min_value=0, value=100)
bike_count = st.number_input("**Bike Count**", min_value=0, value=100)
bus_count = st.number_input("**Bus Count**", min_value=0, value=100)
truck_count = st.number_input("**Truck Count**", min_value=0, value=100)

# Calculate the total
total_count = car_count + bike_count + bus_count + truck_count

# Display the total count
st.write(f"**Total Count**: {total_count}")

# Convert input features to numpy array and reshape
input_features = np.array([car_count, bike_count, bus_count, truck_count, total_count]).reshape(1, -1)

# Make prediction when the button is clicked
if st.button("Predict Traffic Level"):
    prediction = model.predict(input_features)

    # Display prediction result
    if prediction[0] == 0:
        st.warning("Prediction: Heavy Traffic")
    elif prediction[0] == 1:
        st.warning("Prediction: High Traffic")
    elif prediction[0] == 2:
        st.success("Prediction: Low Traffic")
    else:
        st.success("Prediction: Normal Traffic")


# streamlit run C:\Users\DELL\PycharmProjects\pythonProject\Streamlit\traffic_predictor.py