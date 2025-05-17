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

        try {
            const contentType = request.headers.get('Content-Type') || 'application/json';
            console.log('Content-Type:', contentType);
            console.log('Request content length:', request.headers.get('Content-Length') || 'unknown');
            
            // Clone e processe o corpo
            let body;
            try {
                if (contentType.includes('application/json')) {
                    // Se for JSON, vamos analisar e apenas logar informações importantes
                    const jsonData = await request.clone().json();
                    // Vamos logar todos os campos exceto a imagem base64 para evitar estouro do limite de logs
                    const keysToLog = Object.keys(jsonData).filter(k => k !== 'imagem_base64');
                    const logSafeData = {};
                    keysToLog.forEach(k => logSafeData[k] = jsonData[k]);
                    
                    console.log('Dados do evento:', JSON.stringify(logSafeData));
                    if (jsonData.imagem_base64) {
                        console.log('imagem_base64 presente, tamanho aprox:', Math.round(jsonData.imagem_base64.length/1024) + 'KB');
                    }
                    
                    body = await request.clone().text();
                } else {
                    body = await request.clone().text();
                    console.log('Forwarding request body length:', body.length);
                    // Log first 200 characters to avoid overwhelming logs
                    console.log('Forwarding request sample:', body.substring(0, 200) + (body.length > 200 ? '...' : ''));
                }
            } catch (e) {
                console.error('Erro ao processar corpo da requisição:', e);
                body = await request.clone().text();
            }

            console.log('Enviando requisição para:', targetUrl);
            const response = await fetch(targetUrl, {
                method: request.method,
                headers: {
                    'Content-Type': contentType,
                    'Accept': 'application/json',
                    'Authorization': request.headers.get('Authorization') || ''
                },
                body: body,
                redirect: 'follow'
            });

            // Tentar processar a resposta
            const responseBody = await response.text();
            console.log('Status da resposta:', response.status);
            console.log('Response from backend:', responseBody.length > 1000 ? 
                        responseBody.substring(0, 1000) + '...(truncado)' : 
                        responseBody);

            return new Response(responseBody, {
                status: response.status,
                headers: {
                    'Access-Control-Allow-Origin': '*',
                    'Content-Type': response.headers.get('Content-Type') || 'application/json'
                }
            });
        } catch (error) {
            console.error('Erro no processamento do worker:', error);
            return new Response(JSON.stringify({
                error: 'Erro interno no worker',
                message: error.message
            }), {
                status: 500,
                headers: {
                    'Access-Control-Allow-Origin': '*',
                    'Content-Type': 'application/json'
                }
            });
        }
    }
};
