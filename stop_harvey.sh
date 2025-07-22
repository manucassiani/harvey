#!/bin/bash

# Harvey - Script para detener servicios
echo "🛑 Deteniendo Harvey..."
echo "================================"

# Colores para mejor visualización
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Función para encontrar y matar procesos
kill_process() {
    local process_name=$1
    local port=$2
    
    echo -e "${BLUE}🔍 Buscando procesos de ${process_name}...${NC}"
    
    # Buscar por puerto
    if [ ! -z "$port" ]; then
        local pids=$(lsof -ti:$port 2>/dev/null)
        if [ ! -z "$pids" ]; then
            echo -e "${YELLOW}📋 Matando procesos en puerto $port: $pids${NC}"
            echo $pids | xargs kill -TERM 2>/dev/null
            sleep 2
            # Si aún están corriendo, usar kill -9
            echo $pids | xargs kill -9 2>/dev/null
            echo -e "${GREEN}✅ Procesos en puerto $port terminados${NC}"
        else
            echo -e "${YELLOW}ℹ️  No se encontraron procesos en puerto $port${NC}"
        fi
    fi
    
    # Buscar por nombre de proceso
    local pids=$(pgrep -f "$process_name" 2>/dev/null)
    if [ ! -z "$pids" ]; then
        echo -e "${YELLOW}📋 Matando procesos de $process_name: $pids${NC}"
        echo $pids | xargs kill -TERM 2>/dev/null
        sleep 2
        # Si aún están corriendo, usar kill -9
        echo $pids | xargs kill -9 2>/dev/null
        echo -e "${GREEN}✅ Procesos de $process_name terminados${NC}"
    else
        echo -e "${YELLOW}ℹ️  No se encontraron procesos de $process_name${NC}"
    fi
}

# Detener backend (FastAPI/uvicorn)
echo -e "${RED}🔴 Deteniendo Backend...${NC}"
kill_process "uvicorn" "8000"

# Detener frontend (Vite dev server)
echo -e "${RED}🔴 Deteniendo Frontend...${NC}"
kill_process "vite" "8080"

# Limpiar archivos de logs si existen
if [ -f "backend.log" ] || [ -f "frontend.log" ]; then
    echo -e "${BLUE}🧹 Limpiando archivos de logs...${NC}"
    rm -f backend.log frontend.log
    echo -e "${GREEN}✅ Archivos de logs eliminados${NC}"
fi

# Verificar que no queden procesos
echo -e "${BLUE}🔍 Verificación final...${NC}"
backend_running=$(lsof -ti:8000 2>/dev/null)
frontend_running=$(lsof -ti:8080 2>/dev/null)

if [ -z "$backend_running" ] && [ -z "$frontend_running" ]; then
    echo -e "${GREEN}✅ Todos los servicios han sido detenidos correctamente${NC}"
else
    echo -e "${YELLOW}⚠️  Algunos procesos pueden seguir ejecutándose${NC}"
    if [ ! -z "$backend_running" ]; then
        echo -e "${RED}   - Backend aún en puerto 8000${NC}"
    fi
    if [ ! -z "$frontend_running" ]; then
        echo -e "${RED}   - Frontend aún en puerto 8080${NC}"
    fi
fi

echo "================================"
echo -e "${GREEN}🎉 Harvey ha sido detenido${NC}" 