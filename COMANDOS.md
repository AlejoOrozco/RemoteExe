# Lista de Comandos para RemoteExe

Esta guía contiene comandos útiles que puedes ejecutar remotamente en Windows desde tu Mac.

## 📋 Índice
- [Gestión de Procesos](#gestión-de-procesos)
- [Sistema y Apagado](#sistema-y-apagado)
- [Información del Sistema](#información-del-sistema)
- [Red y Conectividad](#red-y-conectividad)
- [Archivos y Carpetas](#archivos-y-carpetas)
- [Mensajes y Notificaciones](#mensajes-y-notificaciones)
- [Servicios de Windows](#servicios-de-windows)
- [Usuarios y Sesiones](#usuarios-y-sesiones)
- [Registro de Windows](#registro-de-windows)
- [Utilidades Útiles](#utilidades-útiles)

---

## 🔄 Gestión de Procesos

### Ver procesos corriendo
```cmd
tasklist
```

### Ver procesos de un programa específico
```cmd
tasklist | findstr chrome
tasklist | findstr python
tasklist | findstr notepad
```

### Cerrar un proceso por nombre
```cmd
taskkill /F /IM notepad.exe
taskkill /F /IM chrome.exe
taskkill /F /IM firefox.exe
taskkill /F /IM python.exe
```

### Cerrar proceso por PID
```cmd
# Primero encuentra el PID
tasklist | findstr chrome

# Luego cierra con el PID
taskkill /F /PID 1234
```

### Cerrar múltiples procesos
```cmd
taskkill /F /IM chrome.exe /IM firefox.exe
```

### Cerrar proceso y sus hijos
```cmd
taskkill /F /IM chrome.exe /T
```

---

## ⚡ Sistema y Apagado

### Apagar el PC
```cmd
shutdown /s /t 60
```
- `/s` = Apagar
- `/t 60` = Esperar 60 segundos

### Apagar inmediatamente
```cmd
shutdown /s /t 0
```

### Reiniciar el PC
```cmd
shutdown /r /t 60
```
- `/r` = Reiniciar
- `/t 60` = Esperar 60 segundos

### Reiniciar inmediatamente
```cmd
shutdown /r /t 0
```

### Reiniciar forzado (cierra programas)
```cmd
shutdown /r /f /t 0
```

### Cancelar apagado/reinicio programado
```cmd
shutdown /a
```

### Cerrar sesión
```cmd
shutdown /l
```

### Hibernar
```cmd
shutdown /h
```

### Suspender
```cmd
rundll32.exe powrprof.dll,SetSuspendState 0,1,0
```

---

## 💻 Información del Sistema

### Información completa del sistema
```cmd
systeminfo
```

### Información del sistema (resumida)
```cmd
systeminfo | findstr /C:"OS Name" /C:"OS Version" /C:"System Type"
```

### Nombre de la computadora
```cmd
hostname
```

### Usuario actual
```cmd
echo %USERNAME%
```

### Fecha y hora
```cmd
date /t
time /t
```

### Versión de Windows
```cmd
ver
```

### Información de CPU
```cmd
wmic cpu get name,numberofcores,numberoflogicalprocessors
```

### Información de memoria
```cmd
wmic computersystem get TotalPhysicalMemory
systeminfo | findstr /C:"Total Physical Memory"
```

### Espacio en disco
```cmd
wmic logicaldisk get size,freespace,caption
```

### Espacio en disco (formato legible)
```cmd
fsutil volume diskfree C:
```

---

## 🌐 Red y Conectividad

### Ver configuración de red
```cmd
ipconfig
```

### Ver IP detallada
```cmd
ipconfig /all
```

### Renovar IP (DHCP)
```cmd
ipconfig /renew
```

### Liberar IP
```cmd
ipconfig /release
```

### Ver conexiones de red activas
```cmd
netstat -an
```

### Ver puertos en uso
```cmd
netstat -an | findstr LISTENING
```

### Ver conexiones establecidas
```cmd
netstat -an | findstr ESTABLISHED
```

### Ping a un servidor
```cmd
ping google.com
ping 8.8.8.8
```

### Ver tabla de enrutamiento
```cmd
route print
```

### Ver conexiones de red con procesos
```cmd
netstat -ano
```

---

## 📁 Archivos y Carpetas

### Listar archivos en carpeta actual
```cmd
dir
```

### Listar archivos en otra carpeta
```cmd
dir C:\Users
```

### Listar archivos ocultos
```cmd
dir /a
```

### Cambiar de directorio
```cmd
cd C:\Users\TuUsuario\Documents
```

### Ver directorio actual
```cmd
cd
```

### Crear carpeta
```cmd
mkdir C:\NuevaCarpeta
```

### Eliminar carpeta vacía
```cmd
rmdir C:\CarpetaVacia
```

### Eliminar carpeta y contenido
```cmd
rmdir /s /q C:\Carpeta
```

### Copiar archivo
```cmd
copy C:\origen.txt C:\destino.txt
```

### Mover archivo
```cmd
move C:\origen.txt C:\destino.txt
```

### Eliminar archivo
```cmd
del C:\archivo.txt
```

### Ver contenido de archivo
```cmd
type C:\archivo.txt
```

### Buscar archivos
```cmd
dir /s C:\*.txt
```

---

## 💬 Mensajes y Notificaciones

### Mensaje con MessageBox (PowerShell)
```cmd
powershell -Command "[System.Windows.Forms.MessageBox]::Show('Tu mensaje aquí', 'Título', 'OK', 'Information')"
```

### Mensaje de advertencia
```cmd
powershell -Command "[System.Windows.Forms.MessageBox]::Show('Mensaje de advertencia', 'Advertencia', 'OK', 'Warning')"
```

### Mensaje de error
```cmd
powershell -Command "[System.Windows.Forms.MessageBox]::Show('Mensaje de error', 'Error', 'OK', 'Error')"
```

### Mensaje con VBScript (alternativa)
```cmd
cscript //nologo -e:vbscript -c:MsgBox "Tu mensaje aquí", vbInformation, "Título"
```

### Notificación Toast (Windows 10/11)
```cmd
powershell -Command "New-BurntToastNotification -Text 'Tu mensaje aquí'"
```

---

## 🔧 Servicios de Windows

### Ver todos los servicios
```cmd
sc query
```

### Ver estado de un servicio específico
```cmd
sc query Spooler
```

### Iniciar un servicio
```cmd
sc start Spooler
```

### Detener un servicio
```cmd
sc stop Spooler
```

### Ver servicios corriendo
```cmd
net start
```

---

## 👥 Usuarios y Sesiones

### Ver usuarios del sistema
```cmd
net user
```

### Ver información de un usuario
```cmd
net user nombre_usuario
```

### Ver usuarios conectados
```cmd
query user
```

### Desconectar una sesión
```cmd
logoff ID_SESION
```

### Ver sesiones activas
```cmd
quser
```

---

## 🔐 Registro de Windows

### Ver valor del registro (PowerShell)
```cmd
powershell -Command "Get-ItemProperty -Path 'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion' -Name ProgramFilesDir"
```

### Exportar clave del registro
```cmd
reg export HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run C:\backup.reg
```

### Importar clave del registro
```cmd
reg import C:\backup.reg
```

---

## 🛠️ Utilidades Útiles

### Limpiar pantalla
```cmd
cls
```

### Ver variables de entorno
```cmd
set
```

### Ver una variable específica
```cmd
echo %PATH%
echo %USERNAME%
echo %COMPUTERNAME%
```

### Ver historial de comandos
```cmd
doskey /history
```

### Abrir calculadora
```cmd
calc
```

### Abrir notepad
```cmd
notepad
```

### Abrir explorador de archivos
```cmd
explorer
```

### Abrir explorador en carpeta específica
```cmd
explorer C:\Users
```

### Ver eventos del sistema
```cmd
wevtutil qe System /c:10 /rd:true /f:text
```

### Ver eventos de aplicación
```cmd
wevtutil qe Application /c:10 /rd:true /f:text
```

### Ver información de BIOS
```cmd
wmic bios get name,version,releasedate
```

### Ver programas instalados
```cmd
wmic product get name,version
```

### Ver programas instalados (más rápido)
```cmd
powershell -Command "Get-WmiObject -Class Win32_Product | Select-Object Name, Version"
```

---

## 🎯 Comandos Útiles para RemoteExe

### Verificar que el listener está corriendo
```cmd
netstat -an | findstr 8888
tasklist | findstr python
```

### Ver el log del listener (si está en C:\)
```cmd
type listener.log
```

### Ver últimas líneas del log
```cmd
powershell -Command "Get-Content listener.log -Tail 20"
```

### Verificar conectividad desde el PC remoto
```cmd
ping TU_IP_MAC
```

### Ver firewall y reglas
```cmd
netsh advfirewall firewall show rule name=all
```

---

## ⚠️ Comandos Peligrosos (Usar con Cuidado)

### Formatear disco (MUY PELIGROSO)
```cmd
format C: /FS:NTFS
```
**⚠️ NO EJECUTAR - Borrará todo el disco**

### Eliminar System32 (DESTRUCTIVO)
```cmd
rmdir /s /q C:\Windows\System32
```
**⚠️ NO EJECUTAR - Destruirá Windows**

### Eliminar todo en una carpeta
```cmd
del /f /s /q C:\Carpeta\*
```
**⚠️ Usar con precaución**

---

## 💡 Tips y Trucos

### Combinar comandos con pipe (|)
```cmd
tasklist | findstr chrome
systeminfo | findstr /C:"OS Name"
```

### Redirigir salida a archivo
```cmd
tasklist > procesos.txt
systeminfo > info_sistema.txt
```

### Ejecutar múltiples comandos
```cmd
tasklist & systeminfo & ipconfig
```

### Comandos en PowerShell
```cmd
powershell -Command "Get-Process | Where-Object {$_.CPU -gt 10}"
```

---

## 📝 Notas Importantes

1. **Permisos**: Algunos comandos requieren permisos de administrador
2. **Rutas**: Usa rutas completas cuando sea posible
3. **Espacios**: Si hay espacios en rutas, usa comillas: `"C:\Program Files\..."`
4. **PowerShell**: Los comandos de PowerShell pueden ser más potentes pero más lentos
5. **Seguridad**: No ejecutes comandos destructivos sin estar seguro

---

## 🔍 Búsqueda Rápida

¿Qué quieres hacer? | Comando
--- | ---
Cerrar un programa | `taskkill /F /IM programa.exe`
Reiniciar PC | `shutdown /r /t 60`
Ver procesos | `tasklist`
Ver IP | `ipconfig`
Mensaje visible | `powershell -Command "[System.Windows.Forms.MessageBox]::Show('Mensaje', 'Título', 'OK', 'Information')"`
Ver información sistema | `systeminfo`
Ver espacio disco | `wmic logicaldisk get size,freespace,caption`

---

**¿Necesitas un comando específico?** Busca en esta lista o pregunta y te ayudo a encontrarlo.
