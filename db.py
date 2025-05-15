# Definição da tabela t_eventos com campo f_imagem alterado para tipo 'upload'
db.define_table('t_eventos',
    Field('f_oque', 'string', label='O que'),
    Field('f_quando', 'datetime', label='Quando'),
    Field('f_onde', 'string', label='Onde'),    Field('f_local', 'string', label='Local'),
    Field('f_imagem', 'text', label='Imagem'),  # Alterado de 'upload' para 'text' para suportar base64
    Field('f_fonte', 'string', label='Fonte'),
    Field('f_endereco', 'string', label='Endereço'),
    Field('f_preco', 'string', label='Preço'),
    Field('f_descricao', 'text', label='Descrição'),
    Field('f_tipo', 'string', label='Tipo')
)