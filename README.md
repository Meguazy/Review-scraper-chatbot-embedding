# googleScraper

In order to install and use the project you need to have installed the followings:
- python 3.8 or above
- docker
- docker-compose

Position yourself in the googlescraper directory and run the command
```
docker-compose up
```

After the docker container has been created, you can install the virtual environment. I suggest using 'pipenv'. The following command should install all the dependencies of the pipfile and pipfile.lock
```
pipenv install
```

# **IMPORTANT**

Open the consumer and the producer in two different terminals, so you can switch between them and see messages being produced and consumed.

Start the consumer by using
```
pipenv run python -m consumer
```
then, start the producer
```
pipenv run python -m producer
```

Once the producer is started it will ask you to insert the URL to scrape. The format of the URL is:
```
https://www.indeed.com/cmp/{company-name}/
```
For example
```
https://www.indeed.com/cmp/Sync-Lab/
```
or
```
https://www.indeed.com/cmp/Google/
```
