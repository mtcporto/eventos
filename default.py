# -*- coding: utf-8 -*-
# Controlador default.py para o servidor Web2py em mtcporto.pythonanywhere.com
# Versão compatível com Python 2.7

# Configuração de CORS simples - igual ao Auralis
response.headers['Access-Control-Allow-Origin'] = '*'
response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
response.headers['Access-Control-Allow-Headers'] = 'Content-Type, X-Requested-With, Authorization'

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

# Função atualizada para lidar com upload de imagens como arquivos
def salvar_imagem():
    """
    Endpoint para upload de imagens
    POST: recebe um arquivo de imagem e salva no servidor
    """
    import os
    import uuid
    
    if request.env.request_method != 'POST':
        return response.json({
            'error': 'Método não suportado'
        }, status=405)
    
    # Verifica se foi enviado um arquivo
    if not request.files or not request.files.get('imagem'):
        return response.json({
            'error': 'Nenhuma imagem enviada'
        }, status=400)
    
    try:
        # Obter o arquivo enviado
        img_file = request.files.get('imagem')
        
        # Extrair a extensão e verificar se é uma imagem válida
        filename = img_file.filename
        extension = os.path.splitext(filename)[1].lower()
        
        if extension not in ['.jpg', '.jpeg', '.png', '.gif', '.webp']:
            return response.json({
                'error': 'Formato de imagem não suportado'
            }, status=400)
        
        # Gerar um nome único para a imagem
        img_name = f"{uuid.uuid4()}{extension}"
        
        # Diretório para salvar as imagens
        img_dir = os.path.join(request.folder, 'static', 'uploads')
        
        # Criar o diretório se não existir
        if not os.path.exists(img_dir):
            os.makedirs(img_dir)
        
        # Caminho completo do arquivo
        img_path = os.path.join(img_dir, img_name)
        
        # Salvar o arquivo
        img_file.save(img_path)
        
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
            # Processar imagem se for enviada como arquivo
            imagem_url = None
            if request.files and request.files.get('imagem'):
                try:
                    # Fazer upload da imagem usando a função salvar_imagem
                    resultado = salvar_imagem()
                    
                    if resultado and isinstance(resultado, dict) and 'url' in resultado:
                        imagem_url = resultado['url']
                except Exception as e:
                    # Em caso de erro no upload, não salvar a imagem
                    print("Erro ao processar imagem:", str(e))
            # Compatibilidade com formato base64 (código antigo)
            elif 'imagem' in data and data['imagem'] and isinstance(data['imagem'], str) and data['imagem'].startswith('data:'):
                try:
                    # Fazer upload da imagem usando a função antiga
                    temp_data = {'imagem': data['imagem']}
                    old_request_method = request.env.request_method
                    request.env.request_method = 'POST'
                    
                    # Usar a versão antiga da função só para compatibilidade
                    import base64
                    import uuid
                    import os
                    
                    img_data = data['imagem']
                    if ',' in img_data:
                        img_format = img_data.split(';')[0].split('/')[1]
                        img_data = img_data.split(',')[1]
                    else:
                        img_format = 'jpeg'
                    
                    img_name = f"{uuid.uuid4()}.{img_format}"
                    img_dir = os.path.join(request.folder, 'static', 'uploads')
                    
                    if not os.path.exists(img_dir):
                        os.makedirs(img_dir)
                    
                    img_path = os.path.join(img_dir, img_name)
                    
                    with open(img_path, 'wb') as f:
                        f.write(base64.b64decode(img_data))
                    
                    imagem_url = URL('static', 'uploads', img_name, host=True)
                    request.env.request_method = old_request_method
                except Exception as e:
                    print("Erro ao processar imagem base64:", str(e))
            elif 'imagem' in data:
                imagem_url = data['imagem']
            
            # Inserir no banco
            evento_id = db.t_eventos.insert(
                f_oque=data['oque'],
                f_quando=data['quando'],
                f_onde=data['onde'],
                f_fonte=data['fonte'],
                f_local=data['local'],
                f_imagem=imagem_url,
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
                    'imagem': e.f_imagem,
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
