import streamlit as st
import pandas as pd
import numpy as np
import os
import joblib
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import seaborn as sns
def main():
    """ Heart Attack Prediction """
    st.title("Heart Attack Mortality Prediction App")

    menu = ["Home", "Login", "SignUp"]
    submenu = ["Plot", "Prediction", "Metrics"]

    choice = st.sidebar.selectbox("Menu", menu)
    if choice == "Home":
        st.subheader("Home")
        st.text("What is Hepatitis?")
    elif choice == "Login":
        username = st.sidebar.text_input("Usename")
        pasword = st.sidebar.text_input("Password", type = "password")
        if st.sidebar.checkbox("Login"):
            if password == "password":
                st.success(f"Welcome {username}")

                activity = st.selectbox("Activity", submenu)
                if activity == "Plot":
                    st.subheader("Viz Plot")
                elif activity == "Prediction":
                    st.subheader("Predictive Analytics")
                elif activity == "Metrics":
                    st.subheader("Analysis od Metrics")

            else:
                st.warning("Your Username/Password is Incorrect")
    elif choice == "SignUp":
        # New User
        new_username = st.text_input("User name")
        new_password = st.text_input("Password", type = "password")
        # Confirm the password
        confirm_password = st.text_input("Password", type = "password")
        if new_password == confirm_password:
            st.success("Password is Confirmed")
        else:
            st.warning("Password is not confirmed")
        if st.button("Submit"):
            pass



if __name__ == '__main__':
    main()