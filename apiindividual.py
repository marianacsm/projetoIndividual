import psutil

ociosidade = psutil.cpu_times_percent(percpu=False).idle / 3600
temperatura = psutil.sensors_temperatures()['nvme'][0].current

print("Ociosidade:", round(ociosidade,2), "Horas")

print("Temperatura:", temperatura, "°C")

#importar a classe slack do arquivo slackCredentials.py
 
from slackCredentials import Slack






