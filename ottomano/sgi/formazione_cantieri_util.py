from .models import FormazioneCantieri, FormazioneCantieri_Cantieri, FORMAZIONE_CANTIERI_CANTIERE_TIPO
from django_pandas.io import read_frame
from personale.models import Lavoratore


class IntestazioneTabella:
    def __init__(self):
        self._analizza2()
        self._crea_df()

    def _crea_df(self):
        lavoratori = Lavoratore.objects.filter(in_forza=True).exclude(cantiere__cantiere='Uffici Sede')
        df = read_frame(lavoratori)
        df = df[['id', 'cognome', 'nome']]

        formazioni = FormazioneCantieri.objects.filter(attivo=True)

        for formazione in formazioni:
            id_formazione = formazione.pk
            df[str(id_formazione)] = False

            qs_id_lavoratori_formati = formazione.lavoratori.all().values_list('id')
            # print(a)
            id_lavoratori_formati =[x[0] for x in qs_id_lavoratori_formati]
            print(id_lavoratori_formati)

            a = df['id'].isin(id_lavoratori_formati)
            print(a)
            # return
            print()
        print(df)

    def _analizza2(self):
        rigo1 = []
        rigo2 = []
        rigo3 = []
        for codice, tipo in FORMAZIONE_CANTIERI_CANTIERE_TIPO:
            cantieri_per_tipo = FormazioneCantieri_Cantieri.objects.filter(tipo=codice, in_corso=True)

            n_colonne_cantieri = 0
            for cantiere in cantieri_per_tipo:
                documenti = FormazioneCantieri.objects.filter(cantiere=cantiere)
                # print(documenti.count())

                for documento in documenti:
                    # print(documento.nome_documento())
                    rigo3.append(documento.nome_documento())

                rigo2.append((cantiere, documenti.count()))
                n_colonne_cantieri += documenti.count()

            rigo1.append((tipo, n_colonne_cantieri))

        self.rigo1 = rigo1
        self.rigo2 = rigo2
        self.rigo3 = rigo3

        self._analizza()

    def _analizza(self):
        duvri = FormazioneCantieri_Cantieri.objects.filter(tipo='0', in_corso=True)

        cantieri = []
        documenti = []
        for ifa in duvri:
            formazioni = FormazioneCantieri.objects.filter(cantiere=ifa)

            for formazione in formazioni:
                documenti.append(formazione.nome_documento())

        cantieri_in_corso = FormazioneCantieri_Cantieri.objects.filter(tipo='1', in_corso=True)

        for cantiere in cantieri_in_corso:
            formazioni = FormazioneCantieri.objects.filter(cantiere=cantiere)

            for formazione in formazioni:
                documenti.append(formazione.nome_documento())

        cantieri_esterni_in_corso = FormazioneCantieri_Cantieri.objects.filter(tipo='2', in_corso=True)

        for cantiere in cantieri_esterni_in_corso:
            formazioni = FormazioneCantieri.objects.filter(cantiere=cantiere)

            for formazione in formazioni:
                documenti.append(formazione.nome_documento())

        self.rigo_3 = documenti


def rigo_3():
    # todo: obsoleto
    duvri = FormazioneCantieri_Cantieri.objects.filter(tipo='0', in_corso=True)

    # print(duvri.count())
    ifa_in_corso = []
    for ifa in duvri:
        formazioni = FormazioneCantieri.objects.filter(cantiere=ifa)

        for formazione in formazioni:
            ifa_in_corso.append(formazione.nome_documento())

    cantieri_in_corso = FormazioneCantieri_Cantieri.objects.filter(tipo='1', in_corso=True)

    cantieri_eni = []
    for cantiere in cantieri_in_corso:
        formazioni = FormazioneCantieri.objects.filter(cantiere=cantiere)

        print(cantiere, formazioni.count())
        for formazione in formazioni:
            cantieri_eni.append(formazione.nome_documento())

    cantieri_esterni_in_corso = FormazioneCantieri_Cantieri.objects.filter(tipo='2', in_corso=True)

    cantieri_esterni = []
    for cantiere in cantieri_esterni_in_corso:
        formazioni = FormazioneCantieri.objects.filter(cantiere=cantiere)

        print(cantiere, formazioni.count())
        for formazione in formazioni:
            cantieri_esterni.append(formazione.nome_documento())

    return ifa_in_corso, cantieri_eni, cantieri_esterni
