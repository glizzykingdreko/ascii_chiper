
class AsciiChiperException(Exception):
    pass

class DecryptionException(AsciiChiperException):
    pass

class EncryptionException(AsciiChiperException):
    pass

class InvalidKeyException(AsciiChiperException):
    pass

class InvalidModelException(AsciiChiperException):
    pass

class InvalidKeyInputException(AsciiChiperException):
    pass

class InvalidSeedInputException(AsciiChiperException):
    pass

class InvalidKeyLengthException(AsciiChiperException):
    pass

class InvalidModeException(AsciiChiperException):
    pass

class InvalidStartIndexException(AsciiChiperException):
    pass

class InvalidEndIndexException(AsciiChiperException):
    pass

class InvalidBaseException(AsciiChiperException):
    pass