import pytest
import produce_api

'''
ensureUniqueItem tests
'''
def test_ensureUniqueItem_Success():
    response = produce_api.ensureUniqueItem('newItem')
    assert response == True

def test_ensureUniqueItem_Fail_ExactMatch():
    response = produce_api.ensureUniqueItem('Lettuce')
    assert response == False

def test_ensureUniqueItem_Fail_CaseInsensitiveMatch():
    response = produce_api.ensureUniqueItem('leTtucE')
    assert response == False

'''
validateName Tests
'''
def test_validateName_Success():
    response = produce_api.validateName('alph4numer1c')
    assert response == True

def test_validateName_Fail_NonAlphanumeric():
    response = produce_api.validateName('non@lph@numeric')
    assert response == False

def test_validateName_Fail_EmptyString():
    response = produce_api.validateName('')
    assert response == False

def test_validateName_Fail_Spaces():
    response = produce_api.validateName('name with spaces')
    assert response == False

'''
validatePrice Tests
'''
def test_validePrice_Success_Int():
    response = produce_api.validatePrice(2)
    assert response == True

def test_validePrice_Success_Decimal():
    response = produce_api.validatePrice(2.55)
    assert response == True

def test_validePrice_Fail_NonNumber():
    response = produce_api.validatePrice('non number')
    assert response == False

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
    response = produce_api.performValidation('name', '2.50')
    assert response == True

def test_performValidation_Fail_NonUnique():
    response = produce_api.performValidation('Lettuce', '2.50')
    assert response == False


def test_performValidation_Fail_NameNonValid():
    response = produce_api.performValidation('nonV@lidN@me', '2.50')
    assert response == False


def test_performValidation_Fail_PriceNonValid():
    response = produce_api.performValidation('validName', 'treefiddy')
    assert response == False






