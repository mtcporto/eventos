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

# Função para salvar uma imagem enviada
def salvar_imagem():
    """
    Endpoint para upload de imagens
    POST: recebe uma imagem e salva no servidor
    """
    import os
    import uuid
    import base64
    
    if request.env.request_method != 'POST':
        return response.json({
            'error': 'Método não suportado'
        }, status=405)
    
    data = get_request_data()
    
    if 'imagem' not in data or not data['imagem']:
        return response.json({
            'error': 'Imagem não fornecida'
        }, status=400)
    
    try:
        # Obter a string base64 da imagem
        img_data = data['imagem']
        
        # Verificar se é realmente uma string base64
        if ',' in img_data:
            # Formato: data:image/jpeg;base64,/9j/4AAQSkZJRg...
            img_format = img_data.split(';')[0].split('/')[1]
            img_data = img_data.split(',')[1]
        else:
            # Assumir formato jpeg para compatibilidade
            img_format = 'jpeg'
        
        # Gerar um nome único para a imagem
        img_name = f"{uuid.uuid4()}.{img_format}"
        
        # Diretório para salvar as imagens
        img_dir = os.path.join(request.folder, 'static', 'uploads')
        
        # Criar o diretório se não existir
        if not os.path.exists(img_dir):
            os.makedirs(img_dir)
        
        # Caminho completo do arquivo
        img_path = os.path.join(img_dir, img_name)
        
        # Decodificar e salvar a imagem
        with open(img_path, 'wb') as f:
            f.write(base64.b64decode(img_data))
        
        # URL relativa para a imagem
        img_url = URL('static', 'uploads', img_name, host=True)
        
        return response.json({
            'status': 'ok',
            'url': img_url
        })
    
    except Exception as e:
        import traceback
        tb = traceback.format_exc()
        
        return response.json({
            'status': 'error',
            'message': str(e),
            'traceback': tb
        }, status=500)

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
            # Processar imagem se estiver em formato base64
            imagem_url = data.get('imagem', None)
            if imagem_url and imagem_url.startswith('data:'):
                try:
                    # Fazer upload da imagem usando a função salvar_imagem
                    temp_data = {'imagem': imagem_url}
                    old_request_method = request.env.request_method
                    request.env.request_method = 'POST'
                    resultado = salvar_imagem()
                    request.env.request_method = old_request_method  # Restaurar método original
                    
                    if resultado and isinstance(resultado, dict) and 'url' in resultado:
                        imagem_url = resultado['url']
                    else:
                        # Falha no upload, não salvar a imagem
                        imagem_url = None
                except Exception as e:
                    # Em caso de erro no upload, não salvar a imagem
                    print("Erro ao processar imagem:", str(e))
                    imagem_url = None
            
            # Inserir no banco
            evento_id = db.t_eventos.insert(
                f_oque=data['oque'],
                f_quando=data['quando'],
                f_onde=data['onde'],
                f_fonte=data['fonte'],
                f_local=data['local'],
                f_imagem=imagem_url,  # Agora sempre salva a URL da imagem
                f_endereco=data.get('endereco', None),
                f_preco=data.get('preco', None),
                f_descricao=data.get('descricao', None),
                f_tipo=data.get('tipo', None),
            )
            
            # Commit explícito
            db.commit()
            
            return response.json({
                'status': 'ok',
                'id': evento_id,
                'imagem_url': imagem_url
            })
        
        except Exception as e:
            # Rollback em caso de erro
            db.rollback()
            import sys
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
                    'imagem': e.f_imagem,  # Agora sempre será uma URL
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
            import sys
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
