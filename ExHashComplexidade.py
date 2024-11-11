import zlib

def hash_crc32(titulo):
    return zlib.crc32(titulo.encode())

def processa_titulos(arquivo, tamanhos_vetor, titulo_especifico):
    titulos_por_indice = {}
    posicao_titulo_especifico = {}

    with open(arquivo, 'r', encoding='utf-8') as f:
        titulos = [linha.strip() for linha in f]  

    titulos.append(titulo_especifico)

    for tamanho_vetor in tamanhos_vetor:
        for titulo in titulos:
            hash_valor = hash_crc32(titulo)
            indice = hash_valor % tamanho_vetor  
            if tamanho_vetor not in titulos_por_indice:
                titulos_por_indice[tamanho_vetor] = {}
            if indice not in titulos_por_indice[tamanho_vetor]:
                titulos_por_indice[tamanho_vetor][indice] = []
            titulos_por_indice[tamanho_vetor][indice].append(titulo)

            if titulo == titulo_especifico:
                posicao_titulo_especifico[tamanho_vetor] = indice

    return titulos_por_indice, posicao_titulo_especifico

def gera_relatorio(titulos_por_indice, posicao_titulo_especifico, arquivo_saida):
    with open(arquivo_saida, 'w', encoding='utf-8') as arquivo:
        for tamanho_vetor, indices in titulos_por_indice.items():
            arquivo.write(f"Relatório para vetor de {tamanho_vetor} posições:\n")

            total_indices_vazios = 0
            for indice in range(tamanho_vetor):
                if indice not in indices:
                    total_indices_vazios += 1
                    arquivo.write(f"Índice {indice}: Vazio\n")
                else:
                    contagem_titulos = len(indices[indice])
                    arquivo.write(f"Índice {indice}: {contagem_titulos} título(s)\n")
            
            arquivo.write(f"\nTotal de índices vazios: {total_indices_vazios}\n")
            posicao_especifica = posicao_titulo_especifico.get(tamanho_vetor)
            arquivo.write(f"\nPosição do título específico ('{titulo_especifico}') para vetor de {tamanho_vetor} posições: {posicao_especifica}\n")
            arquivo.write("\n" + "="*40 + "\n\n")

arquivo = 'livros.txt'
tamanhos_vetor = [20, 131, 1021]  
arquivo_saida = 'relatorio.txt'
titulo_especifico = "ESTUDANDO COMPLEXIDADE COM FELIPE RONZANI SILVA"

titulos_por_indice, posicao_titulo_especifico = processa_titulos(arquivo, tamanhos_vetor, titulo_especifico)

gera_relatorio(titulos_por_indice, posicao_titulo_especifico, arquivo_saida)

print(f"O relatório foi gerado com sucesso em '{arquivo_saida}'")
