## postcode

#### This library was written as a test task. Code reviewer, enjoy!

### Quick start

1 install the library:
```bash
cd postcode
pip install -e '.[dev]'
```

2 run tests:
```bash
pytest .
```

3.1 Usage from shell
```bash
echo 'AB10 6RN' | validate_uk_postcode 2>errors.txt
```

3.2 Usage in a project
```bash
from postcode import uk

postcode = 'EC1A 1BB'
validator = uk.PostcodeValidator(postcode)
result = validator.validate()
assert result.is_valid
assert result.postcode == postcode
assert result.errors == []
```

