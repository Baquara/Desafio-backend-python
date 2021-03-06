#Importando bibliotecas, declarações e variáveis do arquivo principal. Também usando um alias para a definição "app", pois cria ambiguidade quando se utiliza Flask e pode resultar em erros.

from app import *
import app as aplicacao

#Rota para cadastrar pauta, recebendo em JSON o título da pauta e a sua duração em minutos. Por padrão, quando nenhum tempo é declarado, ele define a duração como 1 minuto.

@appflask.route('/api/v1/cadastrarpauta', methods=['POST'])
def cadastrarpauta():
    titulo = request.json.get('titulo', None)
    tempo = request.json.get('tempo', 1)
    tempo_timestamp = datetime.datetime.now() + datetime.timedelta(minutes=tempo)
    tempo_timestamp = int(tempo_timestamp.timestamp())
    try:
        aplicacao.engine.execute('INSERT INTO Pautas (titulo, tempo_timestamp,numero_votos_total,numero_votos_sim,numero_votos_nao) VALUES (\''+titulo+'\',\''+str(tempo_timestamp)+'\',0,0,0)')
    except Exception as e:
        return jsonify("Erro ao cadastrar pauta: "+str(e)), 409
    return jsonify("Pauta cadastrada com sucesso!"), 201


#Rota para cadastrar o associado, recebendo um JSON contendo os atributos nome e CPF. Se o CPF não for válido, retorna um erro.

@appflask.route('/api/v1/cadastrarassociado', methods=['POST'])
def cadastrarassociado():
    nome = request.json.get('nome', None)
    cpf = request.json.get('cpf', None)
    if not aplicacao.validarcpf(cpf):
        return jsonify('''O CPF fornecido não é válido.'''), 409
    try:
        aplicacao.engine.execute('INSERT INTO Associados (nome, cpf) VALUES (\''+nome+'\',\''+str(cpf)+'\')')
    except Exception as e:
        return jsonify("Erro ao cadastrar o(a) Associado(a)! Possivelmente o CPF já estiste no banco de dados. Erro: "+str(e)), 409
    return jsonify("Associado(a) cadastrado(a) com sucesso!"), 201

#Rota para realizar o voto. Recebe o id da pauta, do associado, e o tipo de voto. Apenas votos "Sim" e "Não" serão considerados válidos.


@appflask.route('/api/v1/votarpauta', methods=['POST'])
def votarpauta():
    id_associado = request.json.get('id_associado', None)
    id_pauta = request.json.get('id_pauta', None)
    voto = request.json.get('voto', None)
    if voto != "Sim" and voto != "Não":
        return jsonify('''O voto só pode ser "Sim" ou "Não"'''), 409
    if (aplicacao.validartempo(id_pauta)) == False:
        return jsonify("Esta pauta já se expirou. Não é mais possível votar."), 409
    if (aplicacao.associadoexiste(id_associado)) == False:
        return jsonify("Este(a) usuário(a) não existe. Cadastrar em /api/v1/cadastrarassociado"), 409
    if (aplicacao.validarvoto(id_associado,id_pauta)) == False:
        return jsonify("Este(a) usuário(a) já votou antes."), 409
    try:
        aplicacao.engine.execute('INSERT INTO Votos (id_associado, id_pauta, voto) VALUES (\''+str(id_associado)+'\',\''+str(id_pauta)+'\',\''+str(voto)+'\')')
        aplicacao.engine.execute('UPDATE Pautas SET numero_votos_total = numero_votos_total + 1 WHERE id = '+str(id_pauta))
        if voto == "Sim":
            aplicacao.engine.execute('UPDATE Pautas SET numero_votos_sim = numero_votos_sim + 1 WHERE id = '+str(id_pauta))
        if voto == "Não":
            aplicacao.engine.execute('UPDATE Pautas SET numero_votos_nao = numero_votos_nao + 1 WHERE id = '+str(id_pauta))
    except Exception as e:
        return jsonify("Erro ao votar em pauta: "+str(e)), 409
    return jsonify("Voto computado com sucesso!"), 201

#Rota que retorna todos os dados de uma pauta específica.

@appflask.route('/api/v1/resultadopauta', methods=['GET'])
def resultadopauta():
    id_pauta = request.json.get('id_pauta', None)
    try:
        resultado = aplicacao.engine.execute('SELECT * FROM Pautas WHERE id='+str(id_pauta))
        resultado = aplicacao.convertesql(resultado)
    except Exception as e:
        return jsonify("Erro ao consultar o resultado: "+str(e)), 404
    try:
        return jsonify(resultado[0]), 200
    except Exception as e:
        return jsonify("Não há resultados a serem exibidos."), 404


#Rota que retorna todas as pautas, e os seus dados.

@appflask.route('/api/v1/retornarpautas', methods=['GET'])
def retornarpautas():
    try:
        resultado = aplicacao.engine.execute('SELECT * FROM Pautas;')
        resultado = aplicacao.convertesql(resultado)
    except Exception as e:
        return jsonify("Erro ao consultar as pautas: "+str(e)), 404
    return jsonify(resultado), 200



#Rota que retorna todos os associados cadastrados.

@appflask.route('/api/v1/retornarassociados', methods=['GET'])
def retornarassociados():
    try:
        resultado = aplicacao.engine.execute('SELECT * FROM Associados;')
        resultado = aplicacao.convertesql(resultado)
    except Exception as e:
        return jsonify("Erro ao consultar as pautas: "+str(e)), 404
    return jsonify(resultado), 200

#Rota que retorna todos os votos de todas as pautas.

@appflask.route('/api/v1/retornarvotos', methods=['GET'])
def retornarvotos():
    try:
        resultado = aplicacao.engine.execute('SELECT * FROM Votos;')
        resultado = aplicacao.convertesql(resultado)
    except Exception as e:
        return jsonify("Erro ao consultar as pautas: "+str(e)), 404
    return jsonify(resultado), 200

#Rota que retorna se um associado com um dado CPF pode ou não votar (se o CPF dele é válido, e se está cadastrado)

@appflask.route('/api/v1/users/<string:cpf>', methods=['GET'])
def validarcpf(cpf):
    cpfvalido = aplicacao.validarcpf(cpf)
    if cpfvalido == False:
        abort(404)
    id_associado = aplicacao.localizar_id_por_cpf(cpf)
    if id_associado!=0:
        return jsonify({"status":"ABLE_TO_VOTE"}), 200
    else:
        return jsonify({"status":"UNABLE_TO_VOTE"}), 404

    
#Rota para fins de debugging, que limpa o banco de dados, e o projeto pode ser executado em "clean state".
    
    
@appflask.route('/api/v1/resetarbd', methods=["DELETE"])
def resetarbd():
    try:
        aplicacao.resetar_banco(aplicacao.engine)
        return jsonify("Sucesso ao limpar o banco de dados."), 200
    except Exception as e:
        return jsonify("Erro ao tentar limpar o banco de dados: "+str(e)), 405


#HTTP_METHODS = ['GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'CONNECT', 'OPTIONS', 'TRACE', 'PATCH']

#@appflask.route('/api/v1/debug', methods=HTTP_METHODS)
#def debug():
    #aplicacao.localizar_id_por_cpf("057.818.205-07")
    #aplicacao.associadoexiste(2)
    #aplicacao.resetar_banco(aplicacao.engine)
