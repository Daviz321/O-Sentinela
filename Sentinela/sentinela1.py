import customtkinter as ctk
import re
import random
import string
import unicodedata

def remover_acentos(txt):
    return ''.join(c for c in unicodedata.normalize('NFD', txt)
                   if unicodedata.category(c) != 'Mn')

# =========================
# TEMA
# =========================
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

# =========================
# FONTES
# =========================
TITLE_FONT = ("Arial", 38, "bold")
FONT = ("Arial", 22)
BIG_FONT = ("Arial", 26, "bold")

# =========================
# FONTES CONFIÁVEIS
# =========================
FONTES_CONFIAVEIS = [
    "google.com",
    "microsoft.com",
    "gov.br",
    "wikipedia.org",
    "bbc.com",
    "nytimes.com",
    "minecraft.wiki",
    "g1.globo.com",
    "youtube.com",
    "openai.com",
    "chatgpt.com",
    "blackbox.ai",
    "app.portalsaseducacao.com.br",

    "github.com",
    "cloudflare.com",
    "amazon.com",
    "aws.amazon.com",
    "apple.com",
    "meta.com",
    "instagram.com",
    "facebook.com",
    "linkedin.com",
    "mozilla.org",
    "who.int",
    "unesco.org",
    "unicef.org",
    "nasa.gov",
    "mit.edu",
    "harvard.edu"
]

SITES_MAXIMA_CONFIANCA = [

    "google.com",
    "microsoft.com",
    "github.com",
    "cloudflare.com",
    "openai.com",
    "chatgpt.com",
    "apple.com",
    "amazon.com",
    "youtube.com",

    "wikipedia.org",

    "gov.br",
    "nasa.gov",
    "who.int",

    "unicef.org",
    "unesco.org",
    "un.org",

    "mit.edu",
    "harvard.edu",
    "stanford.edu"

]

# =========================
# PALAVRAS CONFIÁVEIS
# =========================
PALAVRAS_CONFIAVEIS = [
    "estudo","pesquisa","dados","universidade",
    "científico","relatório","publicado","estatística",
    "análise","fonte"
]

# =========================
# BARRA
# =========================
def montar_saida(percent, justificativa, status, tipo):

    blocos = int(percent / 5)

    barra = "█" * blocos + "░" * (20 - blocos)

    texto_just = "\n".join(f"• {j}" for j in justificativa)

    return barra, texto_just


# =========================
# SITE
# =========================
def analisar_site(texto):

    t = texto.lower().strip()

    justificativa = []
    fontes = []

    percent = 0

    # =========================
    # HTTPS
    # =========================
    if t.startswith("https://"):
        percent += 40
        justificativa.append("✔ HTTPS detectado")
    else:
        justificativa.append("✘ Sem HTTPS")

    # =========================
    # CONFIANÇA MÁXIMA
    # =========================
    for site in SITES_MAXIMA_CONFIANCA:

        if site in t:

            percent += 60

            justificativa.append(
            "✔ Fonte altamente reconhecida"
            )

            break

    # =========================
    # DOMÍNIOS CONFIÁVEIS
    # =========================
    for site in FONTES_CONFIAVEIS:

        if site in t:

            percent += 50
            fontes.append(site)

            justificativa.append(
                f"✔ Fonte conhecida"
            )

            break

    # =========================
    # DOMÍNIO GOVERNAMENTAL
    # =========================
    if ".gov" in t:

        percent += 25

        justificativa.append(
            "✔ Domínio governamental"
        )

    # =========================
    # DOMÍNIO EDUCACIONAL
    # =========================
    if ".edu" in t:

        percent += 20

        justificativa.append(
            "✔ Domínio educacional"
        )

    # =========================
    # URL CURTA E LIMPA
    # =========================
    if len(t) < 60:

        percent += 5

        justificativa.append(
            "✔ URL simples"
        )

    # =========================
    # MUITOS SÍMBOLOS
    # =========================
    simbolos = t.count("-") + t.count("_")

    if simbolos >= 5:

        percent -= 15

        justificativa.append(
            "✘ URL suspeita"
        )

    # =========================
    # MUITOS NÚMEROS
    # =========================
    numeros = sum(c.isdigit() for c in t)

    if numeros >= 8:

        percent -= 15

        justificativa.append(
            "✘ Muitos números"
        )

    # =========================
    # IP AO INVÉS DE DOMÍNIO
    # =========================
    if re.search(
        r"https?://\d+\.\d+\.\d+\.\d+",
        t
    ):

        percent -= 30

        justificativa.append(
            "✘ Uso de IP"
        )

    suspeitos = [
        "gratis",
        "premio",
        "pix",
        "ganhe",
        "dinheiro",
        "bonus",
        "presente"
    ]

    for palavra in suspeitos:

        if palavra in t:

            percent -= 10

            justificativa.append(
            "✘ Termo suspeito"
            )

            break

    # =========================
    # LIMITES
    # =========================
    percent = max(0, min(100, percent))

    # =========================
    # STATUS
    # =========================
    if percent >= 70:

        status = "SITE CONFIÁVEL!"
        cor = "green"

    elif percent >= 30:

        status = "SITE RAZOÁVEL!"
        cor = "yellow"

    else:

        status = "SITE SUSPEITO!"
        cor = "red"

    justificativa.insert(
        0,
        f"Segurança do Site: {percent}%"
    )

    return (
        status,
        montar_saida(
            percent,
            justificativa,
            status,
            "site"
        ),
        fontes,
        cor
    )

# =========================
# BASE DE CONHECIMENTO
# =========================
_BASE_CACHE = None

def obter_base_conhecimento():

    global _BASE_CACHE

    # ==========================================
    # CACHE
    # ==========================================
    if _BASE_CACHE is not None:
        return _BASE_CACHE

    import unicodedata
    import re

    # ==========================================
    # NORMALIZAÇÃO
    # ==========================================
    def norm(s):

        s = str(s).lower().strip()

        s = ''.join(
            c for c in unicodedata.normalize('NFD', s)
            if unicodedata.category(c) != 'Mn'
        )

        s = re.sub(r"\s+", " ", s)

        return s.strip()

    # ==========================================
    # ESTRUTURA
    # ==========================================
    fatos = {}

    # ==========================================
    # REGISTRADOR
    # ==========================================
    def registrar(
        frase,
        valor=True,
        categoria="geral",
        peso=10,
        aliases=None,
        prioridade=1,
        tags=None
    ):

        frase = norm(frase)

        # ==========================================
        # EVITAR DUPLICATAS
        # ==========================================
        if frase in fatos:
            return

        fatos[frase] = {

            "valor": valor,
            "categoria": categoria,
            "peso": peso,
            "prioridade": prioridade,
            "tags": tags or [],
            "frase_original": frase

        }

        # ==========================================
        # ALIASES
        # ==========================================
        if aliases:

            for a in aliases:

                a = norm(a)

                if a in fatos:
                    continue

                fatos[a] = {

                    "valor": valor,
                    "categoria": categoria,
                    "peso": max(1, peso - 1),
                    "prioridade": prioridade,
                    "tags": tags or [],
                    "frase_original": frase

                }

    # ==========================================
    # FATOS ABSOLUTOS
    # ==========================================
    registrar(
        "A terra é redonda",
        True,
        "ciencia",
        35,
        [
            "o planeta terra é redondo",
            "terra é esférica",
            "a terra possui formato esférico",
            "o planeta é redondo"
        ],
        prioridade=3,
        tags=["terra", "geografia", "ciencia"]
    )

    registrar(
        "O sol é uma estrela",
        True,
        "astronomia",
        30,
        [
            "sol é estrela"
        ],
        prioridade=3,
        tags=["sol", "astronomia"]
    )

    registrar(
        "A gravidade existe",
        True,
        "fisica",
        35,
        [
            "gravidade é real"
        ],
        prioridade=3,
        tags=["gravidade", "fisica"]
    )

    registrar(
        "Vacinas salvam vidas",
        True,
        "medicina",
        40,
        [
            "vacinas funcionam",
            "vacinas ajudam",
            "vacinas ajudam pessoas"
        ],
        prioridade=3,
        tags=["vacina", "medicina"]
    )

    registrar(
        "Python é uma linguagem de programação",
        True,
        "tecnologia",
        20,
        [
            "python é linguagem",
            "python é linguagem de programacao"
        ],
        prioridade=2,
        tags=["python", "programacao"]
    )

    registrar(
        "A internet existe",
        True,
        "tecnologia",
        20,
        [
            "internet é real",
            "a web existe"
        ],
        prioridade=2,
        tags=["internet", "web"]
    )

    registrar(
        "Humanos possuem DNA",
        True,
        "biologia",
        25,
        [
            "humanos tem dna",
            "seres humanos possuem dna"
        ],
        prioridade=2,
        tags=["dna", "biologia"]
    )

    registrar(
        "A água é composta por hidrogênio e oxigênio",
        True,
        "quimica",
        25,
        [
            "agua é h2o",
            "h2o é água"
        ],
        prioridade=2,
        tags=["agua", "quimica"]
    )

    registrar(
        "O Brasil é um país da América do Sul",
        True,
        "geografia",
        20,
        [
            "brasil fica na america do sul"
        ],
        prioridade=2,
        tags=["brasil", "geografia"]
    )

    registrar(
        "A terra gira em torno do sol",
        True,
        "astronomia",
        30,
        [
            "a terra orbita o sol",
            "terra gira ao redor do sol"
        ],
        prioridade=3,
        tags=["terra", "sol", "astronomia"]
    )

    registrar(
        "Plantas fazem fotossíntese",
        True,
        "biologia",
        20,
        [
            "plantas produzem oxigenio",
            "plantas geram oxigenio"
        ],
        prioridade=2,
        tags=["plantas", "fotossintese"]
    )

    registrar(
        "O coração bombeia sangue",
        True,
        "medicina",
        25,
        prioridade=2,
        tags=["coracao", "medicina"]
    )

    registrar(
        "Humanos precisam de água para sobreviver",
        True,
        "biologia",
        25,
        prioridade=3,
        tags=["agua", "biologia"]
    )

    registrar(
        "O universo existe",
        True,
        "astronomia",
        25,
        prioridade=2,
        tags=["universo"]
    )

    registrar(
        "Átomos existem",
        True,
        "quimica",
        20,
        prioridade=2,
        tags=["atomos"]
    )

    registrar(
        "Elétrons existem",
        True,
        "fisica",
        20,
        prioridade=2,
        tags=["eletrons"]
    )

    registrar(
        "Vírus existem",
        True,
        "biologia",
        20,
        prioridade=2,
        tags=["virus"]
    )

    registrar(
        "Bactérias existem",
        True,
        "biologia",
        20,
        prioridade=2,
        tags=["bacterias"]
    )

    registrar(
        "Inteligência artificial existe",
        True,
        "tecnologia",
        20,
        [
            "ia existe",
            "ai existe"
        ],
        prioridade=2,
        tags=["ia", "ai"]
    )

    registrar(
        "O homo sapiens é humano",
        True,
        "biologia",
        30,
        [
            "homo sapiens é humano",
            "humanos são homo sapiens",
            "o ser humano é homo sapiens",
            "homo sapiens pertence à espécie humana"
        ],
        prioridade=3,
        tags=["homo sapiens", "humanos"]
    )

    # ==========================================
    # FATOS FALSOS
    # ==========================================
    registrar(
        "A terra é plana",
        False,
        "fake",
        45,
        [
            "terra plana existe"
        ],
        prioridade=3,
        tags=["terra plana"]
    )

    registrar(
        "Gravidade não existe",
        False,
        "fake",
        45,
        prioridade=3,
        tags=["gravidade"]
    )

    registrar(
        "Vacinas causam autismo",
        False,
        "fake",
        50,
        [
            "vacina causa autismo"
        ],
        prioridade=3,
        tags=["vacina", "autismo"]
    )

    registrar(
        "Pix infinito existe",
        False,
        "fake",
        50,
        [
            "pix ilimitado",
            "gerador de pix"
        ],
        prioridade=3,
        tags=["pix", "golpe"]
    )

    registrar(
        "Dinheiro infinito existe",
        False,
        "fake",
        50,
        prioridade=3,
        tags=["dinheiro", "golpe"]
    )

    registrar(
        "5G controla mentes",
        False,
        "fake",
        45,
        prioridade=3,
        tags=["5g", "conspiracao"]
    )

    registrar(
        "Covid não existiu",
        False,
        "fake",
        45,
        [
            "covid foi mentira"
        ],
        prioridade=3,
        tags=["covid"]
    )

    registrar(
        "O sol gira em torno da terra",
        False,
        "fake",
        45,
        prioridade=3,
        tags=["sol", "terra"]
    )

    registrar(
        "A lua é holograma",
        False,
        "fake",
        40,
        prioridade=2,
        tags=["lua"]
    )

    registrar(
        "Dinossauros nunca existiram",
        False,
        "fake",
        40,
        prioridade=2,
        tags=["dinossauros"]
    )

    registrar(
        "A terra não gira",
        False,
        "fake",
        40,
        prioridade=2,
        tags=["terra"]
    )

    registrar(
        "Água não existe",
        False,
        "fake",
        45,
        prioridade=2,
        tags=["agua"]
    )

    registrar(
        "O oxigênio não existe",
        False,
        "fake",
        45,
        prioridade=2,
        tags=["oxigenio"]
    )

    registrar(
        "Humanos não precisam dormir",
        False,
        "fake",
        35,
        prioridade=2,
        tags=["humanos", "sono"]
    )

    # ==========================================
    # GEOGRAFIA
    # ==========================================
    paises = {

        "Brasil": "Brasília",
        "França": "Paris",
        "Japão": "Tokyo",
        "Alemanha": "Berlim",
        "Portugal": "Lisboa",
        "Argentina": "Buenos Aires",
        "Estados Unidos": "Washington",
        "Reino Unido": "Londres",
        "Canadá": "Ottawa",
        "Itália": "Roma"

    }

    for pais, capital in paises.items():

        registrar(
            f"{capital} é a capital de {pais}",
            True,
            "geografia",
            15,
            [
                f"{capital} fica em {pais}"
            ],
            prioridade=2,
            tags=["capital", pais.lower()]
        )

        registrar(
            f"{pais} é um país",
            True,
            "geografia",
            10,
            prioridade=1,
            tags=["pais"]
        )

    # ==========================================
    # MATEMÁTICA
    # ==========================================
    matematica = [

        "2 + 2 = 4",
        "1 + 1 = 2",
        "5 x 5 = 25",
        "10 / 2 = 5",
        "Raiz quadrada de 9 é 3",
        "Pi é aproximadamente 3.14"

    ]

    for m in matematica:

        registrar(
            m,
            True,
            "matematica",
            20,
            prioridade=3,
            tags=["matematica"]
        )

    # ==========================================
    # FÍSICA
    # ==========================================
    fisica = [

        "Energia pode ser transformada",
        "Objetos possuem massa",
        "Eletricidade existe",
        "Magnetismo existe",
        "A luz possui velocidade",
        "Som é uma onda"

    ]

    for f in fisica:

        registrar(
            f,
            True,
            "fisica",
            15,
            prioridade=2,
            tags=["fisica"]
        )

    # ==========================================
    # MEDICINA
    # ==========================================
    medicina = [

        "Hospitais existem",
        "Doenças existem",
        "Febre pode indicar doença",
        "Lavar as mãos ajuda na higiene",
        "Sono é importante para a saúde",
        "Exercícios ajudam na saúde"

    ]

    for m in medicina:

        registrar(
            m,
            True,
            "medicina",
            15,
            prioridade=2,
            tags=["medicina"]
        )

    # ==========================================
    # TECNOLOGIA
    # ==========================================
    tecnologia = [

        "Computadores processam dados",
        "Golpes digitais existem",
        "Spam existe",
        "Wi-fi existe",
        "Sites existem",
        "Programação existe"

    ]

    for t in tecnologia:

        registrar(
            t,
            True,
            "tecnologia",
            15,
            prioridade=2,
            tags=["tecnologia"]
        )

    # ==========================================
    # ASTRONOMIA
    # ==========================================
    astronomia = [

        "Galáxias existem",
        "Buracos negros existem",
        "Exoplanetas existem",
        "A NASA existe",
        "Estrelas produzem energia",
        "A luz viaja pelo espaço"

    ]

    for a in astronomia:

        registrar(
            a,
            True,
            "astronomia",
            18,
            prioridade=2,
            tags=["astronomia"]
        )

    # ==========================================
    # ALIASES GLOBAIS
    # ==========================================
    aliases_globais = {

        "eua": "estados unidos",
        "usa": "estados unidos",
        "br": "brasil",
        "ia": "inteligencia artificial",
        "ai": "inteligencia artificial",
        "web": "internet",
        "pc": "computador",
        "covid": "covid-19",
        "jwst": "telescopio james webb",
        "webb": "telescopio james webb",
        "hubble": "telescopio hubble",
        "nasa": "nasa",
        "celular": "smartphone",
        "telefone": "smartphone",
        "net": "internet"

    }

    # ==========================================
    # GERAR ALIASES AUTOMÁTICOS
    # ==========================================
    novos = {}

    for frase, info in fatos.items():

        for alias, original in aliases_globais.items():

            original = norm(original)
            alias = norm(alias)

            if original in frase:

                nova = frase.replace(original, alias)

                if nova not in fatos:

                    novos[nova] = info.copy()

    fatos.update(novos)

    # ==========================================
    # EXPANSÃO AUTOMÁTICA
    # ==========================================
    extras = {}

    for frase, info in fatos.items():

        variantes = set()

        variantes.add(frase.replace(" é ", " e "))
        variantes.add(frase.replace(" existem", " existe"))
        variantes.add(frase.replace(" existe", " existem"))

        for v in variantes:

            v = norm(v)

            if v and v not in fatos:

                extras[v] = info.copy()

    fatos.update(extras)

    # ==========================================
    # CACHE FINAL
    # ==========================================
    _BASE_CACHE = fatos

    return _BASE_CACHE

def analisar_informacao(texto):

    import unicodedata
    import re

    from collections import Counter
    from difflib import SequenceMatcher

    # ==========================================
    # NORMALIZAÇÃO
    # ==========================================
    def norm(s):

        s = str(s).lower().strip()

        s = ''.join(
            c for c in unicodedata.normalize('NFD', s)
            if unicodedata.category(c) != 'Mn'
        )

        return " ".join(s.split())

    t = norm(texto)

    # ==========================================
    # BUSCA INTELIGENTE DE FATOS
    # ==========================================
    def buscar_fato(frase, conhecimento):

        frase = norm(frase)

        melhor_info = None
        melhor_score = 0

        for frase_base, info in conhecimento.items():

            frase_base = norm(frase_base)

            # ==========================================
            # MATCH EXATO
            # ==========================================
            if frase == frase_base:

                return info

            # ==========================================
            # MATCH CONTIDO
            # ==========================================
            if (
                len(frase.split()) >= 3
                and frase_base in frase
            ):

                score = 0.98

            else:

                similaridade = SequenceMatcher(
                    None,
                    frase,
                    frase_base
                ).ratio()

                # ==========================================
                # LIMITE DINÂMICO
                # ==========================================
                limite = (

                    0.97
                    if len(frase_base.split()) <= 3

                    else 0.93
                    if len(frase_base.split()) <= 6

                    else 0.88
                )

                if similaridade < limite:
                    continue

                score = similaridade

            # ==========================================
            # MELHOR MATCH
            # ==========================================
            if score > melhor_score:

                melhor_score = score
                melhor_info = info

        return melhor_info

    # ==========================================
    # ESTRUTURAS
    # ==========================================
    justificativa = []
    fontes = []

    usadas = set()

    bonus = 0
    penal = 0
    sens_score = 0

    penal_clickbait = 0
    penal_fake = 0

    percent = 50

    frases_confiaveis = 0
    frases_suspeitas = 0
    frases_clickbait = 0

    simbolos_exagerados = 0

    teve_fatos_verdadeiros = False
    teve_fatos_falsos = False
    teve_contradicao = False

    # ==========================================
    # REMOVER NEGAÇÕES
    # ==========================================
    def remover_negacoes(frase):

        negacoes = [

            "nao",
            "nunca",
            "jamais"

        ]

        palavras = frase.split()

        return [
            p for p in palavras
            if p not in negacoes
        ]

    # ==========================================
    # CONTEXTOS
    # ==========================================
    contexto_educacional = [

        "trabalho",
        "pesquisa",
        "escola",
        "universidade",
        "faculdade",
        "artigo",
        "cientifico",
        "documentario",
        "checagem",
        "verificacao",
        "estudo",
        "analise",
        "dados",
        "estatistica",
        "evidencia",
        "paper",
        "revisao cientifica",
        "relatorio"

    ]

    contexto_neutro = [

        "filme",
        "serie",
        "anime",
        "manga",
        "jogo",
        "ficcao",
        "historia ficticia"

    ]

    contexto_humor = [

        "meme",
        "piada",
        "zoeira",
        "humor",
        "satira"

    ]

    negadores = [

        "isso e falso",
        "isso foi desmentido",
        "isso e mentira",
        "isso nao e verdade",
        "fake news",
        "boato",
        "desmentido",
        "golpe",
        "enganoso"

    ]

    contexto_pergunta = (

        "?" in texto
        or t.startswith("como")
        or t.startswith("por que")
        or t.startswith("o que")
        or t.startswith("sera")
        or t.startswith("verdade")
        or t.startswith("isso e")

    )

    eh_educacional = any(c in t for c in contexto_educacional)
    eh_neutro = any(c in t for c in contexto_neutro)
    eh_humor = any(c in t for c in contexto_humor)

    tem_negacao = any(n in t for n in negadores)

    # ==========================================
    # BASE DE CONHECIMENTO
    # ==========================================
    conhecimento = obter_base_conhecimento()

    fatos_verdadeiros = set()
    fatos_falsos = set()

    # ==========================================
    # FRASES
    # ==========================================
    frases_texto = re.split(r"[.!?\n]+", t)

    frases_texto = [
        f.strip()
        for f in frases_texto
        if len(f.strip()) >= 2
    ]

    total_frases = max(1, len(frases_texto))

    frase_unica = " ".join(frases_texto).strip()

    texto_curto = (

        len(frases_texto) <= 2
        and len(t.split()) <= 12

    )

    # ==========================================
    # TEXTO CURTO = VERDADE ABSOLUTA
    # ==========================================
    if texto_curto:

        info = buscar_fato(frase_unica, conhecimento)

        if info is not None:

            if info["valor"]:

                percent = 100
                status = "MUITO CONFIÁVEL"
                cor = "green"

                justificativa.append(
                    "✔ Fato conhecido e confirmado"
                )

            else:

                percent = 0
                status = "FALSO"
                cor = "red"

                justificativa.append(
                    "✘ Fato conhecido como falso"
                )

        else:

            percent = 50
            status = "DUVIDOSO"
            cor = "yellow"

            justificativa.append(
                "? Informação desconhecida"
            )

        justificativa.insert(
            0,
            f"Confiabilidade: {percent}%"
        )

        return (

            status,

            montar_saida(
                percent,
                justificativa,
                status,
                "info"
            ),

            fontes,

            cor

        )

    # ==========================================
    # DETECÇÃO DE FATOS
    # ==========================================
    for frase_usuario in frases_texto:

        info = buscar_fato(frase_usuario, conhecimento)

        if info is None:
            continue

        valor = info.get("valor", True)
        peso = info.get("peso", 10)

        if valor:

            fatos_verdadeiros.add(frase_usuario)

            teve_fatos_verdadeiros = True

            bonus += min(peso, 20)

        else:

            fatos_falsos.add(frase_usuario)

            teve_fatos_falsos = True

            if not tem_negacao:

                penal_fake += min(peso, 45)

    # ==========================================
    # CONTRADIÇÕES
    # ==========================================
    contradicoes = [

        ("a terra e redonda", "a terra e plana"),
        ("gravidade existe", "gravidade nao existe"),
        ("virus existem", "virus nao existem"),
        ("internet existe", "internet nao existe"),
        ("vacinas salvam vidas", "vacinas causam autismo")

    ]

    for a, b in contradicoes:

        if norm(a) in t and norm(b) in t:

            penal += 60

            teve_contradicao = True

    # ==========================================
    # TERMOS CONFIÁVEIS
    # ==========================================
    confiavel = {

        "ciencia": 8,
        "cientifico": 10,
        "pesquisa": 8,
        "estudo": 8,
        "dados": 6,
        "estatistica": 10,
        "evidencia": 10,
        "analise": 8,
        "comprovado": 12,
        "universidade": 15,
        "instituto": 12,
        "pesquisadores": 10,
        "especialistas": 8,
        "cientistas": 10

    }

    # ==========================================
    # CLICKBAIT
    # ==========================================
    clickbait = {

        "urgente": 12,
        "chocante": 12,
        "inacreditavel": 15,
        "segredo": 14,
        "revelado": 12,
        "ultima chance": 16,
        "clique aqui": 20,
        "clique ja": 25

    }

    # ==========================================
    # TERMOS FAKE
    # ==========================================
    fake = {

        "nao querem que voce saiba": 30,
        "a verdade escondida": 30,
        "midia mente": 22,
        "governo esconde": 22,
        "conspiracao": 18,
        "pix infinito": 50,
        "vacinas causam autismo": 60

    }

    # ==========================================
    # CONTEÚDO SENSÍVEL
    # ==========================================
    sensivel = {

        "sexo": 2,
        "pornografia": 4,
        "gore": 5,
        "morte": 3,
        "violencia": 4

    }

    # ==========================================
    # REPETIÇÃO / SPAM
    # ==========================================
    palavras = re.findall(r"\w+", t)

    contagem = Counter(palavras)

    total_palavras = max(1, len(palavras))

    for palavra, qtd in contagem.items():

        limite_spam = max(
            4,
            int(total_palavras * 0.08)
        )

        if (

            qtd >= limite_spam
            and len(palavra) > 3
            and palavra not in contexto_educacional

        ):

            penal += min(15, qtd)

            frases_suspeitas += 1

    # ==========================================
    # EXCLAMAÇÕES
    # ==========================================
    excl = texto.count("!")

    if excl >= 3:

        valor = min(25, excl * 3)

        penal += valor

        simbolos_exagerados += excl

    # ==========================================
    # CAPS LOCK
    # ==========================================
    caps_words = [

        p for p in texto.split()
        if len(p) >= 4 and p.isupper()

    ]

    if len(caps_words) >= 3:

        penal += 20

        simbolos_exagerados += len(caps_words)

    # ==========================================
    # EMOJIS
    # ==========================================
    emojis = re.findall(r"[😂🤣🔥💰🚨⚠😱]", texto)

    if len(emojis) >= 3:

        penal += min(20, len(emojis) * 3)

        simbolos_exagerados += len(emojis)

    # ==========================================
    # TERMOS CONFIÁVEIS
    # ==========================================
    for p, peso in confiavel.items():

        if p in t and p not in usadas:

            bonus += peso

            frases_confiaveis += 1

            usadas.add(p)

    # ==========================================
    # CLICKBAIT
    # ==========================================
    for p, peso in clickbait.items():

        if p in t and p not in usadas:

            penal_clickbait += peso

            frases_clickbait += 1

            usadas.add(p)

    # ==========================================
    # TERMOS FAKE
    # ==========================================
    for p, peso in fake.items():

        if p in t and p not in usadas:

            penal_fake += peso

            frases_suspeitas += 1

            usadas.add(p)

    # ==========================================
    # LIMITES
    # ==========================================
    penal += min(45, penal_clickbait)
    penal += min(70, penal_fake)

    bonus = min(100, bonus)
    penal = min(100, penal)

    # ==========================================
    # DENSIDADE FACTUAL
    # ==========================================
    densidade = len(fatos_verdadeiros) / total_frases

    if densidade >= 0.8:

        bonus += 18

    elif densidade >= 0.5:

        bonus += 12

    elif densidade >= 0.3:

        bonus += 6

    # ==========================================
    # SCORE FINAL
    # ==========================================
    if fatos_verdadeiros and not fatos_falsos:

        percent = 65 + bonus - penal

    elif fatos_falsos:

        percent = 40 + bonus - penal

    else:

        percent = 50 + bonus - penal

    # ==========================================
    # AJUSTES
    # ==========================================
    if eh_educacional and percent < 75:

        percent += 10

    if eh_neutro and penal > 20:

        percent += 8

    # ==========================================
    # LIMITES FINAIS
    # ==========================================
    percent = max(
        0,
        min(100, round(percent))
    )

    # ==========================================
    # STATUS
    # ==========================================
    if percent >= 90:

        status = "MUITO CONFIÁVEL"
        cor = "green"

    elif percent >= 70:

        status = "CONFIÁVEL"
        cor = "lightgreen"

    elif percent >= 50:

        status = "DUVIDOSO"
        cor = "yellow"

    elif percent >= 30:

        status = "SUSPEITO"
        cor = "orange"

    else:

        status = "FALSO"
        cor = "red"

    # ==========================================
    # SENSIBILIDADE
    # ==========================================
    if sens_score >= 8:

        nivel_sensibilidade = "MUITO SENSÍVEL"

    elif sens_score >= 4:

        nivel_sensibilidade = "SENSÍVEL"

    else:

        nivel_sensibilidade = "INSENSÍVEL"

    # ==========================================
    # JUSTIFICATIVA
    # ==========================================
    justificativa.append(
        f"Confiabilidade: {percent}%"
    )

    justificativa.append(
        f"Sensibilidade: {nivel_sensibilidade}"
    )

    justificativa.append(
        f"Palavras Confiáveis: {frases_confiaveis}"
    )

    justificativa.append(
        f"Palavras Suspeitas: {frases_suspeitas}"
    )

    justificativa.append(
        f"Palavras de Clickbait: {frases_clickbait}"
    )

    justificativa.append(
        f"Símbolos Exagerados: {simbolos_exagerados}"
    )

    justificativa.append(
        f"{'✔' if teve_fatos_verdadeiros else '✘'} Conhecimento Confirmado"
    )

    # ==========================================
    # RETORNO
    # ==========================================
    return (

        status,

        montar_saida(
            percent,
            justificativa,
            status,
            "info"
        ),

        fontes,

        cor

    )

def analisar_senha(senha):
    import re

    s = senha

    # =========================
    # DETECÇÃO
    # =========================
    tem_maiuscula = bool(re.search(r"[A-Z]", s))
    tem_minuscula = bool(re.search(r"[a-z]", s))
    tem_numero = bool(re.search(r"[0-9]", s))
    tem_simbolo = bool(re.search(r"[!@#$%^&*()_+=\-]", s))
    tamanho_ok = len(s) >= 8

    justificativa = []
    percent = 0

    # =========================
    # MINÚSCULA (10%)
    # =========================
    if tem_minuscula:
        justificativa.append("✔ Letra minúscula")
        percent += 10
    else:
        justificativa.append("✘ Letra minúscula")

    # =========================
    # MAIÚSCULA (30%)
    # =========================
    if tem_maiuscula:
        justificativa.append("✔ Letra maiúscula")
        percent += 30
    else:
        justificativa.append("✘ Letra maiúscula")

    # =========================
    # NÚMERO (20%)
    # =========================
    if tem_numero:
        justificativa.append("✔ Número")
        percent += 20
    else:
        justificativa.append("✘ Número")

    # =========================
    # 8+ CARACTERES (10%)
    # =========================
    if tamanho_ok:
        justificativa.append("✔ 8+ caracteres")
        percent += 10
    else:
        justificativa.append("✘ 8+ caracteres")

    # =========================
    # CARACTERES ESPECIAIS (30%)
    # =========================
    if tem_simbolo:
        justificativa.append("✔ Caracteres especiais")
        percent += 30
    else:
        justificativa.append("✘ Caracteres especiais")

    # =========================
    # ALEATORIEDADE (apenas validação)
    # =========================
    previsivel = (
        s.isdigit()
        or s.isalpha()
        or re.search(r"(123|abc|aaa|111|qwerty|senha|admin)", s.lower())
    )

    if tem_maiuscula and tem_minuscula and tem_numero and tem_simbolo and tamanho_ok and not previsivel:
        justificativa.append("✔ Aleatória")
    else:
        justificativa.append("✘ Aleatória")

    # =========================
    # GRÁFICO FINAL
    # =========================
    percent = min(percent, 100)

    # =========================
    # CLASSIFICAÇÃO (INDEPENDENTE DO GRÁFICO)
    # =========================
    if tem_maiuscula and tem_minuscula and tem_numero and tem_simbolo and tamanho_ok:
        status = "SENHA FORTE!"
        cor = "green"

    elif tem_maiuscula and tem_minuscula and tem_numero:
        status = "SENHA MÉDIA!"
        cor = "yellow"

    else:
        status = "SENHA FRACA!"
        cor = "red"

    # =========================
    # BARRA VISUAL
    # =========================
    blocos = int(percent / 10) * 2
    barra = "█" * blocos + "░" * (20 - blocos)

    justificativa.insert(
        0,
        f"Força da Senha: {percent}%"
    )

    return (
        status,
        (barra, "\n".join(f"• {j}" for j in justificativa)),
        ["sistema"],
        cor
    )

# =========================
# GERADORES (RESTAURADOS)
# =========================
def inserir(valor):
    entrada.delete(0, "end")
    entrada.insert(0, valor)
    processar()


def gerar_forte():
    chars = string.ascii_letters + string.digits + "!@#$%^&*()_+=-"
    senha = [
        random.choice(string.ascii_lowercase),
        random.choice(string.ascii_uppercase),
        random.choice(string.digits),
        random.choice("!@#$%^&*")
    ]
    senha += [random.choice(chars) for _ in range(10)]
    random.shuffle(senha)
    inserir("".join(senha))


def gerar_media():
    nomes = ["Lucas","Maria","Pedro","Ana","Carlos","Bruno","Rafael","Davi", "Joao", "Jean", "Pietro", "Collao", "Arthur", "Matheus", "Jonas", "Luis"]
    inserir(random.choice(nomes) + str(random.randint(10,9999)))


def gerar_fraca():
    opcoes = ["123456","111111","qwerty","abcdef","senha123","admin"]
    inserir(random.choice(opcoes))


def limpar():
    entrada.delete(0, "end")
    resultado.delete("1.0", "end")
    status_label.configure(text="")


# =========================
# PROCESSAR
# =========================
def processar():

    texto = entrada.get()

    if modo.get() == "site":
        status, dados, _, cor = analisar_site(texto)

    elif modo.get() == "info":
        status, dados, _, cor = analisar_informacao(texto)

    else:
        status, dados, _, cor = analisar_senha(texto)

    barra, justificativas = dados

    linhas = [
        l.replace("• ", "")
        for l in justificativas.split("\n")
        if l.strip()
    ]

    resultado_direita_txt = []
    resultado_esquerda_txt = []

    if modo.get() == "info":

        if len(linhas) > 0:
            resultado_direita_txt.append(linhas[0])

        if len(linhas) > 1:
            resultado_direita_txt.append(linhas[1])

        resultado_esquerda_txt = linhas[2:]

    else:

        if len(linhas) > 0:
            resultado_direita_txt.append(linhas[0])

        resultado_esquerda_txt = linhas[1:]

    status_label.configure(
        text=status,
        text_color=cor
    )

    barra_label.configure(
        text=barra
    )

    resultado.configure(
        text="\n".join(resultado_direita_txt)
    )

    justificativas_label.configure(
        text="\n".join(resultado_esquerda_txt)
    )

# =========================
# UI
# =========================
app = ctk.CTk()
app.title("O Sentinela")

# tamanho da tela
largura = app.winfo_screenwidth()
altura = app.winfo_screenheight()

# ocupa toda a tela
app.geometry(f"{largura}x{altura}+0+0")

# remove bordas
app.overrideredirect(True)

# fecha com ESC
app.bind("<Escape>", lambda e: app.destroy())

# =========================
# ESCALA AUTOMÁTICA
# =========================
if largura <= 1366:
    escala = 1.2
else:
    escala = 1.0

ctk.set_widget_scaling(escala)
ctk.set_window_scaling(escala)

# =========================
# FRAME PRINCIPAL
# =========================
main_frame = ctk.CTkFrame(app)
main_frame.pack_propagate(False)
main_frame.pack(fill="both", expand=True, padx=20, pady=10)

# =========================
# TÍTULO
# =========================
titulo = ctk.CTkLabel(
    main_frame,
    text="O SENTINELA",
    font=("Arial", int(38 * escala), "bold")
)
titulo.pack(pady=(20, 30))

# =========================
# ENTRADA
# =========================
entrada = ctk.CTkEntry(
    main_frame,
    width=int(900 * escala),
    height=int(60 * escala),
    font=("Arial", int(22 * escala))
)
entrada.pack(pady=15)

# =========================
# MODOS
# =========================
modo = ctk.StringVar(value="info")

frame = ctk.CTkFrame(main_frame)
frame.pack(pady=15)

ctk.CTkRadioButton(
    frame,
    text="Site",
    variable=modo,
    value="site",
    font=("Arial", int(20 * escala))
).pack(side="left", padx=20)

ctk.CTkRadioButton(
    frame,
    text="Informação",
    variable=modo,
    value="info",
    font=("Arial", int(20 * escala))
).pack(side="left", padx=20)

ctk.CTkRadioButton(
    frame,
    text="Senha",
    variable=modo,
    value="senha",
    font=("Arial", int(20 * escala))
).pack(side="left", padx=20)

# =========================
# BOTÕES
# =========================
BTN_WIDTH = int(500 * escala)
BTN_HEIGHT = int(60 * escala)

ctk.CTkButton(
    main_frame,
    text="VERIFICAR",
    command=processar,
    font=("Arial", int(24 * escala), "bold"),
    width=BTN_WIDTH,
    height=BTN_HEIGHT
).pack(pady=3)

ctk.CTkButton(
    main_frame,
    text="LIMPAR",
    command=limpar,
    font=("Arial", int(24 * escala), "bold"),
    width=BTN_WIDTH,
    height=BTN_HEIGHT
).pack(pady=3)

ctk.CTkButton(
    main_frame,
    text="Gerar Senha Forte",
    command=gerar_forte,
    font=("Arial", int(22 * escala), "bold"),
    width=BTN_WIDTH,
    height=BTN_HEIGHT
).pack(pady=2)

ctk.CTkButton(
    main_frame,
    text="Gerar Senha Média",
    command=gerar_media,
    font=("Arial", int(22 * escala), "bold"),
    width=BTN_WIDTH,
    height=BTN_HEIGHT
).pack(pady=2)

ctk.CTkButton(
    main_frame,
    text="Gerar Senha Fraca",
    command=gerar_fraca,
    font=("Arial", int(22 * escala), "bold"),
    width=BTN_WIDTH,
    height=BTN_HEIGHT
).pack(pady=2)

# =========================
# ÁREA DE RESULTADO
# =========================
resultado_frame = ctk.CTkFrame(main_frame)
resultado_frame.pack(fill="both", expand=True, padx=40, pady=(10, 20))
resultado_frame.pack_propagate(False)

# =========================
# ESQUERDA = JUSTIFICATIVAS
# =========================
resultado_esquerda = ctk.CTkFrame(
    resultado_frame,
    fg_color="transparent"
)
resultado_esquerda.pack(side="left", fill="both", expand=True, padx=30)

titulo_just = ctk.CTkLabel(
    resultado_esquerda,
    text="JUSTIFICATIVAS",
    font=("Arial", 28, "bold")
)
titulo_just.pack(pady=(0, 20))

justificativas_label = ctk.CTkLabel(
    resultado_esquerda,
    text="",
    justify="left",
    anchor="center",
    wraplength=500,
    font=("Arial", 22)
)
justificativas_label.pack(pady=10)

# =========================
# DIREITA = RESULTADO
# =========================
resultado_direita = ctk.CTkFrame(
    resultado_frame,
    fg_color="transparent"
)
resultado_direita.pack(side="right", fill="both", expand=True, padx=30)

# =========================
# TÍTULO RESULTADO
# =========================
titulo_resultado = ctk.CTkLabel(
    resultado_direita,
    text="RESULTADO",
    font=("Arial", 28, "bold")
)
titulo_resultado.pack(pady=(0, 20))

status_label = ctk.CTkLabel(
    resultado_direita,
    text="",
    font=("Arial", 30, "bold")
)
status_label.pack(pady=(0, 20))

barra_label = ctk.CTkLabel(
    resultado_direita,
    text="",
    font=("Consolas", 30)
)
barra_label.pack(pady=15)

resultado = ctk.CTkLabel(
    resultado_direita,
    text="",
    wraplength=700,
    justify="center",
    font=("Arial", 26)
)
resultado.pack(pady=10)

app.mainloop()