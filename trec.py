import requests
from bs4 import BeautifulSoup
import shutil
import os
import tarfile
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# CHANGE THOSE PARAMETERS WITH YOUR OWN AND RUN THE SCRIPT

# define nist website url, username and password  that you have receied here
url = 'YOUR_RETRIEVED_NIST_WEBSITE_URL'
tarFolder = "tarFiles" # will be created in this folder
untarFolder = "openedTarFiles" # will be created in this folder
user, password = 'NIST_USER_NAME', 'NIST_PASSWORD'

# CHANGE THOSE PARAMETERS WITH YOUR OWN AND RUN THE SCRIPT


# We wont use SSL since we trust the downloading page, so hide warnings
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# Open tarfile by creating new folder in  current directory
def openTarFile(folderName, fileName):  
  tarFolder = os.path.abspath(os.path.join(fileName, "..","..", folderName))
  print("path = " + tarFolder)
  with tarfile.open(fileName) as file:
    file.extractall(path=tarFolder)
    print("opening tar")
  return
  

# Download retrieved files from the webpage

def getFiles(files):
  for file in files:
    downloadURL = url + str(file)
    resp = requests.get(downloadURL, auth=(user, password), verify=False, stream=True)
    if (resp.status_code == 200):
      print(downloadURL + ' is being downloaded.')
      path = makePath(tarFolder, str(file))
      
      with open(path, 'wb') as file:
        resp.raw.decode_content = True
        shutil.copyfileobj(resp.raw, file)
      
      openTarFile(untarFolder, path)
    else:
      print("Error while downloading " + downloadUrl + " code : " + str(resp.status_code))
  return

# Create new folder inside the scripts path and create new files in this new path

def makePath(folderName, fileName):
  # Get the scripts file path
  script_dir = os.path.dirname(os.path.realpath('__file__'))
      
  # use os module to join those beacuse of different operating sytems have different file seperators
  file_path = os.path.join(script_dir,folderName, fileName)

  # Create new dir if not exist
  os.makedirs(os.path.dirname(file_path), exist_ok=True)
  return file_path



# Download the tar file URLs from the parsed content

def getFileLinks(resp):
  fileList = []
  html = BeautifulSoup(resp.content, 'html.parser')
  for link in html.find_all('a'):
    if '.gz' in link.get('href'):
    # print link, ' link has been found and added to download list.'
      fileList.append(link.get('href'))
  return fileList

# Connect to the webpage to retrieve download links

def connect(url, usr, pwd):
  resp = requests.get(url, auth=(user, password), verify=False)
  if(resp.status_code == 200): 
    print('Connection successful:' + str(resp.status_code))
    return resp
  else:
    print ('There is an error while connecting the site : ' + str(resp.status_code))

# let the fun begin
resp = connect(url, user, password)
files = getFileLinks(resp)
getFiles(files)
