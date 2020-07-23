import re
import sys
from dataclasses import dataclass, field


@dataclass
class ProcessedPostcode:

    postcode: str
    is_valid: bool = None
    errors: list = field(default_factory=list)


class PostcodeValidator:
    """
        https://en.wikipedia.org/wiki/Postcodes_in_the_United_Kingdom#Formatting

        postcode - between 5 and 7 characters excluding a space
        outward code - between 2 and 4 characters
        area - between 1 and 2 characters, alphabetical
        district - 1 digit or 2 digits or a digit followed by a letter
        inward code - 3 characters long
        sector - 1 digit
        unit - 2 characters
    """

    POSTCODE_MIN_LEN = 5
    POSTCODE_MAX_LEN = 7
    OUTWORD_CODE_MIN_LEN = 2
    OUTWORD_CODE_MAX_LEN = 4
    OUTWORD_CODE_REG_PATTERN_1 = '^[a-zA-Z]{1,2}[0-9][a-zA-Z]$'
    OUTWORD_CODE_REG_PATTERN_2 = '^[a-zA-Z]{1,2}[0-9]{1,2}$'
    OUTWORD_CODE_REG_PATTERN = (
        f'(^GIR$)|({OUTWORD_CODE_REG_PATTERN_1})|({OUTWORD_CODE_REG_PATTERN_2})')
    OUTWORD_PATTERNS_MSG = '(AA9A, A9A, A9, A99, AA9, AA99)'
    INWARD_CODE_LEN = 3

    def __init__(self, postcode):
        self.postcode = postcode.replace(' ', '')
        self.processed_postcode = ProcessedPostcode(postcode=postcode)

    def validate(self):
        self._validate_postcode_length()
        inward_code = self._validate_inward_code()
        outward_code = self._validate_outward_code()
        if self.processed_postcode.errors:
            self.processed_postcode.is_valid = False
        else:
            self.processed_postcode.is_valid = True
            self.processed_postcode.postcode = f'{outward_code} {inward_code}'.upper()

        return self.processed_postcode

    def _validate_postcode_length(self):
        postcode_length = len(self.postcode)
        if postcode_length < self.POSTCODE_MIN_LEN or postcode_length > self.POSTCODE_MAX_LEN:
            self.processed_postcode.errors.append(
                f'postcodes length must be from {self.POSTCODE_MIN_LEN} to'
                f' {self.POSTCODE_MAX_LEN} excluding a space, current is `{postcode_length}`')

    def _validate_inward_code(self):
        inward_code = self.postcode[-3:]
        inward_code_len = len(inward_code)
        if inward_code_len != self.INWARD_CODE_LEN:
            self.processed_postcode.errors.append(
                f'inward codes length must be equal {self.INWARD_CODE_LEN}, '
                f'current is `{inward_code_len}`')

        sector = inward_code[0]
        if not sector.isdigit():
            self.processed_postcode.errors.append(f'sector must be a digit, current is `{sector}`')

        unit = inward_code[1:]
        if not unit.isalpha():
            self.processed_postcode.errors.append(
                f'unit must consist of alphabetic characters, current is `{unit}`')

        return inward_code

    def _validate_outward_code(self):
        outward_code = self.postcode[:-3]
        self._validate_outward_code_length(outward_code)

        if not re.match(self.OUTWORD_CODE_REG_PATTERN, outward_code):
            self.processed_postcode.errors.append(
                f'outword code must follow by one of the patterns: {self.OUTWORD_PATTERNS_MSG}'
                ' where A is an alphabetic character and 9 is a digit,'
                f' current is `{outward_code}`')

        return outward_code

    def _validate_outward_code_length(self, outward_code):
        outward_code_len = len(outward_code)
        if (outward_code_len < self.OUTWORD_CODE_MIN_LEN
                or outward_code_len > self.OUTWORD_CODE_MAX_LEN):
            self.processed_postcode.errors.append(
                f'outward codes length must be from {self.OUTWORD_CODE_MIN_LEN} to'
                f' {self.OUTWORD_CODE_MAX_LEN}, current is `{outward_code_len}`')


def main():
    valid_counter = 0
    invalid_counter = 0
    while (line := sys.stdin.readline()):
        validator = PostcodeValidator(line.strip())
        postcode = validator.validate()
        if postcode.is_valid:
            valid_counter += 1
            print(f'Postcode: `{postcode.postcode}` is correct')
        else:
            invalid_counter += 1
            print(f'Postcode: `{postcode.postcode}` is not correct', file=sys.stderr)
            print('errors:', file=sys.stderr)
            for error in postcode.errors:
                print(f'  {error}', file=sys.stderr)

    print(f'\nall: {valid_counter + invalid_counter}',
          f' valid: {valid_counter}, invalid: {invalid_counter}')


if __name__ == '__main__':
    main()

