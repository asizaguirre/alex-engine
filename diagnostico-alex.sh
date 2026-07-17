#!/bin/bash

echo "======================================"
echo "   DIAGNÓSTICO AlEx ENGINE LOCAL"
echo "======================================"

BASE=$(pwd)

echo
echo "📁 Diretório atual:"
pwd

echo
echo "======================================"
echo "1) Estrutura do projeto"
echo "======================================"

find "$BASE" -maxdepth 3 -type f \
  | grep -E "\.(py|env|yaml|yml|json|md|txt)$" \
  | sort


echo
echo "======================================"
echo "2) Arquivos Python principais"
echo "======================================"

find "$BASE" -name "*.py" -print


echo
echo "======================================"
echo "3) Rotas FastAPI encontradas"
echo "======================================"

grep -R -nE "@app\.(get|post|put|delete|patch)|APIRouter|router\." "$BASE" \
2>/dev/null


echo
echo "======================================"
echo "4) Conteúdo main.py"
echo "======================================"

if [ -f main.py ]; then
    sed -n '1,250p' main.py
else
    echo "main.py não encontrado"
fi


echo
echo "======================================"
echo "5) Processos Python/Uvicorn"
echo "======================================"

ps aux | grep -E "uvicorn|python" | grep -v grep


echo
echo "======================================"
echo "6) Portas utilizadas"
echo "======================================"

sudo lsof -i -P -n | grep LISTEN | grep -E "9002|11434|6333|5432|6379|3000"


echo
echo "======================================"
echo "7) Teste Engine"
echo "======================================"

echo "/health"
curl -s http://localhost:9002/health
echo


echo
echo "/docs"
curl -I -s http://localhost:9002/docs | head -5


echo
echo "======================================"
echo "8) Rotas OpenAPI"
echo "======================================"

curl -s http://localhost:9002/openapi.json \
| python3 -m json.tool 2>/dev/null \
| grep -E '\"/|post|put|get'


echo
echo "======================================"
echo "9) Ollama"
echo "======================================"

curl -s http://localhost:11434/api/tags


echo
echo
echo "======================================"
echo "10) Docker"
echo "======================================"

docker ps


echo
echo "======================================"
echo "11) Variáveis AlEx (sem segredos)"
echo "======================================"

env | grep -E "ALEX|OLLAMA|QDRANT|REDIS|POSTGRES" \
| sed -E 's/(KEY|TOKEN|PASSWORD|SECRET)=.*/\1=***OCULTO***/'


echo
echo "======================================"
echo "FIM DO DIAGNÓSTICO"
echo "======================================"
