from flask import Flask, render_template, request, jsonify, abort
import re
import json
import requests
from sqlalchemy import *
from flask_cors import CORS
import datetime



appflask = Flask(__name__)


import api


appflask.secret_key = b'_8#azL"oyt4z\n\xec]/'

engine = create_engine('sqlite:///banco.db')
engine.echo = False



def resetar_banco(session):
    meta = MetaData()
    meta.reflect(bind=session)
    for table in reversed(meta.sorted_tables):
        print ('Limpando tabela  %s' % table)
        session.execute(table.delete())

def convertesql(sqlobj):
    d, a = {}, []
    for rowproxy in sqlobj:
        for column, value in rowproxy.items():
            d = {**d, **{column: value}}
        a.append(d)
    if(a == []):
        return None
    return a



def validartempo(id_pauta):
    timestamp = engine.execute('SELECT tempo_timestamp FROM Pautas WHERE id='+str(id_pauta))
    timestamp = convertesql(timestamp)
    timestamp = timestamp[0]["tempo_timestamp"]
    timestamp_atual = datetime.datetime.now()
    timestamp_atual = timestamp_atual.timestamp()
    if(int(timestamp_atual) > int(timestamp)):
        return False
    else:
        return True


def validarvoto(id_associado,id_pauta):
    resultado = engine.execute('SELECT * FROM Votos WHERE id_associado='+str(id_associado)+' AND id_pauta='+str(id_pauta))
    resultado = convertesql(resultado)
    if resultado == None:
        return True
    else:
        return False


def localizar_id_por_cpf(cpf):
    resultado = engine.execute('SELECT id FROM Associados WHERE cpf=\''+str(cpf)+'\'')
    resultado = convertesql(resultado)
    if resultado == None:
        return 0
    else:
        return resultado[0]["id"]


def associadoexiste(id):
    resultado = engine.execute('SELECT id FROM Associados WHERE id=\''+str(id)+'\'')
    resultado = convertesql(resultado)
    if resultado == None:
        return False
    else:
        return True


def validarcpf(cpf):

    """ Efetua a validação do CPF, tanto formatação quando dígito verificadores.

    Parâmetros:
        cpf (str): CPF a ser validado

    Retorno:
        bool:
            - Falso, quando o CPF não possuir o formato 999.999.999-99;
            - Falso, quando o CPF não possuir 11 caracteres numéricos;
            - Falso, quando os dígitos verificadores forem inválidos;
            - Verdadeiro, caso contrário.

    Exemplos:

    >>> validate('529.982.247-25')
    True
    >>> validate('52998224725')
    False
    >>> validate('111.111.111-11')
    False
    """

    # Verifica a formatação do CPF
    if not re.match(r'\d{3}\.\d{3}\.\d{3}-\d{2}', str(cpf)):
        return False

    # Obtém apenas os números do CPF, ignorando pontuações
    numbers = [int(digit) for digit in cpf if digit.isdigit()]

    # Verifica se o CPF possui 11 números ou se todos são iguais:
    if len(numbers) != 11 or len(set(numbers)) == 1:
        return False

    # Validação do primeiro dígito verificador:
    sum_of_products = sum(a*b for a, b in zip(numbers[0:9], range(10, 1, -1)))
    expected_digit = (sum_of_products * 10 % 11) % 10
    if numbers[9] != expected_digit:
        return False

    # Validação do segundo dígito verificador:
    sum_of_products = sum(a*b for a, b in zip(numbers[0:10], range(11, 1, -1)))
    expected_digit = (sum_of_products * 10 % 11) % 10
    if numbers[10] != expected_digit:
        return False

    return True




if __name__ == "__main__":
    appflask.run()
 
