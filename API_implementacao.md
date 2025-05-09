# API de Eventos - Documentação de Implementação

Este documento descreve como implementar a API para receber os eventos extraídos pela aplicação do Mini Agente de Eventos.

## Pré-requisitos

- Ambiente Web2py funcionando em mtcporto2.pythonanywhere.com
- Acesso ao diretório de aplicação `eventos`

## Arquivos a Modificar

### 1. Modelo de Dados (models/db.py ou models/eventos.py)

Adicione a definição da tabela `eventos` ao seu modelo de dados:

```python
# Definição da tabela eventos no banco de dados
db.define_table('eventos',
    Field('oque', 'string', required=True, label='O quê'),
    Field('quando', 'string', required=True, label='Quando'),
    Field('onde', 'string', required=True, label='Onde'),
    Field('fonte', 'string', required=True, label='Fonte'),
    Field('local', 'string', required=True, label='Local'),
    Field('imagem', 'text', label='Imagem'),
    Field('endereco', 'string', label='Endereço'),
    Field('preco', 'string', label='Preço'),
    Field('descricao', 'text', label='Descrição'),
    Field('tipo', 'string', label='Tipo de Evento'),
    Field('data_cadastro', 'datetime', default=request.now, label='Data de Cadastro')
)
```

### 2. Controlador (controllers/default.py)

Adicione as funções para a API no controlador:

```python
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
                        'error': f'Campo obrigatório ausente ou vazio: {campo}'
                    }, status=400)
            
            # Preparar dados para inserção
            evento_id = db.eventos.insert(
                oque=dados['oque'],
                quando=dados['quando'],
                onde=dados['onde'],
                fonte=dados['fonte'],
                local=dados['local'],
                imagem=dados.get('imagem', None),  # Campo opcional
                endereco=dados.get('endereco', None),  # Campo opcional
                preco=dados.get('preco', None),  # Campo opcional
                descricao=dados.get('descricao', None),  # Campo opcional
                tipo=dados.get('tipo', None),  # Campo opcional
                data_cadastro=datetime.datetime.now()
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
            logger.error(f"Erro ao processar requisição de evento: {str(e)}")
            
            # Rollback em caso de erro
            db.rollback()
            
            # Retornar erro
            return response.json({
                'error': f'Erro ao processar requisição: {str(e)}',
                'details': traceback.format_exc()
            }, status=500)
    
    def GET(*args, **vars):
        # Configura CORS
        _set_cors_headers()
        
        # Lista eventos limitados aos 100 mais recentes
        eventos = db(db.eventos).select(
            orderby=~db.eventos.data_cadastro,
            limitby=(0, 100)
        )
        
        # Formatar para JSON
        return response.json({
            'eventos': [{'id': e.id,
                        'oque': e.oque,
                        'quando': e.quando,
                        'onde': e.onde,
                        'local': e.local,
                        'fonte': e.fonte} 
                       for e in eventos]
        })
    
    # Retorna apenas estes métodos
    return locals()
```

## Observações de Implementação

1. **CORS**: A implementação atual permite requisições de qualquer origem (`*`). Em um ambiente de produção, você deve restringir isso aos domínios específicos que precisam acessar a API.

2. **Dados de Imagem**: O campo `imagem` está configurado como texto para armazenar URLs ou dados base64. Para imagens grandes, considere usar um serviço de armazenamento externo e armazenar apenas a URL.

3. **Validação**: A implementação atual faz uma validação básica dos campos obrigatórios. Você pode expandir isso para validar formatos específicos (como datas) se necessário.

4. **Segurança**: Em um ambiente de produção, você deve implementar autenticação para proteger o endpoint de escrita da API.

## Testando a API

Você pode testar a API usando curl ou ferramentas como Postman:

```bash
# Listar eventos existentes
curl -X GET https://mtcporto2.pythonanywhere.com/eventos/default/eventos

# Adicionar um novo evento
curl -X POST \
  https://mtcporto2.pythonanywhere.com/eventos/default/eventos \
  -H 'Content-Type: application/json' \
  -d '{
    "oque": "Teste de API",
    "quando": "10/05/2025 19:00",
    "onde": "João Pessoa",
    "fonte": "General Store",
    "local": "Centro Cultural"
  }'
```

## Suporte

Se encontrar problemas na implementação da API, verifique os logs do web2py para diagnosticar erros específicos.
