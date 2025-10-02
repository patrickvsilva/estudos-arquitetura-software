# Resumo do livro Código Limpo

---

## Detalhes do Livro

- Título: Clean Code: A Handbook of Agile Software Craftsmanship

- Autor: Robert C. Martin (Uncle Bob)

- 464 Páginas

---

## Capítulo 1: O que é Código Limpo?

- **Código limpo** é aquele que revela claramente sua intenção, é fácil de ler, entender e modificar.
- Legibilidade é fundamental: código bem escrito é mais fácil de manter, evoluir e colaborar.
- O autor enfatiza que, mesmo que o código funcione, é essencial mantê-lo limpo para evitar problemas de manutenção.
- Código limpo não depende de linguagem, mas de disciplina e cuidado do desenvolvedor.
- Exemplos reais mostram que código limpo é reconhecido por outros desenvolvedores ao ser lido.

**Exemplo 1 – Intenção clara**

```python
# Código sujo
def d(a, b):
    return a / b

# Código limpo
def calcular_taxa_de_conversao(valor_total, quantidade_itens):
    return valor_total / quantidade_itens

```

**Exemplo 2 – Legibilidade**

```python
# Código sujo
x = 10
y = 5
z = x * y

# Código limpo
largura = 10
altura = 5
area = largura * altura

```

---

## Capítulo 2: Significando Nomes

- Nomes são fundamentais para clareza: variáveis, funções e classes devem ter nomes descritivos e específicos.
- Bons nomes tornam o código mais fácil de entender, pesquisar e modificar.
- Evite nomes genéricos, abreviações sem sentido ou nomes que não expressem claramente o propósito.
- Sempre prefira nomes que expliquem o que o elemento representa ou faz, facilitando o entendimento até para quem nunca viu o código antes.
- O esforço em nomear bem reduz tempo de manutenção e evita ambiguidades.

**Exemplo 1 – Nomeando variáveis**

```python
# Código sujo
n = 86400

# Código limpo
segundos_em_um_dia = 86400

```

**Exemplo 2 – Nomeando funções**

```python
# Código sujo
def handle():
    # faz algo
    pass

# Código limpo
def processar_pagamento():
    # processa o pagamento
    pass

```

---

## Capítulo 3: Funções

- Funções devem ser pequenas e ter uma única responsabilidade (“fazer uma coisa só”).
- O nome da função deve indicar claramente o que ela faz.
- Menos argumentos é melhor: idealmente um ou nenhum; funções com muitos argumentos tendem a fazer mais de uma coisa.
- Funções limpas facilitam testes, reutilização e compreensão do sistema.
- O conceito de “extrair função” ajuda a dividir grandes blocos de código em funções menores, cada uma responsável por um comportamento específico.

**Exemplo 1 – Função pequena e com uma responsabilidade**

```python
# Código sujo
def processa(usuario, valor):
    usuario.saldo += valor
    print(f"Saldo atualizado para {usuario.nome}: {usuario.saldo}")

# Código limpo
def adicionar_saldo(usuario, valor):
    usuario.saldo += valor

def mostrar_saldo(usuario):
    print(f"Saldo atualizado para {usuario.nome}: {usuario.saldo}")

```

**Exemplo 2 – Poucos argumentos**

```python
# Código sujo
def criar_usuario(nome, idade, cpf, email, senha, endereco):
    # lógica
    pass

# Código limpo
def criar_usuario(dados_usuario):
    # lógica
    pass

```
