# -*- coding: utf-8 -*-
# Controlador default.py para o servidor Web2py em mtcporto.pythonanywhere.com
# Versão compatível com Python 3

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

# Definição da tabela t_eventos com campo f_imagem alterado para tipo 'upload'
db.define_table('t_eventos',
    Field('f_oque', 'string', label='O que'),
    Field('f_quando', 'datetime', label='Quando'),
    Field('f_onde', 'string', label='Onde'),
    Field('f_local', 'string', label='Local'),
    Field('f_imagem', 'upload', label='Imagem'),  # Alterado de 'text' para 'upload'
    Field('f_fonte', 'string', label='Fonte'),
    Field('f_endereco', 'string', label='Endereço'),
    Field('f_preco', 'string', label='Preço'),
    Field('f_descricao', 'text', label='Descrição'),
    Field('f_tipo', 'string', label='Tipo')
)

# Endpoint para eventos - estruturado como os endpoints do Auralis
def eventos():
    """
    API para eventos
    GET: lista eventos
    POST: adiciona evento
    """
    # Para requisições OPTIONS (preflight CORS)
    if request.env.request_method == 'OPTIONS':
        return {}
    
    # Para requisições POST
    elif request.env.request_method == 'POST':
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
                f_imagem=data.get('imagem', None),  # Armazena a imagem do cartaz do evento
                f_endereco=data.get('endereco', None),
                f_preco=data.get('preco', None),
                f_descricao=data.get('descricao', None),
                f_tipo=data.get('tipo', None),
            )
            
            # Commit explícito
            db.commit()
            
            return response.json({
                'status': 'ok',
                'id': evento_id
            })
        
        except Exception as e:
            # Rollback em caso de erro
            db.rollback()
            import traceback
            
            # Log detalhado do erro
            tb = traceback.format_exc()
            print(tb)
            
            return response.json({
                'status': 'error',
                'message': str(e),
                'traceback': tb
            }, status=500)
    
    # Para requisições GET - listar eventos
    elif request.env.request_method == 'GET':
        try:
            # Query padrão
            query = (db.t_eventos.id > 0)
            
            # Pega resultados do banco
            eventos = db(query).select(orderby=~db.t_eventos.id)
            
            # Formata saída
            resultado = []
            for e in eventos:
                resultado.append({
                    'id': e.id,
                    'oque': e.f_oque,
                    'quando': e.f_quando,
                    'onde': e.f_onde,
                    'local': e.f_local,
                    'fonte': e.f_fonte,
                    'imagem': e.f_imagem,  # Inclui a imagem na resposta
                    'endereco': e.f_endereco,
                    'preco': e.f_preco,
                    'descricao': e.f_descricao,
                    'tipo': e.f_tipo
                })
            
            # Retorna JSON com resultados no formato esperado pelo frontend
            return response.json({
                'eventos': resultado
            })
        
        except Exception as e:
            import traceback
            
            # Log detalhado do erro
            tb = traceback.format_exc()
            print(tb)
            
            return response.json({
                'status': 'error',
                'message': str(e),
                'traceback': tb
            }, status=500)
    
    # Método não suportado
    else:
        return response.json({
            'error': 'Método não suportado'
        }, status=405)

# Para testar o funcionamento
def api_teste():
    """Página para testar a API de eventos"""
    return dict(message="API de eventos está funcionando corretamente")
