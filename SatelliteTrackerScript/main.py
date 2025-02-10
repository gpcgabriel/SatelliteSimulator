from Controller import Controller
from Region import Region
from time import sleep
import sys

# Entrada esperada: python3 main.py -24.7875286 -55.768967 90 52 5 15
if __name__ == '__main__':
    global controller
    global region
    global isSuccess
    i=0 # Variável para controle de etapas

    # Organizando as coordenadas passadas como argumento
    args = sys.argv[1:]
    coordinates = (args[0], args[1], 0)
    search_radius = args[2]
    category_id = args[3]
    steps = int(args[4])
    delay = float(args[5])
    isSuccess = True # Variável de decisão sobre o êxito na execução

    # Instanciando o controlador e a região
    controller = Controller()
    region = Region(coordinates, search_radius, category_id)

    # Verificando se a pasta de logs existe (e criando caso não exista)
    if not controller.check_if_path_exists('logs'):
        controller.print_buffer('Criando pasta de logs')
        try:
            controller.create_path('logs')
        except:
            print('\n##########\nOcorreu um erro na criação da pasta de log\n##########\n')
            exit(1)

    controller.print_buffer('Definindo um nome para o arquivo')
    file_name = controller.datetime_parse_to_str(controller.get_datetime())
    controller.print_buffer(f'{file_name}')

    # Criando o arquivo de logs
    try:
        controller.create_file(f'logs/log_{file_name}.json')
        log_path = f'logs/log_{file_name}.json'
    except:
        print(f'\n##########\nOcorreu um erro na criação do arquivo de log {file_name}\n##########\n')
        exit(1) 

    while i < steps:
        print('\n###################################################')
        i+=1
        controller.print_buffer(f'Etapa {i}')
        print('###################################################\n')

        ###############################################################
        controller.print_buffer('Buscando satélites')
        response = region.find_satellites('')

        try:
            if controller.check_if_solicitation_is_successfull(response):
                satellites_in_region = region.get_satellite_list_in_response(response)
                region.set_satellites(satellites_in_region)

                # Escrevendo os satélites no arquivo de log
                try:
                    controller.print_buffer('Escrevendo no log')
                    controller.write_satellite_in_file(satellites_in_region, log_path)
                    break
                except:
                    print(f'\n##########\nOcorreu um erro ao escrever no arquivo {log_path}\n##########\n')
                    isSuccess = False
        except:
            print('########## Erro no request ##########')
            print('Reconectando...')
            region.change_key()
        ###############################################################

        controller.print_buffer('Em espera')
        sleep(delay) # delay entre uma busca e outra

    # Finalizando o arquivo json
    try:
        controller.close_write_file(log_path)
    except Exception as e:
        print(f'\n##########\nOcorreu um erro ao escrever no final arquivo {log_path}.\n\tEle pode ter ficado desformatado.\n##########\n')
        isSuccess = False

    # Grava os logs em uma planilha (para análise)
    try:
        controller.save_logs_in_sheet(log_path)
    except Exception as e:
        print('Ocorreu um erro: ', e)
        isSuccess = False

    # Verifica se o programa obteve êxito na execução
    if isSuccess:
        controller.print_buffer('Programa executado com sucesso!')
        print(f'\n##########\nPrograma executado com sucesso!\n##########\n')
    else:
        print(f'\n##########\nNem todos os passos foram executados com sucesso.\n##########\n')
