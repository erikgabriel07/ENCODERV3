# ENCODERV3

## Tabela de Conteúdo
- [Introdução](#introdução)
- [Funcionalidades](#funcionalidades)  
- [Instalação](#instalação)  
- [Requisitos](#requisitos)  
- [Como usar](#como-usar)  
- [Contribuições e Suporte](#contribuições-e-suporte)
- [LICENSE](#LICENSE)

## Introdução
**ENCODERV3** é um programa que simula o funcionamento de um ransomware. Este programa utiliza criptografia asimétrica sobre criptografia simétrica.

## 🚀 Funcionalidades

- **Encriptação de arquivos**: Os arquivos são encriptados utilizando uma chave pública.
- **Decriptação de arquivos**: Restaure os arquivos criptografados para o estado original utilizando a chave privada.
- **Interface Simples**: Fácil de usar e configurar.

## 📦 Instalação
```bash
git clone https://github.com/erikgabriel07/ENCODERV3
cd ENCODERV3
```

## 🛠️ Requisitos

Certifique-se de ter o seguinte ambiente configurado:

- Python 3.8 ou superior
- Sistema operacional: Windows, macOS ou Linux

## 🔑 Como Usar

1. **Defina uma chave secreta**:  
   Utilize o programa de geração de par de chaves para gerar sua ``private.pem`` e a sua ``public.pem``
   que será o par de chaves que o programa irá precisar para funcionar. Certifique-se de copiar a chave pública
   em formato base64, ela estará armazenada junto com o arquivo ``public.pem``.

3. **Usando o programa**:  
   ```bash
   python encoderV3.py
   ```

## 🐛 Contribuições e Suporte

Encontrou um bug ou quer adicionar uma nova funcionalidade? Fique à vontade para abrir uma *issue* ou enviar um *pull request*.  

## LICENSE
```
MIT License

Copyright (c) 2024 Erik Gabriel

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
---
