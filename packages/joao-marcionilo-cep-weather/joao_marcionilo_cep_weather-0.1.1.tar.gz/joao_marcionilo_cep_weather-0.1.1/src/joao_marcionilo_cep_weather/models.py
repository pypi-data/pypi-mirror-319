from typing import Literal

from pydantic import BaseModel

capitals = Literal[
    'Rio Branco', 'Maceió', 'Macapá', 'Manaus', 'Salvador', 'Fortaleza', 'Brasília', 'Vitória', 'Goiânia',
    'São Luís', 'Cuiabá', 'Campo Grande', 'Belo Horizonte', 'Belém', 'João Pessoa', 'Curitiba', 'Recife',
    'Teresina', 'Rio de Janeiro', 'Natal', 'Porto Alegre', 'Porto Velho', 'Boa Vista', 'Florianópolis',
    'São Paulo', 'Aracaju', 'Palmas'
]


class CepData(BaseModel):
    cep: str
    logradouro: str
    complemento: str
    unidade: str
    bairro: str
    localidade: str
    uf: str
    estado: str
    regiao: str
    ibge: str
    gia: str
    ddd: str
    siafi: str
