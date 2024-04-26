from .models import FormazioneCantieri, FormazioneCantieri_Cantieri


def rigo_3():
    duvri = FormazioneCantieri_Cantieri.objects.filter(tipo='0', in_corso=True)

    print(duvri.count())
    for ifa in duvri:
        formazioni = FormazioneCantieri.objects.filter(cantiere=ifa)

        for formazione in formazioni:
            print(formazione.nome_documento())
        print()
    #
    cantieri_in_corso = FormazioneCantieri_Cantieri.objects.filter(tipo='1', in_corso=True)

    for cantiere in cantieri_in_corso:
        formazioni = FormazioneCantieri.objects.filter(cantiere=cantiere)

        print(cantiere, formazioni.count())
        for formazione in formazioni:
            print(formazione.nome_documento())

        print()


    return
