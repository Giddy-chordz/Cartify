# ERROR:ValueError: password cannot be longer than 72 bytes
    FIX: i pip installed "bycrypt==4.0.1" and it worked fine, so I added it to the requirements.txt file to ensure that the correct version of bcrypt is installed when setting up the project in the future.

# Unable to login on postman: 
    the issue was that i dont know where to fit in the login details, so i went to the "body" sectionand selected "form-data" and added the "username" and "password" fields with the correct values, and then sent the request, which worked successfully.

# Unable to post products on postman:
    the issue was from my oauth2.py file where i set exp to 'expire' (string) instead of the actual expire time, so i changed it to the correct value and it worked fine... consequence was that jwt was not able to decode the token and thus was not able to verify the user, which is why i was getting an error when trying to post products.