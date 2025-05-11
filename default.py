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

# Função para converter formato de data DD/MM/YYYY para YYYY-MM-DD
def converter_formato_data(data_str):
    from datetime import datetime
    try:
        # Verificar se tem formato DD/MM/YYYY ou DD/MM/YYYY HH:MM
        if '/' in data_str:
            if ' ' in data_str:  # Se tem hora
                data_parte, hora_parte = data_str.split(' ', 1)
                dia, mes, ano = data_parte.split('/')
                # Formatar como YYYY-MM-DD HH:MM
                return f"{ano}-{mes}-{dia} {hora_parte}"
            else:  # Se tem só data
                dia, mes, ano = data_str.split('/')
                # Formatar como YYYY-MM-DD
                return f"{ano}-{mes}-{dia}"
        return data_str  # Retorna sem modificar se não for no formato esperado
    except Exception as e:
        print(f"Erro ao converter data: {e}")
        return data_str

# Função para processar imagem base64 para o formato correto de upload
def processar_imagem_base64(imagem_base64):
    import base64
    import os
    import uuid
    from io import BytesIO
    
    if not imagem_base64:
        return None
        
    try:
        # Verificar se é uma string base64
        if isinstance(imagem_base64, str) and imagem_base64.startswith('data:'):
            # Extrair tipo e dados
            formato, dados_base64 = imagem_base64.split(',', 1)
            
            # Determinar extensão do arquivo
            extensao = 'png'  # extensão padrão
            if 'jpeg' in formato or 'jpg' in formato:
                extensao = 'jpg'
            elif 'png' in formato:
                extensao = 'png'
            
            # Decodificar dados base64
            dados_imagem = base64.b64decode(dados_base64)
            
            # Criar nome de arquivo único
            nome_arquivo = f"evento_{uuid.uuid4().hex}.{extensao}"
            
            # Retornar tupla no formato esperado pelo campo upload
            return (BytesIO(dados_imagem), nome_arquivo)
    except Exception as e:
        print(f"Erro ao processar imagem base64: {e}")
    
    return imagem_base64  # Retornar original se não for base64 ou ocorrer erro


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
            # Converter formato da data se necessário
            quando_convertido = converter_formato_data(data['quando'])
            
            # Processar imagem se presente
            imagem_processada = processar_imagem_base64(data.get('imagem', None))
            
            # Inserir no banco
            evento_id = db.t_eventos.insert(
                f_oque=data['oque'],
                f_quando=quando_convertido,  # Usar data convertida
                f_onde=data['onde'],
                f_fonte=data['fonte'],
                f_local=data['local'],
                f_imagem=imagem_processada,  # Usar imagem processada
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
