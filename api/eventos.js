// Endpoint equivalente ao 'eventos' no servidor web2py
// Arquivo: /api/eventos.js

// Função principal do handler da API
module.exports = async (req, res) => {
  // Configurar cabeçalhos CORS
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept, Authorization');
  
  // Lidar com requisições OPTIONS (preflight)
  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }
  
  // GET: Lista todos os eventos
  if (req.method === 'GET') {
    try {
      // Responder com dados de exemplo
      const eventosExemplo = [
        {
          id: 'exemplo-1',
          oque: 'Show de Jazz',
          quando: '15/05/2025 20:00',
          onde: 'Porto Alegre',
          local: 'Auditório Araújo Vianna',
          fonte: 'Site Oficial'
        },
        {
          id: 'exemplo-2',
          oque: 'Festival de Cinema',
          quando: '20/05/2025 19:00',
          onde: 'Porto Alegre',
          local: 'Cinemateca Capitólio',
          fonte: 'Instagram Oficial'
        }
      ];
      
      return res.status(200).json({ eventos: eventosExemplo });
    } catch (error) {
      console.error('Erro ao buscar eventos:', error);
      return res.status(500).json({ 
        error: 'Erro ao buscar eventos', 
        details: error.message 
      });
    }
  }
  
  // POST: Adiciona um novo evento
  if (req.method === 'POST') {
    try {
      // Verificar se existem dados
      if (!req.body) {
        return res.status(400).json({ error: 'Nenhum dado recebido' });
      }
      
      const dados = req.body;
      
      // Validar campos obrigatórios
      const camposObrigatorios = ['oque', 'quando', 'onde', 'fonte', 'local'];
      for (const campo of camposObrigatorios) {
        if (!dados[campo]) {
          return res.status(400).json({
            error: `Campo obrigatório ausente ou vazio: ${campo}`
          });
        }
      }
      
      // Simular cadastro bem-sucedido (sem banco de dados real)
      console.log('Evento recebido:', dados);
      
      // Retornar resposta de sucesso
      return res.status(201).json({
        status: 'success',
        message: 'Evento cadastrado com sucesso',
        id: `id-${Date.now()}`
      });
      
    } catch (error) {
      console.error('Erro ao processar requisição de evento:', error);
      return res.status(500).json({
        error: `Erro ao processar requisição: ${error.message}`,
        details: error.stack
      });
    }
  }
  
  // Método não suportado
  return res.status(405).json({ 
    error: `Método ${req.method} não suportado` 
  });
};