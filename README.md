

# Produce API

Produce API is a simple python api allowing for management of produce inventory

## Dependencies

Before using Produce API, the following dependencies must be installed on the system. First, you need Python :

- [Python v3.9](https://www.python.org/downloads/release/python-392/)

A list of pip requirements can be found in `requirements.txt`

You call install all other dependencies via:

`pip3 install -r requirements.txt`

Or individually via:

- flask v1.1.2+

  ​	`pip3 install flask`

- flask_restful v0.3.8+

  ​	`pip3 install  flask-RESTful`

- pytest v6.2.2+

  ​	`pip3 install pytest`

- pytest-html v3.1.1+

  ​	`pip3 install pytest-html`

- requests v 2.25.1+

  ​	`pip3 install requests`

## Overview

Produce API is a RESTful api supporting:

- GET
- POST
- DELETE

PUT Method was outside of the requirement of this api and thus was not implemented.

Upon startup, the API database is initialized with the following data from `data/db.json` 

```json
{
    "A12T-4GH7-QPL9-3N4M": 
 	{
        "produce_code": "A12T-4GH7-QPL9-3N4M", 
     	"name": "Lettuce", 
        "price": 3.46
    }, 
    "E5T6-9UI3-TH15-QR88": 
    {
        "produce_code": "E5T6-9UI3-TH15-QR88", 
        "name": "Peach", 
        "price": 2.99
    }, 
    "YRT6-72AS-K736-L4AR": 
    {
        "produce_code": "YRT6-72AS-K736-L4AR", 
        "name": "Green Pepper", 
        "price": 0.79
    }, 
    "TQ4C-VV6T-75ZX-1RMR": 
    {
        "produce_code": "TQ4C-VV6T-75ZX-1RMR", 
        "name": "Gala  Apple", 
        "price": 3.59
    }
}
```

This data is loaded into a python `dict` structure, with the KEY being produce_code and VALUE being the json object representing the produce

### API

**Show all produce**

GET /produce

```http
http://127.0.0.1:5000/produce
```

Response (Example):

Status code:

```
200  - OK
```

Response body:

```json
{
    "produce": [
        {
            "produce_code": "A12T-4GH7-QPL9-3N4M",
            "name": "Lettuce",
            "price": 3.46
        },
        {
            "produce_code": "E5T6-9UI3-TH15-QR88",
            "name": "Peach",
            "price": 2.99
        },
        {
            "produce_code": "YRT6-72AS-K736-L4AR",
            "name": "Green Pepper",
            "price": 0.79
        },
        {
            "produce_code": "TQ4C-VV6T-75ZX-1RMR",
            "name": "Gala  Apple",
            "price": 3.59
        }
    ]
}
```

**Get Produce via Produce Code**

GET /produce/:produceCode

```http
http://127.0.0.1:5000/produce/A12T-4GH7-QPL9-3N4M
```

Response (Example):

Status code:

```
200 - OK
```

Response body:

```json
{
    "produce_code": "A12T-4GH7-QPL9-3N4M", 
    "name": "Lettuce", 
    "price": 3.46
}
```

**Add new produce**

 POST /produce

```
Body - JSON
{
  name: 'Corn',
  price: '2.00'
}
```

Response (Example):

Status code:

```
200
```

Response body:

```json
{
    "produce_code": "T2LM-KW2N=34EK-SS1B", 
    "name": "Corn", 
    "price": 2.00
}
```

- `produce_code` is autogenerated upon POST and is not a parameter to be passed via API call
-  `price` will be formatted to #.## format if not passed in with correct currency format
-  Will return Error Code if:
  -  `name` is already present in the database 
     -  Status Code: 409
     -  Error Code: Conflict
  -  `name` is non-alphanumeric
     - Status Code:480 
     - Error Code: Invalid Input
  -  `price` is not a number
     - Status Code: 480 
     - Error Code: Invalid Input

**Delete Produce by Produce Code**

DELETE /produce/:produce_code

```http
http://127.0.0.1:5000/produce/A12T-4GH7-QPL9-3N4M
```

Response (Example):

Status code:

```
204
```

Response body:

```json
<Empty Response Body>
```

## Testing

Produce API has two testing files, unit_test.py and integration_test.py. Together these tests serve to ensure the api works as expected and asked per design. These test files are located in the 'api/' folder. You must run all tests from this folder.

**NOTE:** You must be in the /api folder to run the tests properly. Before performing any tests, perform:

​	`cd api`

### Test Script

Provided is a bash script `runtests.sh` which has made the process of running the tests simple. In order to execute (ensuring you've called `cd api`):

​	`./runtests.sh`

This will perform the following tasks:

- Start test server as a background process
- Execute unit_test.py and integration_test.py with HTML reporting enabled

### Starting the Server

Before running tests locally, the server will need to be started. To start the server (ensuring you've called `cd api`):

​	`python produce_api.py`

To start the server as a background process:

​	`nohup python produce_api.py &`

This will allow the you to have continued access to the command prompt after starting the server. A log of server traffic can be seen via the `nohup.out` file.

​	**NOTE:** If spawned as a background process, you will need to kill the process once completed. To do so, run:

​		`ps` 

​		This will list all processes running. Find the one that ends with `python` and locate it's `pid`. Then, run:

​		`kill -9 <pid>`

### Running the Tests

In order to run a particular test set, call:

​	`python -m pytest <test_file_name.py>`

In order to run all tests:

​	`python -m pytest`

### Test Reporting

For test reporting, it is recommended to output results in junit format. This is especially useful for our github actions events to parse the results:

​	`python -m pytest --junitxml=result.xml`

## Docker

Provided is a Dockerfile and docker-compose.yml file for use with setting up and running with-in docker.

### Steps to build docker container

First, we need to build the container:

`docker-compose build`

Then, we need to start the container running:

`docker-compose up -d`

This will spawn the container. You can confirm the container is running with the command:

`docker container ps`

This will return information about the container, as well as the container id

Once the container is running, the server is running with-in. You can make requests to the server that is running in the container the same way you do with a server running locally, at port `127.0.0.1:5000`

To kill the docker container:

`docker kill <container id>`



