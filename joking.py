#!/usr/bin/env python3
"""
JOKING - Ferramenta de manipulação de texto com interface bonita no terminal.

Requer as bibliotecas 'rich' e 'deep-translator':
    pip install rich deep-translator --break-system-packages
    (ou apenas: pip install rich deep-translator)

Menu principal:
1 - Alteração de Texto     (Espaçar letras, Inverter texto, Letras por números)
2 - Traduzir Texto          (Português -> Zulu, Inglês -> Zulu)
3 - Codificar/Cifrar Texto  (Binário, Morse, César, Base64, Hex)
0 - Sair
"""

import base64
import sys
import time

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    from rich.prompt import Prompt, IntPrompt
    from rich.align import Align
    from rich.text import Text
    from rich import box
except ImportError:
    print("A biblioteca 'rich' não está instalada.")
    print("Instale com: pip install rich --break-system-packages")
    sys.exit(1)

try:
    from deep_translator import GoogleTranslator
    TRADUTOR_DISPONIVEL = True
except ImportError:
    TRADUTOR_DISPONIVEL = False


console = Console()

BANNER = r"""
     _       _    _             
    | | ___ | | _(_)_ __   __ _  
 _  | |/ _ \| |/ / | '_ \ / _` | 
| |_| | (_) |   <| | | | | (_| | 
 \___/ \___/|_|\_\_|_| |_|\__, | 
                          |___/  
"""


def mostrar_banner() -> None:
    console.clear()
    texto_banner = Text(BANNER, style="bold magenta")
    console.print(Align.center(texto_banner))
    console.print(
        Align.center(
            "[bold cyan]Ferramenta de manipulação de texto[/bold cyan] "
            "[dim]v1.0[/dim]"
        )
    )
    console.print(Align.center("[dim italic]por RRespxwnss[/dim italic]"))
    console.print()


def mostrar_resultado(original: str, resultado: str, titulo: str) -> None:
    painel = Panel(
        f"[bold]Original:[/bold]  [white]{original}[/white]\n"
        f"[bold]Resultado:[/bold] [bold green]{resultado}[/bold green]",
        title=f"[bold cyan]{titulo}[/bold cyan]",
        border_style="green",
        box=box.ROUNDED,
    )
    console.print(painel)


def carregando(mensagem: str = "Processando") -> None:
    with console.status(f"[bold cyan]{mensagem}...[/bold cyan]", spinner="dots"):
        time.sleep(0.5)


# ============================================================
# MENU PRINCIPAL
# ============================================================

def mostrar_menu_principal() -> None:
    tabela = Table(
        box=box.ROUNDED,
        show_header=True,
        header_style="bold white on magenta",
        border_style="magenta",
    )
    tabela.add_column("Opção", justify="center", style="bold yellow", width=8)
    tabela.add_column("Menu", style="white")
    tabela.add_column("Contém", style="dim italic")

    tabela.add_row("1", "Alteração de Texto", "Espaçar letras, Inverter texto, Letras por números")
    tabela.add_row("2", "Traduzir Texto", "Português -> Zulu, Inglês -> Zulu")
    tabela.add_row("3", "Codificar/Cifrar Texto", "Binário, Morse, César, Base64, Hex")
    tabela.add_row("0", "Sair", "")

    console.print(Panel(tabela, title="[bold]JOKING - MENU PRINCIPAL[/bold]", border_style="cyan", expand=False))
    console.print()


# ============================================================
# 1) ALTERAÇÃO DE TEXTO
# ============================================================

def espacar_letras(texto: str) -> str:
    sem_espacos = texto.replace(" ", "")
    return " ".join(sem_espacos)


def inverter_texto(texto: str) -> str:
    return texto[::-1]


def trocar_letras_por_numeros(texto: str) -> str:
    trocas = {
        "e": "3", "E": "3",
        "a": "4", "A": "4",
        "i": "1", "I": "1",
    }
    return "".join(trocas.get(c, c) for c in texto)


def mostrar_submenu_alteracao() -> None:
    tabela = Table(
        box=box.ROUNDED,
        show_header=True,
        header_style="bold white on green",
        border_style="green",
    )
    tabela.add_column("Opção", justify="center", style="bold yellow", width=8)
    tabela.add_column("Descrição", style="white")
    tabela.add_column("Exemplo", style="dim italic")

    tabela.add_row("1", "Espaçar letras", "'Boa Tarde' -> 'B o a T a r d e'")
    tabela.add_row("2", "Inverter texto", "'Boa tarde' -> 'edrat aoB'")
    tabela.add_row("3", "Trocar letras por números", "'Boa tarde' -> 'Bo4 t4rd3'")
    tabela.add_row("0", "Voltar", "")

    console.print(
        Panel(tabela, title="[bold]ALTERAÇÃO DE TEXTO[/bold]", border_style="green", expand=False)
    )
    console.print()


def executar_alteracao() -> None:
    while True:
        mostrar_banner()
        mostrar_submenu_alteracao()

        sub_opcao = Prompt.ask(
            "[bold yellow]Escolha uma opção[/bold yellow]",
            choices=["0", "1", "2", "3"],
            show_choices=False,
        )

        if sub_opcao == "0":
            return

        texto = Prompt.ask("[bold yellow]Digite a palavra ou frase[/bold yellow]")

        if sub_opcao == "1":
            carregando("Espaçando letras")
            resultado = espacar_letras(texto)
            titulo = "ESPAÇAR LETRAS"
        elif sub_opcao == "2":
            carregando("Invertendo texto")
            resultado = inverter_texto(texto)
            titulo = "INVERTER TEXTO"
        else:
            carregando("Trocando letras por números")
            resultado = trocar_letras_por_numeros(texto)
            titulo = "LETRAS POR NÚMEROS"

        console.print()
        mostrar_resultado(texto, resultado, titulo)
        console.print()
        Prompt.ask("[dim]Pressione ENTER para voltar[/dim]", default="", show_default=False)


# ============================================================
# 2) TRADUZIR TEXTO
# ============================================================

def traduzir_texto(texto: str, idioma_origem: str) -> str:
    """Traduz um texto para zulu, a partir do idioma de origem informado ('pt' ou 'en')."""
    if not TRADUTOR_DISPONIVEL:
        return "[ERRO] Biblioteca 'deep-translator' não instalada. Rode: pip install deep-translator"

    try:
        return GoogleTranslator(source=idioma_origem, target="zu").translate(texto)
    except Exception as erro:
        return f"[ERRO] Não foi possível traduzir. Verifique sua internet. Detalhe: {erro}"


def mostrar_submenu_traducao() -> None:
    tabela = Table(
        box=box.ROUNDED,
        show_header=True,
        header_style="bold white on yellow",
        border_style="yellow",
    )
    tabela.add_column("Opção", justify="center", style="bold yellow", width=8)
    tabela.add_column("Tradução", style="white")
    tabela.add_column("Exemplo", style="dim italic")

    tabela.add_row("1", "Português -> Zulu", "'Boa tarde' -> 'Sawubona'")
    tabela.add_row("2", "Inglês -> Zulu", "'Good afternoon' -> 'Sawubona'")
    tabela.add_row("0", "Voltar", "")

    console.print(
        Panel(tabela, title="[bold]TRADUZIR TEXTO[/bold]", border_style="yellow", expand=False)
    )
    console.print()


def executar_traducao() -> None:
    while True:
        mostrar_banner()
        mostrar_submenu_traducao()

        sub_opcao = Prompt.ask(
            "[bold yellow]Escolha uma opção[/bold yellow]",
            choices=["0", "1", "2"],
            show_choices=False,
        )

        if sub_opcao == "0":
            return

        texto = Prompt.ask("[bold yellow]Digite a palavra ou frase[/bold yellow]")

        if sub_opcao == "1":
            carregando("Traduzindo do português para zulu")
            resultado = traduzir_texto(texto, "pt")
            titulo = "PORTUGUÊS -> ZULU"
        else:
            carregando("Traduzindo do inglês para zulu")
            resultado = traduzir_texto(texto, "en")
            titulo = "INGLÊS -> ZULU"

        console.print()
        mostrar_resultado(texto, resultado, titulo)
        console.print()
        Prompt.ask("[dim]Pressione ENTER para voltar[/dim]", default="", show_default=False)


# ============================================================
# 3) CODIFICAR/CIFRAR TEXTO
# ============================================================

def texto_para_binario(texto: str) -> str:
    """Converte cada caractere em seu valor binário (8 bits), separados por espaço."""
    return " ".join(format(ord(c), "08b") for c in texto)


MORSE_CODE = {
    "A": ".-", "B": "-...", "C": "-.-.", "D": "-..", "E": ".",
    "F": "..-.", "G": "--.", "H": "....", "I": "..", "J": ".---",
    "K": "-.-", "L": ".-..", "M": "--", "N": "-.", "O": "---",
    "P": ".--.", "Q": "--.-", "R": ".-.", "S": "...", "T": "-",
    "U": "..-", "V": "...-", "W": ".--", "X": "-..-", "Y": "-.--",
    "Z": "--..",
    "0": "-----", "1": ".----", "2": "..---", "3": "...--", "4": "....-",
    "5": ".....", "6": "-....", "7": "--...", "8": "---..", "9": "----.",
    ".": ".-.-.-", ",": "--..--", "?": "..--..", "!": "-.-.--",
}


def texto_para_morse(texto: str) -> str:
    """Converte o texto em código morse (letras separadas por espaço, palavras por '/')."""
    palavras = texto.upper().split(" ")
    resultado_palavras = []
    for palavra in palavras:
        letras = [MORSE_CODE.get(c, c) for c in palavra]
        resultado_palavras.append(" ".join(letras))
    return " / ".join(resultado_palavras)


def cifra_cesar(texto: str, deslocamento: int) -> str:
    """Aplica a cifra de César, deslocando cada letra pelo número informado."""
    resultado = []
    for c in texto:
        if c.isupper():
            resultado.append(chr((ord(c) - ord("A") + deslocamento) % 26 + ord("A")))
        elif c.islower():
            resultado.append(chr((ord(c) - ord("a") + deslocamento) % 26 + ord("a")))
        else:
            resultado.append(c)
    return "".join(resultado)


def texto_para_base64(texto: str) -> str:
    """Codifica o texto em Base64."""
    return base64.b64encode(texto.encode("utf-8")).decode("utf-8")


def texto_para_hex(texto: str) -> str:
    """Codifica o texto em hexadecimal."""
    return texto.encode("utf-8").hex(" ")


def mostrar_submenu_codificacao() -> None:
    tabela = Table(
        box=box.ROUNDED,
        show_header=True,
        header_style="bold white on blue",
        border_style="blue",
    )
    tabela.add_column("Opção", justify="center", style="bold yellow", width=8)
    tabela.add_column("Formato", style="white")
    tabela.add_column("Exemplo", style="dim italic")

    tabela.add_row("1", "Binário", "'Oi' -> '01001111 01101001'")
    tabela.add_row("2", "Código Morse", "'Oi' -> '--- ..'")
    tabela.add_row("3", "Cifra de César", "'Oi' (deslocamento 1) -> 'Pj'")
    tabela.add_row("4", "Base64", "'Oi' -> 'T2k='")
    tabela.add_row("5", "Hex", "'Oi' -> '4f 69'")
    tabela.add_row("0", "Voltar", "")

    console.print(
        Panel(tabela, title="[bold]CODIFICAR / CIFRAR TEXTO[/bold]", border_style="blue", expand=False)
    )
    console.print()


def executar_codificacao() -> None:
    while True:
        mostrar_banner()
        mostrar_submenu_codificacao()

        sub_opcao = Prompt.ask(
            "[bold yellow]Escolha um formato[/bold yellow]",
            choices=["0", "1", "2", "3", "4", "5"],
            show_choices=False,
        )

        if sub_opcao == "0":
            return

        texto = Prompt.ask("[bold yellow]Digite a palavra ou frase[/bold yellow]")

        if sub_opcao == "1":
            carregando("Convertendo para binário")
            resultado = texto_para_binario(texto)
            titulo = "BINÁRIO"
        elif sub_opcao == "2":
            carregando("Convertendo para código morse")
            resultado = texto_para_morse(texto)
            titulo = "CÓDIGO MORSE"
        elif sub_opcao == "3":
            deslocamento = IntPrompt.ask(
                "[bold yellow]Deslocamento da cifra de César (ex: 3)[/bold yellow]"
            )
            carregando("Aplicando cifra de César")
            resultado = cifra_cesar(texto, deslocamento)
            titulo = f"CIFRA DE CÉSAR (deslocamento {deslocamento})"
        elif sub_opcao == "4":
            carregando("Convertendo para Base64")
            resultado = texto_para_base64(texto)
            titulo = "BASE64"
        else:
            carregando("Convertendo para hexadecimal")
            resultado = texto_para_hex(texto)
            titulo = "HEX"

        console.print()
        mostrar_resultado(texto, resultado, titulo)
        console.print()
        Prompt.ask("[dim]Pressione ENTER para voltar[/dim]", default="", show_default=False)


# ============================================================
# LOOP PRINCIPAL
# ============================================================

def main() -> None:
    while True:
        mostrar_banner()
        mostrar_menu_principal()

        opcao = Prompt.ask(
            "[bold yellow]Escolha uma opção[/bold yellow]",
            choices=["0", "1", "2", "3"],
            show_choices=False,
        )

        if opcao == "0":
            console.print()
            console.print(Align.center("[bold magenta]Até mais! 👋[/bold magenta]"))
            console.print()
            break
        elif opcao == "1":
            executar_alteracao()
        elif opcao == "2":
            executar_traducao()
        else:
            executar_codificacao()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[bold red]Interrompido pelo usuário.[/bold red]")