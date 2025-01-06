# sacra

A collection of modules implementing various **sacra**.

> **_sacra_**: things sacred, holy, part of rites, or works of art.

Sacra is derived from the Latin word _sacrum_, meaning sacred or holy. This
repository contains tools and scripts that combine functionality, creativity,
a hint of esotericism, and a reverence for craft.

## Modules

- `sacra.polyskelion`: Generate polyskelion like a
  [triskelion](https://en.wikipedia.org/wiki/Triskelion)

## Installation

This repository is meant to be light on dependencies but are a few.

```bash
pip install sacra
```

## Usage

Most sacra included in this library are given their own executable
installation.

```bash
polyskelion  # Displays a polyskelion
polyskelion -h
polyskelion --spirals 4 --out quadskelion.png
```

The scripts contained in this package may also be used as a library.

```python
from sacra import polyskelion as ps

# Adjust parameters to your needs. They are defaulted
params = ps.PolyskelionParams()
figure = ps.plot_polyskelion(params)  # Returns a matplotlib.figure.Figure
```

## Contributing

Contributions are welcome. If you'd like to contribute:

1. Fork the repository.
2. Create a new branch for your feature or bugfix:
   ```bash
   git checkout -b feature-name
   ```
3. Make your changes and commit them:
   ```bash
   git commit -m "Add feature name"
   ```
4. Push your branch and open a pull request:
   ```bash
   git push origin feature-name
   ```

This project aims to have 100% test coverage with very few `# pragma: no
cover` exceptions.

## License

This project is licensed under the [MIT License](LICENSE). Feel free to use,
modify, and distribute it.
