import subprocess, time, os


bot = subprocess.Popen(["python", "bot.py"])
script = subprocess.Popen(["python", "script.py"])

if input('Нажмите Enter для завершения'):
    bot.terminate()
    script.terminate()
    