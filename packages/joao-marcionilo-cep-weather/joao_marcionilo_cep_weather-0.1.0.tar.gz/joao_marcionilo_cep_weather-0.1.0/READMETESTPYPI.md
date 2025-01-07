> **WARNING!**
> PYPI example of how to install may not work. Use the installation guide bellow instead

# CEP Weather

Package to fetch data from an CEP API and scrape weather of a capital in Brazil

## Installation

In the terminal you can install the package without its dependencies

```
py -m pip install --index-url https://test.pypi.org/simple/ --no-deps joao_marcionilo_cep_weather
```

Then you can install the dependencies

```
py -m pip install joao_marcionilo_cep_weather
```

> This package and its dependencies should be installed separately, if not pip will try installing all packages
> from [test pypi](https://test.pypi.org/) and may result in installing the wrong packages

## Try it out

You can test the package with a local API running the following code

```
from joao_marcionilo_cep_weather import server

server.run()
```

[Click here](http://127.0.0.1:8000/docs) while running the code to access the doc of the API