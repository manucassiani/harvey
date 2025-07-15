#!/bin/bash

# Harvey - Script para ver logs en tiempo real
echo "📊 Monitoreando logs de Harvey..."
echo "================================"

# Colores para mejor visualización
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Verificar que los archivos de logs existan
if [ ! -f "backend.log" ] && [ ! -f "frontend.log" ]; then
    echo -e "${RED}❌ No se encontraron archivos de logs${NC}"
    echo -e "${YELLOW}💡 Primero ejecute: ./start_harvey.sh${NC}"
    exit 1
fi

# Función para limpiar al salir
cleanup() {
    echo -e "\n${YELLOW}🛑 Deteniendo monitoreo de logs...${NC}"
    exit 0
}

# Capturar señales para cleanup
trap cleanup SIGINT SIGTERM

echo -e "${GREEN}✅ Monitoreando logs en tiempo real${NC}"
echo -e "${YELLOW}⚠️  Para detener el monitoreo presione Ctrl+C${NC}"
echo "================================"

# Usar multitail si está disponible, sino usar tail
if command -v multitail > /dev/null 2>&1; then
    echo -e "${BLUE}📱 Usando multitail para mejor visualización...${NC}"
    multitail -ci green -l "tail -f backend.log" -ci blue -l "tail -f frontend.log"
else
    echo -e "${BLUE}📱 Mostrando logs combinados...${NC}"
    echo ""
    
    # Mostrar logs con prefijos de colores
    tail -f backend.log frontend.log | while read line; do
        if [[ "$line" =~ ^==\> ]]; then
            # Línea de separación de archivos
            echo -e "${YELLOW}$line${NC}"
        elif [[ "$line" =~ backend\.log ]]; then
            # Skip the filename line
            continue
        elif [[ "$line" =~ frontend\.log ]]; then
            # Skip the filename line
            continue
        else
            # Determinar si es backend o frontend basado en el contexto
            if [[ "$line" =~ (uvicorn|FastAPI|INFO|WARNING|ERROR) ]]; then
                echo -e "${GREEN}[BACKEND]${NC} $line"
            elif [[ "$line" =~ (vite|Local:|Network:|ready|compiled) ]]; then
                echo -e "${BLUE}[FRONTEND]${NC} $line"
            else
                echo "$line"
            fi
        fi
    done
fi 