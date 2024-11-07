import streamlit as st
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta
import plotly.express as px

# Page configuration
st.set_page_config(page_title="Gym Membership Management", page_icon="🏋️", layout="centered")
# Title
st.title("Gym Membership Management System")
st.write("Manage your gym members' details easily.")
# Sample member data (in a real application, this would be connected to a database)
if 'members' not in st.session_state:
    st.session_state['members'] = pd.DataFrame(columns=['Name', 'Age', 'Gender',
'Membership Plan','Membership activation date', 'Height',"Weight",'Plan commencement date','Membership expiry date','Contact'])
# Function to add a new member
def add_member(name, age, gender, plan, height, weight, contact):
    new_member = pd.DataFrame([{
        'Name': name,
        'Age': age,
        'Gender': gender,
        'Membership Plan': plan,
        'Membership activation date': datetime.now().strftime('%d %B %Y'),
        'Height': height,
        "Weight": weight,
        'Plan commencement date': datetime.now().strftime('%d %B %Y'),
        'Membership expiry date': formatted_expiry_date,
        'Contact': contact}])
    # Concatenate the new member row to the existing DataFrame
    st.session_state['members'] = pd.concat([st.session_state['members'], new_member], ignore_index=True)
    st.success("Member added successfully!")
# Sidebar for navigation
page = st.sidebar.radio("Navigation", ["Home", "Add Member", "View Members", "Update Member",  "Calorie Check"])

if page == "Home":
    # st.header("Welcome to the Classic Fitness Membership Management System")
    st.markdown("<h1 style='color:red;'>Welcome to the Classic Fitness Membership Management System</h1>",unsafe_allow_html=True)
elif page == "Add Member":
    st.header("Add New Member")

    with st.form(key='add_member_form'):
        name = st.text_input("Name")
        age = st.number_input("Age", min_value=10, max_value=100, value=25)
        gender = st.selectbox("Gender", ["Male", "Female"])
        plan = st.selectbox("Membership Plan", ["Monthly", "3-Months", "6-Months", "9-Months", "12-Months"])
        height = st.number_input("Height(in Cm)", min_value=10, value=160)
        weight = st.number_input("Weight(in Kg)", min_value=10, value=60)
        contact = st.text_input("Contact Number")
        # submit button
        submit_button = st.form_submit_button("Add Member")

        if plan == "Monthly":
            expiry_date = datetime.now() + relativedelta(months=1)
        elif plan == "3-Months":
            expiry_date = datetime.now() + relativedelta(months=3)
        elif plan == "6-Months":
            expiry_date = datetime.now() + relativedelta(months=6)
        elif plan == "9-Months":
            expiry_date = datetime.now() + relativedelta(months=9)
        elif plan == "12-Months":
            expiry_date = datetime.now() + relativedelta(months=12)

        # Format the expiry date
        formatted_expiry_date = expiry_date.strftime('%d %B %Y')
        if submit_button:
            if name:
                add_member(name, age, gender, plan,height, weight, contact)
            else:
                st.error("Please fill out all required fields.")

elif page == "View Members":
    st.header("Member List")
    if not st.session_state['members'].empty:
        st.dataframe(st.session_state['members'])
        selected_member_name = st.selectbox("Select Member to Delete", st.session_state['members']['Name'].tolist())
        # Add a button to delete the selected member
        if st.button("Delete Selected Member"):
            st.session_state['members'] = st.session_state['members'][
                st.session_state['members']['Name'] != selected_member_name]
            st.write(f"Member '{selected_member_name}' has been deleted.")
    else:
        st.write("No members available. Please add members.")

def update_member(selected_member, name, age, gender, plan, height, weight,commencement, expiry, contact):
    # Update member details based on the selected member
    st.session_state['members'].loc[selected_member, 'Name'] = name
    st.session_state['members'].loc[selected_member, 'Age'] = age
    st.session_state['members'].loc[selected_member, 'Gender'] = gender
    st.session_state['members'].loc[selected_member, 'Membership Plan'] = plan
    st.session_state['members'].loc[selected_member, 'Height'] = height
    st.session_state['members'].loc[selected_member, 'Weight'] = weight
    st.session_state['members'].loc[selected_member, 'Plan commencement date'] = commencement
    st.session_state['members'].loc[selected_member, 'Contact'] = contact
    st.session_state['members'].loc[selected_member, 'Membership expiry date'] = formatted_expiry_date
    st.success("Member details updated successfully!")

# Update Member page
if page == "Update Member":
    st.header("Update Member Details")
    # Select a member to update
    member_names = st.session_state['members']['Name'].tolist()
    if member_names:
        selected_member_name = st.selectbox("Select Member to Update", member_names)

        # Get the selected member's index
        selected_member_index = \
            st.session_state['members'][st.session_state['members']['Name'] == selected_member_name].index[0]

        # Get current details of the selected member
        current_member = st.session_state['members'].iloc[selected_member_index]

        # Create input fields for the details
        name = st.text_input("Name", value=current_member['Name'])
        age = st.number_input("Age", value=current_member['Age'], min_value=0)
        gender = st.selectbox("Gender", options=['Male', 'Female'],
                              index=['Male', 'Female', 'Other'].index(current_member['Gender']))
        plan = st.selectbox("Membership Plan",options=['Monthly', '3-Months', '6-Months', '9-Months', '12-Months'],
                            index=['Monthly', '3-Months', '6-Months', '9-Months', '12-Months'].index(current_member['Membership Plan']))
        height = st.text_input("Height", value=current_member['Height'])
        weight = st.text_input("Weight", value=current_member['Weight'])
        commencement = st.date_input("Plan commencement date").strftime('%d %B %Y')
        contact = st.text_input("Contact", value=current_member['Contact'])
        if plan == "Monthly":
            expiry_date = datetime.now() + relativedelta(months=1)
        elif plan == "3-Months":
            expiry_date = datetime.now() + relativedelta(months=3)
        elif plan == "6-Months":
            expiry_date = datetime.now() + relativedelta(months=6)
        elif plan == "9-Months":
            expiry_date = datetime.now() + relativedelta(months=9)
        elif plan == "12-Months":
            expiry_date = datetime.now() + relativedelta(months=12)
        formatted_expiry_date = expiry_date.strftime('%d %B %Y')
        expiry=formatted_expiry_date
        # Update button
        if st.button("Update Member"):
            update_member(selected_member_index, name, age, gender, plan, height, weight, commencement,expiry, contact)
    else:
        st.write("No members found to update.")


def calculate_maintenance_calories(selected_member_name, age, gender, height, weight, activity_level):
    # Height and weight are already assumed to be in correct units (cm and kg)
    if selected_member_name:
        # Update the session state DataFrame for the selected member
        st.session_state['members'].loc[st.session_state['members']['Name'] == selected_member_name, 'Age'] = age
        st.session_state['members'].loc[st.session_state['members']['Name'] == selected_member_name, 'Gender'] = gender
        st.session_state['members'].loc[st.session_state['members']['Name'] == selected_member_name, 'Height'] = height
        st.session_state['members'].loc[st.session_state['members']['Name'] == selected_member_name, 'Weight'] = weight
    age = int(age)
    height = float(height)
    weight = float(weight)
    # Calculate BMR
    if gender == 'Male':
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    else:
        bmr = 10 * weight + 6.25 * height - 5 * age - 161

    # Determine TDEE based on activity level
    activity_factors = {
        "Sedentary": 1.2,
        "Lightly active": 1.375,
        "Moderately active": 1.55,
        "Very active": 1.725,
        "Super active": 1.9
    }
    tdee = bmr * activity_factors[activity_level]
    return tdee


if page == "Calorie Check":
    if 'members' not in st.session_state or st.session_state['members'].empty:
        st.write("Please add a member to check their TDEE.")
    else:
        member_names = st.session_state['members']['Name'].tolist()
        if member_names:
            selected_member_name = st.selectbox("Select Member to Check", member_names)
            if selected_member_name:
                # Retrieve the member's details from the DataFrame
                member_data = st.session_state['members'].loc[st.session_state['members']['Name'] == selected_member_name]
                if not member_data.empty:
                    age = member_data['Age'].values[0]
                    gender = member_data['Gender'].values[0]
                    height = member_data['Height'].values[0]
                    weight = member_data['Weight'].values[0]

                    # Display the details and allow input for activity level
                    st.write(f"**Age**: {age}")
                    st.write(f"**Gender**: {gender}")
                    st.write(f"**Height (cm)**: {height}")
                    st.write(f"**Weight (kg)**: {weight}")

                    # Input for activity level
                    activity_level = st.selectbox("Activity Level",
                                                  ["Sedentary", "Lightly active", "Moderately active", "Very active",
                                                   "Super active"])

                    if st.button("**Check TDEE**"):
                        # Calculate TDEE only if selected_member_name is not None
                        tdee = calculate_maintenance_calories(selected_member_name, age, gender, height, weight,
                                                              activity_level)
                        st.write(
                            f"Total Daily Energy Expenditure (TDEE) for {selected_member_name}: {tdee:.2f} calories/day")
                else:
                    st.write("No data available for the selected member.")
            else:
                st.write("Please select a member to check their TDEE.")
        else:
            st.write("No members found. Please add a member to check their TDEE.")


        def calculate_macros(tdee, weight_kg, goal):
            tdee = float(tdee)
            weight_kg = float(weight_kg)
            # Protein intake: 2.0 grams per kg for cutting, 2.2 grams for bulking, and 1.8 grams for maintenance
            protein_per_kg = {
                "cutting": 2.0,
                "bulking": 2.2,
                "maintenance": 1.8
            }
            protein_grams = protein_per_kg[goal] * weight_kg
            protein_calories = protein_grams * 4  # 4 calories per gram of protein

            # Fat intake: 25% of total daily calories for maintenance, lower for cutting (20%) and higher for bulking (30%)
            fat_percentage = {
                "cutting": 0.20,
                "bulking": 0.30,
                "maintenance": 0.25
            }
            fat_calories = tdee * fat_percentage[goal]
            fat_grams = fat_calories / 9  # 9 calories per gram of fat

            # Calculate carb intake with remaining calories
            carb_calories = tdee - (protein_calories + fat_calories)
            carb_grams = carb_calories / 4  # 4 calories per gram of carbs

            # Fiber intake: 14 grams per 1,000 calories
            fiber_grams = (tdee / 1000) * 14

            return {
                "Protein (grams)": protein_grams,
                "Fat (grams)": fat_grams,
                "Carbs (grams)": carb_grams,
                "Fiber (grams)": fiber_grams
            }


        tdee = calculate_maintenance_calories(selected_member_name, age, gender, height, weight, activity_level)
        # st.write(f"Total Daily Energy Expenditure (TDEE) for {selected_member_name}: {tdee:.2f} calories/day")

        goal = st.selectbox("**Select Goal**", ["maintenance", "cutting", "bulking"])
        st.write(f"Calculating macros for goal: {goal}")
        macros = calculate_macros(tdee, weight, goal)

        # Display macro results
        # for macro, value in macros.items():
        #     st.write(f"{macro}: {value:.2f} grams")
        macro_df = pd.DataFrame.from_dict(macros, orient='index', columns=['Grams'])
        st.markdown("### Macronutrient Breakdown")
        st.table(macro_df)
        fig = px.pie(values=[macros['Protein (grams)'], macros['Fat (grams)'], macros['Carbs (grams)']],
                     names=['Protein', 'Fat', 'Carbs'],title='Macronutrient Breakdown',color_discrete_sequence=['red', 'blue', 'green'])
        st.plotly_chart(fig)
st.sidebar.write("**Contact Support:** Phone number: +91 9080973308")
# streamlit run C:\Users\MM34\PycharmProjects\pythonProject\Practice.py
