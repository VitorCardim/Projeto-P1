import sys
# teste
TODO_FILE = 'todo.txt'
ARCHIVE_FILE = 'done.txt'

RED   = "\033[1;31m"  
BLUE  = "\033[1;34m"
CYAN  = "\033[1;36m"
GREEN = "\033[0;32m"
RESET = "\033[0;0m"
BOLD    = "\033[;1m"
REVERSE = "\033[;7m"
YELLOW = "\033[0;33m"

ADICIONAR = 'a'
REMOVER = 'r'
FAZER = 'f'
PRIORIZAR = 'p'
LISTAR = 'l'

# Imprime texto com cores. Por exemplo, para imprimir "Oi mundo!" em vermelho, basta usar
#
# printCores('Oi mundo!', RED)
# printCores('Texto amarelo e negrito', YELLOW + BOLD)

def printCores(texto, cor) :
  print(cor + texto + RESET)
  

# Adiciona um compromisso aa agenda. Um compromisso tem no minimo
# uma descrição. Adicionalmente, pode ter, em caráter opcional, uma
# data (formato DDMMAAAA), um horário (formato HHMM), uma prioridade de A a Z, 
# um contexto onde a atividade será realizada (precedido pelo caractere
# '@') e um projeto do qual faz parte (precedido pelo caractere '+'). Esses
# itens opcionais são os elementos da tupla "extras", o segundo parâmetro da
# função.
#
# extras ~ (data, hora, prioridade, contexto, projeto)
#
# Qualquer elemento da tupla que contenha um string vazio ('') não
# deve ser levado em consideração. 
def adicionar(descricao, extras):  
  if descricao  == '' :
    return False
  else:
      data = '' 
      hora = ''
      pri = ''
      contexto = ''
      projeto = ''
    
      for x in extras:
        if dataValida(x) == True:
           data = x
        elif contextoValido(x) == True:
           contexto = x
        elif projetoValido(x) == True:
            projeto = x
        elif prioridadeValida(x) == True:
           pri = x
        elif horaValida(x) == True:
            hora = x
      novaAtividade = descricao+' '+ data +' '+ hora+' '+pri+' '+contexto+' '+projeto
  try: 
    fp = open(TODO_FILE, 'a')
    fp.write(novaAtividade + "\n")
    fp.close()
  except IOError as err:
    print("Não foi possível escrever para o arquivo " + TODO_FILE)
    print(err)
    return False
  return True
def prioridadeValida(pri):
  pri = pri.strip('(')
  pri = pri.strip(')')
  pri = pri.strip()
  pri = pri.lower()
  lista = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
  for x in lista:
    if x == pri:
      return True
  return False
def horaValida(horaMin) :
  if len(horaMin) != 4 or not soDigitos(horaMin):
    return False
  else:
    hora = int(horaMin[0:2])
    minu = int(horaMin[2:4])
    if (hora < 00) or (hora > 24) or (minu > 59) or (minu < 00):
      return False
    return True
def dataValida(data) :
  if len(data) == 8 and soDigitos(data):
    dia = int(data[0:2])
    mes = int(data[3:4])
    mes30 = [4,6,8,10,11]
    mes31 =[1,3,5,7,9,12]
    if mes <= 12 and mes >= 1:
      if dia == 2 and mes == 28:
        return True
      if dia == 30:
        for x in mes30:
          if x == mes:
            return True
      if dia == 31:
        for x in mes31:
          if x == 30:
            return True
  return False
def projetoValido(proj):
  if len(proj) >= 2 and proj[0:1] == '+':
    return True
  return False
def contextoValido(cont):
  if len(cont) >= 2 and cont[0:1] == '+':
    return True
  return False
def soDigitos(numero) :
  if type(numero) != str :
    return False
  for x in numero :
    if x < '0' or x > '9' :
      return False
  return True
def organizar(linhas):
  itens = []

  for l in linhas:
    data = '' 
    hora = ''
    pri = ''
    desc = ''
    contexto = ''
    projeto = ''
  
    l = l.strip() 
    tokens = l.split()
    while tokens != []:
     for x in tokens:
       if dataValida(x) == True:
         data = tokens.pop(0)
       elif contextoValido(x) == True:
         contexto = tokens.pop(0)
       elif projetoValido(x) == True:
         projeto = tokens.pop(0)
       elif prioridadeValida(x) == True:
         pri = tokens.pop(0)
       elif horaValida(x) == True:
         hora = tokens.pop(0)
       else:
         desc = desc + tokens.pop(0) + ' '
    itens.append((desc, (data, hora, pri, contexto, projeto)))

  return itens


# Datas e horas são armazenadas nos formatos DDMMAAAA e HHMM, mas são exibidas
# como se espera (com os separadores apropridados). 
#
# Uma extensão possível é listar com base em diversos critérios: (i) atividades com certa prioridade;
# (ii) atividades a ser realizadas em certo contexto; (iii) atividades associadas com
# determinado projeto; (vi) atividades de determinado dia (data específica, hoje ou amanhã). Isso não
# é uma das tarefas básicas do projeto, porém. 
def listar():

  ################ COMPLETAR
  return 

def ordenarPorDataHora(itens):

  ################ COMPLETAR

  return itens
   
def ordenarPorPrioridade(itens):

  ################ COMPLETAR

  return itens

def fazer(num):

  ################ COMPLETAR

  return 

def remover():

  ################ COMPLETAR

  return

# prioridade é uma letra entre A a Z, onde A é a mais alta e Z a mais baixa.
# num é o número da atividade cuja prioridade se planeja modificar, conforme
# exibido pelo comando 'l'. 
def priorizar(num, prioridade):

  ################ COMPLETAR

  return 



# Esta função processa os comandos e informações passados através da linha de comando e identifica
# que função do programa deve ser invocada. Por exemplo, se o comando 'adicionar' foi usado,
# isso significa que a função adicionar() deve ser invocada para registrar a nova atividade.
# O bloco principal fica responsável também por tirar espaços em branco no início e fim dos strings
# usando o método strip(). Além disso, realiza a validação de horas, datas, prioridades, contextos e
# projetos. 
def processarComandos(comandos) :
  if comandos[1] == ADICIONAR:
    comandos.pop(0) # remove 'agenda.py'
    comandos.pop(0) # remove 'adicionar'
    itemParaAdicionar = organizar([' '.join(comandos)])[0]
    # itemParaAdicionar = (descricao, (prioridade, data, hora, contexto, projeto))
    adicionar(itemParaAdicionar[0], itemParaAdicionar[1]) # novos itens não têm prioridade
  elif comandos[1] == LISTAR:
    return    
    ################ COMPLETAR

  elif comandos[1] == REMOVER:
    return    

    ################ COMPLETAR    

  elif comandos[1] == FAZER:
    return    

    ################ COMPLETAR

  elif comandos[1] == PRIORIZAR:
    return    

    ################ COMPLETAR

  else :
    print("Comando inválido.")
    
  
# sys.argv é uma lista de strings onde o primeiro elemento é o nome do programa
# invocado a partir da linha de comando e os elementos restantes são tudo que
# foi fornecido em sequência. Por exemplo, se o programa foi invocado como
#
# python3 agenda.py a Mudar de nome.
#
# sys.argv terá como conteúdo
#
# ['agenda.py', 'a', 'Mudar', 'de', 'nome']
processarComandos(sys.argv)
