import streamlit as st
from PIL import Image
import time

# Configuring the Page
st.set_page_config(page_title="Classic fitness", page_icon="💪", layout="centered")

# Sidebar Menu
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Trainer Profiles", "Membership Plans", "Contact & Feedback"])

# Load Images for Slideshow
gym_photos = [
    "C:\\Users\\DELL\\Downloads\\gym.jpg",  # Add paths to your images
    "C:\\Users\\DELL\\Downloads\\gym1.jpg",
    "C:\\Users\\DELL\\Downloads\\gym2.jpg",
    "C:\\Users\\DELL\\Downloads\\gym3.jpg"
]

# Home Page
if page == "Home":
    st.markdown("""
        <style>.title-style { font-size: 48px; color: #DC143C; text-align: left; font-weight: bold; font-family: 'Arial',sans-serif; margin-bottom: 20px;}
        </style>
        <div class="title-style">Welcome to Classic Fitness!</div>
        """,unsafe_allow_html=True)

    st.write("Achieve your fitness goals with our state-of-the-art facility and dedicated trainers.")
    st.write(
        "We offer personalized training programs, modern equipment, and a motivating environment for all fitness levels.")
    st.header("Become the strongest version of yourself")

    # Slideshow
    img_container = st.empty()
    # while True:
    for img_path in gym_photos:
        img = Image.open(img_path)
        img_container.image(img, use_column_width=True)
        time.sleep(2)

# Trainer Profiles
elif page == "Trainer Profiles":
    # st.title("Meet Our Trainers")
    st.markdown("""
            <style>.title-style { font-size: 48px; color: #DC143C; text-align: left; font-weight: bold; font-family: 'Arial',sans-serif; margin-bottom: 20px;}
            </style>
            <div class="title-style">Meet Our Trainers</div>
            """, unsafe_allow_html=True)
    # Trainer 1 Profile
    st.image("C:\\Users\\DELL\\Downloads\\gym2.jpg", use_column_width=True)  # Replace with trainer image path
    st.subheader("Purusothaman - Head Trainer")
    st.write("Certified Personal Trainer with 10 years of experience in weight training and sports performance.")

    # Trainer 2 Profile
    st.image("C:\\Users\\DELL\\Downloads\\gym1.jpg", use_column_width=True)  # Replace with trainer image path
    st.subheader("Maran - Fitness Coach")
    st.write("Passionate Fitness Coach specializing in HIIT and nutrition plans tailored to individual needs.")

# Membership Plans
elif page == "Membership Plans":
    # st.title("Choose Your Plan")
    st.markdown("""
                <style>.title-style { font-size: 48px; color: #DC143C; text-align: left; font-weight: bold; font-family: 'Arial',serif; margin-bottom: 20px;}
                </style>
                <div class="title-style">Choose Your Plan</div>
                """, unsafe_allow_html=True)
    st.header("Basic Plan")
    st.subheader("Affordable pricing for every fitness goal:")
    # Displaying membership plans
    st.write("### Advance Payment")
    st.write("**₹1,000** (one-time advance payment)")

    st.write("### Monthly Plans")
    st.write("**₹1,000/month** - Pay monthly for flexibility.")

    st.write("### 3-Month Plan")
    st.write("**₹2,000** for 3 months - Great for short-term goals.")

    st.write("### 6-Month Plan")
    st.write("**₹4,000** for 6 months - Commitment to serious training.")

    st.write("### 9-Month Plan")
    st.write("**₹4,000** for 9 months - Best value for prolonged dedication.")

    st.write("### Annual Plan")
    st.write("**₹8,000** for 12 months - Long-term savings and commitment.")

# Contact & Feedback
elif page == "Contact & Feedback":
    st.title("Contact Us")
    st.header("Get in Touch")

    # Contact details
    st.write("If you have any questions or want to know more about our gym, feel free to reach out:")
    st.write("**📞**: +91 98844 68461")
    st.write("**💬**: +91 97907 86867")
    st.write("**📸**: classic_fitness_unisex (Instagram)")
    st.write("**🏢**: 18, Saragabani Velunayakar, Jayaram Naicker Street, Sholinganallur, Chennai, Tamil Nadu 600119")

    st.write("Fill in the form below to get in touch with us or give us your feedback.")
    with st.form("contact_form"):
        name = st.text_input("Your Name")
        email = st.text_input("Your Email")
        message = st.text_area("Message / Feedback")
        submit = st.form_submit_button("Submit")

        if submit:
            st.success(f"Thank you, {name}! Your message has been sent.")

# streamlit run C:\Users\DELL\PycharmProjects\pythonProject\Streamlit\gym.py --server.port 8502