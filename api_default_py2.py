# -*- coding: utf-8 -*-
# Controlador default.py para o servidor Web2py em mtcporto2.pythonanywhere.com
# Versão compatível com Python 2.7 e 3+
# Adicione este código ao seu arquivo controllers/default.py existente

# Configuração de CORS - configuração global
response.headers['Access-Control-Allow-Origin'] = '*'
response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
response.headers['Access-Control-Allow-Headers'] = 'Content-Type, X-Requested-With, Authorization'

# Função auxiliar para aplicar cabeçalhos CORS em cada requisição
def set_cors_headers():
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, X-Requested-With, Authorization'

# Função auxiliar para obter dados da requisição tanto em JSON quanto form-data
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

# Endpoint OPTIONS para lidar com preflight requests do CORS
def options():
    """Responde a requisições OPTIONS do CORS preflight"""
    set_cors_headers()
    return {}

# Endpoint específico para OPTIONS na rota /eventos
def eventos_options():
    set_cors_headers()
    return {}

# Endpoint principal para receber eventos
@request.restful()
def eventos():
    """
    API para receber eventos extraídos de imagens.
    
    GET: Lista todos os eventos cadastrados
    POST: Adiciona um novo evento
    """
    def POST(*args, **vars):
        # Garantir que os cabeçalhos CORS sejam aplicados
        set_cors_headers()
        
        try:
            # Obter dados da requisição usando a função auxiliar
            dados = get_request_data()
            
            if not dados:
                return response.json({'error': 'Nenhum dado recebido'}, status=400)
            
            # Validar campos obrigatórios
            campos_obrigatorios = ['oque', 'quando', 'onde', 'fonte', 'local']
            for campo in campos_obrigatorios:
                if campo not in dados or not dados[campo]:
                    return response.json({
                        'error': 'Campo obrigatório ausente ou vazio: {0}'.format(campo)
                    }, status=400)
            
            # Preparar dados para inserção
            evento_id = db.t_eventos.insert(
                f_oque=dados['oque'],
                f_quando=dados['quando'],
                f_onde=dados['onde'],
                f_fonte=dados['fonte'],
                f_local=dados['local'],
                f_imagem=dados.get('imagem', None),  # Campo opcional
                f_endereco=dados.get('endereco', None),  # Campo opcional
                f_preco=dados.get('preco', None),  # Campo opcional
                f_descricao=dados.get('descricao', None),  # Campo opcional
                f_tipo=dados.get('tipo', None),  # Campo opcional
                f_data_cadastro=datetime.datetime.now()
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
            # Log do erro
            logger.error("Erro ao processar requisição de evento: {0}".format(str(e)))
            
            # Rollback em caso de erro
            db.rollback()
            
            # Retornar erro
            return response.json({
                'error': 'Erro ao processar requisição: {0}'.format(str(e)),
                'details': traceback.format_exc()
            }, status=500)
    
    def GET(*args, **vars):
        # Garantir que os cabeçalhos CORS sejam aplicados
        set_cors_headers()
        
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
    
    def OPTIONS(*args, **vars):
        # Garantir que os cabeçalhos CORS sejam aplicados
        set_cors_headers()
        return {}
    
    # Retorna todos os métodos, incluindo OPTIONS
    return locals()

# Configurar rota OPTIONS para /eventos/default/eventos
# Esta é a chave para o funcionamento em Python 2.7
def _():
    from gluon.custom_import import track_changes
    track_changes(True)
    import gluon.http
    gluon.http.parse_options_uri('/eventos/default/eventos', eventos_options)

# Para testar o funcionamento, você pode adicionar esta rota:
def api_teste():
    """Página para testar a API de eventos"""
    set_cors_headers()  # Aplicar CORS mesmo na página de teste
    return dict(message="API de eventos está funcionando corretamente")
