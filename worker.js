export default {
    async fetch(request, env, ctx) {
      const targetUrl = 'https://mtcporto.pythonanywhere.com/eventos/default/eventos';
  
      if (request.method === 'OPTIONS') {
        return new Response(null, {
          status: 204,
          headers: {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type, X-Requested-With, Authorization',
            'Access-Control-Max-Age': '86400'
          }
        });
      }
  
      // Clona o corpo da requisição como um buffer (útil para FormData e multipart)
      const reqClone = request.clone();
      const body = await reqClone.arrayBuffer();
  
      // Reencaminha com os mesmos headers e corpo intacto
      const response = await fetch(targetUrl, {
        method: request.method,
        headers: request.headers,
        body: body,
        redirect: 'follow'
      });
  
      // Lê resposta como buffer para manter arquivos binários
      const responseBody = await response.arrayBuffer();
      const contentType = response.headers.get('Content-Type') || 'application/json';
  
      return new Response(responseBody, {
        status: response.status,
        headers: {
          'Access-Control-Allow-Origin': '*',
          'Content-Type': contentType
        }
      });
    }
  }
  