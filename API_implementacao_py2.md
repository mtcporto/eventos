# Instruções para Implementação da API (Python 2.7)

Este documento contém instruções para implementar a API de eventos no servidor Web2py em mtcporto2.pythonanywhere.com, que executa Python 2.7.

## Arquivos necessários

Os seguintes arquivos devem ser carregados para o servidor:

1. **Controller** (`controllers/default.py`): 
   - Use o conteúdo do arquivo `api_default_py2.py` que já está compatível com Python 2.7.

2. **Modelo de dados** (`models/eventos.py`):
   ```python
   # -*- coding: utf-8 -*-
   # Definição da tabela eventos no banco de dados
   # Utilizamos prefixo t_ para tabelas e f_ para campos para evitar palavras reservadas SQL
   db.define_table('t_eventos',
       Field('f_oque', 'string', required=True, label='O quê'),
       Field('f_quando', 'string', required=True, label='Quando'),
       Field('f_onde', 'string', required=True, label='Onde'),
       Field('f_fonte', 'string', required=True, label='Fonte'),
       Field('f_local', 'string', required=True, label='Local'), # 'local' é palavra reservada em SQL
       Field('f_imagem', 'text', label='Imagem'),
       Field('f_endereco', 'string', label='Endereço'),
       Field('f_preco', 'string', label='Preço'),
       Field('f_descricao', 'text', label='Descrição'),
       Field('f_tipo', 'string', label='Tipo de Evento'),
       Field('f_data_cadastro', 'datetime', default=request.now, label='Data de Cadastro')
   )
   ```

## Passos para implementação

1. Acesse o painel de controle do PythonAnywhere em: https://www.pythonanywhere.com

2. Faça login na sua conta (mtcporto2).

3. Abra o console bash e navegue até a pasta do aplicativo web2py:
   ```bash
   cd /home/mtcporto2/web2py
   ```

4. Navegue até a pasta do aplicativo "eventos":
   ```bash
   cd applications/eventos
   ```

5. Backup dos arquivos existentes (se necessário):
   ```bash
   cp controllers/default.py controllers/default.py.bak
   ```

6. Crie ou edite os arquivos necessários:

   **controllers/default.py**:
   ```bash
   nano controllers/default.py
   ```
   Cole o conteúdo do arquivo `api_default_py2.py` e salve (Ctrl+O, Enter, Ctrl+X).

   **models/eventos.py**:
   ```bash
   nano models/eventos.py
   ```
   Cole o código do modelo de dados e salve.

7. Verifique as permissões dos arquivos:
   ```bash
   chmod 644 controllers/default.py models/eventos.py
   ```

8. Reinicie o aplicativo web2py no painel de controle do PythonAnywhere.

## Testando a implementação

Use o script `test_api_py2.py` para testar a API:

1. No seu ambiente local:
   ```bash
   python test_api_py2.py
   ```

2. Verifique se:
   - O teste CORS retorna os cabeçalhos corretos
   - O GET retorna a lista de eventos (se houver)
   - O POST insere um novo evento corretamente

3. Se você receber um erro, verifique os logs do aplicativo no painel de controle do PythonAnywhere.

## Problemas comuns e soluções

1. **Erro de sintaxe Python**: Se aparecer um erro mencionando "SyntaxError: invalid syntax" na linha com `f"..."`, isso indica que o arquivo ainda contém f-strings (Python 3.6+) ao invés do formato Python 2.7. Certifique-se de usar `'texto {0}'.format(variavel)` em vez de `f'texto {variavel}'`.

2. **Erro de CORS**: Se o aplicativo web estiver recebendo erro de CORS, verifique se as funções `_set_cors_headers()` e `options()` estão devidamente implementadas no controller.

3. **Erro 500 Internal Server Error**: Verifique os logs de erro do web2py para detalhes. Geralmente isso está relacionado a:
   - Sintaxe incompatível com Python 2.7
   - Falta de uma dependência
   - Problema com a definição do banco de dados

4. **Tabela "eventos" não existe**: Execute a migração do banco de dados através do painel admin do web2py ou recarregue o aplicativo completamente.

## Considerações de segurança

Para aumentar a segurança da sua API em produção, consulte o arquivo `API_seguranca_py2.md` com recomendações compatíveis com Python 2.7.

## Próximos passos

1. Implemente validações mais robustas para os dados recebidos
2. Restrinja os cabeçalhos CORS apenas para origens específicas
3. Adicione autenticação à API
4. Implemente mecanismos de caching para melhorar desempenho
