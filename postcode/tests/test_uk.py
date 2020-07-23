from postcode import uk


def test_validate_positive_cases():
    validator = uk.PostcodeValidator('EC1A 1BB')
    result = validator.validate()
    assert result.is_valid
    assert result.postcode == 'EC1A 1BB'

    validator = uk.PostcodeValidator('w1a 0ax')
    result = validator.validate()
    assert result.is_valid
    assert result.postcode == 'W1A 0AX'

    validator = uk.PostcodeValidator('M1 1AE')
    result = validator.validate()
    assert result.is_valid
    assert result.postcode == 'M1 1AE'

    validator = uk.PostcodeValidator('B33 8TH')
    result = validator.validate()
    assert result.is_valid
    assert result.postcode == 'B33 8TH'

    validator = uk.PostcodeValidator('cr2 6xh')
    result = validator.validate()
    assert result.is_valid
    assert result.postcode == 'CR2 6XH'

    validator = uk.PostcodeValidator('DN55 1PT')
    result = validator.validate()
    assert result.is_valid
    assert result.postcode == 'DN55 1PT'


def test_postcode_length():
    """postcode is between 5 to 7 excluding a space
    """
    validator = uk.PostcodeValidator('EC1A')
    validator._validate_postcode_length()
    assert len(validator.processed_postcode.errors) == 1

    validator = uk.PostcodeValidator('EC1AB 1AK')
    validator._validate_postcode_length()
    assert len(validator.processed_postcode.errors) == 1


def test_outward_code_length():
    """outward code - between 2 and 4 characters
    """
    validator = uk.PostcodeValidator('EC1AA 1BB')
    validator._validate_outward_code_length('EC1AA')
    assert len(validator.processed_postcode.errors) == 1

    validator = uk.PostcodeValidator('E 1BB')
    validator._validate_outward_code_length('E')
    assert len(validator.processed_postcode.errors) == 1


def test_area_length():
    """
    area - from 1 to 2 characters and alphabetical
    """
    validator = uk.PostcodeValidator('121A 1BB')
    validator._validate_outward_code()
    assert len(validator.processed_postcode.errors) == 1
    assert 'patterns' in validator.processed_postcode.errors[0]

    validator = uk.PostcodeValidator('ECEC1A 1BB')
    validator._validate_outward_code()
    assert len(validator.processed_postcode.errors) == 2


def test_district():
    """
    district - 1 digit or 2 digits or a digit followed by a letter
    """
    validator = uk.PostcodeValidator('ECA 1BB')
    validator._validate_outward_code()
    assert len(validator.processed_postcode.errors) == 1
    assert 'patterns' in validator.processed_postcode.errors[0]

    validator = uk.PostcodeValidator('ECAA 1BB')
    validator._validate_outward_code()
    assert len(validator.processed_postcode.errors) == 1
    assert 'patterns' in validator.processed_postcode.errors[0]

    validator = uk.PostcodeValidator('ECB1 1BB')
    validator._validate_outward_code()
    assert len(validator.processed_postcode.errors) == 1
    assert 'patterns' in validator.processed_postcode.errors[0]


def test_sector():
    """
    sector - 1 digit
    """
    validator = uk.PostcodeValidator('EC1A CBB')
    validator._validate_inward_code()
    assert len(validator.processed_postcode.errors) == 1
    assert 'sector' in validator.processed_postcode.errors[0]


def test_unit():
    """
    unit - 2 characters
    """

    validator = uk.PostcodeValidator('EC1A 178')
    validator._validate_inward_code()
    assert len(validator.processed_postcode.errors) == 1
    assert 'unit' in validator.processed_postcode.errors[0]


def test_regexp_outword_code():
    postcode = 'EC1( 1BB'
    validator = uk.PostcodeValidator(postcode)
    result = validator.validate()

    assert result.is_valid == False
    assert len(validator.processed_postcode.errors) == 1
    assert 'pattern' in validator.processed_postcode.errors[0]

    postcode = ')EC1 1BB'
    validator = uk.PostcodeValidator(postcode)
    result = validator.validate()

    assert result.is_valid == False
    assert len(validator.processed_postcode.errors) == 1
    assert 'pattern' in validator.processed_postcode.errors[0]

    postcode = 'E1Q( 1BB'
    validator = uk.PostcodeValidator(postcode)
    result = validator.validate()

    assert result.is_valid == False
    assert len(validator.processed_postcode.errors) == 1
    assert 'pattern' in validator.processed_postcode.errors[0]

    postcode = ')E1Q 1BB'
    validator = uk.PostcodeValidator(postcode)
    result = validator.validate()

    assert result.is_valid == False
    assert len(validator.processed_postcode.errors) == 1
    assert 'pattern' in validator.processed_postcode.errors[0]

    postcode = 'GIR? 1BB'
    validator = uk.PostcodeValidator(postcode)
    result = validator.validate()

    assert result.is_valid == False
    assert len(validator.processed_postcode.errors) == 1
    assert 'pattern' in validator.processed_postcode.errors[0]

    postcode = '!GIR 1BB'
    validator = uk.PostcodeValidator(postcode)
    result = validator.validate()

    assert result.is_valid == False
    assert len(validator.processed_postcode.errors) == 1
    assert 'pattern' in validator.processed_postcode.errors[0]


def test_exceptions():
    postcode_exc = 'GIR 0AA'
    validator = uk.PostcodeValidator(postcode_exc)
    postcode = validator.validate()

    assert postcode.is_valid
    assert postcode.postcode == postcode_exc

