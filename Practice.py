import streamlit as st

# Function to update a member's details
def update_member(selected_member, name, age, gender, plan, contact):
    # Update member details based on the selected member
    st.session_state['members'].loc[selected_member, 'Name'] = name
    st.session_state['members'].loc[selected_member, 'Age'] = age
    st.session_state['members'].loc[selected_member, 'Gender'] = gender
    st.session_state['members'].loc[selected_member, 'Membership Plan'] = plan
    st.session_state['members'].loc[selected_member, 'Contact'] = contact
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
        gender = st.selectbox("Gender", options=['Male', 'Female', 'Other'],
                              index=['Male', 'Female', 'Other'].index(current_member['Gender']))
        plan = st.selectbox("Membership Plan", options=['Monthly', 'Quarterly', '3-Months', '6-Months', '9-Months', '12-Months'],
                            index=['Monthly', 'Quarterly', '3-Months', '6-Months', '9-Months', '12-Months'].index(current_member['Membership Plan']))
        contact = st.text_input("Contact", value=current_member['Contact'])

        # Update button
        if st.button("Update Member"):
            update_member(selected_member_index, name, age, gender, plan, contact)
    else:
        st.write("No members found to update.")
