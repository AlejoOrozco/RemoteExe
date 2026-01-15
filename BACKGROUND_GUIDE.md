# Guía: Ejecutar Listener en Segundo Plano

Esta guía explica cómo hacer que el listener siga ejecutándose después de cerrar la terminal.

## 🪟 Opciones para Windows

### Opción 1: Script Helper (Más Fácil) ⭐ RECOMENDADO

**Para ejecutar en background (ventana minimizada):**
1. Doble clic en `start_listener.bat`
2. El listener se ejecutará en una ventana minimizada
3. Puedes cerrar la terminal original, el listener seguirá corriendo

**Para ejecutar completamente oculto (sin ventana):**
1. Doble clic en `start_listener_hidden.bat`
2. El listener se ejecutará sin ninguna ventana visible
3. Revisa `listener.log` para verificar que está corriendo

**Para detener el listener:**
1. Doble clic en `stop_listener.bat`
2. O abre Task Manager y termina el proceso `python.exe` o `listener.exe`

### Opción 2: Desde CMD Manualmente

**Ejecutar en nueva ventana minimizada:**
```cmd
start /MIN python listener.py
```

**Ejecutar completamente oculto (sin ventana):**
```cmd
start /B pythonw listener.py
```

**Ejecutar y cerrar CMD inmediatamente:**
```cmd
start "" python listener.py
exit
```

### Opción 3: Auto-Start al Iniciar Windows (Mejor para Producción)

Esto hace que el listener inicie automáticamente cuando Windows arranca:

1. **Ejecuta el instalador como Administrador:**
   ```cmd
   # Abre CMD como Administrador (Windows + X -> "Símbolo del sistema (Administrador)")
   cd C:\ruta\a\tu\carpeta
   python install_listener.py
   ```

2. **El listener se iniciará automáticamente en cada arranque**
3. **No necesitas hacer nada más**

## 🍎 Opciones para Mac/Linux

### Opción 1: Usar `nohup` (No Hang Up)

```bash
nohup python3 listener.py > listener_output.log 2>&1 &
```

- `nohup` = No termina el proceso al cerrar la terminal
- `> listener_output.log` = Redirige la salida a un archivo
- `2>&1` = También captura errores
- `&` = Ejecuta en background

**Para detener:**
```bash
# Encontrar el proceso
ps aux | grep listener.py

# Matar el proceso (reemplaza PID con el número que encuentres)
kill PID
```

### Opción 2: Usar `screen` (Recomendado)

```bash
# Instalar screen (si no está instalado)
# macOS: brew install screen
# Linux: sudo apt-get install screen

# Iniciar screen
screen -S remoteexe

# Dentro de screen, ejecutar el listener
python3 listener.py

# Presionar Ctrl+A luego D para "detach" (salir sin cerrar)
# El listener seguirá corriendo

# Para volver a ver el listener:
screen -r remoteexe

# Para detener: entrar a screen y presionar Ctrl+C
```

### Opción 3: Usar `tmux` (Alternativa a screen)

```bash
# Instalar tmux (si no está instalado)
# macOS: brew install tmux
# Linux: sudo apt-get install tmux

# Iniciar nueva sesión
tmux new -s remoteexe

# Ejecutar listener
python3 listener.py

# Presionar Ctrl+B luego D para "detach"

# Para volver:
tmux attach -t remoteexe
```

## 🔍 Verificar que Está Corriendo

### Windows

**Ver procesos Python:**
```cmd
tasklist | findstr python
```

**Ver si el puerto está en uso:**
```cmd
netstat -an | findstr 8888
```

**Revisar el log:**
```cmd
type listener.log
```

### Mac/Linux

**Ver procesos:**
```bash
ps aux | grep listener
```

**Ver si el puerto está en uso:**
```bash
lsof -i :8888
# O
netstat -an | grep 8888
```

**Revisar el log:**
```bash
tail -f listener.log
```

## 🛑 Detener el Listener

### Windows

**Método 1: Script helper**
```cmd
stop_listener.bat
```

**Método 2: Task Manager**
1. Abre Task Manager (Ctrl+Shift+Esc)
2. Busca `python.exe` o `listener.exe`
3. Clic derecho -> "Finalizar tarea"

**Método 3: Desde CMD**
```cmd
taskkill /F /IM python.exe /FI "WINDOWTITLE eq listener.py*"
```

### Mac/Linux

**Encontrar y matar:**
```bash
# Encontrar el PID
ps aux | grep listener.py

# Matar (reemplaza PID)
kill PID

# Si no funciona, forzar:
kill -9 PID
```

## 📝 Recomendaciones

### Para Desarrollo/Pruebas:
- Usa `start_listener.bat` (Windows) o `screen` (Mac/Linux)
- Fácil de iniciar y detener
- Puedes ver los logs en tiempo real

### Para Producción:
- Usa `install_listener.py` para auto-start en Windows
- El listener iniciará automáticamente en cada arranque
- Corre como servicio del sistema

### Para Máquinas Virtuales:
- Usa `start_listener_hidden.bat` o `pythonw listener.py`
- No ocupa espacio en pantalla
- Revisa `listener.log` para verificar estado

## ⚠️ Notas Importantes

1. **Logs**: Siempre revisa `listener.log` para ver qué está pasando
2. **Firewall**: Asegúrate de que los puertos 8888 y 8889 estén abiertos
3. **Permisos**: Algunos comandos pueden requerir permisos de administrador
4. **Configuración**: Asegúrate de que `config.json` esté en la misma carpeta

## 🐛 Solución de Problemas

**El listener no inicia:**
- Verifica que Python esté instalado
- Revisa `listener.log` para errores
- Asegúrate de que `config.json` existe

**El listener se detiene al cerrar terminal:**
- Usa `start_listener.bat` en lugar de ejecutar directamente
- O usa `pythonw` en lugar de `python` (Windows)

**No puedo conectarme desde broadcaster:**
- Verifica que el listener esté corriendo: `tasklist | findstr python`
- Verifica el firewall
- Revisa que la IP sea correcta
