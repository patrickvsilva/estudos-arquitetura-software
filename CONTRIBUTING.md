# Guia de Contribuição

Obrigado por considerar contribuir com este projeto! Este documento fornece diretrizes para contribuir.

## Como Contribuir

### 1. Reportar Bugs

Se você encontrar um bug, por favor:
- Verifique se o bug já não foi reportado nas [Issues](../../issues)
- Abra uma nova issue com:
  - Título claro e descritivo
  - Descrição detalhada do problema
  - Passos para reproduzir
  - Comportamento esperado vs. atual
  - Screenshots (se aplicável)

### 2. Sugerir Melhorias

Para sugerir melhorias:
- Abra uma issue descrevendo sua sugestão
- Explique por que a melhoria seria útil
- Forneça exemplos de uso, se possível

### 3. Enviar Pull Requests

#### Preparação

1. **Fork o repositório**
   ```bash
   # Clone seu fork
   git clone https://github.com/seu-usuario/estudos-arquitetura-software.git
   cd estudos-arquitetura-software
   ```

2. **Crie um branch para sua feature**
   ```bash
   git checkout -b feature/minha-feature
   # ou
   git checkout -b docs/minha-documentacao
   # ou
   git checkout -b fix/meu-bugfix
   ```

3. **Configure o ambiente**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # ou
   venv\Scripts\activate  # Windows
   
   pip install -r requirements.txt
   ```

#### Desenvolvimento

1. **Faça suas alterações**
   - Siga as convenções de código Python (PEP 8)
   - Adicione type hints
   - Documente seu código
   - Mantenha o código limpo e legível

2. **Execute testes**
   ```bash
   # Se houver testes
   pytest
   ```

3. **Formate o código**
   ```bash
   black .
   isort .
   ```

4. **Verifique qualidade**
   ```bash
   pylint seu_arquivo.py
   mypy seu_arquivo.py
   ```

#### Submissão

1. **Commit suas mudanças**
   ```bash
   git add .
   git commit -m "feat: adiciona nova funcionalidade X"
   ```
   
   Use commits semânticos:
   - `feat:` nova funcionalidade
   - `fix:` correção de bug
   - `docs:` documentação
   - `refactor:` refatoração de código
   - `test:` adição ou correção de testes
   - `chore:` tarefas de manutenção

2. **Push para seu fork**
   ```bash
   git push origin feature/minha-feature
   ```

3. **Abra um Pull Request**
   - Vá para o repositório original no GitHub
   - Clique em "New Pull Request"
   - Selecione seu branch
   - Preencha o template com:
     - Descrição clara das mudanças
     - Issue relacionada (se houver)
     - Screenshots (se aplicável)
     - Checklist de verificação

## Padrões de Código

### Python

```python
# Bom exemplo
from typing import List, Optional

def calcular_media(numeros: List[float]) -> float:
    """
    Calcula a média aritmética de uma lista de números.
    
    Args:
        numeros: Lista de números de ponto flutuante.
        
    Returns:
        A média aritmética dos números.
        
    Raises:
        ValueError: Se a lista estiver vazia.
    """
    if not numeros:
        raise ValueError("Lista não pode estar vazia")
    return sum(numeros) / len(numeros)
```

### Estrutura de Arquivos

```
novo_modulo/
├── __init__.py
├── models.py          # Modelos de dados
├── services.py        # Lógica de negócio
├── utils.py          # Utilitários
└── tests/
    └── test_services.py
```

### Documentação

- Use docstrings em módulos, classes e funções
- Adicione exemplos de uso quando apropriado
- Mantenha README.md atualizado
- Documente decisões arquiteturais importantes

## Tipos de Contribuição

### Documentação

- Corrigir erros de digitação
- Melhorar clareza da documentação
- Adicionar exemplos
- Traduzir documentação

### Código

- Implementar novos design patterns
- Adicionar exemplos práticos
- Melhorar código existente
- Adicionar testes

### Conteúdo Educacional

- Adicionar tutoriais
- Criar exercícios práticos
- Compartilhar recursos de estudo
- Adicionar referências úteis

## Revisão de Code

Ao revisar Pull Requests, considere:

- [ ] O código segue os padrões do projeto?
- [ ] A documentação está completa e clara?
- [ ] Os testes passam?
- [ ] O código é eficiente e manutenível?
- [ ] As mudanças são bem explicadas?

## Código de Conduta

Este projeto adota um Código de Conduta que esperamos que todos os participantes sigam:

### Nossa Promessa

Nós, como membros, contribuidores e líderes, nos comprometemos a tornar a participação em nossa comunidade uma experiência livre de assédio para todos.

### Nossos Padrões

Exemplos de comportamento que contribuem para um ambiente positivo:

- Usar linguagem acolhedora e inclusiva
- Respeitar pontos de vista e experiências diferentes
- Aceitar críticas construtivas graciosamente
- Focar no que é melhor para a comunidade
- Mostrar empatia com outros membros da comunidade

Exemplos de comportamento inaceitável:

- Uso de linguagem ou imagens sexualizadas
- Comentários trolls, insultos ou ataques pessoais
- Assédio público ou privado
- Publicar informações privadas de outros sem permissão

## Licença

Ao contribuir, você concorda que suas contribuições serão licenciadas sob a mesma licença MIT do projeto.

## Perguntas?

Se tiver dúvidas, sinta-se à vontade para:
- Abrir uma issue
- Entrar em contato através do GitHub

---

Obrigado por contribuir! 🎉
