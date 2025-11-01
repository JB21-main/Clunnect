# Clunnect is a web application allowing users to create and join clubs at UTD.

## Current Features
   Account Creation
   Authentication
   Club Creation
   Joining Clubs

## To Download and Run Clunnect

 1. In your Terminal clone the repository using:
       git clone https://github.com/JB21-main/Clunnect.git
       cd clunnect

 2. You will need to set up the enviorment:
       python -m venv venv
       venv/Scripts/activate

 3. Install Dependencies
       pip install -r requirements.txt

 4. Create a .env file in clunnect/src/main/python/group 7/clunnect the file should be formatted as such
       SUPABASE_KEY=[YOUR SUPABASE KEY]
       SUPABASE_URL=[YOUR SUPABASE URL]
   You can find the url and key on the supabase website when you create your database to be used.


 5. Running the application
       python TestApp.py
    then on a browser go to https://127.0.0.1:5000/


## KNOWN ISSUES:
       Errors only appear on the login page and can pile up until visited again
       There is no confirmation for joining a club other than the database adding a member to a club
       The same email can be used multiple times for multiple accounts

## Contributors:
   "Liam D. Godkin"
   "Jose Manuel Beltran Gonzales"
   "Jovita Jijo"
   "Kandhan Rameshkumar"
   "Lohita Nagalakshmi"
   "Taylor Beers"