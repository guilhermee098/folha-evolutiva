"""Script para extrair a imagem do cabeçalho do template."""
from docx import Document
import os

caminho_template = 'template_saida/template_saida.docx'
doc = Document(caminho_template)

print("Extraindo imagem do template...")

# Acessa o cabeçalho
header = doc.sections[0].header

# Procura por imagens nos relationships
for rel_id, rel in header.part.rels.items():
    if 'image' in rel.reltype.lower():
        print(f"Encontrada imagem: {rel_id}")
        
        # Pega a imagem
        image_part = rel.target_part
        image_bytes = image_part.blob
        
        # Descobre a extensão
        content_type = image_part.content_type
        if 'png' in content_type:
            extensao = 'png'
        elif 'jpeg' in content_type or 'jpg' in content_type:
            extensao = 'jpg'
        elif 'gif' in content_type:
            extensao = 'gif'
        else:
            extensao = 'bin'
        
        # Salva a imagem
        nome_arquivo = f'logo_extraida.{extensao}'
        with open(nome_arquivo, 'wb') as f:
            f.write(image_bytes)
        
        print(f"OK - Imagem salva como: {nome_arquivo}")
        print(f"  Tamanho: {len(image_bytes)} bytes")
        print(f"  Tipo: {content_type}")

print("\nConcluido!")
