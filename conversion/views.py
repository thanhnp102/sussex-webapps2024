from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import Conversion

gbp_exchange = {"data":{"AUD":1.9383244007,"BGN":2.282195937,"BRL":6.5281650224,"CAD":1.7174559977,"CHF":1.1342044526,"CNY":8.9998388167,"CZK":29.4487737788,"DKK":8.7315791787,"EUR":1.1702822862,"GBP":1,"HKD":9.7315289796,"HRK":8.4654822684,"HUF":462.3166386099,"IDR":20091.4827255399,"ILS":4.6703882505,"INR":103.9369186207,"ISK":176.5558541986,"JPY":192.2928400392,"KRW":1725.5886213902,"MXN":21.1697842728,"MYR":5.9593346729,"NOK":13.6446909414,"NZD":2.1095889279,"PHP":70.8695401098,"PLN":5.109961762,"RON":5.8221591763,"RUB":116.999903272,"SEK":13.6083889814,"SGD":1.6960726912,"THB":45.5949649925,"TRY":40.4024635363,"USD":1.2432087954,"ZAR":23.6580810705}}


@api_view(['GET'])
def exchange(request, base_currency):
    base_currency = base_currency.upper()
    if base_currency == "GBP":
        rates = {
            "base_currency": base_currency,
            "data": gbp_exchange["data"]
        }
    else:
        rates = {
            "base_currency": base_currency,
            "data": dict()
        }
        rates["data"]["GBP"] = 1/gbp_exchange["data"][base_currency]
        for currency, rate in gbp_exchange["data"].items():
            rates["data"][currency] = gbp_exchange["data"][currency] * rates["data"]["GBP"]
    serializer = Conversion(rates)
    return Response(serializer.data)
