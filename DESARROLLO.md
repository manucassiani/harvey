# Guía de Desarrollo - Harvey

## Scripts de Desarrollo

### 🚀 Iniciar Harvey
```bash
./start_harvey.sh
```

**¿Qué hace?**
- Activa el entorno virtual de Python
- Instala dependencias automáticamente
- Inicia el backend FastAPI en puerto 8000
- Inicia el frontend React en puerto 5173
- Monitorea ambos servicios

**Servicios disponibles:**
- 🌐 Frontend: http://localhost:8080
- 🔧 Backend: http://localhost:8000
- 📚 API Docs: http://localhost:8000/docs

### 📊 Monitorear Logs
```bash
./logs_harvey.sh
```

**¿Qué hace?**
- Muestra logs en tiempo real
- Distingue entre backend y frontend con colores
- Útil para debugging

### 🛑 Detener Harvey
```bash
./stop_harvey.sh
```

**¿Qué hace?**
- Detiene todos los servicios de manera limpia
- Mata procesos en puertos 8000 y 8080
- Limpia archivos de logs
- Verifica que no queden procesos ejecutándose

## Flujo de Trabajo Recomendado

1. **Iniciar desarrollo:**
   ```bash
   ./start_harvey.sh
   ```

2. **Monitorear logs (en otra terminal):**
   ```bash
   ./logs_harvey.sh
   ```

3. **Desarrollar normalmente**
   - Los archivos se recargan automáticamente
   - Backend con hot reload
   - Frontend con hot reload

4. **Detener al finalizar:**
   ```bash
   ./stop_harvey.sh
   ```

## Resolución de Problemas

### Error: "El entorno virtual 'harvey' no existe"
```bash
pyenv virtualenv 3.12.11 harvey
pyenv local harvey
```

### Error: "No se encontró npm"
```bash
sudo apt update
sudo apt install nodejs npm
```

### Puertos ocupados
```bash
# Verificar qué está usando los puertos
lsof -i :8000
lsof -i :8080

# Usar el script de detener
./stop_harvey.sh
```

### Logs no aparecen
```bash
# Verificar que los archivos existan
ls -la *.log

# Los logs se crean cuando se inician los servicios
```

## Desarrollo Manual (Alternativo)

Si prefieres manejar los servicios manualmente:

### Backend
```bash
cd backend
source venv/bin/activate  # o: pyenv activate harvey
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend
```bash
cd frontend
npm run dev
```

## Tips de Desarrollo

- **Usa los scripts**: Son más confiables que manejar todo manualmente
- **Monitorea logs**: Te ayuda a detectar problemas rápidamente
- **Detén limpiamente**: Evita procesos zombi que pueden causar problemas
- **Reinstala dependencias**: Si algo falla, los scripts reinstalan automáticamente 