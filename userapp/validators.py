def validate_pword(password, confirmation, username, email):
    if len(password) < 8:
        return "Invalid Password"
    
    if password != confirmation:
        return "Invalid Password"
    
    if username == password:
        return "Invalid Password"

    if email == password:
        return "Invalid Password"
    
    if email == username:
        return "Invalid Username"
    
    upper_count = 0
    special_count = 0
    num_count = 0

    for character in password:
        if character.isupper():
            upper_count += 1
        elif not character.isalnum():
            special_count += 1
        elif character.isdigit():
            num_count += 1

    if upper_count == 0 or num_count == 0 or special_count == 0:
        return "Invalid Password"
    
    else:
        return None
