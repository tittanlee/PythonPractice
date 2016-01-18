# -*- coding: <utf-8>-*-
from temboo.Library.Facebook.OAuth import InitializeOAuth
from temboo.Library.Facebook.OAuth import FinalizeOAuth
from temboo.Library.Facebook.Searching import Search
from temboo.core.session import TembooSession
import json
import os, os.path

FACEBOOK_APP_ID  = "534039770107244"
FACEBOOK_APP_SEC = "27b30f0ea6204f63feefd41efb8b384c"
FACEBOOK_PER_SCOPE = "publish_actions"
FACEBOOK_USER_ACCESS_TOKEN = ""

def InitializeOAuthProcess():
  # Create a session with your Temboo account details
  session = TembooSession("tittanlee", "myFirstApp", "0u4EYYzLgkQu4OEDPIaVVPhJfgA9N0jk")

  # Instantiate the Choreo
  initializeOAuthChoreo = InitializeOAuth(session)

  # Get an InputSet object for the Choreo
  initializeOAuthInputs = initializeOAuthChoreo.new_input_set()

  # Set the Choreo inputs
  initializeOAuthInputs.set_AppID(FACEBOOK_APP_ID)
  initializeOAuthInputs.set_Scope(FACEBOOK_PER_SCOPE)

  # Execute the Choreo
  initializeOAuthResults = initializeOAuthChoreo.execute_with_results(initializeOAuthInputs)

  # Print the Choreo outputs
  AuthUrl    = initializeOAuthResults.get_AuthorizationURL()
  CallBackId = initializeOAuthResults.get_CallbackID()
  print("AuthorizationURL: " + AuthUrl)
  print("CallbackID: " + CallBackId)

  # Instantiate the Choreo
  finalizeOAuthChoreo = FinalizeOAuth(session)

  # Get an InputSet object for the Choreo
  finalizeOAuthInputs = finalizeOAuthChoreo.new_input_set()

  # Set the Choreo inputs
  finalizeOAuthInputs.set_AppID(FACEBOOK_APP_ID)
  
  # OPTIONAL INPUT 
  # LongLivedToken - bool
  finalizeOAuthInputs.set_LongLivedToken("true")

  # SuppressErrors
  finalizeOAuthInputs.set_LongLivedToken("true")

  #TimeOut
  finalizeOAuthInputs.set_Timeout("60")

  finalizeOAuthInputs.set_CallbackID(CallBackId)
  finalizeOAuthInputs.set_AppSecret(FACEBOOK_APP_SEC)

  # Execute the Choreo
  finalizeOAuthResults = finalizeOAuthChoreo.execute_with_results(finalizeOAuthInputs)

  # Print the Choreo outputs
  Access_Token = finalizeOAuthResults.get_AccessToken()
  print("AccessToken: " + finalizeOAuthResults.get_AccessToken())
  print("ErrorMessage: " + finalizeOAuthResults.get_ErrorMessage())
  print("Expires: " + finalizeOAuthResults.get_Expires()/60/60/24)

  f = open('TokenFile',"w")
  f.write(Access_Token)
  f.close()

def IsUserAccessTokenValid():
  global FACEBOOK_USER_ACCESS_TOKEN
  Result = False
  FilePath ='./TokenFile'

  if os.path.isfile(FilePath) and os.access(FilePath, os.R_OK):
    f = open(FilePath, 'r')
    Token = f.readline()
    if (len(Token) == 0):
      Result = False
    else:
      FACEBOOK_USER_ACCESS_TOKEN = Token
      print("AccessToken: " + FACEBOOK_USER_ACCESS_TOKEN)
      Result = True
  else:
    print('TokenFile is not exist, re applicationing ...')
    Result = False
  f.close()
  return Result

def FacebookSearch(KeyWord):
  # Create a session with your Temboo account details
  session = TembooSession("tittanlee", "myFirstApp", "0u4EYYzLgkQu4OEDPIaVVPhJfgA9N0jk")

  # Instantiate the Choreo
  searchChoreo = Search(session)

  # Get an InputSet object for the Choreo
  searchInputs = searchChoreo.new_input_set()

  # Set credential to use for execution
  searchInputs.set_credential('tittanlee')

  # Set the Choreo inputs
  searchInputs.set_ObjectType("group")
  searchInputs.set_Center("taiwan")
  searchInputs.set_Query(KeyWord)

  # Execute the Choreo
  searchResults = searchChoreo.execute_with_results(searchInputs)

  # Print the Choreo outputs
  # print("Response: " + searchResults.get_Response())
  # print("HasNext: " + searchResults.get_HasNext())
  # print("HasPrevious: " + searchResults.get_HasPrevious())

  Response = searchResults.get_Response()
  Dict = json.loads(Response)

  for List in Dict['data']:
    print(List)

  print(Dict['paging']['next'])

IsTokenValid = IsUserAccessTokenValid()
if not IsTokenValid:
  InitializeOAuthProcess()

FacebookSearch('免費廣告')
