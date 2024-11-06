import streamlit as st
import pickle

# Load the trained model
with open("C:\\Users\\DELL\\PycharmProjects\\pythonProject\\Streamlit\\Fake_news.pickle", "rb") as f:
    model = pickle.load(f)

# Load the vectorizer
with open("C:\\Users\\DELL\\PycharmProjects\\pythonProject\\Streamlit\\vectorizer.pickle", "rb") as f:
    vectorizer = pickle.load(f)

# Streamlit layout
st.set_page_config(page_title="Fake News Prediction", page_icon="⚠", layout="centered")
st.title("Fake News Prediction App")
st.write("Enter text below to predict if it is fake or true.")

# User input
input_string = st.text_area("Enter the text here")

if st.button("Predict"):
    if input_string:
        # Transform the input text using the vectorizer
        input_transformed = vectorizer.transform([input_string])

        # Predict using the model
        prediction = model.predict(input_transformed)

        # Display the prediction
        if prediction[0] == '1':
            st.warning("The text is fake.")
        else:
            st.success("The text is true.")
    else:
        st.error("Please enter some text before making a prediction.")



# streamlit run C:\Users\DELL\PycharmProjects\pythonProject\Streamlit\Fake_News.py