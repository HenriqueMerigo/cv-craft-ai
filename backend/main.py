import io
import os
import zipfile
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, StreamingResponse
from pydantic import BaseModel
from typing import Optional

from ai_service import otimizar_curriculo
from pdf_generator import gerar_pdf

app = FastAPI(title="CV Craft AI - API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class CurriculoSchema(BaseModel):
    nome: str
    cargo_desejado: str
    email: str
    telefone: Optional[str] = ""
    linkedin: Optional[str] = ""
    experiencia_bruta: str
    educacao_bruta: Optional[str] = ""
    habilidades_brutas: Optional[str] = ""
    descricao_vaga: Optional[str] = ""
    gerar_ingles: Optional[bool] = False


# Rotas das Páginas Estáticas
@app.get("/", response_class=FileResponse)
async def serve_frontend():
    frontend_path = os.path.join(os.path.dirname(__file__), "..", "frontend", "index.html")
    if os.path.exists(frontend_path):
        return FileResponse(frontend_path)
    return {"status": "ok", "message": "API CV Craft AI está online!"}


@app.get("/qrcode_pix.jpeg", response_class=FileResponse)
async def serve_qrcode_pix():
    path = os.path.join(os.path.dirname(__file__), "..", "frontend", "qrcode.jpeg")
    if os.path.exists(path):
        return FileResponse(path)
    raise HTTPException(status_code=404, detail="Imagem do QR Code não encontrada.")


@app.get("/privacidade", response_class=FileResponse)
async def serve_privacidade():
    path = os.path.join(os.path.dirname(__file__), "..", "frontend", "privacidade.html")
    return FileResponse(path)


@app.get("/termos", response_class=FileResponse)
async def serve_termos():
    path = os.path.join(os.path.dirname(__file__), "..", "frontend", "termos.html")
    return FileResponse(path)


@app.get("/suporte", response_class=FileResponse)
async def serve_suporte():
    path = os.path.join(os.path.dirname(__file__), "..", "frontend", "suporte.html")
    return FileResponse(path)


@app.post("/api/gerar-curriculo")
async def endpoint_gerar_curriculo(payload: CurriculoSchema):
    try:
        dados_input = payload.model_dump()
        habilidades_lista = [
            h.strip() for h in payload.habilidades_brutas.split(",") if h.strip()
        ]
        dados_input["habilidades_lista"] = habilidades_lista

        nome_slug = payload.nome.lower().replace(" ", "_")

        # 1. Gera versão em Português
        dados_pt = otimizar_curriculo(dados_input, idioma="pt")
        pdf_pt = gerar_pdf(dados_pessoais=dados_input, dados_ia=dados_pt, idioma="pt")

        if not payload.gerar_ingles:
            return StreamingResponse(
                io.BytesIO(pdf_pt),
                media_type="application/pdf",
                headers={"Content-Disposition": f"attachment; filename=curriculo_{nome_slug}_pt.pdf"},
            )

        # 2. Se pediu em inglês, gera versão EN e empacota em ZIP
        dados_en = otimizar_curriculo(dados_input, idioma="en")
        pdf_en = gerar_pdf(dados_pessoais=dados_input, dados_ia=dados_en, idioma="en")

        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
            zip_file.writestr(f"curriculo_{nome_slug}_PT.pdf", pdf_pt)
            zip_file.writestr(f"curriculo_{nome_slug}_EN.pdf", pdf_en)

        zip_buffer.seek(0)

        return StreamingResponse(
            zip_buffer,
            media_type="application/zip",
            headers={"Content-Disposition": f"attachment; filename=curriculos_{nome_slug}.zip"},
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro no processamento: {str(e)}")