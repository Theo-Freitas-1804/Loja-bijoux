from datetime import date, timedelta
from flask import request


def calcular_proxima_sexta():
  hoje = date.today()

  dias_ate_sexta = (4 - hoje.weekday()) % 7

  if dias_ate_sexta == 0:
      dias_ate_sexta = 7

  return hoje + timedelta(days=dias_ate_sexta)


def calcular_data_entrega():

  horario = request.form.get("horario")

  if horario == "proxima_sexta":

      return calcular_proxima_sexta()

  elif horario == "sexta_seguinte":

      return calcular_proxima_sexta() + timedelta(days=7)

  elif horario == "agendado":

      data_agendada = request.form.get(
          "data_agendada"
      )

      return date.fromisoformat(
          data_agendada
      )

  return None