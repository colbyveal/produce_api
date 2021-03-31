import requests
import pytest
import flask
import produce_api

url="http://127.0.0.1:5000"

def test_GET_produceList_Success():
    response = requests.get(url + '/produce')
    assert response.ok
    assert response.json() == {
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

def test_GET_productByProduceID_Success():
    response = requests.get(url + '/produce' + '/A12T-4GH7-QPL9-3N4M')
    assert response.ok
    assert response.json() == {'produce_code': 'A12T-4GH7-QPL9-3N4M', 'name': 'Lettuce', 'price': 3.46}

def test_GET_productByProduceID_Fail_NotFound():
    response = requests.get(url + '/produce' + '/CODE-ISNT-HERE-OOPS')
    assert response.status_code == 404
    assert response.reason == "NOT FOUND"

def test_POST_AND_DELETE_newProduct_Success():
    response = requests.post(url + '/produce', data={'name' : 'newProduct', 'price' : 2.00})
    assert response.ok
    jsonResponse = response.json()
    assert jsonResponse['name'] == 'newProduct'
    assert jsonResponse['price'] == '2.00'
    prodCode = jsonResponse['produce_code']

    'remove after to ensure subsequent test runs still pass'
    delResponse = requests.delete(url + '/produce/' + prodCode)
    assert delResponse.status_code == 204

def test_POST_newProduct_Fail_NonAlphaNumName():
    response = requests.post(url + '/produce', data={'name' : 'non@lph@Num', 'price' : 2.00})
    assert response.status_code == 400
    assert response.reason == "BAD REQUEST"

def test_POST_newProduct_Fail_NonNumberPrice():
    response = requests.post(url + '/produce', data={'name' : 'non@lph@Num', 'price' : 'treefiddy'})
    assert response.status_code == 400
    assert response.reason == "BAD REQUEST"

def test_POST_newProduct_Fail_ProductAlreadyInDB():
    response = requests.post(url + '/produce', data={'name' : 'lettuce', 'price' : '2'})
    assert response.status_code == 409
    assert response.reason == "CONFLICT"

def test_DELETE_product_Fail_NotFound():
    response = requests.get(url + '/produce' + '/CODE-ISNT-HERE-OOPS')
    assert response.status_code == 404
    assert response.reason == "NOT FOUND"

def pytest_sessionfinish(session):
    produce_api.shutdown()