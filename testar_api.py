"""
Script de teste para a API de Geração de Folha de Evolução
"""

import requests
import os

# URL da API
API_URL = "http://localhost:8000"

def testar_health():
    """Testa se a API está online"""
    print("Testando conexao com a API...")
    try:
        response = requests.get(f"{API_URL}/health")
        if response.status_code == 200:
            print("API esta online!")
            print(f"   Resposta: {response.json()}")
            return True
        else:
            print(f"API retornou status: {response.status_code}")
            return False
    except Exception as e:
        print(f"Erro ao conectar: {e}")
        return False

def testar_config():
    """Testa o endpoint de configurações"""
    print("\nVerificando configuracoes da API...")
    try:
        response = requests.get(f"{API_URL}/config")
        if response.status_code == 200:
            config = response.json()
            print("Configuracoes carregadas:")
            print(f"   Template: {config['template_path']}")
            print(f"   Template existe: {config['template_exists']}")
            print(f"   Duracao atendimento: {config['config']['duracao_atendimento_minutos']} min")
            return True
        else:
            print(f"Erro ao obter configuracoes: {response.status_code}")
            return False
    except Exception as e:
        print(f"Erro: {e}")
        return False

def testar_processar(arquivo_entrada):
    """Testa o processamento de um arquivo"""
    print(f"\nProcessando arquivo: {arquivo_entrada}")
    
    if not os.path.exists(arquivo_entrada):
        print(f"Arquivo nao encontrado: {arquivo_entrada}")
        return False
    
    try:
        with open(arquivo_entrada, 'rb') as f:
            files = {'arquivo': (os.path.basename(arquivo_entrada), f, 'application/vnd.openxmlformats-officedocument.wordprocessingml.document')}
            
            print("   Enviando arquivo para a API...")
            response = requests.post(f"{API_URL}/processar", files=files)
        
        if response.status_code == 200:
            # Salva o arquivo retornado
            arquivo_saida = f"saida/Evolucao_TESTE_API_{os.path.basename(arquivo_entrada)}"
            with open(arquivo_saida, 'wb') as f:
                f.write(response.content)
            
            print(f"Documento processado com sucesso!")
            print(f"   Arquivo salvo em: {arquivo_saida}")
            print(f"   Tamanho: {len(response.content)} bytes")
            return True
        else:
            print(f"Erro ao processar: {response.status_code}")
            try:
                erro = response.json()
                print(f"   Detalhe: {erro.get('detail', 'Erro desconhecido')}")
            except:
                print(f"   Resposta: {response.text}")
            return False
    
    except Exception as e:
        print(f"Erro: {e}")
        return False

def main():
    print("="*60)
    print("TESTE DA API - GERADOR DE FOLHA DE EVOLUCAO")
    print("="*60)
    
    # Teste 1: Health Check
    if not testar_health():
        print("\nAPI nao esta disponivel. Certifique-se de que esta rodando:")
        print("   python api.py")
        return
    
    # Teste 2: Configurações
    testar_config()
    
    # Teste 3: Processar arquivo
    arquivo_teste = "entrada/JOAO PAULO NUNES - Folha de frequência JULHO.docx"
    testar_processar(arquivo_teste)
    
    print("\n" + "="*60)
    print("Testes concluidos!")
    print("="*60)
    print("\nDicas:")
    print("   - Acesse http://localhost:8000/docs para documentacao interativa")
    print("   - Abra interface.html no navegador para usar a interface web")
    print("   - Use Ctrl+C no terminal da API para parar o servidor")

if __name__ == "__main__":
    main()
