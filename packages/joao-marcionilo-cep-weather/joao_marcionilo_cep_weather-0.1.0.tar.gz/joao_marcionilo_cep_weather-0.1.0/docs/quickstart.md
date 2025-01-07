# Quickstart

Package to fetch data from an CEP API and scrape weather of a capital in Brazil

## Fetch CEP

**Function:** `cep_weather.get_data(cep:str)`

Fetch a capital's data from the API https://viacep.com.br/


### Example

```
from joao_marcionilo_cep_weather import get_data

data = get_data("60130240")
print(data)
```

### Parameters

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| `cep` | `str` | To be searched |



### Return type: `dict`
    

## Fetch Capital

**Function:** `cep_weather.get_capital(cep:str)`

Try to find the capital of a given CEP with the API https://viacep.com.br/


### Example

```
from joao_marcionilo_cep_weather import get_capital

capital = get_capital("60130240")
print(capital)
```

### Parameters

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| `cep` | `str` | To be searched |



### Return type: `str`
    

## Fetch Weather Forecast

**Function:** `cep_weather.get_capital_weather(capital:str, existing_capitals=True)`

Scrape for the weather of a capital in https://previsao.inmet.gov.br/


### Example

```
from joao_marcionilo_cep_weather import get_capital_weather

weather = get_capital_weather("São Paulo")
print(weather)
```

### Parameters

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| `capital` | `str` | To be searched |
| `existing_capitals` | `bool` | True will raise an ValueError case the capital is invalid |



### Return type: `str`
    