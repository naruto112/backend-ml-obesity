Monte um sistema backend em python que utilizando api flask para que receba um payload de dados com os seguintes campos:
- idade "tipo do campo deve ser inteiro"

- sexo_biologico "aqui será aceito: 1 ou 2"
Campo com dominio
1 - Masculino
2 - Feminino


- come_vegetaiis "aqui irá aceitar: 1, 2, 3"
Campo com dominio
1 - raramente
2 - as vezes
3 - sempre



- refeicoes_diariamente "aqui irá aceitar de forma inteiro: 1, 2, 3, 4, 5"
Campo com dominio
1 - uma refeição
2 - duas refeições
3 - três refeições
4 - quatro refeições
5 - mais do que 4 refeições


- come_entre_refeicao "aqui irá aceitar no, somentimes, frequently, always"
Campo com dominio
no - não consome
somentimes - as vezes
frequently - frequentemente
always - sempre


- litro_agua "aqui irá aceiitar; 1, 2, 3 campo apenas numeros inteiros"


- frequencia_semanal_atvidade_fisica "aqui você irá aceitar: 0, 1, 2, 3 e 4"
Campo com dominio
0 - nenhuma
1 - 1-2x na semana
2 - 3-4x na semana
3 - 5x na semana
4 - mais do que 5 na semana


- horas_dispositivo_eletronico "aqui você irá aceitar: 0, 1, 2"
Campo com dominio
0 - 0-2h ao dia
1 - 3-5h ao dia
2 - maior que 5h ao dia

- consome_bebida_alcoolica "aqui irá aceitar no, somentimes, frequently, always"
Campo com dominio
no - não consome
somentimes - as vezes
frequently - frequentemente
always - sempre


- historico_familiar "aqui será aceito: yes ou no"
Campo com dominio
yes - Sim
no - Não

- alimentos_calorico "aqui será aceito: yes ou no"
Campo com dominio
yes - Sim
no - Não

- meio_transporte "aqui será aceito: automobile, motorbike, bike, public_transportation, walking"
Campo com dominio
automobile - Carro
motorbike - moto
bike - bicicleta
public_transportation - transporte publico
walking - a pé

- obesity "esse campo será aceito Insufficient_Weight (abaixo do peso), Normal_Weight (peso normal),
Overweight_Level_I (sobrepeso I), Overweight_Level_II (sobrepeso II), Obesity_Type_I (obesidade I), Obesity_Type_II (obesidade II),
Obesity_Type_III (obesidade III)"
Crie os dominios para esse campo


Pode observar que o payload possui os campos obrigatórios o tipos necessarios e que essa API precisa existir endpoint para que o sistema mostre os dados de dominio dos campos para que o usuário selecione qual seria o campo de sua escolha.

Como podemos ver precisamos salvar esses dados em um banco de dados, com isso crie um docker subindo a imagem do postresql para que tenhamos o banco de dados conectado com a aplicação em backend feita em python com flask. Crie o script para essa criação das tabelas e depois deverá executar esse script para criar a tabela com os dominio dos campos e que cada campo seja uma representação da tabela que será uma tabela de formulario de cadastro de obesidade.

