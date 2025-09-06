# Chatbot Three

O Chatbot da Three busca atender as dúvidas dos usuários da plataforma, oferecendo suporte e direcionamento.

A Three é uma plataforma gamificada de ensino de programação atualmente em desenvolvimento, idealizada por alunos de Engenharia de Software - UFCA.

## Tecnologias utilizadas
- Backend em Python com o framework Flask
- Frontend com HTML, CSS e JavaScript

## Estrutura base da aplicação
```bash
meu_projeto/
│
├── static/
│   ├── css/
│   ├── js/
│   └── img/
│
├── app/
│   ├── services/
│   │   └── index.html
│   │
│   ├── templates/
│   │   └── index.html
│   │
│   ├── __init__.py
│   └── routes.py
│
├── app.py
└── requirements.txt
```

## Executando o projeto na sua máquina

Clone o repositório:
```bash
git clone https://github.com/ufca-es/three-chatbot
```

Crie o ambiente virtual:
```bash
py -3 -m venv .venv
```

Inicialize o .venv:
```bash
.venv\Scripts\activate
```

Instale as dependências (pacotes):
```bash
pip install -r requirements.txt
```

Inicialize o servidor Flask:
```bash
$env:FLASK_APP="app.py"
$env:FLASK_ENV="development"
flask run
```

## Desenvolvido por
- [Sebastião Sousa Soares](https://github.com/SebastiaoSoares)
- [Espedito Ramom Mascena Ricarto](https://github.com/RamomRicarto)
- [Sabrina Alencar Soares](https://github.com/sabrinaalencaar)

#### Orientador:
- [Jayr Alencar Pereira](https://github.com/jayralencar)
