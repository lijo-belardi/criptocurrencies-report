import requests
from pprint import pprint

class Report:
    def __init__(self):
        self.url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'

        self.params = {
            "start": "1",
            "limit": "5000",
            "convert": "USD"
        }

        self.headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': '72a39680-12c5-46ac-803e-a9610f91049f',
        }

    def dati_aggiornati(self):
        database = requests.get(url=self.url, headers=self.headers, params=self.params).json()
        return database["data"]

    def volume_maggiore(self):
        risultati_report = Report()
        insieme_criptovalute = risultati_report.dati_aggiornati()
        nome_criptovaluta = []
        volume_criptovaluta = 0
        for criptovaluta in insieme_criptovalute:
            if criptovaluta["quote"]["USD"]["volume_24h"] > volume_criptovaluta:
                volume_criptovaluta = criptovaluta["quote"]["USD"]["volume_24h"]
                nome_criptovaluta = criptovaluta["name"]
        return nome_criptovaluta, volume_criptovaluta

    def incremento_percentuale_migliori_e_peggiori_24h(self):
        risultati_report = Report()
        insieme_criptovalute = risultati_report.dati_aggiornati()
        nome_criptovaluta = []
        incremento_percentuale_24h = []
        for criptovaluta in insieme_criptovalute:
            nome_criptovaluta.append(criptovaluta["name"])
            incremento_percentuale_24h.append(criptovaluta["quote"]["USD"]["percent_change_24h"])

        dizionario = dict(zip(nome_criptovaluta, incremento_percentuale_24h))
        dizionario_ordinato_migliori_criptovalute = sorted(dizionario.items(), key=lambda x: x[1], reverse=True)
        dizionario_ordinato_peggiori_criptovalute = sorted(dizionario.items(), key=lambda x: x[1])

        migliori_10 = list(dizionario_ordinato_migliori_criptovalute[:10])
        peggiori_10 = list(dizionario_ordinato_peggiori_criptovalute[:10])
        return migliori_10, peggiori_10

    def acquisto_volume_maggiore_24h(self):
        risultati_report = Report()
        insieme_criptovalute = risultati_report.dati_aggiornati()
        lista_criptovalute_volume_maggiore_24h = []
        volume_24_riferimento = 76000000
        denaro_necessario = 0
        for criptovaluta in insieme_criptovalute:
            if criptovaluta["quote"]["USD"]["volume_24h"] > volume_24_riferimento:
                lista_criptovalute_volume_maggiore_24h.append(criptovaluta["name"])
                denaro_necessario += criptovaluta["quote"]["USD"]["price"]
        return lista_criptovalute_volume_maggiore_24h, volume_24_riferimento, denaro_necessario

    def stampa(self):
        nome_richiesta_1, volume_richiesta_1 = Report.volume_maggiore(self)
        migliori_10, peggiori_10 = Report.incremento_percentuale_migliori_e_peggiori_24h(self)
        lista_criptovalute_volume_maggiore_24h, volume_24_riferimento, denaro_necessario = Report.acquisto_volume_maggiore_24h(self)

        #Richiesta 1
        print(f"\nLa criptovaluta con il volume maggiore nelle ultime 24 ore è: {nome_richiesta_1}\n"
               f"Il suo volume corrisponde a: {volume_richiesta_1}$")

        #Richiesta 2
        print(f"\nLe 10 criptovalute con l'incremento percentuale MIGLIORE nelle ultime 24 ore sono:")
        for x in migliori_10:
            print(x)

        print(f"\nLe 10 criptovalute con l'incremento percentuale PEGGIORE nelle ultime 24 ore sono:")
        for y in peggiori_10:
            print(y)

        #Richiesta 4
        print(f"\n\nNumero criptovalute con volume superiore a {volume_24_riferimento}$ nelle ultime 24 ore:\n{len(lista_criptovalute_volume_maggiore_24h)}")
        print(f"Denaro necessario per acquistare una unità di queste {len(lista_criptovalute_volume_maggiore_24h)} criptovalute:\n{denaro_necessario}$")
        print(f"\nLista delle {len(lista_criptovalute_volume_maggiore_24h)} criptovalute:")
        for criptovaluta in lista_criptovalute_volume_maggiore_24h:
            print(criptovaluta)
        return f"\nGrazie per l'attenzione"


risultati = Report()

print(risultati.stampa())