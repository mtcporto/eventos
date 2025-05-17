# -*- coding: utf-8 -*-
# Controlador default.py para o servidor Web2py em mtcporto.pythonanywhere.com
from gluon.contenttype import contenttype
import os
import traceback
import base64
import uuid
import json
from gluon import current

db = current.globalenv['db']

# Configure global CORS - web2py automatically includes response and request objects
def index():
    # Define CORS headers for all responses
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, X-Requested-With, Authorization'
    return dict(message="API de eventos está funcionando corretamente")

# Helper function to set CORS headers for each response
def _set_cors_headers():
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, X-Requested-With, Authorization'

# Get request data from JSON or POST vars
def get_request_data():
    try:
        # Try to get data from request.json
        data = request.json
        if data:
            return data
    except Exception as e:
        print(f"Erro ao decodificar JSON: {str(e)}")
        
    try:
        # If JSON parsing fails, try to read the raw body and parse it manually
        import json
        body = request.body.read().decode('utf-8')
        if body:
            print(f"Tentando decodificar manualmente: {body[:200]}")
            data = json.loads(body)
            return data
    except Exception as e:
        print(f"Erro ao decodificar manualmente: {str(e)}")
        
    # Finally, fall back to form vars or empty dict
    return request.vars or {}

# Handle OPTIONS request for CORS preflight
def options():
    _set_cors_headers()
    return {}

# Convert date format for consistency
def converter_formato_data(data_str):
    from datetime import datetime
    try:
        if '/' in data_str:
            if ' ' in data_str:
                data_parte, hora_parte = data_str.split(' ', 1)
                dia, mes, ano = data_parte.split('/')
                return f"{ano}-{mes}-{dia} {hora_parte}"
            else:
                dia, mes, ano = data_str.split('/')
                return f"{ano}-{mes}-{dia}"
        return data_str
    except Exception as e:
        print(f"Erro ao converter data: {e}")
        return data_str

# Save base64 image and return filename
def _save_base64_image(base64_data):
    """
    Função auxiliar para salvar uma imagem base64 no servidor
    Retorna o nome do arquivo salvo
    """
    try:
        # Verificar se a string base64 parece válida
        if not base64_data or not isinstance(base64_data, str):
            print("Dados base64 inválidos")
            return None
            
        # Remover prefixo data:image se existir
        if ',' in base64_data:
            header, base64_data = base64_data.split(',', 1)
            # Detectar extensão da imagem a partir do cabeçalho
            if 'image/jpeg' in header:
                ext = 'jpg'
            elif 'image/png' in header:
                ext = 'png'
            else:
                ext = 'jpg'  # Padrão se não conseguir detectar
        else:
            ext = 'jpg'  # Padrão se não tiver cabeçalho
            
        # Decodificar os dados base64
        try:
            image_data = base64.b64decode(base64_data)
        except Exception as e:
            print(f"Erro ao decodificar base64: {e}")
            return None
            
        # Gerar um nome único para o arquivo
        filename = f"{uuid.uuid4()}.{ext}"
        filepath = os.path.join(request.folder, 'uploads', filename)
        
        # Salvar o arquivo
        with open(filepath, 'wb') as f:
            f.write(image_data)
            
        print(f"Imagem base64 salva como: {filename}")
        return filename
    except Exception as e:
        print(f"Erro ao salvar imagem base64: {e}")
        print(traceback.format_exc())
        return None

# Serve image from uploads folder
def imagem():
    _set_cors_headers()

    nome_arquivo = request.args(0)
    if not nome_arquivo:
        response.status = 400
        return response.json({'error': 'Arquivo não especificado'})

    caminho = os.path.join(request.folder, 'uploads', nome_arquivo)

    if not os.path.isfile(caminho):
        response.status = 404
        return response.json({'error': 'Arquivo não encontrado'})

    response.headers['Content-Type'] = contenttype(nome_arquivo)
    return open(caminho, 'rb').read()

# Handle image upload (legacy endpoint, now using base64)
def upload_imagem():
    try:
        _set_cors_headers()
        if request.env.request_method == 'OPTIONS':
            return {}
        elif request.env.request_method == 'POST':
            # Log para debug (sem imprimir conteúdo de request.vars que pode ser muito grande)
            print("POST recebido para upload_imagem")
            print(f"Content-Type: {request.env.http_content_type}")
            
            # Verificar se a chave 'imagem' existe nas variáveis sem imprimir o conteúdo completo
            print(f"Chaves em request.vars: {list(request.vars.keys())}")
            
            # Em vez de usar request.vars.get(), acessamos diretamente a lista vars
            if 'imagem' in request.vars:
                imagem = request.vars['imagem']
                print("Imagem encontrada nas vars")
                
                # Verificar se é um objeto de arquivo (sem usar operador 'and' com objeto de arquivo)
                if hasattr(imagem, 'filename'):
                    print(f"Nome do arquivo: {imagem.filename}")
                    ext = imagem.filename.split('.')[-1].lower()
                    print(f"Extensão: {ext}")
                    
                    if ext not in ['jpg', 'jpeg', 'png']:
                        response.status = 400
                        return response.json({'error': f'Formato não permitido: {ext}'})
                    try:
                        print("Antes de salvar arquivo")
                        nome = db.t_eventos.f_imagem.store(imagem.file, imagem.filename)
                        print(f"Arquivo salvo como: {nome}")
                        return response.json({'status': 'ok', 'nome_arquivo': nome})
                    except Exception as store_error:
                        print(f"Erro ao salvar arquivo: {store_error}")
                        print(traceback.format_exc())
                        raise # Re-lança a exceção para ser capturada pelo bloco de exceção externo
                else:
                    print("Campo imagem existe, mas não é um objeto de arquivo")
                    response.status = 400
                    return response.json({'error': 'Imagem não é um arquivo válido'})
            else:
                print("Campo 'imagem' não encontrado na requisição")
                response.status = 400
                return response.json({'error': 'Campo imagem não enviado na requisição'})
        else:
            response.status = 405
            return response.json({'error': 'Método não suportado'})
    except Exception as e:
        _set_cors_headers()
        print(f"Exceção em upload_imagem: {str(e)}")
        print(traceback.format_exc())
        response.status = 500
        return response.json({'error': 'Erro interno', 'message': str(e)})

# Main endpoint to handle events
def eventos():
    # Always set CORS headers first for every request
    _set_cors_headers()

    try:
        if request.env.request_method == 'OPTIONS':
            return {}
        elif request.env.request_method == 'POST':
            # Add debugging logs to inspect request body and headers
            try:
                if request.env.request_method == 'POST':
                    # Debugging logs
                    import logging
                    logging.basicConfig(filename='/tmp/backend_debug.log', level=logging.DEBUG)
                    logging.debug(f"Headers: {request.env.http_headers}")
                    logging.debug(f"Body: {request.body.read()}")
                    request.body.seek(0)  # Reset body stream after reading

                    data = get_request_data()

                    if not data:
                        response.status = 400
                        return response.json({'error': 'Dados não recebidos na requisição'})

                    # ...existing code...

            except Exception as e:
                import logging
                logging.basicConfig(filename='/tmp/backend_debug.log', level=logging.ERROR)
                logging.error(f"Exception: {str(e)}")
                raise

            data = get_request_data()

            if not data:
                response.status = 400
                return response.json({'error': 'Dados não recebidos na requisição'})

            campos_obrigatorios = ['oque', 'quando', 'onde', 'fonte', 'local']
            for campo in campos_obrigatorios:
                if campo not in data or not data[campo]:
                    response.status = 400
                    return response.json({'error': f"Campo obrigatório ausente ou vazio: {campo}"})

            nome_imagem = None
            if 'imagem_base64' in data and data['imagem_base64']:
                nome_imagem = _save_base64_image(data['imagem_base64'])

            try:
                quando_convertido = converter_formato_data(data['quando'])
                evento_id = db.t_eventos.insert(
                    f_oque=data['oque'],
                    f_quando=quando_convertido,
                    f_onde=data['onde'],
                    f_fonte=data['fonte'],
                    f_local=data['local'],
                    f_imagem=data.get('imagem', nome_imagem),
                    f_endereco=data.get('endereco'),
                    f_preco=data.get('preco'),
                    f_descricao=data.get('descricao'),
                    f_tipo=data.get('tipo')
                )
                db.commit()
                return response.json({'status': 'ok', 'id': evento_id})
            except Exception as e:
                db.rollback()
                response.status = 500
                return response.json({'status': 'error', 'message': str(e)})
        elif request.env.request_method == 'GET':
            try:
                query = (db.t_eventos.id > 0)
                eventos = db(query).select(orderby=~db.t_eventos.id)
                resultado = [{
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
                } for e in eventos]
                return response.json({'eventos': resultado})
            except Exception as e:
                response.status = 500
                return response.json({'status': 'error', 'message': str(e)})
        else:
            response.status = 405
            return response.json({'error': 'Método não suportado'})
    except Exception as e:
        response.status = 500
        return response.json({'error': 'Erro interno', 'message': str(e)})

def api_teste():
    _set_cors_headers()
    return dict(message="API de eventos está funcionando corretamente")
