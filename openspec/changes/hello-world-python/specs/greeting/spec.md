# greeting Specification

## ADDED Requirements

### Requirement: Greeting function
The system SHALL provide a function `hello(name)` that returns a greeting string.

#### Scenario: Default greeting
- **WHEN** `hello()` is called with no argument
- **THEN** it returns `"Hello, World!"`

#### Scenario: Named greeting
- **WHEN** `hello("Dan")` is called
- **THEN** it returns `"Hello, Dan!"`

#### Scenario: Blank name falls back
- **WHEN** `hello("")` or `hello("   ")` is called
- **THEN** it returns `"Hello, World!"`
