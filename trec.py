import requests
from bs4 import BeautifulSoup
import shutil
import os
import tarfile
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import gzip
import subprocess
import logging
import sys

# define nist website url, username and password  that you have receied here
url = 'YOUR_URL_HERE'
user, password = 'YOUR_USER_NAME_HERE', 'YOUR_PASSWORD_HERE'


# We wont use SSL since we trust the downloading page, so hide warnings
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# get tweets from the dat files which are opened from the tar files

def openDatFiles(untarFolder, reverseDownload, begin, end):

    list = os.listdir(untarFolder)
    list.sort()
    if reverseDownload == True:
        list.reverse()

    if end > len(os.listdir(untarFolder)):
        end = len(os.listdir(untarFolder))
        print("Entered bigger value than folder size, setting end point to maximum")
    
    for i in range(begin, end):
    
        # dat file directory is in the same level with this script file, get its path
        datFolderPath = os.path.join(untarFolder, list[i])
    
        datFileList = os.listdir(datFolderPath)
        datFileList.sort()

        for datFile in datFileList:
            # remove dat extension
            datFileName = os.path.splitext(datFile)[0]

            # Crate a path for downloaded tweets data and its repair data
            jsonPath = makePath(jsonFolder, datFileName + ".json.gz")
            repairJsonPath = makePath(repairJsonFolder, datFileName + ".json.gz")
            datFilePath = makePath(datFolderPath, datFile)
      
            with subprocess.Popen(['sh', 'target/appassembler/bin/AsyncHTMLStatusBlockCrawler', '\\'
   ,'-data',datFilePath,'-output', jsonPath, '\\', '-repair', repairJsonPath], stdout=subprocess.PIPE) as proc:
                path = makePath(logFolder,datFileName+".log")
                print("logging to:" + path)
                logging.basicConfig(filename=path, level=logging.DEBUG)
                logging.info(proc.stdout.read().decode('utf-8'))
    return

# Repair
def repairDatFiles(repairJsonFolder):
    for repairFile in os.listdir(repairJsonFolder):
        repairFilePath = os.path.join(repairJsonFolder, repairFile)
        repairFile = os.path.splitext(repairFile)[0]
        if os.path.isdir(repairFilePath) == True:
            repairDatFiles(repairFilePath)
        else:
            repairFileName = makePath(jsonFolder, repairFile + ".repair.json.gz")
            with subprocess.Popen(['sh', 'target/appassembler/bin/AsyncHTMLStatusBlockCrawler','\\'
   ,'-data', repairFilePath, '-output', repairFileName], stdout=subprocess.PIPE) as proc:
                path = makePath(logFolder, repairFile+".repair.log")
                print("logging repair to:" + path)
                logging.basicConfig(filename=path, level=logging.DEBUG)
                logging.info(proc.stdout.read().decode('utf-8'))
    return

# Open gz file by creating new folder in  current directory
def openGzFiles(files):
    datFolders = []
    for file in files:
        tarFolder = os.path.abspath(os.path.join(file, "..","..", untarFolder))

        if ".tar" in file:
            with tarfile.open(file) as tar:
                tar.extractall(path=tarFolder)
                print("opening .tar.gz " + file)
                datFolders.append(tarFolder)
        else:
            baseName = os.path.basename(file)
            path = makePath(tarFolder, baseName)
            fileName = os.path.splitext(path)[0] 
            with gzip.open(file, 'rb') as file_in, open(fileName, 'wb') as file_out:
                file_content =file_in.read()
                file_out.write(file_content)
                print("opening .gz " + path)
                datFolders.append(path)
    return
                

# Download retrieved files from the webpage

def getFiles(files):
    pathlist = []
    for file in files:
        downloadURL = url + str(file)
        resp = requests.get(downloadURL, auth=(user, password), verify=False, stream=True)
        if (resp.status_code == 200):
            print(downloadURL + ' is being downloaded.')
            path = makePath(tarFolder, str(file))
            
            with open(path, 'wb') as file:
                resp.raw.decode_content = True
                shutil.copyfileobj(resp.raw, file)
            
            pathlist.append(path)
        else:
            print("Error while downloading " + downloadUrl + " code : " + str(resp.status_code))
    return pathlist

# Create new folder inside the scripts path and create new files in this new path

def makePath(folderName, fileName): 
    # use os module to join those beacuse of different operating sytems have different file seperators
    file_path = os.path.join(currentFolder,folderName, fileName)

    # Create new dir if not exist
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    return file_path



# Download the tar file URLs from the parsed content

def getFileLinks(resp):
    fileList = []
    html = BeautifulSoup(resp.content, 'html.parser')
    for link in html.find_all('a'):
        if 'tar' in link.get('href'):
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



currentFolder = os.path.dirname(os.path.realpath('__file__'))   
tarFolder = 'tarFiles'
untarFolder = 'openedTarFiles'
jsonFolder = 'jsonFiles'
logFolder = 'logFiles'
repairJsonFolder = 'repairJsonFiles'

reverse = False
numberOfFolders = None

# let the fun begin
resp = connect(url, user, password)
tar = getFileLinks(resp)
downloadedTar = getFiles(tar)
openGzFiles(downloadedTar)

temp = 0

for arg in sys.argv:
    if arg != os.path.basename(__file__):
        if arg == "--reverse":
            reverse = True
        else:
            print(arg)
            try:
                number = int(arg)
            except ValueError:
                print("Your input must be an integer for begin and end range")
            else:
                if(number>0):
                    if(number>temp):
                        begin = temp
                        end = number
                        temp = end
                    else:
                        begin = number
                else:
                    print("Please enter a positive integer")
openDatFiles(untarFolder, reverse, begin, end)
repairDatFiles(repairJsonFolder)
