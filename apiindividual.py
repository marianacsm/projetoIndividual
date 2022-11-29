import psutil
import slack

ociosidade = psutil.cpu_times_percent(percpu=False).idle / 3600

temperatura = psutil.sensors_temperatures()['nvme'][0].current

print("Ociosidade:", round(ociosidade,2), "Horas")

print("Temperatura:", temperatura, "°C")

# #importar a classe slack do arquivo slackCredentials.py
# from slackCredentials.py import Slack

# #instanciar a classe Slack
# slack = Slack()

# #enviar mensagem para o canal #general
# slack.post_message("#general", "Ociosidade: " + str(round(ociosidade,2)) + " Horas")
# slack.post_message("#general", "Temperatura: " + str(temperatura) + " °C")










