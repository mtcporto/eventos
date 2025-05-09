# Solução para erro "invalid table/column name 'local' is a 'ALL' reserved SQL/NOSQL keyword"

Encontramos um erro no servidor web2py relacionado ao uso de uma palavra reservada SQL como nome de coluna. O web2py não permite o uso de palavras reservadas para os nomes de tabelas e colunas, e "local" é uma dessas palavras reservadas.

## O problema

O erro ocorreu porque o campo `local` na definição da tabela é uma palavra reservada em SQL:

```
<type 'exceptions.SyntaxError'> invalid table/column name "local" is a "ALL" reserved SQL/NOSQL keyword
```

Como bem lembrado, o criador do web2py, Massimo Di Pierro, adotava a convenção de usar prefixos `t_` para tabelas e `f_` para campos, justamente para evitar conflitos com palavras reservadas.

## A solução

Foram realizadas as seguintes alterações nos arquivos para resolver este problema:

1. **api_default_py2.py**:
   - Renomeada a tabela de `eventos` para `t_eventos`
   - Adicionado prefixo `f_` a todos os nomes de campos

```python
# Antes
db.eventos.insert(
    oque=dados['oque'],
    quando=dados['quando'],
    onde=dados['onde'],
    fonte=dados['fonte'],
    local=dados['local'],
    # ...
)

# Depois
db.t_eventos.insert(
    f_oque=dados['oque'],
    f_quando=dados['quando'],
    f_onde=dados['onde'],
    f_fonte=dados['fonte'],
    f_local=dados['local'],
    # ...
)
```

2. **Definição da tabela**:

```python
# Antes
db.define_table('eventos',
    Field('oque', 'string', required=True, label='O quê'),
    Field('quando', 'string', required=True, label='Quando'),
    # ...
    Field('local', 'string', required=True, label='Local'),
    # ...
)

# Depois
db.define_table('t_eventos',
    Field('f_oque', 'string', required=True, label='O quê'),
    Field('f_quando', 'string', required=True, label='Quando'),
    # ...
    Field('f_local', 'string', required=True, label='Local'),
    # ...
)
```

## Implementando no servidor

1. **Suba os arquivos atualizados para o servidor**:
   - Use o arquivo `api_default_py2.py` como base para o controller `default.py`
   - Crie o arquivo `models/eventos.py` com a definição correta da tabela

2. **Mapeamento dos dados no front-end**: 
   O front-end continua enviando dados com os nomes originais (sem o prefixo `f_`), e o controller é responsável pelo mapeamento correto.

3. **Se a tabela já existir no banco de dados**:
   - Faça backup dos dados
   - Crie a nova tabela com os nomes corretos
   - Migre os dados da tabela antiga para a nova

4. **Teste a API**:
   - Use o script `test_api_py2.py` para verificar se tudo está funcionando corretamente

## Lista de palavras reservadas comuns em SQL

Para evitar problemas futuros, aqui está uma lista de palavras reservadas comuns em SQL que devem ser evitadas como nomes de tabelas ou campos:

```
ADD, ALL, ALTER, AND, ANY, AS, ASC, AUTHORIZATION, BACKUP, BEGIN, BETWEEN, BREAK, 
BROWSE, BULK, BY, CASCADE, CASE, CHECK, CHECKPOINT, CLOSE, CLUSTERED, COALESCE, 
COLLATE, COLUMN, COMMIT, COMPUTE, CONSTRAINT, CONTAINS, CONTAINSTABLE, CONTINUE, 
CONVERT, CREATE, CROSS, CURRENT, CURRENT_DATE, CURRENT_TIME, CURRENT_TIMESTAMP, 
CURRENT_USER, CURSOR, DATABASE, DBCC, DEALLOCATE, DECLARE, DEFAULT, DELETE, DENY, 
DESC, DISK, DISTINCT, DISTRIBUTED, DOUBLE, DROP, DUMP, ELSE, END, ERRLVL, ESCAPE, 
EXCEPT, EXEC, EXECUTE, EXISTS, EXIT, EXTERNAL, FETCH, FILE, FILLFACTOR, FOR, FOREIGN, 
FREETEXT, FREETEXTTABLE, FROM, FULL, FUNCTION, GOTO, GRANT, GROUP, HAVING, HOLDLOCK, 
IDENTITY, IDENTITY_INSERT, IDENTITYCOL, IF, IN, INDEX, INNER, INSERT, INTERSECT, INTO, 
IS, JOIN, KEY, KILL, LEFT, LIKE, LINENO, LOAD, LOCAL, NATIONAL, NOCHECK, NONCLUSTERED, 
NOT, NULL, NULLIF, OF, OFF, OFFSETS, ON, OPEN, OPENDATASOURCE, OPENQUERY, OPENROWSET, 
OPENXML, OPTION, OR, ORDER, OUTER, OVER, PERCENT, PIVOT, PLAN, PRECISION, PRIMARY, 
PRINT, PROC, PROCEDURE, PUBLIC, RAISERROR, READ, READTEXT, RECONFIGURE, REFERENCES, 
REPLICATION, RESTORE, RESTRICT, RETURN, REVOKE, RIGHT, ROLLBACK, ROWCOUNT, ROWGUIDCOL, 
RULE, SAVE, SCHEMA, SECURITYAUDIT, SELECT, SEMANTICKEYPHRASETABLE, SEMANTICSIMILARITYDETAILSTABLE, 
SEMANTICSIMILARITYTABLE, SESSION_USER, SET, SETUSER, SHUTDOWN, SOME, STATISTICS, SYSTEM_USER, 
TABLE, TABLESAMPLE, TEXTSIZE, THEN, TO, TOP, TRAN, TRANSACTION, TRIGGER, TRUNCATE, 
TRY_CONVERT, TSEQUAL, UNION, UNIQUE, UNPIVOT, UPDATE, UPDATETEXT, USE, USER, VALUES, 
VARYING, VIEW, WAITFOR, WHEN, WHERE, WHILE, WITH, WITHIN GROUP, WRITETEXT
```

Ao usar o prefixo `t_` para tabelas e `f_` para campos, você evita problemas com palavras reservadas como foi o caso de `local`.
