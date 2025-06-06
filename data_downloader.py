import requests

class getData():
    print('Get data init!')
    url = "https://anfavea.com.br/docs/SeriesTemporais_Autoveiculos.xlsm"  
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    }

    resposta = requests.get(url, headers=headers)

    if resposta.status_code == 200:
        with open("files/arquivo.xlsm", "wb") as f:
            f.write(resposta.content)
        print("Download sucessful!")
    else:
        print(f"Erro ao baixar: {resposta.status_code}")