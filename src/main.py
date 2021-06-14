import time
import random

#Saudação do jogo 
print("\nBem vindo ao jogo de advinhação!\n")

numero_secreto = round(random.random() * 100)

time.sleep(3.0)

#Fã service
print("Não entre em panico!!!\n".upper())

time.sleep(3.0)

print("Trabalhando no gerador de improbabilidade infinita...\n")

time.sleep(3.0)

#Pergunta Lançada
print("Prepare-se...\n")

time.sleep(3.0)

print("Pergunta...\n")

time.sleep(3.0)

print("Qual é a resposta para a vida, o universo e tudo mais?\n")

time.sleep(3.0)

print("Ajustando o gerador de improbabilidade infinita...\n")

time.sleep(3.0)

print("A resposta está entre 0 e 100\n")

time.sleep(1.0)

print("Pense na sua resposta... O tempo está acabando...\n")

#Timer
contagem = 6
for i in range(5):
    contagem = contagem - 1
    print(contagem, end="...\n")
    time.sleep(1.0)

chute = 0

tentativa_bonus = 0

#Loop do jogo
tentativas = 0
while chute != numero_secreto:

    time.sleep(2.0)

    chute = int(input("Digite o seu número: \n"))

    tentativas = tentativas + 1

    print("Seu chute é {}. \n".format(chute))

    if chute == 42 and chute == numero_secreto:
        print("Resposta correta!\n")
        break
    
    #Mais fã service
    elif chute == 42 and chute != numero_secreto:
        time.sleep(2)
        print("Você errou! :(\n")
        time.sleep(2)
        print("""42 já foi a resposta um dia.\n
Tente acertar a nova resposta do gerador de improbabilidade infinita. \n""")
        time.sleep(3)
        print("""Porém, você ganhou um bônus de mochileiro das galáxias.\n
Essa tentativa não será computada.\n""")
        time.sleep(2)
        print("Tente novamente...\n")
        time.sleep(2)
        tentativa_bonus = tentativa_bonus + 1
        if chute > numero_secreto:
            time.sleep(1.0)
            print("A resposta é um número menor que {}.\n".format(chute))
        else:
            time.sleep(1.0)
            print("A resposta é um número maior que {}.\n".format(chute))  
        tentativas = tentativas - 1

    elif chute != 42 and chute == numero_secreto:
        print("Resposta correta!\n")
        break
    
    else:
        print("Você errou! :(\n")
        if chute > numero_secreto:
            time.sleep(1.0)
            print("A resposta é um número menor que {}.\n".format(chute))
        else:
            time.sleep(1.0)
            print("A resposta é um número maior que {}.\n".format(chute))      
    
    
#Fim de jogo. Resultado
print("Fim de jogo.\n")
print(f"""Você acertou a resposta para a vida o univero e tudo mais
do gerador de improbabilidade infinita em {tentativas} tentativas.
""")
if tentativa_bonus > 0:
    tentativa_bonus = 1
    print(f"Você teve {tentativa_bonus} tentativa bônus de mochileiro das galáxias.\n")
