// Endpoint equivalente ao 'eventos' no servidor web2py
// Arquivo: /api/eventos.js

const { MongoClient } = require('mongodb');

// URI de conexão com MongoDB (substitua pela sua própria)
const MONGODB_URI = process.env.MONGODB_URI || "mongodb+srv://user:password@cluster.mongodb.net/eventos";
const DB_NAME = 'eventos_db';

// Configuração do cliente MongoDB
let cachedClient = null;
let cachedDb = null;

// Função para conectar ao MongoDB
async function connectToDatabase() {
  if (cachedClient && cachedDb) {
    return { client: cachedClient, db: cachedDb };
  }

  const client = await MongoClient.connect(MONGODB_URI, { 
    useNewUrlParser: true, 
    useUnifiedTopology: true 
  });

  const db = client.db(DB_NAME);
  
  cachedClient = client;
  cachedDb = db;
  
  return { client, db };
}

// Função principal do handler da API
module.exports = async (req, res) => {
  // Configurar cabeçalhos CORS (não necessário se estiver no mesmo domínio)
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
      const { db } = await connectToDatabase();
      const eventos = await db
        .collection('eventos')
        .find({})
        .sort({ data_cadastro: -1 })
        .limit(100)
        .toArray();
        
      // Formatar resposta similar ao web2py
      const eventosFormatados = eventos.map(e => ({
        id: e._id.toString(),
        oque: e.oque,
        quando: e.quando,
        onde: e.onde,
        local: e.local,
        fonte: e.fonte
      }));
      
      return res.status(200).json({ eventos: eventosFormatados });
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
      
      // Preparar dados para inserção
      const novoEvento = {
        oque: dados.oque,
        quando: dados.quando,
        onde: dados.onde,
        fonte: dados.fonte,
        local: dados.local,
        imagem: dados.imagem || null,
        endereco: dados.endereco || null,
        preco: dados.preco || null,
        descricao: dados.descricao || null,
        tipo: dados.tipo || null,
        data_cadastro: new Date()
      };
      
      // Conectar e inserir no banco
      const { db } = await connectToDatabase();
      const resultado = await db.collection('eventos').insertOne(novoEvento);
      
      // Retornar resposta de sucesso
      return res.status(201).json({
        status: 'success',
        message: 'Evento cadastrado com sucesso',
        id: resultado.insertedId.toString()
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