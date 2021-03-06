import requests
import pytest
import time


def teste1():
    response = requests.delete("http://127.0.0.1:5000/api/v1/resetarbd")
    assert response.status_code == 200
    assert response.text == '"Sucesso ao limpar o banco de dados."\n'
    
def teste2():
    data = {
        'titulo': 'Pauta criada para testes',
        'tempo': 15
    }
    url = 'http://127.0.0.1:5000/api/v1/cadastrarpauta'

    response = requests.post(url, json=data)

    assert response.status_code == 201
    assert response.text == '"Pauta cadastrada com sucesso!"\n'
    
    
    
def teste3():
    data = {
        'nome': 'João Silva',
        'cpf': '677.084.680-27'
    }
    url = 'http://127.0.0.1:5000/api/v1/cadastrarassociado'

    response = requests.post(url, json=data)

    assert response.status_code == 201
    assert response.text == '"Associado(a) cadastrado(a) com sucesso!"\n'
    
    
def teste4():
    data = {
'id_associado':'2',
'id_pauta': '1',
'voto':'Sim'
    }
    url = 'http://127.0.0.1:5000/api/v1/votarpauta'

    response = requests.post(url, json=data)

    assert response.status_code == 409
    assert 'existe. Cadastrar em /api/v1/cadastrarassociado"\n' in response.text
    

def teste5():
    data = {
        'nome': 'Felipe Abreu',
        'cpf': '495.428.210-18'
    }
    url = 'http://127.0.0.1:5000/api/v1/cadastrarassociado'

    response = requests.post(url, json=data)

    assert response.status_code == 201
    assert response.text == '"Associado(a) cadastrado(a) com sucesso!"\n'
    
    
def teste6():
    data = {
'id_associado':'2',
'id_pauta': '1',
'voto':'Sim'
    }
    url = 'http://127.0.0.1:5000/api/v1/votarpauta'

    response = requests.post(url, json=data)

    assert response.status_code == 201
    assert 'Voto computado com sucesso!' in response.text

def teste7():
    data = {
'id_associado':'2',
'id_pauta': '1',
'voto':'Sim'
    }
    url = 'http://127.0.0.1:5000/api/v1/votarpauta'

    response = requests.post(url, json=data)

    assert response.status_code == 409
    assert 'votou antes.' in response.text

def teste8():
    data = {
        'titulo': 'Mais uma outra pauta criada para testes',
    }
    url = 'http://127.0.0.1:5000/api/v1/cadastrarpauta'

    response = requests.post(url, json=data)

    assert response.status_code == 201
    assert response.text == '"Pauta cadastrada com sucesso!"\n'
    
def teste9():

    url = 'http://127.0.0.1:5000/api/v1/retornarpautas'

    response = requests.get(url)

    assert response.status_code == 200
    
    
def teste10():
    data = {
'id_associado':'2',
'id_pauta': '1',
'voto':'a'
    }
    url = 'http://127.0.0.1:5000/api/v1/votarpauta'

    response = requests.post(url, json=data)

    assert response.status_code == 409
    assert 'O voto s\\u00f3 pode ser \\"Sim\\" ou \\"N\\u00e3o\\' in response.text
    
    
def teste11():
    data = {
'id_associado':'2',
'id_pauta': '2',
'voto':'Não'
    }
    url = 'http://127.0.0.1:5000/api/v1/votarpauta'

    response = requests.post(url, json=data)

    assert response.status_code == 201
    assert 'sucesso' in response.text
    time.sleep(65)
    


def teste12():
    data = {
'id_associado':'1',
'id_pauta': '2',
'voto':'Sim'
    }
    url = 'http://127.0.0.1:5000/api/v1/votarpauta'

    response = requests.post(url, json=data)

    assert response.status_code == 409
    assert 'expirou' in response.text
    
    
def teste11():
    data = {
'id_pauta': '2',
    }
    url = 'http://127.0.0.1:5000/api/v1/resultadopauta'

    response = requests.get(url, json=data)

    assert response.status_code == 200
    
    
def teste12():
    data = {
'id_associado':'1',
'id_pauta': '1',
'voto':'Sim'
    }
    url = 'http://127.0.0.1:5000/api/v1/votarpauta'

    response = requests.post(url, json=data)

    assert response.status_code == 201
    assert 'sucesso' in response.text
    
    
def teste13():

    url = 'http://127.0.0.1:5000/api/v1/retornarvotos'

    response = requests.get(url)

    assert response.status_code == 200
    
def teste13():

    url = 'http://127.0.0.1:5000/api/v1/retornarassociados'

    response = requests.get(url)

    assert response.status_code == 200
    
    
def teste14():

    url = 'http://127.0.0.1:5000/api/v1/users/495.428.210-18'

    response = requests.get(url)

    assert response.status_code == 200
    assert 'ABLE_TO_VOTE' in response.text
    
    
def teste15():

    url = 'http://127.0.0.1:5000/api/v1/users/1234567890'

    response = requests.get(url)

    assert response.status_code == 404
