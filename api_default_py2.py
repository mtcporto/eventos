# -*- coding: utf-8 -*-
# Controlador default.py para o servidor Web2py em mtcporto2.pythonanywhere.com
# Versão compatível com Python 2.7

# Configuração de CORS simples - igual ao Auralis
response.headers['Access-Control-Allow-Origin'] = '*'
response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
response.headers['Access-Control-Allow-Headers'] = 'Content-Type, X-Requested-With, Authorization'

# Função auxiliar para obter dados da requisição - igual ao Auralis
def get_request_data():
    data = None
    try:
        data = request.json
    except:
        data = None
    if not data:
        # form-data ou x-www-form-urlencoded fallback
        data = request.vars or {}
    return data

# Endpoint OPTIONS básico
def options():
    return {}

# Endpoint para eventos - estruturado como os endpoints do Auralis
def eventos():
    """
    API para eventos
    GET: lista eventos
    POST: adiciona evento
    """
    # Para requisições POST
    if request.env.request_method == 'POST':
        data = get_request_data()
        
        # Validar campos obrigatórios
        campos_obrigatorios = ['oque', 'quando', 'onde', 'fonte', 'local']
        for campo in campos_obrigatorios:
            if campo not in data or not data[campo]:
                return response.json({
                    'error': 'Campo obrigatório ausente ou vazio: {0}'.format(campo)
                })
        
        try:
            # Inserir no banco
            evento_id = db.t_eventos.insert(
                f_oque=data['oque'],
                f_quando=data['quando'],
                f_onde=data['onde'],
                f_fonte=data['fonte'],
                f_local=data['local'],
                f_imagem=data.get('imagem', None),
                f_endereco=data.get('endereco', None),
                f_preco=data.get('preco', None),
                f_descricao=data.get('descricao', None),
                f_tipo=data.get('tipo', None),
                f_data_cadastro=request.now
            )
            
            # Commit na transação
            db.commit()
            
            # Retornar resposta de sucesso
            return response.json({
                'status': 'success',
                'message': 'Evento cadastrado com sucesso',
                'id': evento_id
            })
        except Exception as e:
            # Log do erro e rollback
            import sys, traceback
            print("Erro: ", sys.exc_info())
            print(traceback.format_exc())
            db.rollback()
            
            return response.json({
                'error': 'Erro ao processar requisição: {0}'.format(str(e))
            })
    
    # Para requisições GET
    elif request.env.request_method == 'GET':
        try:
            # Lista eventos limitados aos 100 mais recentes
            eventos = db(db.t_eventos).select(
                orderby=~db.t_eventos.f_data_cadastro,
                limitby=(0, 100)
            )
            
            # Formatar para JSON
            return response.json({
                'eventos': [{'id': e.id,
                           'oque': e.f_oque,
                           'quando': e.f_quando,
                           'onde': e.f_onde,
                           'local': e.f_local,
                           'fonte': e.f_fonte} 
                          for e in eventos]
            })
        except Exception as e:
            return response.json({'error': str(e)})
    
    # Para outras requisições
    return response.json({'message': 'Método não suportado'})

# Para testar o funcionamento
def api_teste():
    """Página para testar a API de eventos"""
    return dict(message="API de eventos está funcionando corretamente")
