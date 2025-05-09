#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Script de teste para a API de eventos (Compatível com Python 2.7)

import sys
import json
import base64
import os
try:
    from urllib.parse import urljoin  # Python 3
except ImportError:
    from urlparse import urljoin  # Python 2
try:
    from datetime import datetime
    now = datetime.now
except ImportError:
    import datetime
    now = datetime.datetime.now

# Para Python 2, importamos o pacote requests diretamente
try:
    import requests
except ImportError:
    print("O pacote 'requests' é necessário. Instale com: pip install requests")
    sys.exit(1)

# URL Base da API
API_BASE_URL = "https://mtcporto2.pythonanywhere.com/eventos/default/"
API_ENDPOINT = urljoin(API_BASE_URL, "eventos")

def test_get():
    """Testa o método GET da API para listar eventos"""
    try:
        response = requests.get(API_ENDPOINT)
        data = response.json()
        print("Resposta: {0}".format(json.dumps(data, indent=2, ensure_ascii=False)))
        print("Total de eventos retornados: {0}".format(len(data.get('eventos', []))))
        print("Teste GET bem-sucedido\n")
        return data
    except Exception as e:
        print("Erro ao testar GET: {0}".format(e))
        return None

def test_post(include_image=False):
    """Testa o método POST da API para inserir um evento"""
    try:
        # Cria um evento de teste
        evento = {
            "oque": "Evento de Teste API - {0}".format(now().strftime('%Y-%m-%d %H:%M:%S')),
            "quando": "01/01/2024 19:00",
            "onde": "Porto Alegre",
            "fonte": "Teste Automatizado",
            "local": "PyThonanywhere",
            "descricao": "Este é um evento de teste enviado por um script automatizado.",
            "endereco": "Rua dos Testes, 123",
            "preco": "Gratuito",
            "tipo": "Teste"
        }
        
        # Adiciona uma imagem de teste se solicitado
        if include_image:
            # Tenta encontrar uma imagem de teste
            image_path = os.path.join(os.path.dirname(__file__), "test_image.jpg")
            if os.path.exists(image_path):
                with open(image_path, "rb") as img_file:
                    image_data = base64.b64encode(img_file.read()).decode('utf-8')
                    evento["imagem"] = "data:image/jpeg;base64,{0}".format(image_data)
                print("Imagem incluída no teste")
            else:
                print("Arquivo de imagem de teste não encontrado em:", image_path)
        
        print("\nEnviando evento de teste para a API...")
        
        # Envia a requisição
        response = requests.post(
            API_ENDPOINT,
            json=evento,
            headers={'Content-Type': 'application/json'}
        )
        
        print("Status: {0}".format(response.status_code))
        print("Resposta: {0}".format(json.dumps(response.json(), indent=2, ensure_ascii=False)))
        
        # Verifica o resultado
        if response.status_code == 200 and "success" in response.json()["status"]:
            print("\nTeste POST bem-sucedido\n")
        else:
            print("Teste POST falhou com status {0}\n".format(response.status_code))
            
        return response.json()
    except Exception as e:
        print("Erro ao testar POST: {0}".format(e))
        return None

def test_cors():
    """Testa se a API está configurada corretamente para CORS"""
    try:
        print("\nTestando configuração CORS...")
        
        # Simula uma requisição OPTIONS de preflight
        response = requests.options(
            API_ENDPOINT, 
            headers={
                'Origin': 'http://localhost:8000',
                'Access-Control-Request-Method': 'POST',
                'Access-Control-Request-Headers': 'Content-Type'
            }
        )
        
        print("Status: {0}".format(response.status_code))
        print("Cabeçalhos de resposta:")
        for header, value in response.headers.items():
            if header.lower().startswith('access-control'):
                print("  {0}: {1}".format(header, value))
        
        # Verifica se os cabeçalhos CORS estão presentes
        if 'access-control-allow-origin' in map(str.lower, response.headers.keys()):
            print("\nConfigurações CORS detectadas\n")
        else:
            print("\nAVISO: Cabeçalhos CORS não encontrados na resposta!\n")
            
        return response
    except Exception as e:
        print("Erro ao testar CORS: {0}".format(e))
        return None

if __name__ == "__main__":
    print("=== TESTE DA API DE EVENTOS ===")
    print("URL da API:", API_ENDPOINT)
    
    # Executa os testes
    test_cors()
    test_get()
    test_post()
    
    # Teste com imagem é opcional
    if "--with-image" in sys.argv:
        test_post(include_image=True)
    
    print("Testes concluídos.")
