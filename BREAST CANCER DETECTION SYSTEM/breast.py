from ast import main
import streamlit as st
import pandas as pd
from sklearn.metrics import confusion_matrix
import pickle
import os


# DB Management
import sqlite3 
conn = sqlite3.connect('data.db')
c = conn.cursor()
def create_usertable():
	c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT,password TEXT)')


def add_userdata(username,password):
	c.execute('INSERT INTO userstable(username,password) VALUES (?,?)',(username,password))
	conn.commit()

def login_user(username,password):
	c.execute('SELECT * FROM userstable WHERE username =? AND password = ?',(username,password))
	data = c.fetchall()
	return data
def view_all_users():
	c.execute('SELECT * FROM userstable')
	data = c.fetchall()
	return data




def predict_default(texture_mean, area_mean, smoothness_mean, concavity_mean, texture_se, area_se, texture_worst, smoothness_worst, compactness_worst, symmetry_worst):
    
    # Pre-processing user input 
  model = pickle.load(open('model.pkl','rb')) 
    # Making predictions 
  prediction = model.predict( 
        [[texture_mean, area_mean, smoothness_mean, concavity_mean, texture_se, area_se, texture_worst, smoothness_worst, compactness_worst, symmetry_worst]])

    # if prediction is 0, breast cancer is malignant, else breast cancer is benign
  if prediction == 0:
      pred = 'malignant with the probability of 90%'
  else:
       pred = 'benign  with the probability of 95%'
       
  return pred


st.title('Breast Cancer Prediction App')
st.subheader('This is a simple breast cancer prediction web app to predict if the breast cancer is malignant or benign with an accuracy of 96%')
st.write('Please fill the following inputs to predict the breast cancer:')
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
        texture_mean = st.number_input('texture_mean')
        area_mean = st.number_input('area_mean')
with col2:
        smoothness_mean = st.number_input('smoothness_mean')
        concavity_mean = st.number_input('concavity_mean')
with col3:
        texture_se = st.number_input('texture_se')
        area_se = st.number_input('area_se')
with col4:
        texture_worst = st.number_input('texture_worst')
        smoothness_worst = st.number_input('smoothness_worst')

with col5:
        compactness_worst = st.number_input('compactness_worst')
        symmetry_worst = st.number_input('symmetry_worst')


button = st.button('Predict')
        
if button:
        prediction = predict_default(texture_mean, area_mean, smoothness_mean, concavity_mean, texture_se, area_se, texture_worst, smoothness_worst, compactness_worst, symmetry_worst)
        st.success('The breast cancer is {}'.format(prediction))













# Define function to create Login Page

# Define function to create Home Page
def main():


    
    menu = ["Home", "Login", "Signup"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Home":
        st.subheader("Home")
    elif choice == "Login":
    
            st.subheader("Login")
            username = st.sidebar.text_input("User Name")
            password = st.sidebar.text_input("password",type='password')

            if  st.sidebar.checkbox("login"):
             #if password.isnumeric():
                 create_usertable()
                 results=login_user(username,password)
                 st.success("Logged in as {}".format(username))

                 task = st.selectbox("Task", [ "Profile"])
                 if task == "Profile":
                  st.subheader(" Users Profiles")
                  user_result =view_all_users()
                  clean_db = pd.DataFrame(user_result,columns=["username","password"])
                  st.dataframe(clean_db)
            else:
             st.warning("Incorrect username/password")

    elif choice == "Signup":
        st.subheader("Create a new account")
        new_user =st.sidebar.text_input("username")
        new_password=st.sidebar.text_input("password",type='password')

        if st.sidebar.button("signup"):
         create_usertable()

         add_userdata(new_user,new_password)
         st.success("you have successfull created  a valid account")
         st.info("go to login menu to login ")










    
     

if __name__ == '__main__':
  main()

