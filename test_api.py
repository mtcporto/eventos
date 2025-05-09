#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para testar a API de eventos
Uso: python test_api.py
"""

import requests
import json
import base64
import sys
from datetime import datetime

API_URL = "https://mtcporto2.pythonanywhere.com/eventos/default/eventos"

def test_get_eventos():
    """Testa a listagem de eventos"""
    print("Testando GET /eventos...")
    
    try:
        response = requests.get(API_URL)
        response.raise_for_status()  # Lança exceção se o status não for 2xx
        
        data = response.json()
        print(f"Resposta: {json.dumps(data, indent=2, ensure_ascii=False)}")
        print(f"Total de eventos retornados: {len(data.get('eventos', []))}")
        print("Teste GET concluído com sucesso!\n")
        
    except Exception as e:
        print(f"Erro ao testar GET: {e}")

def test_post_evento():
    """Testa a criação de um evento"""
    print("Testando POST /eventos...")
    
    # Evento de teste
    evento = {
        "oque": f"Evento de Teste API - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "quando": "15/05/2025 20:00",
        "onde": "João Pessoa",
        "fonte": "Teste Automatizado",
        "local": "Centro de Convenções",
        "descricao": "Este é um evento de teste gerado automaticamente para validar a API."
    }
    
    try:
        # Adicionar uma pequena imagem de teste em base64
        try:
            with open("test_image.jpg", "rb") as image_file:
                image_data = base64.b64encode(image_file.read()).decode('utf-8')
                evento["imagem"] = f"data:image/jpeg;base64,{image_data}"
        except:
            # Se não encontrar a imagem, continua sem ela
            print("Imagem de teste não encontrada, enviando sem imagem...")
        
        # Enviar requisição
        response = requests.post(
            API_URL,
            json=evento,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Status: {response.status_code}")
        print(f"Resposta: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        
        if response.status_code in (200, 201):
            print("Teste POST concluído com sucesso!\n")
        else:
            print(f"Teste POST falhou com status {response.status_code}\n")
            
    except Exception as e:
        print(f"Erro ao testar POST: {e}")

def test_cors():
    """Testa se o servidor está respondendo ao preflight CORS"""
    print("Testando OPTIONS (CORS preflight)...")
    
    try:
        response = requests.options(
            API_URL,
            headers={
                "Origin": "http://localhost",
                "Access-Control-Request-Method": "POST",
                "Access-Control-Request-Headers": "Content-Type, Authorization"
            }
        )
        
        print(f"Status: {response.status_code}")
        print("Headers:")
        for header, value in response.headers.items():
            if header.startswith('Access-Control-'):
                print(f"  {header}: {value}")
        
        if response.status_code == 200 and 'Access-Control-Allow-Origin' in response.headers:
            print("Teste CORS concluído com sucesso!\n")
        else:
            print("Teste CORS falhou: Configuração CORS incompleta\n")
            
    except Exception as e:
        print(f"Erro ao testar CORS: {e}")

if __name__ == "__main__":
    print("===== Testando API de Eventos =====")
    
    # Executar testes
    test_cors()
    test_get_eventos()
    test_post_evento()
    
    print("===== Testes concluídos =====")
