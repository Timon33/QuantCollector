# Definitions

## Time Formats

- use datetime library to handle dates internally
- use timezone objects
- when saving files use `unix timestaps` with second resolution

## Save Paths

- top level directory contains the asset classes
- asset class directory's contain `underlying` directory and different derivatives
- all contain separate folders for the time resolution of the data
- these contain a symbol depending on the asset class etc

## Symbols

- Symbols should be representable as unique strings

## Data Formats

Data Formats depend on the asset class and type (`underlying`, `options`, etc.)
