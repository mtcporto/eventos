# Recomendações de Segurança para a API de Eventos (Compatível Python 2.7+)

Este documento fornece recomendações para melhorar a segurança da API de eventos quando em produção.

## 1. Restringir os Cabeçalhos CORS

Atualmente, a API permite requisições de qualquer origem (`*`). Em produção, restrinja para apenas os domínios necessários:

```python
def _set_cors_headers():
    # Verificar se a origem está na lista de origens permitidas
    origin = request.env.http_origin
    allowed_origins = ['https://seusite.com', 'http://localhost:8000']
    
    if origin in allowed_origins:
        response.headers['Access-Control-Allow-Origin'] = origin
    else:
        # Não adicionar o cabeçalho CORS se a origem não estiver na lista
        return
        
    response.headers['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept, Authorization'
    response.headers['Access-Control-Max-Age'] = '3600'
```

## 2. Implementar Autenticação

Adicione um sistema de autenticação, como tokens JWT ou chaves de API:

```python
def eventos():
    def POST(*args, **vars):
        # Verificar autenticação
        auth_header = request.env.http_authorization
        if not auth_header or not validate_api_key(auth_header):
            return response.json({'error': 'Não autorizado'}, status=401)
        
        # Continuar com o processamento...
```

Função de validação de chave:

```python
def validate_api_key(auth_header):
    # Formato esperado: "Bearer YOUR_API_KEY"
    if not auth_header.startswith('Bearer '):
        return False
    
    api_key = auth_header[7:]  # Remover "Bearer "
    
    # Verificar a chave API (em uma tabela de chaves válidas)
    valid_keys = db(db.api_keys.key == api_key).select().first()
    return valid_keys is not None
```

## 3. Limitar Taxa de Requisições (Rate Limiting)

Implemente limites de taxa para evitar sobrecarga do servidor:

```python
# No início do arquivo (módulo de cache global)
from gluon.contrib.redis_utils import RedisClient
import time

redis_client = RedisClient(host='localhost', port=6379, db=0)

def check_rate_limit(ip_address, limit=100, window=3600):
    """
    Verifica se um IP excedeu o limite de requisições
    limit: Máximo de requisições permitidas
    window: Período em segundos (default: 1 hora)
    """
    current_time = int(time.time())
    key = "rate_limit:{0}".format(ip_address)  # Formatação compatível com Python 2.7
    
    # Adicionar timestamp atual
    redis_client.zadd(key, {current_time: current_time})
    
    # Remover timestamps antigos (fora da janela de tempo)
    redis_client.zremrangebyscore(key, 0, current_time - window)
    
    # Verificar contagem
    count = redis_client.zcard(key)
    
    # Definir expiração do conjunto para evitar crescimento infinito
    redis_client.expire(key, window)
    
    # Retornar True se dentro do limite
    return count <= limit

# No controlador:
def eventos():
    def POST(*args, **vars):
        # Verificar limite de taxa
        client_ip = request.client
        if not check_rate_limit(client_ip, limit=50, window=3600):
            return response.json({
                'error': 'Limite de requisições excedido. Tente novamente mais tarde.'
            }, status=429)
        
        # Continuar processamento...
```

## 4. Validação de Dados Mais Rigorosa

Implemente validação mais rigorosa para os dados recebidos:

```python
def validate_evento(dados):
    """Valida os dados do evento mais rigorosamente"""
    errors = []
    
    # Validar tamanho dos campos
    if len(dados.get('oque', '')) > 200:
        errors.append("Campo 'oque' excede o tamanho máximo (200 caracteres)")
        
    # Validar formato de data/hora
    import re
    if not re.match(r'^\d{2}/\d{2}/\d{4} \d{2}:\d{2}$', dados.get('quando', '')):
        errors.append("Campo 'quando' deve estar no formato DD/MM/AAAA HH:MM")
    
    # Sanitizar dados para evitar XSS
    for campo in ['oque', 'onde', 'fonte', 'local', 'descricao']:
        if campo in dados:
            dados[campo] = sanitize_html(dados[campo])
    
    return errors, dados

# E no controlador:
def POST(*args, **vars):
    # ...
    errors, dados_sanitizados = validate_evento(dados)
    if errors:
        return response.json({'error': 'Erro de validação', 'details': errors}, status=400)
    # ...
```

## 5. Armazenamento de Imagens Otimizado

Ao invés de armazenar imagens como Base64 no banco de dados, considere:

1. Limitar o tamanho máximo da imagem recebida
2. Armazenar em um serviço de armazenamento como Amazon S3
3. Salvar apenas URLs no banco de dados

```python
def POST(*args, **vars):
    # ...
    # Se a imagem for muito grande
    if len(dados.get('imagem', '')) > 5000000:  # ~5MB
        return response.json({
            'error': 'Imagem muito grande. O tamanho máximo é 5MB.'
        }, status=400)
    
    # Processar/redimensionar a imagem e armazenar externamente
    if 'imagem' in dados and dados['imagem']:
        image_url = upload_to_storage(dados['imagem'])
        dados['imagem'] = image_url  # Substituir pelo URL
    # ...
```

## 6. Logs e Monitoramento

Adicione logs detalhados para diagnóstico e detecção de tentativas de ataque:

```python
def eventos():
    def POST(*args, **vars):
        start_time = time.time()
        client_ip = request.client
        
        try:
            # Processar normalmente...
            
            # Log de sucesso
            logger.info("API POST /eventos sucesso: IP={0}, Evento='{1}', Tempo={2:.2f}s".format(
                client_ip, dados['oque'], time.time()-start_time))
            
        except Exception as e:
            # Log detalhado do erro
            logger.error("API POST /eventos erro: IP={0}, Erro={1}, Tempo={2:.2f}s".format(
                client_ip, str(e), time.time()-start_time))
            # ...
```

## 7. Gerenciamento de Dependências

Mantenha todas as bibliotecas e o próprio Web2py atualizados para evitar vulnerabilidades conhecidas.

## Implementação Gradual

Estas medidas podem ser implementadas gradualmente, começando pelas mais críticas:

1. Primeiro: Validação rigorosa e sanitização de dados
2. Segundo: Restrição de CORS para origens específicas
3. Terceiro: Autenticação via chaves de API
4. Quarto: Rate limiting para evitar sobrecarga

Esta abordagem incremental melhora a segurança sem interromper o funcionamento da aplicação.
