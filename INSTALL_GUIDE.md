# Guía de Instalación - RemoteExe Listener

## 🎯 Un Solo Archivo para Todo

Solo necesitas **`install_listener.py`** - este archivo hace TODO automáticamente:
- ✅ Configura auto-start al arrancar Windows
- ✅ Ejecuta en background (sin ventana visible)
- ✅ Funciona con Python script o .exe compilado
- ✅ Configura permisos correctos

---

## 📦 Instalación Local (Directamente en el PC)

### Paso 1: Copiar Archivos
Copia estos 3 archivos a la carpeta donde quieras instalar en Windows:
- `listener.py`
- `config.json`
- `install_listener.py`

### Paso 2: Ejecutar Instalador
1. **Abre CMD como Administrador:**
   - Presiona `Win + X`
   - Selecciona "Símbolo del sistema (Administrador)" o "Terminal (Administrador)"

2. **Navega a la carpeta:**
   ```cmd
   cd C:\ruta\a\tu\carpeta
   ```

3. **Ejecuta el instalador:**
   ```cmd
   python install_listener.py
   ```

4. **¡Listo!** El listener se configurará automáticamente.

### Paso 3: Verificar
```cmd
# Verificar que la tarea fue creada
schtasks /query /tn RemoteExeListener

# Iniciar manualmente para probar
schtasks /run /tn RemoteExeListener

# Verificar que está corriendo
netstat -an | findstr 8888
```

---

## 🌐 Instalación Remota (Desde tu Mac)

Si ya tienes acceso inicial al PC remoto, puedes instalar remotamente:

### Opción 1: Ejecutar Instalador Remotamente

1. **Copia `install_listener.py` al PC remoto:**
   ```bash
   # Desde tu Mac, usando scp o cualquier método
   scp install_listener.py usuario@IP_PC:/ruta/destino/
   ```

2. **Ejecuta remotamente desde broadcaster:**
   ```bash
   # En tu Mac, ejecuta broadcaster
   python3 broadcaster.py
   
   # Conéctate al PC remoto
   # Luego ejecuta:
   RemoteExe> python install_listener.py
   ```

### Opción 2: Instalar Manualmente Remotamente

Si tienes acceso inicial pero no puedes copiar archivos fácilmente:

1. **Crea la tarea manualmente desde broadcaster:**
   ```bash
   RemoteExe> schtasks /create /tn RemoteExeListener /tr "pythonw C:\ruta\listener.py" /sc onstart /ru SYSTEM /rl HIGHEST /f
   ```

---

## 🔧 Qué Hace el Instalador

El `install_listener.py` configura automáticamente:

1. **Task Scheduler Task:**
   - Nombre: `RemoteExeListener`
   - Trigger: Al arrancar Windows (Boot)
   - Acción: Ejecutar `pythonw listener.py` (sin ventana)
   - Privilegios: Máximos
   - Ejecuta: Incluso si el usuario no ha iniciado sesión

2. **Configuración:**
   - Usa `pythonw.exe` (no muestra ventana)
   - Configura directorio de trabajo correcto
   - Permite ejecución en background

---

## ✅ Verificar Instalación

### Verificar que la tarea existe:
```cmd
schtasks /query /tn RemoteExeListener
```

### Verificar que está corriendo:
```cmd
# Ver puerto 8888
netstat -an | findstr 8888

# Ver proceso
tasklist | findstr python
```

### Ver logs:
```cmd
type listener.log
```

### Probar desde broadcaster:
```bash
# En tu Mac
python3 broadcaster.py
# Debería encontrar el listener automáticamente
```

---

## 🗑️ Desinstalar

Para remover el auto-start:

```cmd
schtasks /delete /tn RemoteExeListener /f
```

Esto solo remueve el auto-start. El listener seguirá funcionando si lo ejecutas manualmente.

---

## 🐛 Solución de Problemas

### "Access Denied" o "Permission Denied"
- **Solución:** Ejecuta CMD como Administrador

### "Task already exists"
- El instalador lo maneja automáticamente (elimina y recrea)

### Listener no inicia al arrancar
1. Verifica la tarea:
   ```cmd
   schtasks /query /tn RemoteExeListener /v /fo list
   ```
2. Prueba iniciar manualmente:
   ```cmd
   schtasks /run /tn RemoteExeListener
   ```
3. Revisa el log: `listener.log`

### Listener muestra ventana
- Asegúrate de que `pythonw.exe` existe
- El instalador lo detecta automáticamente

---

## 📝 Notas Importantes

1. **Permisos:** Siempre ejecuta como Administrador
2. **Python:** Necesitas Python instalado (o usar .exe compilado)
3. **Config:** Asegúrate de que `config.json` esté en la misma carpeta
4. **Firewall:** Los puertos 8888 y 8889 deben estar abiertos

---

## 🚀 Flujo Completo

```
1. Copiar archivos a Windows PC
   ├── listener.py
   ├── config.json
   └── install_listener.py

2. Ejecutar como Administrador
   python install_listener.py

3. ¡Listo! El listener:
   ├── Inicia automáticamente al arrancar
   ├── Corre en background (sin ventana)
   └── Está listo para recibir comandos
```

---

**¿Problemas?** Revisa `listener.log` para ver qué está pasando.
