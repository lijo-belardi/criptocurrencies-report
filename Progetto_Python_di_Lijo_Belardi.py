import requests
import json
import datetime

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

    def volume_maggiore(self): #Richiesta 1
        risultati_report = Report()
        insieme_criptovalute = risultati_report.dati_aggiornati()
        nome_criptovaluta = []
        volume_criptovaluta = 0
        for criptovaluta in insieme_criptovalute:
            if criptovaluta["quote"]["USD"]["volume_24h"] > volume_criptovaluta:
                volume_criptovaluta = criptovaluta["quote"]["USD"]["volume_24h"]
                nome_criptovaluta = criptovaluta["name"]
        return nome_criptovaluta, volume_criptovaluta

    def incremento_percentuale_migliori_e_peggiori_24h(self): #Richiesta 2
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

    def denaro_necessario_acquisto_prime_20_criptovalute(self): #Richiesta 3
        risultati_report = Report()
        insieme_criptovalute = risultati_report.dati_aggiornati()
        lista_capitalizzazione_criptovalute = {}
        lista_migliori_20_cap = []
        denaro_necessario = 0

        for criptovaluta in insieme_criptovalute:
            lista_capitalizzazione_criptovalute[criptovaluta["quote"]["USD"]["market_cap"]] = criptovaluta["name"]

        for elemento in sorted(lista_capitalizzazione_criptovalute.keys(), reverse=True):
            if len(lista_migliori_20_cap) < 20:
                lista_migliori_20_cap.append((lista_capitalizzazione_criptovalute[elemento], elemento))

        for criptovaluta in insieme_criptovalute:
            for y in range(20):
                if lista_migliori_20_cap[y][0] == criptovaluta["name"]:
                    denaro_necessario += criptovaluta["quote"]["USD"]["price"]
        return lista_capitalizzazione_criptovalute, lista_migliori_20_cap, denaro_necessario

    def acquisto_volume_maggiore_24h(self): #Richiesta 4
        risultati_report = Report()
        insieme_criptovalute = risultati_report.dati_aggiornati()
        lista_criptovalute_volume_maggiore_24h = []
        volume_24_riferimento = 76000000
        denaro_necessario_2 = 0
        for criptovaluta in insieme_criptovalute:
            if criptovaluta["quote"]["USD"]["volume_24h"] > volume_24_riferimento:
                lista_criptovalute_volume_maggiore_24h.append(criptovaluta["name"])
                denaro_necessario_2 += criptovaluta["quote"]["USD"]["price"]
        return lista_criptovalute_volume_maggiore_24h, volume_24_riferimento, denaro_necessario_2

    def guadagno_perdita_percentuale(self): #Richiesta 5
        risultati_report = Report()
        insieme_criptovalute = risultati_report.dati_aggiornati()

        lista_capitalizzazione = {}
        lista_migliori_20 = []
        prezzo_totale = 0
        prezzo_totale_precedente = 0

        for criptovaluta in insieme_criptovalute:
            lista_capitalizzazione[criptovaluta["quote"]["USD"]["market_cap"]] = criptovaluta["name"]
        for elemento in sorted(lista_capitalizzazione.keys(), reverse=True):
            if len(lista_migliori_20) < 20:
                lista_migliori_20.append((lista_capitalizzazione[elemento], elemento))

        for criptovaluta in insieme_criptovalute:
            for x in range(20):
                if lista_migliori_20[x][0] == criptovaluta["name"]:
                    prezzo_totale += criptovaluta["quote"]["USD"]["price"]
                    prezzo_totale_precedente += criptovaluta["quote"]["USD"]["price"] - ((criptovaluta["quote"]["USD"]["price"] * criptovaluta["quote"]["USD"]["percent_change_24h"]) / 100)

        perdita_guadagno_percentuale = ((prezzo_totale_precedente * 100) - (prezzo_totale * 100)) / -prezzo_totale
        return lista_migliori_20, prezzo_totale, prezzo_totale_precedente, perdita_guadagno_percentuale

    def stampa(self):
        nome_richiesta_1, volume_richiesta_1 = Report.volume_maggiore(self)
        migliori_10, peggiori_10 = Report.incremento_percentuale_migliori_e_peggiori_24h(self)
        lista_criptovalute_volume_maggiore_24h, volume_24_riferimento, denaro_necessario_2 = Report.acquisto_volume_maggiore_24h(self)
        lista_migliori_20, prezzo_totale, prezzo_totale_precedente, perdita_guadagno_percentuale = Report.guadagno_perdita_percentuale(self)
        lista_capitalizzazione_criptovalute, lista_migliori_20_cap, denaro_necessario = Report.denaro_necessario_acquisto_prime_20_criptovalute(self)

        #Richiesta 1
        print(f"\nLa criptovaluta con il volume maggiore nelle ultime 24 ore è: {nome_richiesta_1}\n"
               f"Il suo volume corrisponde a: {volume_richiesta_1} $")

        #Richiesta 2
        print(f"\nLe 10 criptovalute con l'incremento percentuale MIGLIORE nelle ultime 24 ore sono:")
        for x in migliori_10:
            print(x)

        print(f"\nLe 10 criptovalute con l'incremento percentuale PEGGIORE nelle ultime 24 ore sono:")
        for y in peggiori_10:
            print(y)

        #Richiesta 3
        print(f"\n\nLista delle {len(lista_migliori_20_cap)} criptovalute per capitalizzazione di mercato:")
        for x in lista_migliori_20_cap:
            print(x)

        print(f"\nDenaro necessario per comprare ognuna delle {len(lista_migliori_20_cap)} criptovalute: {denaro_necessario} $")

        #Richiesta 4
        print(f"\n\nNumero criptovalute con volume superiore a {volume_24_riferimento} $ nelle ultime 24 ore: {len(lista_criptovalute_volume_maggiore_24h)}")
        print(f"Denaro necessario per comprare ognuna delle {len(lista_criptovalute_volume_maggiore_24h)} criptovalute: {denaro_necessario_2} $")
        print(f"\nLista delle {len(lista_criptovalute_volume_maggiore_24h)} criptovalute:")
        for criptovaluta in lista_criptovalute_volume_maggiore_24h:
            print(criptovaluta)

        #Richiesta 5
        print(f"\n\nAnalisi prezzo totale di acquisto tra ieri ed oggi sulle migliori {len(lista_migliori_20)} criptovalute per capitalizzazione:")
        print(f"- Prezzo totale (ieri): {prezzo_totale_precedente} $")
        print(f"- Prezzo totale (oggi): {prezzo_totale} $")

        if prezzo_totale > prezzo_totale_precedente:
            print(f"- Percentuale di guadagno: {perdita_guadagno_percentuale} %")
        else:
            print(f"- Percentuale di perdita: {perdita_guadagno_percentuale} %")

        timestamp= datetime.datetime.now().strftime("%d_%m_%Y_%H_%M_%S")

        report ={}
        report["richiesta_1"] = []
        report["richiesta_1"].append({
            "nome": nome_richiesta_1,
            "volume_24h": volume_richiesta_1
        })
        report["richiesta_2"] = []
        report["richiesta_2"].append({
            "migliori_10": migliori_10,
            "peggiori_10": peggiori_10
        })
        report["richiesta_3"] = []
        report["richiesta_3"].append({
            "migliori_20": lista_migliori_20_cap,
            "denaro_necessario": denaro_necessario
        })
        report["richiesta_4"] = []
        report["richiesta_4"].append({
            "criptovalute_volume_maggiore_24h": lista_criptovalute_volume_maggiore_24h,
            "denaro_necessario": denaro_necessario_2
        })
        report["richiesta_5"] = []
        report["richiesta_5"].append({
            "prezzo_totale_giorno_precedente": prezzo_totale_precedente,
            "prezzo_totale": prezzo_totale,
            "percentuale_perdita_guadagno": perdita_guadagno_percentuale
        })

        with open(timestamp+".json", "w") as outfile:
            json.dump(report, outfile, indent=4)

risultati = Report()
risultati.stampa()