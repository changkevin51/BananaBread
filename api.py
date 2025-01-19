import os
import requests
import urllib.parse
from urllib.parse import urlparse, parse_qs, urlencode
from dotenv import load_dotenv
from flask import Flask, request, redirect, session
import json

app = Flask(__name__)
app.secret_key = os.urandom(24)
load_dotenv()

class SurveyMonkeyAPI:
    BASE_URL = "https://api.surveymonkey.com"
    AUTH_ENDPOINT = "/oauth/authorize"
    TOKEN_ENDPOINT = "/oauth/token" # "/oauth/token"
    API_VERSION = "v3"

    def __init__(self):
        self.client_id = "jJOWaKvDRHWsyUInwRGLjg"
        # self.api_key = #os.getenv("API_KEY")
        self.redirect_uri = "http://localhost:5000/callback"
        self.access_token = "cOmUpOXfevWx560egh1njqAG36aYQUiG8wE.tB9lPUydOUz-7.jhfZ3Ei03vSrK8v33QW4NMifTsaZfItjgCtRo5ZytZIzlMf6o3jRJbnoSo219ux1jVKs9xD9Y3L9lg"
        
    def get_auth_url(self):
        params = {
            "response_type": "code",
            "client_id": "jJOWaKvDRHWsyUInwRGLjg",
            "redirect_uri": "http://localhost:5000/callback",
            "scope": "surveys_read surveys_write"
        }
        auth_url = f"https://api.surveymonkey.com/oauth/authorize?{urlencode(params)}"
        print(f"Generated Auth URL: {auth_url}")  # Add this line for debugging
        return auth_url
    def handle_redirect(self, redirect_url):
        """Extract authorization code from redirect URL"""
        parsed = urlparse(redirect_url)
        query_params = parse_qs(parsed.query)
        return query_params.get("code", [None])[0]

    def get_access_token(self, auth_code):
        # """Exchange authorization code for access token"""
        # data = {
        #     "client_id": self.client_id,
        #     "client_secret": self.api_key,
        #     "code": auth_code,
        #     "redirect_uri": self.redirect_uri,
        #     "grant_type": "authorization_code"
        # }
        
        # response = requests.post(
        #     f"{self.BASE_URL}{self.TOKEN_ENDPOINT}",
        #     data=data
        # )
        
        # if response.status_code == 200:
        #     self.access_token = response.json().get("access_token")
        #     return self.access_token
        # else:
        #     raise Exception(f"Token exchange failed: {response.text}")
        return "cOmUpOXfevWx560egh1njqAG36aYQUiG8wE.tB9lPUydOUz-7.jhfZ3Ei03vSrK8v33QW4NMifTsaZfItjgCtRo5ZytZIzlMf6o3jRJbnoSo219ux1jVKs9xD9Y3L9lg"

    def make_request(self, endpoint, method="GET", data=None):
        """Make authenticated API request"""
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        
        url = f"{self.BASE_URL}/{self.API_VERSION}/{endpoint}"
        
        response = requests.request(
            method=method,
            url=url,
            headers=headers,
            json=data
        )
        
        return response.json()

    def get_user_details(self):
        """Get authenticated user details"""
        return self.make_request("users/me")

    def list_surveys(self):
        """Get list of surveys"""
        return self.make_request("surveys")
    
    def create_survey(self, title, language="en"):
        """Create a new survey"""
        data = {
            "title": title,
            "language": language
        }
        response = self.make_request("surveys", method="POST", data=data)
        print("Survey Response:", response)
        return self.make_request("surveys", method="POST", data=data)

    def modify_survey(self, survey_id, data):
        """Modify existing survey"""
        return self.make_request(f"surveys/{survey_id}", method="PATCH", data=data)

    def add_page(self, survey_id, title):
        """Add page to survey"""
        data = {
            "title": title
        }
        return self.make_request(f"surveys/{survey_id}/pages", method="POST", data=data)

    def add_question(self, survey_id, page_id, question_data):
        """Add question to survey page"""
        return self.make_request(
            f"surveys/{survey_id}/pages/{page_id}/questions", 
            method="POST", 
            data=question_data
        )

# Usage example
if __name__ == "__main__":
    api = SurveyMonkeyAPI()
    
    # Get authorization URL with scopes
    auth_url = api.get_auth_url()
    print(f"Visit this URL to authorize: {auth_url}")
    
    # Get authorization code from redirect
    redirect_url = input("Enter the redirect URL: ")
    auth_code = api.handle_redirect(redirect_url)
    
    if auth_code:
        api.get_access_token(auth_code)
        
        # Create new survey
        new_survey = api.create_survey("My Test Survey")
        print(new_survey)
        survey_id = new_survey["id"]
        
        # Add page
        page = api.add_page(survey_id, "Page 1")
        page_id = page["id"]
        
        # Add question
        question = {
            "headings": [{"heading": "What is your favorite color?"}],
            "family": "single_choice",
            "answers": {
                "choices": [
                    {"text": "Red"},
                    {"text": "Blue"},
                    {"text": "Green"}
                ]
            }
        }
        api.add_question(survey_id, page_id, question)


# @app.route('/')
# def home():
#     api = SurveyMonkeyAPI()
#     return redirect(api.get_auth_url())

@app.route('/callback')
def callback():
    error = request.args.get('error')
    if error:
        return f"Authorization failed: {error}"
        
    api = SurveyMonkeyAPI()
    code = request.args.get('code')
    if code:
        try:
            # Get access token
            token = api.get_access_token(code)
            session['access_token'] = token
            
            # Create new survey
            survey_data = {
                "title": "New Test Survey",
                "nickname": "Demo Survey",
                "language": "en",
                "buttons_text": {
                    "next_button": "Next",
                    "prev_button": "Previous",
                    "done_button": "Submit"
                },
                "footer": True
            }
            
            response = api.make_request("surveys", method="POST", data=survey_data)
            
            # Redirect to survey edit URL
            if "edit_url" in response:
                return redirect(response["edit_url"])
            else:
                return f"Failed to get survey edit URL: {response}"
                
        except Exception as e:
            return f"Error creating survey: {str(e)}"
            
    return "Failed to get authorization code"
@app.route('/dashboard')
def dashboard():
    if 'access_token' not in session:
        return redirect('/')
        
    api = SurveyMonkeyAPI()
    api.access_token = session['access_token']
    try:
        user = api.get_user_details()
        surveys = api.list_surveys()
        return json.dumps({
            'user': user,
            'surveys': surveys
        }, indent=2)
    except Exception as e:
        return f"API request failed: {str(e)}"

if __name__ == "__main__":
    app.run(port=5000, debug=True)