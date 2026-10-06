# Definição do Dataset

Este documento descreve a estrutura do dataset sintético utilizado no desenvolvimento do sistema de prevenção e detecção de fraudes em serviços bancários digitais. Os dados são simulados para fins académicos e não correspondem a dados reais do ABSA Bank Mozambique.

## Campos do Dataset

### 1. transaction_id

- **Descrição:** Identificador único atribuído a cada transacção.
- **Tipo de dado:** String
- **Exemplo:** TX000001
- **Origem:** Gerado automaticamente pelo sistema.
- **Uso no Machine Learning:** Não.

### 2. customer_id

- **Descrição:** Identificador único do cliente responsável pela transacção.
- **Tipo de dado:** String
- **Exemplo:** C0001
- **Origem:** Gerado automaticamente no dataset sintético.
- **Uso no Machine Learning:** Não directamente. É utilizado para construir características relacionadas com o comportamento histórico do cliente.

### 3. amount

- **Descrição:** Valor monetário da transacção realizada pelo cliente.
- **Tipo de dado:** Float
- **Unidade:** Metical (MT)
- **Exemplo:** 2500.00
- **Origem:** Gerado de forma sintética com base no perfil de transacções do cliente.
- **Uso no Machine Learning:** Sim. O valor da transacção pode contribuir para a identificação de comportamentos financeiros anómalos, sobretudo quando analisado em relação ao histórico do cliente.

### 4. timestamp

- **Descrição:** Data e hora em que a transacção foi realizada.
- **Tipo de dado:** DateTime
- **Exemplo:** 2026-08-15 14:32:18
- **Origem:** Gerado de forma sintética de acordo com os padrões temporais definidos para as transacções.
- **Uso no Machine Learning:** Não directamente. A partir deste campo poderão ser extraídas características temporais, como a hora da transacção, para análise de possíveis comportamentos anómalos.

### 5. beneficiary_new

- **Descrição:** Indica se o beneficiário da transacção é novo para o cliente.
- **Tipo de dado:** Booleano/Binário
- **Valores:** 0 = beneficiário conhecido; 1 = beneficiário novo.
- **Exemplo:** 1
- **Origem:** Determinado a partir do histórico sintético de beneficiários associados ao cliente.
- **Uso no Machine Learning:** Sim. Pode contribuir para a identificação de alterações no comportamento habitual do cliente, especialmente quando combinado com outros indicadores de risco.

### 6. device_new

- **Descrição:** Indica se a transacção foi realizada através de um dispositivo ainda não associado ao histórico do cliente.
- **Tipo de dado:** Booleano/Binário
- **Valores:** 0 = dispositivo conhecido; 1 = dispositivo novo.
- **Exemplo:** 1
- **Origem:** Determinado a partir do histórico sintético de dispositivos utilizados pelo cliente.
- **Uso no Machine Learning:** Sim. Pode contribuir para a identificação de alterações no padrão habitual de acesso do cliente, especialmente quando combinado com outros indicadores de risco.

### 7. ip_anomaly

- **Descrição:** Indica se o contexto do endereço IP associado à transacção apresenta um comportamento diferente do padrão habitual simulado para o cliente.
- **Tipo de dado:** Booleano/Binário
- **Valores:** 0 = contexto de IP habitual; 1 = contexto de IP anómalo.
- **Exemplo:** 1
- **Origem:** Gerado de forma sintética com base no perfil de acesso atribuído ao cliente.
- **Uso no Machine Learning:** Sim. Pode contribuir para a identificação de alterações no contexto habitual de acesso, devendo ser analisado em conjunto com outras características da transacção.

### 8. location_anomaly

- **Descrição:** Indica se o contexto geográfico associado à transacção apresenta uma alteração em relação ao padrão habitual simulado para o cliente.
- **Tipo de dado:** Booleano/Binário
- **Valores:** 0 = localização habitual; 1 = localização anómala.
- **Exemplo:** 1
- **Origem:** Gerado de forma sintética com base no perfil de localização atribuído ao cliente.
- **Uso no Machine Learning:** Sim. Pode contribuir para a identificação de alterações no contexto habitual das transacções, especialmente quando combinado com outros indicadores de risco.

### 9. transactions_last_10m

- **Descrição:** Número de transacções realizadas pelo cliente nos 10 minutos anteriores à transacção actual.
- **Tipo de dado:** Inteiro
- **Exemplo:** 5
- **Origem:** Calculado a partir do histórico temporal das transacções sintéticas do cliente.
- **Uso no Machine Learning:** Sim. Permite representar a frequência recente de transacções e pode contribuir para a identificação de sequências anormalmente rápidas de operações.

### 10. customer_avg_amount

- **Descrição:** Valor médio das transacções anteriores realizadas pelo cliente.
- **Tipo de dado:** Float
- **Unidade:** Metical (MT)
- **Exemplo:** 2000.00
- **Origem:** Calculado a partir do histórico de transacções sintéticas anteriores do cliente.
- **Uso no Machine Learning:** Sim. Permite representar o comportamento financeiro habitual do cliente e comparar o valor da transacção actual com o seu histórico.

### 11. amount_ratio

- **Descrição:** Relação entre o valor da transacção actual e o valor médio das transacções anteriores do cliente.
- **Tipo de dado:** Float
- **Fórmula:** amount / customer_avg_amount
- **Exemplo:** 20.0
- **Origem:** Calculado a partir dos campos amount e customer_avg_amount.
- **Uso no Machine Learning:** Sim. Permite medir o quanto o valor da transacção actual se desvia, em termos relativos, do comportamento financeiro habitual do cliente.

### 12. customer_tx_count_24h

- **Descrição:** Número de transacções realizadas pelo cliente nas 24 horas anteriores à transacção actual.
- **Tipo de dado:** Inteiro
- **Exemplo:** 14
- **Origem:** Calculado a partir do histórico temporal das transacções sintéticas do cliente.
- **Uso no Machine Learning:** Sim. Permite representar a intensidade recente da actividade transaccional do cliente e pode contribuir para a identificação de alterações no seu padrão habitual.

### 13. beneficiary_tx_count

- **Descrição:** Número de transacções anteriores realizadas pelo cliente para o beneficiário associado à transacção actual.
- **Tipo de dado:** Inteiro
- **Exemplo:** 8
- **Origem:** Calculado a partir do histórico de transacções sintéticas entre o cliente e o beneficiário.
- **Uso no Machine Learning:** Sim. Permite representar a relação histórica entre o cliente e o beneficiário, contribuindo para distinguir beneficiários frequentes de beneficiários pouco utilizados ou novos.

### 14. hour

- **Descrição:** Hora do dia em que a transacção foi realizada, extraída do timestamp.
- **Tipo de dado:** Inteiro
- **Intervalo:** 0 a 23
- **Exemplo:** 3
- **Origem:** Extraído do campo timestamp.
- **Uso no Machine Learning:** Sim. Permite representar padrões temporais das transacções e pode contribuir para a identificação de operações realizadas em horários menos habituais.

### 15. fraud_label

- **Descrição:** Indica a classe atribuída à transacção, distinguindo operações legítimas de operações fraudulentas no dataset sintético.
- **Tipo de dado:** Booleano/Binário
- **Valores:** 0 = transacção legítima; 1 = transacção fraudulenta.
- **Exemplo:** 1
- **Origem:** Atribuído durante o processo controlado de geração dos dados sintéticos, de acordo com os cenários de fraude definidos para o protótipo.
- **Uso no Machine Learning:** Sim, como variável alvo (target). É a classe que os modelos de Machine Learning serão treinados para prever.


## Perfis Sintéticos de Clientes

Para tornar o dataset mais próximo de um cenário comportamental realista, cada cliente sintético possuirá um perfil próprio de utilização dos serviços bancários digitais. As transacções legítimas serão geradas considerando esse perfil, evitando que todos os clientes apresentem exactamente o mesmo comportamento.

Cada perfil poderá incluir características como:

- valor médio habitual das transacções;
- variação dos valores transferidos;
- frequência habitual de transacções;
- conjunto de beneficiários frequentes;
- dispositivos habitualmente utilizados;
- padrões de horário das transacções;
- contexto habitual de localização e acesso.

Os perfis são inteiramente sintéticos e foram definidos exclusivamente para fins de desenvolvimento e avaliação do protótipo, não representando perfis reais de clientes do ABSA Bank Mozambique.

### Escala inicial de desenvolvimento

Durante a fase inicial de desenvolvimento, serão utilizados 100 clientes sintéticos. Esta quantidade será utilizada para validar a lógica de geração dos perfis e das transacções antes da produção do dataset experimental completo.

A dimensão final do dataset será definida posteriormente, após a validação do gerador e análise da distribuição das transacções legítimas e fraudulentas.

### Perfis de movimentação financeira

Para introduzir diversidade comportamental no dataset sintético, os clientes serão inicialmente distribuídos em três perfis de movimentação financeira:

- **Baixa movimentação:** 50 clientes, com valor médio habitual de transacções entre 500 e 5.000 MT.
- **Média movimentação:** 35 clientes, com valor médio habitual de transacções entre 5.000 e 25.000 MT.
- **Alta movimentação:** 15 clientes, com valor médio habitual de transacções entre 25.000 e 100.000 MT.

Estes intervalos constituem parâmetros de simulação definidos para o protótipo e não representam limites ou segmentos oficiais utilizados pelo ABSA Bank Mozambique.

O valor médio específico será atribuído individualmente a cada cliente dentro do intervalo correspondente ao seu perfil. Desta forma, a análise de valores anómalos poderá considerar o comportamento individual do cliente, em vez de assumir que transacções de elevado valor são necessariamente fraudulentas.

### Frequência habitual de transacções

Os clientes sintéticos apresentarão diferentes níveis de frequência transaccional, permitindo representar comportamentos de utilização distintos.

Para a fase inicial de desenvolvimento serão considerados os seguintes níveis:

- **Baixa frequência:** aproximadamente 1 a 3 transacções por semana.
- **Média frequência:** aproximadamente 4 a 10 transacções por semana.
- **Alta frequência:** aproximadamente 11 a 25 transacções por semana.

A frequência será atribuída aos clientes com variação individual e não será determinada exclusivamente pelo perfil de movimentação financeira. Desta forma, um cliente que realiza transacções de valores elevados não terá necessariamente uma elevada quantidade de transacções.

Estes valores constituem parâmetros de simulação definidos para o protótipo e não representam padrões oficiais de clientes do ABSA Bank Mozambique.

### Beneficiários habituais

Cada cliente sintético possuirá um conjunto de beneficiários habituais, utilizado para representar relações transaccionais recorrentes.

Durante a fase inicial, cada cliente terá entre 2 e 8 beneficiários habituais. As transacções legítimas serão realizadas predominantemente para estes beneficiários, embora possam ocorrer ocasionalmente transacções legítimas para novos beneficiários.

O histórico entre cliente e beneficiário será utilizado para calcular características como beneficiary_new e beneficiary_tx_count.

Os beneficiários e as relações entre estes e os clientes são inteiramente sintéticos e não representam clientes ou contas reais do ABSA Bank Mozambique.

### Padrões de horário das transacções

As transacções sintéticas serão geradas considerando diferentes padrões temporais de utilização dos serviços bancários digitais.

A maior parte das transacções legítimas será gerada entre as 06h00 e as 23h00, período considerado como a janela principal de actividade para efeitos da simulação. No entanto, também poderão ocorrer transacções legítimas entre as 23h00 e as 06h00, em menor frequência.

Desta forma, o horário da transacção não será utilizado isoladamente para determinar a existência de fraude. Operações realizadas em horários menos frequentes constituirão apenas um possível indicador comportamental quando analisadas em conjunto com outras características.

Estes padrões constituem parâmetros de simulação definidos para o protótipo e não representam horários ou critérios oficiais utilizados pelo ABSA Bank Mozambique.

### Perfil de dispositivo e contexto de acesso

Cada cliente sintético possuirá um perfil habitual de acesso aos serviços bancários digitais, utilizado como referência para a geração das transacções.

O perfil incluirá dispositivos habitualmente utilizados e contextos simulados de acesso e localização. A maioria das transacções legítimas será realizada dentro do padrão habitual do cliente. No entanto, poderão ocorrer ocasionalmente alterações legítimas, como a utilização de um novo dispositivo, um contexto de IP diferente ou uma localização diferente da habitual.

Estas alterações não serão consideradas fraude de forma automática. Serão tratadas como características comportamentais que poderão contribuir para a avaliação do risco quando combinadas com outros indicadores.

Este mecanismo será utilizado na geração das características device_new, ip_anomaly e location_anomaly. Todos os perfis e contextos utilizados são sintéticos e não representam dados ou mecanismos internos do ABSA Bank Mozambique.

## Geração das Transacções Legítimas

As transacções legítimas serão geradas de acordo com os perfis individuais atribuídos aos clientes.

O processo de geração deverá considerar:

- valor médio habitual do cliente;
- variação normal dos valores;
- frequência de utilização;
- beneficiários conhecidos;
- horário habitual;
- dispositivos conhecidos;
- contexto habitual de acesso e localização.

Será introduzida alguma variação nos comportamentos legítimos para evitar que o dataset apresente padrões excessivamente previsíveis.

Por exemplo, uma transacção legítima poderá ocasionalmente:

- apresentar valor superior à média;
- utilizar um beneficiário novo;
- utilizar um dispositivo novo;
- ocorrer durante a madrugada;
- apresentar contexto de localização diferente.

Assim, nenhum indicador isolado deverá representar automaticamente uma fraude.

---

## Cenários Sintéticos de Fraude

As transacções fraudulentas serão introduzidas de forma controlada no dataset através de diferentes cenários de comportamento anómalo.

### Valor anormalmente elevado

Neste cenário, o valor da transacção será significativamente superior ao comportamento financeiro habitual do cliente.

Exemplo:

- média habitual do cliente: 2.000 MT;
- transacção simulada: 40.000 MT;
- amount_ratio: 20.

O valor elevado não será utilizado isoladamente para determinar fraude.

### Transferência para beneficiário novo

Neste cenário, será simulada uma transferência para um beneficiário ainda não existente no histórico do cliente.

Características possíveis:

- beneficiary_new = 1;
- beneficiary_tx_count = 0.

Este comportamento poderá ser combinado com outros indicadores de risco.

### Utilização de dispositivo novo

Será simulada a utilização de um dispositivo diferente dos habitualmente associados ao cliente.

Característica principal:

- device_new = 1.

A presença de um dispositivo novo, isoladamente, não será suficiente para determinar fraude.

### Contexto de acesso anómalo

Este cenário poderá apresentar alterações relacionadas com:

- IP;
- localização;
- dispositivo.

Exemplo:

- device_new = 1;
- ip_anomaly = 1;
- location_anomaly = 1.

O objectivo será representar alterações significativas no contexto habitual de acesso.

### Transacção em horário anómalo

Neste cenário serão geradas transacções em períodos pouco habituais para determinado perfil de cliente.

Por exemplo:

- comportamento normal: operações predominantemente durante o dia;
- transacção simulada: 02h30.

O horário será combinado com outras características, evitando uma associação automática entre madrugada e fraude.

### Rajada de transferências

Será simulado um cenário em que várias transacções são realizadas num intervalo de tempo reduzido.

Este comportamento poderá provocar valores elevados em:

- transactions_last_10m;
- customer_tx_count_24h.

O objectivo será representar situações em que várias transferências são realizadas rapidamente.

### Simulação de comprometimento da conta

Um cenário mais complexo poderá representar uma situação de possível comprometimento de uma conta.

Uma transacção poderá combinar vários sinais, por exemplo:

- valor muito acima da média;
- dispositivo novo;
- beneficiário novo;
- contexto de IP anómalo;
- localização anómala;
- horário pouco habitual;
- várias transacções num período reduzido.

---

## Níveis de Dificuldade dos Casos de Fraude

Para evitar que todas as fraudes sejam facilmente identificáveis, serão introduzidos diferentes níveis de dificuldade.

### Fraudes fáceis

Apresentam vários indicadores de anomalia simultaneamente.

### Fraudes moderadas

Apresentam alguns indicadores de risco, mantendo parte do comportamento normal do cliente.

### Fraudes difíceis

Apresentam comportamento semelhante a uma transacção legítima, possuindo apenas pequenas alterações no padrão habitual.

A inclusão destes níveis pretende reduzir o risco de criação de um dataset excessivamente simples para os algoritmos de Machine Learning.

---

## Atribuição do fraud_label

A variável fraud_label será atribuída durante o processo controlado de geração dos dados.

As transacções geradas através do comportamento normal do cliente receberão:

fraud_label = 0

As operações injectadas através dos cenários sintéticos de fraude receberão:

fraud_label = 1

A atribuição da classe será realizada pelo mecanismo de geração dos dados e não pelo modelo de Machine Learning.

Posteriormente, os modelos utilizarão fraud_label como variável alvo durante o processo de treino supervisionado.

---

## Desequilíbrio entre Transacções Legítimas e Fraudulentas

O dataset não deverá possuir a mesma quantidade de transacções legítimas e fraudulentas.

As transacções fraudulentas deverão constituir uma proporção menor do conjunto total, criando um problema de classificação desequilibrada.

A percentagem exacta de fraude será definida após os primeiros testes do gerador.

Durante a fase de Machine Learning poderão ser analisadas técnicas apropriadas para lidar com o desequilíbrio das classes.

---

## Geração das Características Históricas

Algumas características não serão geradas aleatoriamente, mas calculadas utilizando as transacções anteriores do cliente.

Entre estas encontram-se:

- transactions_last_10m;
- customer_avg_amount;
- amount_ratio;
- customer_tx_count_24h;
- beneficiary_tx_count.

O cálculo destas características deverá utilizar apenas informação disponível antes da transacção analisada.

Não deverão ser utilizadas transacções futuras para calcular características históricas, evitando fuga de informação durante a construção do dataset.

---

## Organização dos Dados

Os ficheiros serão organizados através da seguinte estrutura:

data/
├── raw/
└── processed/

### data/raw

Contém os dados originalmente produzidos pelo gerador sintético antes das etapas de preparação para Machine Learning.

### data/processed

Contém os dados depois das operações de limpeza, transformação, selecção de características e preparação para treino dos modelos.

---

## Reprodutibilidade

O processo de geração dos dados deverá utilizar uma semente aleatória definida no código.

A utilização de uma seed permitirá reproduzir o mesmo dataset quando necessário durante os testes e a avaliação experimental.

Este procedimento facilita:

- comparação entre modelos;
- repetição dos experimentos;
- validação de resultados;
- documentação científica do projecto.

---

## Validação do Dataset

Antes de utilizar o dataset para Machine Learning serão realizadas verificações destinadas a identificar possíveis problemas.

Serão analisados:

- número total de transacções;
- número de clientes;
- percentagem de fraudes;
- existência de valores ausentes;
- duplicação de transaction_id;
- distribuição dos valores monetários;
- distribuição das transacções por hora;
- proporção de beneficiários novos;
- proporção de dispositivos novos;
- distribuição das classes;
- coerência das características históricas.

Também será verificada a existência de padrões artificiais que possam tornar a classificação excessivamente simples.

---

## Limitações dos Dados Sintéticos

A utilização de dados sintéticos permite desenvolver e testar o protótipo sem acesso a dados bancários sensíveis.

No entanto, dados simulados não reproduzem integralmente a complexidade das transacções realizadas em ambientes bancários reais.

Os resultados obtidos durante a avaliação dos modelos deverão, portanto, ser interpretados no contexto experimental do protótipo.

Uma eventual aplicação num ambiente bancário real exigiria validação adicional utilizando dados reais devidamente autorizados, anonimizados e sujeitos aos requisitos de segurança, privacidade e regulamentação aplicáveis.

---

## Relação com o Caso de Estudo

O ABSA Bank Mozambique constitui o caso de estudo do projecto.

Contudo, a estrutura deste dataset não deve ser interpretada como representação da base de dados, arquitectura interna, regras antifraude ou mecanismos actualmente utilizados pelo ABSA Bank Mozambique.

O dataset foi concebido para permitir o desenvolvimento experimental de um protótipo académico de prevenção e detecção de fraude utilizando técnicas de Machine Learning.