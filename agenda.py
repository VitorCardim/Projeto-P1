import sys
TODO_FILE = 'todo.txt'
ARCHIVE_FILE = 'done.txt'
RED   = "\033[1;31m"
BLUE  = "\033[0;34m"
CYAN  = "\033[0;36m"
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
def printCores(texto, cor):
    print(cor + texto + RESET)
def adicionar(descricao, extras):
    if descricao  == '':
         return False
    else:
        data = ''
        hora = ''
        pri = ''
        contexto = ''
        projeto = ''
        for x in extras:#os strips pra tirar espaços no inicio e final
            if dataValida(x) == True:
                data = x
            elif horaValida(x) == True:
                hora = x
            elif contextoValido(x) == True:
                contexto = contexto+' '+x
                contexto = contexto.strip()
            elif projetoValido(x) == True:
                projeto = projeto+' '+x
                projeto = projeto.strip()
            elif prioridadeValida(x) == True:
                pri = x.upper()
    atividade = data+' '+hora+' '+pri+' '+descricao+' '+contexto+' '+projeto
    atividade = atividade.split()#caso algum dos elementos for em branco, pra garantir sem espaçamentos, como ja estao na ordem, nao vai ter bronca os reordenar com o for
    novaAtividade = ''
    for x in atividade:
        novaAtividade = novaAtividade+' '+x
        novaAtividade = novaAtividade.strip()
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
    if len(pri) == 3:
        pri = pri.strip('(')
        pri = pri.strip(')')
        pri = pri.strip()
        pri = pri.lower()
        lista = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
        for x in lista:
            if x == pri:
              return True
    return False
def horaValida(horaMin):
    if len(horaMin) != 4 or not soDigitos(horaMin):
        return False
    else:
        hora = int(horaMin[0:2])
        minu = int(horaMin[2:4])
        if (hora < 00) or (hora > 23) or (minu > 59) or (minu < 00):
            return False
    return True
def dataValida(data):
    if len(data) == 8 and soDigitos(data):
        dia = int(data[0:2])
        mes = int(data[2:4])
        mes30 = [4,6,8,10,11]
        mes31 =[1,3,5,7,9,12]
        if mes <= 12 and mes >= 1:
            if dia <= 29 and dia >= 1:
                return True
        elif dia == 30:
            for x in mes30:
                if x == mes:
                    return True
        elif dia == 31:
            for x in mes31:
                if x == 30:
                    return True
    return False
def projetoValido(proj):
    if len(proj) >= 2 and proj[0:1] == '+':
        return True
    return False
def contextoValido(cont):
    if len(cont) >= 2 and cont[0:1] == '@':
        return True
    return False
def soDigitos(numero):
    if type(numero) != str:
        return False
    for x in numero:
        if x < '0' or x > '9':
            return False
    return True
def verificar(lista,op1,op2): #funcao auxiliar para o organizar ( verifica se ainda existe algum contexto ou projeto)
    for x in lista:
        if x[0:1] == op1 or x[0:1] == op2:
            return True
    return False
def organizar(linhas):
    itens = []
    for l in linhas:
        data = ''
        hora = ''
        pri = ''
        desc = ''
        contexto = ''
        projeto = ''
        t = l.strip()
        tokens = t.split()
        for x in tokens:
            if dataValida(x) == True:
                data = x
                tokens.remove(x)
                break
            else:
                for x in tokens:
                    if horaValida(x) == True:
                        hora = x
                        tokens.remove(x)
                        break
                    else:
                        for x in tokens:
                            if prioridadeValida(x) == True:
                                pri = x
                                tokens.remove(x)
                                break
        if data != '':
            for x in tokens:
                if horaValida(x) == True:
                    hora = x
                    tokens.remove(x)
                    break
                else:
                    for x in tokens:
                        if prioridadeValida(x) == True:
                            pri = x
                            tokens.remove(x)
                            break
        if hora != '':
            for x in tokens:
                if prioridadeValida(x) == True:
                    pri = x
                    tokens.remove(x)
                    break
        t = True
        while t == True:
            for x in tokens:
                if x[0:1] == '+':
                    projeto = projeto+' '+ x
                    tokens.remove(x)
                    projeto = projeto.strip()
                if x[0:1] == '@':
                    contexto = contexto +' '+ x
                    tokens.remove(x)
                    contexto = contexto.strip()
            t = verificar(tokens,'+','@')#necessario pois quando se usa remove ou pop, se pula alguns elementos na verificação
        for x in tokens:
            desc = desc+' '+x
            desc = desc.strip()
        if desc == '': #solucao encontrada para erro no processar comandos, pra processar o organizar mesmo sem a descricao e so algo valido.
            itens.append(('', ('', '', '', '', '')))
        else:
            pri = pri.upper()
            itens.append((desc, (data, hora, pri, contexto, projeto)))
    i = 0
    while i < len(itens):
        t = 0
        while t < len(itens):
            for x in itens:
                if x == ('',('','','','','')):
                    itens.remove(x)
            t = t+1
        i = i +1
    return itens
def printar(lista, cor):#printar cores e organiza com prioridade na frente pra printar
    for k in lista:
        printa = []
        string = ''
        data = k[1][1][0]
        hora = k[1][1][1]
        contexto = k[1][1][3]
        projeto = k[1][1][4]
        desc = k[1][0]
        pri = k[1][1][2]
        printa.append(str(k[0]))
        printa.append(pri)
        printa.append(data)
        printa.append(hora)
        printa.append(desc)
        printa.append(contexto)
        printa.append(projeto)
        for x in printa:
            string = string.strip() +' '+ x
            string.strip()
        if string != '':
            if cor == 'nenhuma':
                print(string)
            else:
                printCores(string,cor)
    return
def listar():
    fp = open(TODO_FILE, 'r')
    linhas = fp.readlines()
    fp.close()
    itens = organizar(linhas)
    itens = ordenarPorDataHora(itens)
    itens = ordenarPorPrioridade(itens)
    organizado = []
    organizadonum = []
    pria = []
    prib = []
    pric = []
    prid = []
    nopri = []
    for x in itens:
        data = ''
        hora = ''
        if x[1][0] != '':
            data = x[1][0][0:2]+'/'+x[1][0][2:4]+'/'+x[1][0][4:8]
        if x[1][1] != '':
            hora = x[1][1][0:2]+'h'+x[1][1][2:4]+'m'
        organizado.append((x[0], (data, hora, x[1][2], x[1][3], x[1][4])))
    i = 0
    add = ''
    while i < len(organizado):
        add = [i+1]+[organizado[i]]
        organizadonum.append(add)
        i = i+1
    for x in organizadonum:
        if x[1][1][2] == '(A)':
            pria.append(x)
        elif x[1][1][2] == '(B)':
            prib.append(x)
        elif x[1][1][2] == '(C)':
            pric.append(x)
        elif x[1][1][2] == '(D)':
            prid.append(x)
        else:
            nopri.append(x)
    return printar(pria,RED), printar(prib,BLUE), printar(pric,GREEN), printar(prid,YELLOW), printar(nopri,'nenhuma') #vermelho já tá com negrito no código
def ordenarPorDataHora(itens):
    data = []
    nodata = []
    nodata1 = []
    nohora = []
    for x in itens:
        if x[1][0] == '':
            nodata1.append(x)
        else:
            data.append(x)
    for x in nodata1:
        if x[1][1] == '':
            nohora.append(x)
        else:
            nodata.append(x)
    i = 0
    while i < len(data): #bubble ano
        t = 0
        while t < len(data) -1:
            if (data[t][1][0][4:8] >= data[t+1][1][0][4:8]):
                data[t],data[t+1] = data[t+1],data[t]
            t = t+1
        i = i+1
    i = 0
    while i < len(data): #bubble mes no ano
        t = 0
        while t < len(data) -1:
            if (data[t][1][0][4:8] == data[t+1][1][0][4:8]) and (data[t][1][0][2:4] >= data[t+1][1][0][2:4]):
                data[t],data[t+1] = data[t+1],data[t]
            t = t+1
        i = i+1
    i = 0
    while i < len(data): #bubble dia no mes
        t = 0
        while t < len(data) -1:
            if (data[t][1][0][4:8] == data[t+1][1][0][4:8]) and (data[t][1][0][2:4] == data[t+1][1][0][2:4]) and (data[t][1][0][0:2] >= data[t+1][1][0][0:2]) :
                data[t],data[t+1] = data[t+1],data[t]
            t = t+1
        i = i+1
    i = 0
    while i < len(data): #bubble hora no dia
        t = 0
        while t < len(data) -1:
            if (data[t][1][0][4:8] == data[t+1][1][0][4:8]) and (data[t][1][0][2:4] == data[t+1][1][0][2:4]) and (data[t][1][0][0:2] == data[t+1][1][0][0:2]) and (data[t][1][1][0:2] >= data[t+1][1][1][0:2]):
                data[t],data[t+1] = data[t+1],data[t]
            t = t+1
        i = i+1
    i = 0
    while i < len(data): #bubble minuto na hora
        t = 0
        while t < len(data) -1:
            if (data[t][1][0][4:8] == data[t+1][1][0][4:8]) and (data[t][1][0][2:4] == data[t+1][1][0][2:4]) and (data[t][1][0][0:2] == data[t+1][1][0][0:2]) and (data[t][1][1][0:2] == data[t+1][1][1][0:2]) and (data[t][1][1][2:4] >= data[t+1][1][1][2:4]):
                data[t],data[t+1] = data[t+1],data[t]
            t = t+1
        i = i+1
    i = 0
    while i < len(nodata): #bubble hora
        t = 0
        while t < len(nodata) -1:
            if nodata[t][1][1][0:2] >= nodata[t+1][1][1][0:2]:
                nodata[t],nodata[t+1] = nodata[t+1],nodata[t]
            t = t+1
        i = i+1
    i = 0
    while i < len(nodata): #bubble minuto na hora
        t = 0
        while t < len(nodata) -1:
            if (nodata[t][1][1][0:2] == nodata[t+1][1][1][0:2]) and (nodata[t][1][1][2:4] >= nodata[t+1][1][1][2:4]):
                nodata[t],nodata[t+1] = nodata[t+1],nodata[t]
            t = t+1
        i = i+1
    itens = data+nodata+nohora
    return itens
def ordenarPorPrioridade(itens):
    nopri = []
    compri = []
    for x in itens:
        if x[1][2] == '':
            nopri.append(x)
        else:
            compri.append(x)
    i = 0
    while i < len(compri):
        t = 0
        while t < len(compri) - 1:
            if compri[t][1][2] > compri[t+1][1][2]:
                compri[t], compri[t+1] = compri[t+1], compri[t]
            t = t+1
        i = i +1
    itens = compri+nopri
    return itens
def fazer(num):
    fp = open(TODO_FILE, 'r')
    linhas = fp.readlines()
    fp.close()
    itens = organizar(linhas)
    itens = ordenarPorDataHora(itens)
    itens = ordenarPorPrioridade(itens)
    organizado = []
    if int(num) <= len(itens):
        i = 0
        while i < len(itens):
            add = [i+1]+[itens[i]]
            organizado.append(add)
            i = i+1
        for x in organizado:
            if int(num) == x[0]:
                apagar = x[1]
        procurar = apagar[1][0]
        procurar = procurar.strip()+' '+ apagar[1][1]
        procurar = procurar.strip()+' '+ apagar[1][2]
        procurar = procurar.strip()+' '+ apagar[0]
        procurar = procurar.strip()+' '+ apagar[1][3]
        procurar = procurar.strip()+' '+ apagar[1][4]
        procurar = procurar.strip()
        fp = open(TODO_FILE,'w')
        for x in linhas:
            if x != procurar +"\n":
                fp.write(x)
            else:
                ok = x
        fp.close()
        fp = open(ARCHIVE_FILE, 'a')
        fp.write(ok)
        fp.close()
    else:
        err = IOError
        print("Não foi possível concluir a tarefa, numero invalido")
        print(err)
        return False    
    return
def remover(num):
    fp = open(TODO_FILE, 'r')
    linhas = fp.readlines()
    fp.close()
    itens = organizar(linhas)
    itens = ordenarPorDataHora(itens)
    itens = ordenarPorPrioridade(itens)
    organizado = []
    if int(num) <= len(itens):
        i = 0
        while i < len(itens):
            add = [i+1]+[itens[i]]
            organizado.append(add)
            i = i+1
        for x in organizado:
            if int(num) == x[0]:
                apagar = x[1]
        procurar = apagar[1][0]
        procurar = procurar.strip()+' '+ apagar[1][1]
        procurar = procurar.strip()+' '+ apagar[1][2]
        procurar = procurar.strip()+' '+ apagar[0]
        procurar = procurar.strip()+' '+ apagar[1][3]
        procurar = procurar.strip()+' '+ apagar[1][4]
        procurar = procurar.strip()
        fp = open(TODO_FILE,'w')
        for x in linhas:
            if x != procurar +"\n":
                fp.write(x)
                
    else:
        err = IOError
        print("Não foi possível remover a tarefa, numero invalido")
        print(err)
        return False
def priorizar(num, prioridade):
    fp = open(TODO_FILE, 'r')
    linhas = fp.readlines()
    fp.close()
    itens = organizar(linhas)
    itens = ordenarPorDataHora(itens)
    itens = ordenarPorPrioridade(itens)
    organizado = []
    prio = '('+prioridade+')'
    fp = open(TODO_FILE,'w')
    if int(num) <= len(itens) and (prioridadeValida(prioridade) == True or prioridadeValida(prio) == True):
        i = 0
        if prioridadeValida(prioridade) == True:
            novo = prioridade
        else:
            novo = prio
                            
        while i < len(itens):
            add = [i+1]+[itens[i]]
            organizado.append(add)
            i = i+1
        for x in organizado:
            if int(num) == x[0]:
                apagar = x[1]
        procurar = apagar[1][0]
        procurar = procurar.strip()+' '+ apagar[1][1]
        procurar = procurar.strip()+' '+ apagar[1][2]
        procurar = procurar.strip()+' '+ apagar[0]
        procurar = procurar.strip()+' '+ apagar[1][3]
        procurar = procurar.strip()+' '+ apagar[1][4]
        procurar = procurar.strip()
        mudar = apagar[1][0]
        mudar = mudar.strip()+' '+ apagar[1][1]
        mudar = mudar.strip()+' '+ novo
        mudar = mudar.strip()+' '+ apagar[0]
        mudar = mudar.strip()+' '+ apagar[1][3]
        mudar = mudar.strip()+' '+ apagar[1][4]
        mudar = mudar.strip()
        for x in linhas:
            if x != procurar+"\n":
                fp.write(x)
            else:
                fp.write(mudar+"\n")                    
        fp.close()
    else:
        err = IOError
        print("Não foi possível mudar a prioridade da tarefa, numero invalido")
        print(err)
        return False
    return
def processarComandos(comandos):
  if comandos[1] == ADICIONAR:
    comandos.pop(0)
    comandos.pop(0)
    itemParaAdicionar = organizar([' '.join(comandos)])[0]
    adicionar(itemParaAdicionar[0], itemParaAdicionar[1])
  elif comandos[1] == LISTAR:
      comandos.pop(0)
      comandos.pop(0)
      return listar()
  elif comandos[1] == REMOVER:
      comandos.pop(0)
      comandos.pop(0)
      return remover(comandos[0])
  elif comandos[1] == FAZER:
      comandos.pop(0)
      comandos.pop(0)
      return fazer(comandos[0])
  elif comandos[1] == PRIORIZAR:
      comandos.pop(0)
      comandos.pop(0)
      return priorizar(comandos[0],comandos[1])
  else :
    print("Comando inválido.")
processarComandos(sys.argv)
