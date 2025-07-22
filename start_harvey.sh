#!/bin/bash

# Harvey - Script para iniciar backend y frontend
echo "🚀 Iniciando Harvey..."
echo "================================"

# Colores para mejor visualización
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Función para limpiar procesos al salir
cleanup() {
    echo -e "\n${YELLOW}🛑 Deteniendo servicios...${NC}"
    # Matar procesos en background
    jobs -p | xargs -r kill
    exit 0
}

# Capturar señales para cleanup
trap cleanup SIGINT SIGTERM

# Verificar que estamos en el directorio correcto
if [ ! -d "backend" ] || [ ! -d "frontend" ]; then
    echo -e "${RED}❌ Error: Debe ejecutar este script desde el directorio raíz del proyecto${NC}"
    exit 1
fi

# Verificar que el entorno virtual existe
if ! pyenv versions | grep -q "harvey"; then
    echo -e "${RED}❌ Error: El entorno virtual 'harvey' no existe${NC}"
    echo -e "${YELLOW}💡 Ejecute: pyenv virtualenv 3.12.11 harvey${NC}"
    exit 1
fi

# Activar entorno virtual
echo -e "${BLUE}🐍 Activando entorno virtual...${NC}"
eval "$(pyenv init -)"
pyenv activate harvey

# Verificar dependencias del backend
echo -e "${BLUE}🔍 Verificando dependencias del backend...${NC}"
cd backend
if [ ! -f "requirements.txt" ]; then
    echo -e "${RED}❌ Error: No se encontró requirements.txt${NC}"
    exit 1
fi

# Instalar dependencias si es necesario
pip install -r requirements.txt > /dev/null 2>&1

# Verificar dependencias del frontend
echo -e "${BLUE}🔍 Verificando dependencias del frontend...${NC}"
cd ../frontend
if [ ! -f "package.json" ]; then
    echo -e "${RED}❌ Error: No se encontró package.json${NC}"
    exit 1
fi

# Instalar dependencias si es necesario
npm install > /dev/null 2>&1

# Volver al directorio raíz
cd ..

echo -e "${GREEN}✅ Dependencias verificadas${NC}"
echo "================================"

# Iniciar backend
echo -e "${BLUE}🚀 Iniciando Backend (FastAPI)...${NC}"
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000 > ../backend.log 2>&1 &
BACKEND_PID=$!
cd ..

# Esperar un poco para que el backend se inicie
sleep 3

# Verificar que el backend se inició correctamente
if kill -0 $BACKEND_PID 2>/dev/null; then
    echo -e "${GREEN}✅ Backend iniciado en http://localhost:8000${NC}"
else
    echo -e "${RED}❌ Error al iniciar el backend${NC}"
    exit 1
fi

# Iniciar frontend
echo -e "${BLUE}🚀 Iniciando Frontend (React + Vite)...${NC}"
cd frontend
npm run dev > ../frontend.log 2>&1 &
FRONTEND_PID=$!
cd ..

# Esperar un poco para que el frontend se inicie
sleep 3

# Verificar que el frontend se inició correctamente
if kill -0 $FRONTEND_PID 2>/dev/null; then
    echo -e "${GREEN}✅ Frontend iniciado en http://localhost:8080${NC}"
else
    echo -e "${RED}❌ Error al iniciar el frontend${NC}"
    exit 1
fi

echo "================================"
echo -e "${GREEN}🎉 Harvey está ejecutándose!${NC}"
echo ""
echo -e "${YELLOW}📋 Servicios disponibles:${NC}"
echo -e "   🔗 Frontend: ${BLUE}http://localhost:8080${NC}"
echo -e "   🔗 Backend:  ${BLUE}http://localhost:8000${NC}"
echo -e "   🔗 API Docs: ${BLUE}http://localhost:8000/docs${NC}"
echo ""
echo -e "${YELLOW}📊 Logs en tiempo real:${NC}"
echo -e "   📄 Backend:  ${BLUE}tail -f backend.log${NC}"
echo -e "   📄 Frontend: ${BLUE}tail -f frontend.log${NC}"
echo ""
echo -e "${YELLOW}⚠️  Para detener los servicios presione Ctrl+C${NC}"
echo "================================"

# Mantener el script ejecutándose y mostrar logs
while true; do
    # Verificar que ambos procesos sigan ejecutándose
    if ! kill -0 $BACKEND_PID 2>/dev/null; then
        echo -e "${RED}❌ Backend se detuvo inesperadamente${NC}"
        break
    fi
    
    if ! kill -0 $FRONTEND_PID 2>/dev/null; then
        echo -e "${RED}❌ Frontend se detuvo inesperadamente${NC}"
        break
    fi
    
    sleep 5
done

# Cleanup al salir
cleanup 