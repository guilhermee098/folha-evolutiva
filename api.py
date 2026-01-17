from fastapi import FastAPI, File, UploadFile, HTTPException, Request
from fastapi.responses import FileResponse, JSONResponse, Response, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import tempfile
import os
import shutil
from pathlib import Path
import logging
import time
from datetime import datetime

# Importa as funções do main.py
from main import (
    validar_arquivo_entrada,
    extrair_dados_cabecalho,
    identificar_e_extrair_tabelas,
    gerar_word_evolucao,
    carregar_configuracao,
    CONFIG_PADRAO
)

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)

# Cria a aplicação FastAPI
app = FastAPI(
    title="Gerador de Folha de Evolução Transdisciplinar",
    description="API para converter Folhas de Frequência em Folhas de Evolução automaticamente",
    version="1.0.0"
)

# Configuração CORS (permite acesso de outras origens)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition"]
)

# Garante que os diretórios necessários existem
Path("temp_uploads").mkdir(exist_ok=True)
Path("temp_outputs").mkdir(exist_ok=True)

# Handler global de exceções
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Handler para capturar todas as exceções não tratadas"""
    logger.error("="*60)
    logger.error(f"EXCECAO NAO TRATADA")
    logger.error(f"URL: {request.url}")
    logger.error(f"Metodo: {request.method}")
    logger.error(f"Cliente: {request.client.host}")
    logger.error(f"Erro: {str(exc)}")
    logger.error("="*60)
    logger.exception("Traceback completo:")
    
    return JSONResponse(
        status_code=500,
        content={
            "detail": f"Erro interno do servidor: {str(exc)}",
            "type": type(exc).__name__
        }
    )

# Middleware para logging de todas as requisições
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Middleware que loga todas as requisições HTTP"""
    start_time = time.time()
    timestamp = datetime.now().strftime("%H:%M:%S")
    
    # Log da requisição recebida
    logger.info(f"[{timestamp}] {request.method} {request.url.path} - Cliente: {request.client.host}")
    
    try:
        response = await call_next(request)
        process_time = time.time() - start_time
        
        # Log da resposta
        status_emoji = "OK" if response.status_code < 400 else "ERRO"
        logger.info(f"[{timestamp}] {status_emoji} {request.method} {request.url.path} - Status: {response.status_code} - Tempo: {process_time:.2f}s")
        
        return response
    except Exception as e:
        process_time = time.time() - start_time
        logger.error(f"[{timestamp}] FALHA {request.method} {request.url.path} - ERRO: {str(e)} - Tempo: {process_time:.2f}s")
        raise

@app.get("/")
async def root():
    """Endpoint raiz - serve a interface HTML."""
    logger.info("Endpoint / acessado - servindo interface.html")
    
    # Serve o arquivo interface.html
    if os.path.exists("interface.html"):
        with open("interface.html", "r", encoding="utf-8") as f:
            html_content = f.read()
        return HTMLResponse(content=html_content)
    else:
        return {
            "message": "API Gerador de Folha de Evolução Transdisciplinar",
            "version": "1.0.0",
            "endpoints": {
                "POST /processar": "Upload de arquivo de frequência e geração de evolução",
                "GET /health": "Status da API",
                "GET /config": "Configurações atuais",
                "GET /docs": "Documentação interativa"
            },
            "nota": "Arquivo interface.html não encontrado"
        }

@app.get("/api/info")
async def api_info():
    """Informações da API (endpoint alternativo)."""
    logger.info("Endpoint /api/info acessado")
    return {
        "message": "API Gerador de Folha de Evolução Transdisciplinar",
        "version": "1.0.0",
        "endpoints": {
            "POST /processar": "Upload de arquivo de frequência e geração de evolução",
            "GET /health": "Status da API",
            "GET /config": "Configurações atuais"
        }
    }

@app.get("/health")
async def health_check():
    """Verifica se a API está funcionando."""
    logger.debug("Health check solicitado")
    return {
        "status": "ok",
        "message": "API está funcionando corretamente"
    }

@app.get("/config")
async def get_config():
    """Retorna as configurações atuais."""
    logger.info("Configuracoes solicitadas")
    config = carregar_configuracao()
    template_exists = os.path.exists(config["caminho_template"])
    logger.info(f"Template existe: {template_exists}")
    return {
        "config": config,
        "template_path": config["caminho_template"],
        "template_exists": template_exists
    }

@app.post("/processar")
async def processar_folha_frequencia(
    arquivo: UploadFile = File(..., description="Arquivo .docx da Folha de Frequência")
):
    """
    Processa uma Folha de Frequência e retorna a Folha de Evolução gerada.
    
    - **arquivo**: Arquivo .docx da Folha de Frequência
    
    Retorna: Arquivo .docx da Folha de Evolução gerada
    """
    
    logger.info("="*60)
    logger.info(f"NOVA REQUISICAO - Arquivo: {arquivo.filename}")
    logger.info(f"Content-Type: {arquivo.content_type}")
    logger.info("="*60)
    
    # Validação do tipo de arquivo
    if not arquivo.filename.endswith('.docx'):
        logger.warning(f"Arquivo rejeitado: {arquivo.filename} (formato invalido)")
        logger.warning(f"Extensao recebida: {arquivo.filename.split('.')[-1] if '.' in arquivo.filename else 'sem extensao'}")
        raise HTTPException(
            status_code=400,
            detail="Arquivo deve ser no formato .docx"
        )
    
    logger.info("Validacao: Formato .docx OK")
    
    # Cria arquivos temporários
    temp_input = None
    temp_output = None
    
    try:
        # Salva o arquivo de entrada temporariamente
        logger.info("Salvando arquivo temporariamente...")
        with tempfile.NamedTemporaryFile(delete=False, suffix='.docx', dir='temp_uploads') as tmp_input:
            temp_input = tmp_input.name
            content = await arquivo.read()
            tmp_input.write(content)
        
        tamanho_mb = len(content) / (1024 * 1024)
        logger.info(f"Arquivo salvo: {temp_input}")
        logger.info(f"Tamanho: {len(content)} bytes ({tamanho_mb:.2f} MB)")
        
        # Valida o arquivo
        logger.info("Validando integridade do arquivo...")
        if not validar_arquivo_entrada(temp_input):
            logger.error("Arquivo invalido ou corrompido")
            raise HTTPException(
                status_code=400,
                detail="Arquivo inválido ou corrompido"
            )
        
        logger.info("Validacao: Arquivo integro OK")
        
        # Carrega configurações
        logger.info("Carregando configuracoes...")
        config = carregar_configuracao()
        logger.info(f"Configuracoes carregadas: duracao={config['duracao_atendimento_minutos']}min")
        
        # Verifica se o template existe
        if not os.path.exists(config["caminho_template"]):
            logger.error(f"Template nao encontrado: {config['caminho_template']}")
            raise HTTPException(
                status_code=500,
                detail=f"Template não encontrado: {config['caminho_template']}"
            )
        
        logger.info(f"Template encontrado: {config['caminho_template']}")
        
        # Extrai dados do cabeçalho
        dados_cabecalho = None
        if config.get("extrair_cabecalho_de_entrada", False):
            logger.info("Extraindo dados do cabecalho...")
            dados_cabecalho = extrair_dados_cabecalho(temp_input)
            if dados_cabecalho:
                logger.info(f"Cabecalho extraido: {len(dados_cabecalho)} campos")
                for key, value in dados_cabecalho.items():
                    valor_resumido = str(value)[:50] + "..." if len(str(value)) > 50 else str(value)
                    logger.info(f"  - {key}: {valor_resumido}")
            else:
                logger.warning("Nenhum dado de cabecalho extraido")
        
        # Extrai dados das tabelas
        logger.info("Identificando e extraindo tabelas...")
        dados, erros, avisos = identificar_e_extrair_tabelas(temp_input, config)
        
        if erros:
            logger.warning(f"Erros encontrados durante extracao: {len(erros)}")
            for erro in erros[:3]:  # Mostra apenas os 3 primeiros
                logger.warning(f"  - {erro}")
        
        if avisos:
            logger.info(f"Avisos durante extracao: {len(avisos)}")
        
        if not dados:
            logger.error("Nenhum dado valido encontrado no arquivo")
            raise HTTPException(
                status_code=400,
                detail="Nenhum dado válido encontrado no arquivo. Verifique se contém as colunas: DATA, HORÁRIO, PROCEDIMENTO"
            )
        
        # Conta procedimentos (especialidades serão extraídas depois)
        procedimentos_unicos = set()
        for item in dados:
            proc = item.get('procedimento', '')
            # Extrai a especialidade do procedimento (primeira palavra em maiúscula)
            palavras = proc.upper().split()
            if palavras:
                especialidade = palavras[0]
                procedimentos_unicos.add(especialidade)
        
        total_registros = len(dados)
        logger.info(f"Dados extraidos com sucesso:")
        logger.info(f"  - Total de registros: {total_registros}")
        logger.info(f"  - Procedimentos/Especialidades encontradas: {len(procedimentos_unicos)}")
        for esp in sorted(procedimentos_unicos):
            count = sum(1 for item in dados if esp in item.get('procedimento', '').upper())
            logger.info(f"    * {esp}: {count} atendimento(s)")
        
        # Gera o arquivo de saída
        logger.info("Criando arquivo de saida temporario...")
        with tempfile.NamedTemporaryFile(delete=False, suffix='.docx', dir='temp_outputs') as tmp_output:
            temp_output = tmp_output.name
        
        logger.info(f"Arquivo de saida: {temp_output}")
        
        # Gera o documento de evolução
        logger.info("Gerando documento de evolucao (pode levar alguns segundos)...")
        sucesso = gerar_word_evolucao(dados, temp_output, config, dados_cabecalho)
        
        if not sucesso:
            logger.error("Erro ao gerar o documento de evolucao")
            raise HTTPException(
                status_code=500,
                detail="Erro ao gerar o documento de evolução"
            )
        
        # Verifica tamanho do arquivo gerado
        tamanho_saida = os.path.getsize(temp_output)
        tamanho_saida_mb = tamanho_saida / (1024 * 1024)
        logger.info(f"Documento gerado com sucesso!")
        logger.info(f"  - Tamanho: {tamanho_saida} bytes ({tamanho_saida_mb:.2f} MB)")
        logger.info(f"  - Registros processados: {total_registros}")
        logger.info(f"  - Procedimentos/Especialidades: {len(procedimentos_unicos)}")
        
        logger.info("Enviando arquivo para o cliente...")
        
        # Lê o arquivo em memória antes de enviar
        with open(temp_output, 'rb') as f:
            arquivo_bytes = f.read()
        
        logger.info(f"Arquivo lido em memoria: {len(arquivo_bytes)} bytes")
        
        # Limpa arquivos temporários ANTES de enviar
        cleanup_files(temp_input, temp_output)
        
        # Retorna o arquivo como bytes
        response = Response(
            content=arquivo_bytes,
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            headers={
                "Content-Disposition": f"attachment; filename=Evolucao_{Path(arquivo.filename).stem}.docx",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Expose-Headers": "Content-Disposition"
            }
        )
        
        logger.info(f"Resposta enviada com sucesso - {len(arquivo_bytes)} bytes")
        return response
    
    except HTTPException:
        # Re-raise HTTP exceptions
        cleanup_files(temp_input, temp_output)
        logger.error("Requisicao finalizada com erro HTTP")
        raise
    
    except Exception as e:
        # Limpa arquivos temporários em caso de erro
        cleanup_files(temp_input, temp_output)
        logger.error(f"ERRO CRITICO ao processar arquivo: {e}")
        logger.exception("Traceback completo:")
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao processar arquivo: {str(e)}"
        )

def cleanup_files(*files):
    """Limpa arquivos temporários."""
    for file in files:
        if file and os.path.exists(file):
            try:
                os.unlink(file)
                logger.info(f"Arquivo temporario removido: {os.path.basename(file)}")
            except Exception as e:
                logger.warning(f"Nao foi possivel remover arquivo temporario {file}: {e}")

@app.on_event("startup")
async def startup_event():
    """Executado ao iniciar a API."""
    logger.info("")
    logger.info("="*60)
    logger.info("API INICIADA - GERADOR DE FOLHA DE EVOLUCAO")
    logger.info("="*60)
    logger.info("Versao: 1.0.0")
    logger.info("Porta: 8000")
    logger.info("")
    logger.info("Verificando configuracoes...")
    
    config = carregar_configuracao()
    if os.path.exists(config["caminho_template"]):
        logger.info(f"Template encontrado: {config['caminho_template']}")
    else:
        logger.warning(f"AVISO: Template NAO encontrado: {config['caminho_template']}")
        logger.warning("A API nao conseguira processar arquivos sem o template!")
    
    # Verifica diretórios temporários
    if os.path.exists("temp_uploads"):
        logger.info("Diretorio temp_uploads: OK")
    else:
        logger.info("Criando diretorio temp_uploads...")
        Path("temp_uploads").mkdir(exist_ok=True)
    
    if os.path.exists("temp_outputs"):
        logger.info("Diretorio temp_outputs: OK")
    else:
        logger.info("Criando diretorio temp_outputs...")
        Path("temp_outputs").mkdir(exist_ok=True)
    
    logger.info("")
    logger.info("="*60)
    logger.info("API PRONTA PARA RECEBER REQUISICOES")
    logger.info("="*60)
    logger.info("Endpoints disponiveis:")
    logger.info("  GET  /         - Informacoes da API")
    logger.info("  GET  /health   - Status da API")
    logger.info("  GET  /config   - Configuracoes atuais")
    logger.info("  POST /processar - Processar folha de frequencia")
    logger.info("  GET  /docs     - Documentacao interativa (Swagger)")
    logger.info("="*60)
    logger.info("")

@app.on_event("shutdown")
async def shutdown_event():
    """Executado ao desligar a API."""
    logger.info("")
    logger.info("="*60)
    logger.info("ENCERRANDO API...")
    logger.info("="*60)
    
    # Limpa diretórios temporários
    for dir_path in ["temp_uploads", "temp_outputs"]:
        if os.path.exists(dir_path):
            try:
                files_count = len(os.listdir(dir_path))
                if files_count > 0:
                    logger.info(f"Limpando {files_count} arquivo(s) em {dir_path}/")
                shutil.rmtree(dir_path)
                logger.info(f"Diretorio temporario removido: {dir_path}/")
            except Exception as e:
                logger.warning(f"Erro ao remover diretorio {dir_path}: {e}")
    
    logger.info("API encerrada com sucesso")
    logger.info("="*60)
    logger.info("")

if __name__ == "__main__":
    import uvicorn
    
    # Inicia o servidor
    uvicorn.run(
        "api:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
