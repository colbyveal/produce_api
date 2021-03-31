import pytest
import produce_api

PRODUCE = {
    "A12T-4GH7-QPL9-3N4M": {
        "produce_code": "A12T-4GH7-QPL9-3N4M",
        "name": "Lettuce",
        "price": 3.46
    },
    "E5T6-9UI3-TH15-QR88": {
        "produce_code": "E5T6-9UI3-TH15-QR88",
        "name": "Peach",
        "price": 2.99
    },
    "YRT6-72AS-K736-L4AR": {
        "produce_code": "YRT6-72AS-K736-L4AR",
        "name": "Green Pepper",
        "price": 0.79
    },
    "TQ4C-VV6T-75ZX-1RMR": {
        "produce_code": "TQ4C-VV6T-75ZX-1RMR",
        "name": "Gala  Apple",
        "price": 3.59
    }
}

'''
ensureUniqueItem tests
'''
def test_ensureUniqueItem_Success():
    result = produce_api.ensureUniqueItem('newItem', PRODUCE)
    assert result == True

def test_ensureUniqueItem_Fail_ExactMatch():
    result = produce_api.ensureUniqueItem('Lettuce', PRODUCE)
    assert result == False

def test_ensureUniqueItem_Fail_CaseInsensitiveMatch():
    result = produce_api.ensureUniqueItem('leTtucE', PRODUCE)
    assert result == False

'''
validateName Tests
'''
def test_validateName_Success():
    result = produce_api.validateName('alph4numer1c')
    assert result == True

def test_validateName_Fail_NonAlphanumeric():
    result = produce_api.validateName('non@lph@numeric')
    assert result == False

def test_validateName_Fail_EmptyString():
    result = produce_api.validateName('')
    assert result == False

def test_validateName_Fail_Spaces():
    result = produce_api.validateName('name with spaces')
    assert result == False

'''
validatePrice Tests
'''
def test_validePrice_Success_Int():
    result = produce_api.validatePrice(2)
    assert result == True

def test_validePrice_Success_Decimal():
    result = produce_api.validatePrice(2.55)
    assert result == True

def test_validePrice_Fail_NonNumber():
    result = produce_api.validatePrice('non number')
    assert result == False

'''
generateProduceCode Tests
'''
def test_generateProduceCode_Success_Length():
    produceCode = produce_api.generateProduceCode()
    assert len(produceCode) is 19

def test_generateProduceCode_Success_Format():
    produceCode = produce_api.generateProduceCode()
    splitCode = produceCode.split('-')
    assert len(splitCode) is 4
    assert len(splitCode[0]) is 4
    assert len(splitCode[1]) is 4
    assert len(splitCode[2]) is 4
    assert len(splitCode[3]) is 4

def test_generateProduceCode_Success_Alphanumeric():
    produceCode = produce_api.generateProduceCode()
    splitCode = produceCode.split('-')
    assert splitCode[0].isalnum()
    assert splitCode[1].isalnum()
    assert splitCode[2].isalnum()
    assert splitCode[3].isalnum()

'''
formatPrice Tests
'''
def test_formatPrice_Success_Int():
    formatted = produce_api.formatPrice(2)
    assert formatted == '2.00'

def test_formatPrice_Success_SingleDecimal():
    formatted = produce_api.formatPrice(2.6)
    assert formatted == '2.60'

'python rounding returns this value, so it is what I am using'
def test_formatPrice_Success_TwoDecimal():
    formatted = produce_api.formatPrice(2.65)
    assert formatted == '2.65'

def test_formatPrice_Success_ThreeDecimal_RoundUp():
    formatted = produce_api.formatPrice(2.656)
    assert formatted == '2.66'

def test_formatPrice_Success_ThreeDecimal_RoundDown():
    formatted = produce_api.formatPrice(2.654)
    assert formatted == '2.65'

def test_formatPrice_Success_LargeDecimalAmount():
    formatted = produce_api.formatPrice(2.6574832143)
    assert formatted == '2.66'

'''
performValidation Tests
'''
def test_performValidation_Success_ValidAndUnique():
    result = produce_api.performValidation('name', '2.50', PRODUCE)
    assert result == 200

def test_performValidation_Fail_NonUnique():
    result = produce_api.performValidation('Lettuce', '2.50', PRODUCE)
    assert result == ("Conflict", 409)


def test_performValidation_Fail_NameNonValid():
    result = produce_api.performValidation('nonV@lidN@me', '2.50', PRODUCE)
    assert result == ("Bad Request", 400)


def test_performValidation_Fail_PriceNonValid():
    result = produce_api.performValidation('validName', 'treefiddy', PRODUCE)
    assert result == ("Bad Request", 400)

'''
transformData Tests
'''
def test_transformData_Success():
    result = produce_api.transformData(PRODUCE)
    assert result == {
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