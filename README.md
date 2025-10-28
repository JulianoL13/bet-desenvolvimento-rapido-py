# ✈️ Plane Crash Game

Um jogo de crash/aviaozinho desenvolvido com Kivy, KivyMD e KivyLang em uma única tela.

## 🎮 Como Jogar

1. **Faça sua aposta**: Digite o valor que deseja apostar
2. **Inicie o jogo**: Pressione ESPAÇO para começar
3. **Cashout**: Pressione C para sacar seus ganhos antes do crash
4. **Objetivo**: Sacar antes que o avião "crash" e você perca tudo

## 🚀 Instalação

1. Instale as dependências:
```bash
pip install -r requirements.txt
```

2. Execute o jogo:
```bash
python main.py
```

## 🎯 Funcionalidades

- **Sistema de Apostas**: Aposte valores personalizados
- **Multiplicadores Dinâmicos**: Algoritmo realista de crash
- **Cashout**: Saque seus ganhos a qualquer momento
- **Histórico**: Veja seus últimos resultados na mesma tela
- **Interface Material**: Design moderno com KivyMD
- **Tela Única**: Tudo em uma interface simples e direta

## 🎨 Controles

- **ESPAÇO**: Iniciar jogo
- **C**: Cashout (sacar ganhos)
- **Mouse**: Navegar pela interface

## 📱 Compatibilidade

- Windows, Linux, macOS
- Android (com buildozer)
- iOS (com buildozer)

## 🔧 Tecnologias

- **Kivy 2.3.1**: Framework principal
- **KivyMD 1.1.1**: Material Design
- **KivyLang**: Linguagem de layout
- **Python**: Linguagem de programação

## 📊 Algoritmo de Crash

O jogo usa um algoritmo baseado em distribuição exponencial:
- 50% chance de crash antes de 2x
- 25% chance de crash antes de 4x
- 12.5% chance de crash antes de 8x
- E assim por diante...

## 🎮 Interface

- **Tela única** com todas as funcionalidades
- **Saldo e apostas** sempre visíveis
- **Multiplicador em tempo real**
- **Histórico dos últimos resultados**
- **Animações do avião** (decolagem e crash)

## ⚠️ Aviso

Este é um jogo de demonstração. Jogue com responsabilidade!