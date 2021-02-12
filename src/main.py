import time

print("\nBem vindo ao jogo de advinhação!\n")

numero_secreto = 42

time.sleep(3.0)

print("Pergunta...\n")

time.sleep(3.0)

print("Prepare-se...\n")

time.sleep(3.0)

print("Qual é a resposta para a vida o universo e tudo mais?\n")

time.sleep(2.0)

print("Pense na sua resposta...\n")

contagem = 6
for i in range(5):
    contagem = contagem - 1
    print(contagem, end="...\n")
    time.sleep(1.0)

chute = 0

while chute != numero_secreto:
    time.sleep(2.0)
    chute = int(input("Digite o seu número: \n"))

    print("Seu chute é {}. \n".format(chute))

    if chute == 42:
        print("Resposta correta!\n")
    else:
        print("Você errou! :(\n")
        if chute > numero_secreto:
            time.sleep(1.0)
            print("A resposta é um número menor que {}.\n".format(chute))
        else:
            time.sleep(1.0)
            print("A resposta é um número maior que {}.\n".format(chute))      

print("Fim de jogo.\n")