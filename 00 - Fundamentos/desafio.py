import textwrap

def menu():
    menu = """\n
    ================ MENU ================
    [d] Depositar
    [s] Sacar
    [e] Extrato
    [nu] Novo usuário
    [nc] Nova conta
    [l] Listar contas
    [q] Sair
    => """
    return input(textwrap.dedent(menu))

def depositar(valor, saldo, extrato, mensagem, /):
    if valor > 0:
        saldo += valor
        extrato += f"Depósito: R$ {valor:.2f}\n"
        mensagem = "=== Depósito realizado com sucesso! ==="
    else:
        mensagem = "\n@@@ Operação falhou! O valor informado é inválido. @@@"

    return saldo, extrato, mensagem

def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques, mensagem):
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques

    if excedeu_saldo:
        mensagem = "@@@ Operação falhou! Você não tem saldo suficiente. @@@"

    elif excedeu_limite:
        mensagem = "@@@ Operação falhou! O valor do saque excede o limite. @@@"

    elif excedeu_saques:
        mensagem = "@@@ Operação falhou! Número máximo de saques excedido. @@@"

    elif valor > 0:
        saldo -= valor
        extrato += f"Saque: R$ {valor:.2f}\n"
        numero_saques += 1
        mensagem = "=== Saque realizado com sucesso! ==="

    else:
        mensagem = "@@@ Operação falhou! O valor informado é inválido. @@@"

    return saldo, extrato, mensagem

def exibir_extrato(saldo, /, *, extrato):
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo: R$ {saldo:.2f}")
    print("==========================================")     

def cadastrar_usuario(usuarios):
    cpf = input("CPF (somente números): ")
    usuario = filtrar_usuario(cpf, usuarios)
    
    if usuario:
        return "@@@ Usuário com esse CPF já cadastrado. @@@"

    nome = input("Nome completo: ")
    data_nascimento = input("Data de nascimento (dd-mm-aaaa): ")
    endereco = input("Endereço (logradouro, número - bairro - cidade/sigla estado): ")

    usuarios.append({
        "nome": nome,
        "data_nascimento": data_nascimento,
        "cpf": cpf,
        "endereco": endereco
    })
    return "=== Usuário cadastrado com sucesso! ==="

def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None

def criar_conta(agencia, numero_conta, usuarios, contas):
    cpf = input("CPF do usuário: ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        for conta in contas:
            if conta["numero_conta"] == numero_conta:
                return "@@@ Já existe uma conta com esse número. @@@"
        contas.append({
            "agencia": agencia,
            "numero_conta": numero_conta,
            "usuario": usuario
        })
        return "=== Conta criada com sucesso! ==="
    else:
        return "@@@ Usuário não encontrado, fluxo de criação de conta encerrado. @@@"

def listar_contas(contas):
    for conta in contas:
        linha = f"""\
            Agência:\t{conta['agencia']}
            C/C:\t\t{conta['numero_conta']}
            Titular:\t{conta['usuario']['nome']}
        """
        print("=" * 100)
        print(textwrap.dedent(linha))

def main():
    LIMITE_SAQUES = 3
    AGENCIA = "0001"

    saldo = 0
    limite = 500
    extrato = ""
    mensagem = ""
    numero_saques = 0
    usuarios = []
    contas = []
    
    while True:   
        opcao = menu()

        if opcao == "d":
            valor = float(input("Informe o valor do depósito: "))
            saldo, extrato, mensagem = depositar(valor, saldo, extrato, mensagem)
            if mensagem:
                print(f"\n {mensagem} ")

        elif opcao == "s":
            valor = float(input("Informe o valor do saque: "))
            saldo, extrato, mensagem = sacar(
                valor =valor, 
                saldo=saldo, 
                limite=limite, 
                extrato=extrato, 
                numero_saques=numero_saques, 
                limite_saques=LIMITE_SAQUES,
                mensagem=mensagem)
            if mensagem:
                print(f"\n {mensagem} ")

        elif opcao == "e":
            exibir_extrato(saldo, extrato=extrato)

        elif opcao == "nu":
            mensagem = cadastrar_usuario(usuarios)
            if mensagem:
                print(f"\n {mensagem} ")

        elif opcao == "nc":
            numero_conta = len(contas) + 1
            mensagem = criar_conta(AGENCIA, numero_conta, usuarios, contas)
            if mensagem:
                print(f"\n {mensagem} ")

        elif opcao == "l":
            for conta in contas:
                usuario = conta["usuario"]
                print(f"Agência: {conta['agencia']} | Conta: {conta['numero_conta']} | Titular: {usuario['nome']}")

        elif opcao == "q":
            break

        else:
            print("\n@@@ Operação inválida, por favor selecione novamente a operação desejada. @@@")

main()