import datetime as dt

fuso = dt.timezone(dt.timedelta(hours=-3))

def tempo_desde(data):

  if data is None:
      return "Nunca acessou"

  if data.tzinfo is None:
      data = data.replace(tzinfo=fuso)

  agora = dt.datetime.now(fuso)

  diferenca = agora - data

  segundos = int(diferenca.total_seconds())

  if segundos < 60:
      return "🟢 Online agora"

  if segundos < 3600:
      minutos = segundos // 60
      return f"Visto há {minutos} min"

  if segundos < 86400:
      horas = segundos // 3600
      minutos = (segundos % 3600) // 60

      if minutos:
          return f"Visto há {horas}h {minutos}min"

      return f"Visto há {horas}h"

  dias = diferenca.days

  if dias == 1:
      return "Visto ontem"

  return f"Visto há {dias} dias"