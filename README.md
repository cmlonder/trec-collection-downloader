# TREC 2011 Twitter Collection Downloader

* Downloads approximately 16 million tweets which are gathered by TREC in 2011. 
* Enables download from multiple machine and save your time (in a single machine, it may last +30 days!)
* Retry failed downloads
* Write downloads into log file
* Combines all failed/succeed download statistics
* Uncompress all zips into one folder

For more information about collection https://github.com/lintool/twitter-tools/wiki/Tweets2011-Collection and TREC 
http://trec.nist.gov/data/tweets/

## Prerequests

* Python 3.5.*
* Download https://github.com/lintool/twitter-tools to your local. This is main tool to fetch the tweets. Installing steps of the tool is as decribed in its page:


  * The main Maven artifact for the TREC Microblog API is `twitter-tools-core`. The latest releases of Maven artifacts are available at [Maven Central](http://search.maven.org/#search%7Cga%7C1%7Ccc.twittertools).

  * You can clone the repo with the following command:

    ```
    $ git clone git://github.com/lintool/twitter-tools.git
    ``` 

  * Once you've cloned the repository, change directory into `twitter-tools-core` and build the package with Maven:

    ```
    $ cd twitter-tools-core
    $ mvn clean package appassembler:assemble
    ```

  * For more information, see the [project wiki](https://github.com/lintool/twitter-tools/wiki).

* Than clone this repo with the following command into the `twitter-tools-core` directory that you have cd into in previous step:

  ```
  https://github.com/cmlonder/trec-collection-downloader.git
  ```

* Install required libraries by running this command:

  ```
  pip3.5 install -r requirements.txt
  ```

Or if your default python version is 3.5 than you can run this command with using directly `pip` command instead of `pip3.5`

  ```
  pip install -r requirements.txt
  ```

* If you haven't pip installed (which is must be installed default when you install Python 3.5) than follow those steps:

  * To install pip, securely download [get-pip.py](https://bootstrap.pypa.io/get-pip.py)

  * Then run the following:

    ```
    python3.5 get-pip.py
    ```

  * or if your default python version is 3.5 you can run this command with using directly `python` instead of `python3.5`

    ```
    python get-pip.py
    ```

  * For the rest of the tutorial, it is assumed that your default python version is 3.5 and `python` command will be used in examples.

* Get your URL, username and password via http://trec.nist.gov/data/tweets/ .Pay attention to this section in the link:

> Email the signed agreement, as a PDF file, to Angela Ellis <angela.ellis@nist.gov>. In the body of your email,
> Be clear that you are requesting the Tweets2011 dataset
> Include your name,
> your email address, and
> the name of your organization.
> We will respond to your request with a URL, a username, and a password with which you can download the tweet lists. Please allow seven business days for a respons


## Folder Structure

Here is the folder structure which this script will create.

**tarFiles:** Compressed files which is firstly downloaded from the site you have received from the TREC authorities.

**openedTarFiles:** Uncompressed files which are structured like DAY/DAY-NUMBER.dat. There are 17 days and 100 dat files in each day

**jsonFiles:** Compressed JSON files that fetched by using dat files. There are approximately 10.000 tweets in each file

**repairJsonFiles:** JSON files which has the information that failed fetches. Those will be downloaded automatically by the script into jsonFiles folder with the extension *.repair.json.gz*

**logFiles:** Log files for each json file.


## Usage

1) Update url, user and password with your own ones

```python
url = 'YOUR_URL_HERE'
user, password = 'YOUR_USER_NAME_HERE', 'YOUR_PASSWORD_HERE'
```

2) Run the script for default usage. This will fetch tweets(10.000 per .dat file) from each .dat file (100 per folder) from each folder (17 folder). This is not good scenario cause it will cost you +30 more days, but if you have acceptable time and connection go with this one.

```
python trec.py
```

3) Download the corpus with reverse order.

```
python trec.py --reverse
```

4) Download the corpus from folder number 5 to 10

```
python trec.py 5 10
```

5) Download the corpus from folder number 0 to 5 with reverse order

```
python trec.py --inverse 0 5
```

6) Download the corpus from 0 (default beginning number if only 1 number is given) to 5

```
python trec.py 5
```

## Example Scenario

You have 4 machine to download the corpus. Or you can start 4 different command line in a single machine if you have good bandwith and processor. It will be faster than single connection. So run the script in each machine with given ranges and than merge your jsonFiles folders. Use any number of machine like this scenario to download corpus with minimum amount of time.

```
python trec.py 0 3
python trec.py 4 7
python trec.py 8 11
python trec.py 12 17
```

