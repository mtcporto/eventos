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

        const body = await request.clone().text();
        console.log('Forwarding request body length:', body.length);
        // Log first 200 characters to avoid overwhelming logs
        console.log('Forwarding request sample:', body.substring(0, 200) + (body.length > 200 ? '...' : ''));

        const contentType = request.headers.get('Content-Type') || 'application/json';
        console.log('Content-Type:', contentType);

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

        const responseBody = await response.text();
        console.log('Response from backend:', responseBody);

        return new Response(responseBody, {
            status: response.status,
            headers: {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': response.headers.get('Content-Type') || 'application/json'
            }
        });
    }
};
