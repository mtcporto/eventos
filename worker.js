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
                // Essencial: vamos otimizar o conteúdo antes de enviar para o backend
                if (contentType.includes('application/json')) {
                    try {
                        // Se for JSON, primeiro vamos otimizar os dados
                        const jsonData = await request.clone().json();
                        
                        // Log seguro (sem imagem base64)
                        const keysToLog = Object.keys(jsonData).filter(k => k !== 'imagem_base64');
                        const logSafeData = {};
                        keysToLog.forEach(k => logSafeData[k] = jsonData[k]);
                        console.log('Dados do evento:', JSON.stringify(logSafeData));
                        
                        // Verificar se a imagem é muito grande e redimensionar se necessário
                        if (jsonData.imagem_base64) {
                            const originalSize = jsonData.imagem_base64.length;
                            console.log('imagem_base64 presente, tamanho aprox:', Math.round(originalSize/1024) + 'KB');
                            
                            // Se a imagem base64 for maior que 150KB, vamos otimizá-la
                            if (originalSize > 150000) {
                                console.log('Otimizando imagem no worker...');
                                
                                // Remover cabeçalho data:image... se existir
                                let imageData = jsonData.imagem_base64;
                                if (imageData.includes(',')) {
                                    imageData = imageData.split(',')[1];
                                }
                                
                                // Limitar tamanho máximo para 150KB
                                const maxSizeBytes = 150000;
                                if (imageData.length > maxSizeBytes) {
                                    jsonData.imagem_base64 = 'data:image/jpeg;base64,' + imageData.substring(0, maxSizeBytes);
                                    console.log('Imagem truncada para ~150KB');
                                } else {
                                    jsonData.imagem_base64 = 'data:image/jpeg;base64,' + imageData;
                                }
                            }
                        }
                        
                        // Usar a versão otimizada do body
                        body = JSON.stringify(jsonData);
                        console.log('Corpo JSON processado, tamanho final:', Math.round(body.length/1024) + 'KB');
                    } catch (jsonError) {
                        console.error('Erro ao processar JSON:', jsonError);
                        body = await request.clone().text();
                    }
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

            // Verificar se o corpo é muito grande (mais de 1MB)
            if (body && body.length > 1000000) {
                console.log('Requisição muito grande, enviando versão compacta');
                
                // Se for JSON, tentar extrair apenas os dados essenciais
                try {
                    const jsonData = JSON.parse(body);
                    
                    // Se tiver a imagem base64, verificar e reduzir ainda mais se necessário
                    if (jsonData.imagem_base64 && jsonData.imagem_base64.length > 100000) {
                        console.log('Imagem base64 ainda muito grande, reduzindo mais');
                        // Remover o prefixo data:image se existir
                        let imageData = jsonData.imagem_base64;
                        if (imageData.includes(',')) {
                            imageData = imageData.split(',')[1];
                        }
                        
                        // Limitar o tamanho da imagem para evitar problemas
                        if (imageData.length > 100000) {
                            jsonData.imagem_base64 = imageData.substring(0, 100000);
                            console.log('Imagem truncada para 100KB');
                        }
                    }
                    
                    // Usar a versão otimizada
                    body = JSON.stringify(jsonData);
                    console.log('JSON reempacotado, novo tamanho:', body.length);
                } catch (e) {
                    console.error('Erro ao reprocessar JSON:', e);
                    // Continuar com o body original
                }
            }
            
            console.log('Enviando requisição para:', targetUrl);
            
            // Verificar se é GET ou HEAD - esses métodos não podem ter corpo
            const requestOptions = {
                method: request.method,
                headers: {
                    'Content-Type': contentType,
                    'Accept': 'application/json',
                    'Authorization': request.headers.get('Authorization') || ''
                },
                redirect: 'follow'
            };
            
            // Adicionar o corpo apenas se NÃO for GET ou HEAD
            if (request.method !== 'GET' && request.method !== 'HEAD') {
                requestOptions.body = body;
            }
            
            const response = await fetch(targetUrl, requestOptions);

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
