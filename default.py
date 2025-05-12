# -*- coding: utf-8 -*-
# Controlador default.py para o servidor Web2py em mtcporto.pythonanywhere.com
# Versão compatível com Python 3

# Configuração de CORS - aplicada a TODAS as respostas
def _set_cors_headers():
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, X-Requested-With, Authorization'

# Aplicar CORS para todas as requisições
_set_cors_headers()

# Função auxiliar para obter dados da requisição
def get_request_data():
    try:
        return request.json
    except:
        return request.vars or {}

# Endpoint OPTIONS básico
def options():
    _set_cors_headers()
    return {}

# Função para converter formato de data DD/MM/YYYY para YYYY-MM-DD
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

# Servir imagem de evento com CORS liberado
def imagem():
    _set_cors_headers()
    import os
    from gluon.contenttype import contenttype

    nome_arquivo = request.args(0)
    if not nome_arquivo:
        response.status = 400
        return response.json({'error': 'Arquivo não especificado'})

    caminho = os.path.join(request.folder, 'uploads', nome_arquivo)

    if not os.path.isfile(caminho):
        response.status = 404
        return response.json({'error': 'Arquivo não encontrado'})

    response.headers['Content-Type'] = contenttype(nome_arquivo)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return open(caminho, 'rb').read()


def eventos():
    if request.env.request_method == 'OPTIONS':
        _set_cors_headers()
        return {}

    elif request.env.request_method == 'POST':
        _set_cors_headers()
        data = get_request_data()

        # Validar campos obrigatórios
        campos_obrigatorios = ['oque', 'quando', 'onde', 'fonte', 'local']
        for campo in campos_obrigatorios:
            if campo not in data or not data[campo]:
                response.status = 400
                return response.json({
                    'error': f"Campo obrigatório ausente ou vazio: {campo}"
                })

        try:
            import uuid
            quando_convertido = converter_formato_data(data['quando'])
            imagem_upload = data.get('imagem')
            nome_arquivo_imagem = None

            # Validação e renomeação segura da imagem (caso enviada)
            if imagem_upload and hasattr(imagem_upload, 'filename'):
                ext = imagem_upload.filename.split('.')[-1].lower()
                if ext not in ['jpg', 'jpeg', 'png']:
                    response.status = 400
                    return response.json({'error': 'Formato de imagem não permitido'})

                # Gera nome único
                nome_arquivo_imagem = f"evento_{uuid.uuid4().hex}.{ext}"
                imagem_upload.filename = nome_arquivo_imagem

            evento_id = db.t_eventos.insert(
                f_oque=data['oque'],
                f_quando=quando_convertido,
                f_onde=data['onde'],
                f_fonte=data['fonte'],
                f_local=data['local'],
                f_imagem=imagem_upload,  # Salva com novo nome
                f_endereco=data.get('endereco'),
                f_preco=data.get('preco'),
                f_descricao=data.get('descricao'),
                f_tipo=data.get('tipo')
            )

            db.commit()
            return response.json({
                'status': 'ok',
                'id': evento_id,
                'imagem': nome_arquivo_imagem  # ← retorna nome do arquivo
            })

        except Exception as e:
            db.rollback()
            import traceback
            tb = traceback.format_exc()
            print(tb)
            response.status = 500
            return response.json({
                'status': 'error',
                'message': str(e),
                'traceback': tb
            })

    elif request.env.request_method == 'GET':
        try:
            query = (db.t_eventos.id > 0)
            eventos = db(query).select(orderby=~db.t_eventos.id)

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

            return response.json({'eventos': resultado})

        except Exception as e:
            import traceback
            tb = traceback.format_exc()
            print(tb)
            response.status = 500
            return response.json({
                'status': 'error',
                'message': str(e),
                'traceback': tb
            })

    else:
        response.status = 405
        return response.json({'error': 'Método não suportado'})


# Página de teste da API
def api_teste():
    return dict(message="API de eventos está funcionando corretamente")
