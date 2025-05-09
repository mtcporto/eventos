# -*- coding: utf-8 -*-
# Controlador default.py para o servidor Web2py em mtcporto2.pythonanywhere.com
# Versão compatível com Python 2.7 e 3+
# Adicione este código ao seu arquivo controllers/default.py existente

# Configuração de CORS para permitir requisições do seu domínio local
def _set_cors_headers():
    """Define cabeçalhos CORS para permitir requisições de origens externas"""
    response.headers['Access-Control-Allow-Origin'] = '*'  # Permite de qualquer origem - Restrinja em produção
    response.headers['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept, Authorization'
    response.headers['Access-Control-Max-Age'] = '3600'  # Cache por 1 hora

# Endpoint OPTIONS para lidar com preflight requests do CORS
def options():
    """Responde a requisições OPTIONS do CORS preflight"""
    _set_cors_headers()
    return response.json({'status': 'ok'})

# Endpoint principal para receber eventos
@request.restful()
def eventos():
    """
    API para receber eventos extraídos de imagens.
    
    GET: Lista todos os eventos cadastrados
    POST: Adiciona um novo evento
    """
    def POST(*args, **vars):
        # Configura CORS
        _set_cors_headers()
        
        # Verifica se a requisição tem corpo JSON
        try:
            # Ler dados do corpo da requisição
            dados = request.json
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
        # Configura CORS
        _set_cors_headers()
        
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
    
    # Retorna apenas estes métodos
    return locals()

# Modelo de dados necessário para o web2py
# Adicione isto ao seu models/db.py ou crie um arquivo models/eventos.py

"""
# Definição da tabela eventos no banco de dados
db.define_table('t_eventos',
    Field('f_oque', 'string', required=True, label='O quê'),
    Field('f_quando', 'string', required=True, label='Quando'),
    Field('f_onde', 'string', required=True, label='Onde'),
    Field('f_fonte', 'string', required=True, label='Fonte'),
    Field('f_local', 'string', required=True, label='Local'),
    Field('f_imagem', 'text', label='Imagem'),
    Field('f_endereco', 'string', label='Endereço'),
    Field('f_preco', 'string', label='Preço'),
    Field('f_descricao', 'text', label='Descrição'),
    Field('f_tipo', 'string', label='Tipo de Evento'),
    Field('f_data_cadastro', 'datetime', default=request.now, label='Data de Cadastro')
"""

# Para testar o funcionamento, você pode adicionar esta rota:
def api_teste():
    """Página para testar a API de eventos"""
    return dict(message="API de eventos está funcionando corretamente")
