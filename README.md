# Desafio-backend-python

Repositório com a solução de um desafio para vaga de Backend.

Esta solução foi elaborada no Framework Flask, na Linguagem Python. Para fins de portabilidade, o banco de dados utilizado para este projeto (cujo pré-requisito é persistência de dados) é SQLite.

As rotas de API se encontram inteiramente documentadas na seguinte URL do Postman:

https://documenter.getpostman.com/view/13068940/Tz5jefpE


## Dependências

É necessário ter o Python 3 instalado no sistema, em seguida executar:

>pip install -r requirements.txt

## Como executar

Clonar o projeto:

>git clone https://github.com/Baquara/Desafio-backend-python.git

Em seguida,

>cd Desafio-backend-python
>
>export FLASK_APP=app.py
>
>flask run

Por padrão a aplicação é executada em http://127.0.0.1:5000/ .

Em seguida, verificar a documentação das rotas:

https://documenter.getpostman.com/view/13068940/Tz5jefpE


## Testes automatizados:

No diretório principal , está presente o arquivo testes_auto.py, que pode ser executado usando a biblioteca pytest. A API precisa estar em execução na máquina local (http://127.0.0.1:5000/) para que os testes sejam executados. 

>pytest testes_auto.py
