import os
import json
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key) if api_key else None


def otimizar_curriculo(dados: dict, idioma: str = "pt") -> dict:
    if not client:
        raise ValueError("GEMINI_API_KEY não foi configurada no arquivo .env")

    instrucao_idioma = (
        "Gere o conteúdo totalmente em PORTUGUÊS DO BRASIL."
        if idioma == "pt"
        else "Generate the content ENTIRELY IN ENGLISH, using natural professional corporate phrasing and ATS action verbs."
    )

    prompt = f"""
    Você é um recrutador sênior e especialista em otimização de currículos para sistemas ATS.
    {instrucao_idioma}

    Sua tarefa é analisar os dados informados pelo candidato e reescrevê-los para torná-los altamente atrativos e profissionais.

    REGRAS DE OTIMIZAÇÃO:
    1. Resumo Profissional: Crie um parágrafo conciso (3 a 4 linhas) destacando perfil, competências e conquistas.
    2. Experiências Profissionais: Transforme em bullet points focados em impacto, usando verbos de ação fortes.
    3. Palavras-chave ATS: Se a 'descricao_vaga' for fornecida, incorpore termos estratégicos dela de forma natural.
    4. Mantenha a fidelidade aos fatos fornecidos.

    DADOS BRUTOS DO CANDIDATO:
    {json.dumps(dados, ensure_ascii=False, indent=2)}

    Retorne estritamente um JSON com a estrutura:
    {{
      "resumo_profissional": "string",
      "experiencias": [
        {{
          "cargo": "string",
          "empresa": "string",
          "periodo": "string",
          "bullet_points": ["string"]
        }}
      ],
      "formacao": "string",
      "habilidades": ["string"]
    }}
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            temperature=0.3,
        ),
    )

    return json.loads(response.text)