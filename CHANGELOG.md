# Changelog

All notable changes to this project will be documented in this file.

## [0.1.2] - 2023-03-25
### Added
- Added optional start and end key arguments for the Interleave encryption method.
- Support for lambda functions in the encryption/decryption steps options (index/start/end). The key length will be passed as an argument.
- Added premade lambda functions: `Chiper.PENULTIMATE_OF_KE`Y and `Chiper.MIDDLE_OF_KEY`.
- Implemented type checking for input parameters.

### Changed
- Modified the encrypt/decrypt steps from `Dict[str, dict]` to `List[Dict[str, dict]]` to support using the same encryption method multiple times in the sequence.

### Fixed

### Removed

## [0.1.1] - 2023-03-23
### Added
- Added the possibility to encrypt/decrypt by passing an encryption key directly.
- Added "reverse" as an encryption and decryption method.
- Improved documentation.

### Changed

### Fixed
- Fixed swap reverse issue.

### Removed

## [0.1.0] - 2023-03-22
### Added
- Initial implementation of `ascii_chiper`.
- Support for encrypting and decrypting strings, integers, and dictionaries.
- Multiple encryption techniques including swapping, XOR shifting, interleaving, rotation, XOR base, XOR addition, and interleaving with key.
- Pre-configured encryption configurations for quick use.
- Custom encryption configuration support.
- Examples demonstrating various use cases of the module.
- Detailed README with usage instructions, encryption methods, and configurations.
- MIT License and Personal Thoughts section in the README.

### Changed

### Fixed

### Removed
