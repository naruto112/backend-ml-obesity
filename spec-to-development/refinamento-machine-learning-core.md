Olhe para o código do repositório C:\Users\renat\OneDrive\Área de Trabalho\TC\FASE4\notebook-ml-obesidade\model.ipynb

e vamos implementar nesse projeto C:\Users\renat\OneDrive\Área de Trabalho\TC\FASE4\backend a função que quando eu chamar a rota /api/v1/obesity-records do metodo post ele irá receber o payload que essa api irá receber porém esses dados deverão passar por uma camada de serviço de função que está no projeto notebook-ml-obesidade\model.ipynb e irá acionar uma camada de modelo que se encontra nesse projeto pronto e irá retornar o resultado do campo obesity e a camada de serviço irá saber se com os inputs de entrada o modelo irá predizer se a pessoa é Insufficient_Weight, Normal_Weight, Overweight_Level_I, Overweight_Level_II, Obesity_Type_I, Obesity_Type_II, Obesity_Type_III e será salvo no banco de dados do backend que possui um postgresql. Quando eu chamar a api /api/v1/obesity-records/{record_id} irei ver o resultado dos campos recebemos por um input do POST mais o resultado do modelo gravando no campo já mencionado.

lembre-se de usar o modelo hgb.joblib que foi gerado pelo arquivo model.ipynb após a analise exploratório e entendimento do arquivo Obesity.csv que eles se encontram C:\Users\renat\OneDrive\Área de Trabalho\TC\FASE4\notebook-ml-obesidade

Existe um projeto que fez algo parecido deixo aqui embaixo de referencia:
novo_cliente = [0, # ID_Cliente
                    input_carro_proprio, # Tem_carro
                    input_casa_propria, # Tem_Casa_Propria
                    telefone_trabalho, # Tem_telefone_trabalho
                    telefone, # Tem_telefone_fixo
                    email,  # Tem_email
                    membros_familia,  # Tamanho_Familia
                    input_rendimentos, # Rendimento_anual	
                    input_idade, # Idade
                    input_tempo_experiencia, # Anos_empregado
                    input_categoria_renda, # Categoria_de_renda
                    input_grau_escolaridade, # Grau_Escolaridade
                    input_estado_civil, # Estado_Civil	
                    input_tipo_moradia, # Moradia                                                  
                    input_ocupacao, # Ocupacao
                     0 # target (Mau)
                    ]


# Separando os dados em treino e teste
def data_split(df, test_size):
    SEED = 1561651
    treino_df, teste_df = train_test_split(df, test_size=test_size, random_state=SEED)
    return treino_df.reset_index(drop=True), teste_df.reset_index(drop=True)

treino_df, teste_df = data_split(dados, 0.2)

#Criando novo cliente
cliente_predict_df = pd.DataFrame([novo_cliente],columns=teste_df.columns)

#Concatenando novo cliente ao dataframe dos dados de teste
teste_novo_cliente  = pd.concat([teste_df,cliente_predict_df],ignore_index=True)

#Pipeline
def pipeline_teste(df):

    pipeline = Pipeline([
        ('feature_dropper', DropFeatures()),
        ('OneHotEncoding', OneHotEncodingNames()),
        ('ordinal_feature', OrdinalFeature()),
        ('min_max_scaler', MinMaxWithFeatNames()),
    ])
    df_pipeline = pipeline.fit_transform(df)
    return df_pipeline

#Aplicando a pipeline
teste_novo_cliente = pipeline_teste(teste_novo_cliente)

#retirando a coluna target
cliente_pred = teste_novo_cliente.drop(['Mau'], axis=1)

#Predições 
if st.button('Enviar'):
    model = joblib.load('modelo/xgb.joblib')
    final_pred = model.predict(cliente_pred)
    predicao_cliente = final_pred[-1]
    proba_cliente = None

    if hasattr(model, 'predict_proba'):
        proba_cliente = model.predict_proba(cliente_pred)[-1]

    logger.info('final_pred completo: %s', final_pred)
    logger.info('predicao_cliente: %s | tipo: %s', predicao_cliente, type(predicao_cliente))
    logger.info('proba_cliente: %s', proba_cliente)
    print(f'final_pred completo: {final_pred}', flush=True)
    print(f'predicao_cliente: {predicao_cliente} | tipo: {type(predicao_cliente)}', flush=True)
    print(f'proba_cliente: {proba_cliente}', flush=True)

    if predicao_cliente == 0:
        st.success('### Parabéns! Você teve o cartão de crédito aprovado')
        st.balloons()
    else:
        st.error('### Infelizmente, não podemos liberar crédito para você agora!')