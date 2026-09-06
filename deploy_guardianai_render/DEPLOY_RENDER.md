# 🚀 Guia de Deploy 24/7 da Guardian AI no Render.com

Este guia orienta o deploy gratuito da API FastAPI da **Guardian AI** no **Render.com** com URL pública HTTPS permanente para integração com o aplicativo Mobile.

---

## 📋 Pré-requisitos
1. Conta no [Render.com](https://render.com) (login gratuito com GitHub).
2. Chave de API do Google Gemini (`GEMINI_API_KEY`) obtida no [Google AI Studio](https://aistudio.google.com/).

---

## 🛠️ Passo a Passo de Publicação (2 Minutos)

### 1. Criar Novo Web Service no Render
1. Acesse o painel do Render e clique em **New +** ➔ **Web Service**.
2. Selecione a opção **"Build and deploy from a Git repository"**.
3. Conecte o repositório da disciplina: `Challenge-Pet-Guardian-3/Disruptive-Architectures-IoT-IoB-IA` (ou o repositório onde o código estiver hospedado).

### 2. Configurar os Parâmetros do Serviço
Preencha os campos com as seguintes configurações:

| Campo | Valor a Preencher |
| :--- | :--- |
| **Name** | `petguardian-ai` *(ou o nome de sua preferência)* |
| **Region** | `Oregon (US West)` *(ou Ohio / Frankfurt)* |
| **Branch** | `main` |
| **Root Directory** | `deploy_guardianai_render` |
| **Runtime** | `Python 3` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `uvicorn api:app --host 0.0.0.0 --port $PORT` |
| **Instance Type** | `Free` ($0/mês) |

### 3. Configurar Variáveis de Ambiente (Environment Variables)
Na seção **Environment Variables**, adicione:
- **Key:** `GEMINI_API_KEY`
- **Value:** `sua_chave_do_gemini_aqui`
- **Key:** `PYTHON_VERSION`
- **Value:** `3.11.8`

### 4. Concluir Deploy
1. Clique no botão **Create Web Service**.
2. O Render iniciará o build automaticamente e exibirá os logs em tempo real.
3. Ao finalizar, o status mudará para **Live** e sua URL pública HTTPS será gerada:
   `https://petguardian-ai.onrender.com`

---

## 🧪 Testando a API no Ar

### 1. Health Check
Abra no navegador: `https://petguardian-ai.onrender.com/`
Retorno esperado:
```json
{
  "status": "online",
  "service": "PetGuardian AI Microservice",
  "model": "gemini-2.5-flash",
  "framework": "FastAPI + Google GenAI SDK",
  "version": "1.0.0"
}
```

### 2. Documentação Interativa Swagger UI
Acesse: `https://petguardian-ai.onrender.com/docs`

---

## 📱 Vinculação com o Aplicativo Mobile
Basta colar a URL gerada no arquivo [`Mobile-Application-Development/src/config/env.ts`](file:///c:/Users/Enzo/new_backup/FIAP/_Projetos/Challenge%20Clyvo%203/Mobile-Application-Development/src/config/env.ts):

```typescript
export const env = {
  apiUrl: `http://${host}:8091`,
  aiUrl: 'https://petguardian-ai.onrender.com', // URL pública do Render
};
```
