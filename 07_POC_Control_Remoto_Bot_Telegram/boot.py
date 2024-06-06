## Contenido boot.py (archivo de configuracion se ejecuta nada mas arrancar la maq)
## Aqui se definen los parametros USB (se ejecuta antes del usb)


import usb_cdc, usb_hid, storage, supervisor

storage.disable_usb_drive() #desabilito storaje para liberar endpoints
#Haces el dispositivo mas dificil de detectar


#Configuro parametros USB:         Fabricante    , Producto          , VID  , PID
supervisor.set_usb_identification("c1b3rtr4cks_2024","Hack_USB_Python",0x2E8A,0x0005)


#Ojo si desabilitas el CDC y el usb_drive pierdes el control
#Pero haces el dispositivo mas dificil de detectar
#usb_cdc.enable(console=False, data=True)    # desabilita cdc

#Habilito Raton (para que haga de jiggler)
#usb_hid.enable((usb_hid.Device.MOUSE,))
usb_hid.enable((usb_hid.Device.KEYBOARD,usb_hid.Device.MOUSE))


print("fin boot.py")