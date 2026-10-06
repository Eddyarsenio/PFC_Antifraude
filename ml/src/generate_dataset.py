import random
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

# Semente para tornar a geração dos dados reproduzível
SEED = 42

random.seed(SEED)
np.random.seed(SEED)

# Número inicial de clientes sintéticos
NUM_CUSTOMERS = 100

# Número de dias utilizados na geração inicial das transacções
SIMULATION_DAYS = 7

# Data inicial da simulação
SIMULATION_START = datetime(2026, 1, 1)

# Proporção inicial de transacções fraudulentas sintéticas
FRAUD_RATIO = 0.10

# Gerar identificadores únicos para os clientes
customer_ids = [
    f"C{i:04d}"
    for i in range(1, NUM_CUSTOMERS + 1)
]


# Criar os perfis de movimentação financeira
movement_profiles = (
    ["baixo"] * 50 +
    ["medio"] * 35 +
    ["alto"] * 15
)

# Embaralhar os perfis entre os clientes
random.shuffle(movement_profiles)

# Associar cada cliente ao seu perfil
customers = pd.DataFrame({
    "customer_id": customer_ids,
    "movement_profile": movement_profiles
})

# Gerar o valor médio habitual de transacção de cada cliente
def generate_average_amount(profile):
    if profile == "baixo":
        return round(random.uniform(500, 5000), 2)
    elif profile == "medio":
        return round(random.uniform(5000, 25000), 2)
    else:
        return round(random.uniform(25000, 100000), 2)


customers["avg_amount"] = customers["movement_profile"].apply(
    generate_average_amount
)

# Gerar o perfil de frequência de transacções de cada cliente
def generate_frequency_profile():
    return random.choice(["baixa", "media", "alta"])


customers["frequency_profile"] = [
    generate_frequency_profile()
    for _ in range(NUM_CUSTOMERS)
]

# Gerar o número habitual de transacções por semana
def generate_weekly_transactions(frequency):
    if frequency == "baixa":
        return random.randint(1, 3)
    elif frequency == "media":
        return random.randint(4, 10)
    else:
        return random.randint(11, 25)


customers["weekly_transactions"] = customers["frequency_profile"].apply(
    generate_weekly_transactions
)

# Gerar o número de beneficiários habituais de cada cliente
customers["num_usual_beneficiaries"] = [
    random.randint(2, 8)
    for _ in range(NUM_CUSTOMERS)
]

# Criar os beneficiários habituais de cada cliente
usual_beneficiaries = {}
beneficiary_counter = 1

for _, customer in customers.iterrows():
    customer_beneficiaries = []

    for _ in range(customer["num_usual_beneficiaries"]):
        beneficiary_id = f"B{beneficiary_counter:04d}"
        customer_beneficiaries.append(beneficiary_id)
        beneficiary_counter += 1

    usual_beneficiaries[customer["customer_id"]] = customer_beneficiaries

# Gerar o número de dispositivos habituais de cada cliente
customers["num_usual_devices"] = [
    random.randint(1, 3)
    for _ in range(NUM_CUSTOMERS)
]

# Criar os dispositivos habituais de cada cliente
usual_devices = {}
device_counter = 1

for _, customer in customers.iterrows():
    customer_devices = []

    for _ in range(customer["num_usual_devices"]):
        device_id = f"D{device_counter:04d}"
        customer_devices.append(device_id)
        device_counter += 1

    usual_devices[customer["customer_id"]] = customer_devices

# Lista onde serão armazenadas todas as transacções geradas
transactions = []

transaction_counter = 1

# Determinar quantas transacções cada cliente realizará
for _, customer in customers.iterrows():
    num_transactions = customer["weekly_transactions"]

    for _ in range(num_transactions):
        transaction_id = f"TX{transaction_counter:06d}"
        transaction_counter += 1

        # Gerar um valor de transacção próximo da média habitual do cliente
        amount = np.random.normal(
            loc=customer["avg_amount"],
            scale=customer["avg_amount"] * 0.30
        )

        # Evitar valores negativos ou demasiado pequenos
        amount = max(50, amount)

        # Arredondar para duas casas decimais
        amount = round(amount, 2)

                # Escolher aleatoriamente um dos 7 dias da simulação
        transaction_day = random.randint(0, SIMULATION_DAYS - 1)

        # Gerar a hora da transacção
        # A maioria ocorre entre 06h00 e 23h00
        if random.random() < 0.90:
            transaction_hour = random.randint(6, 22)
        else:
            transaction_hour = random.choice([23, 0, 1, 2, 3, 4, 5])

        minute = random.randint(0, 59)
        second = random.randint(0, 59)

        timestamp = (
            SIMULATION_START
            + timedelta(days=transaction_day)
            + timedelta(
                hours=transaction_hour,
                minutes=minute,
                seconds=second
            )
        )

                # Escolher o beneficiário da transacção
        customer_id = customer["customer_id"]

        if random.random() < 0.90:
            # 90% das transacções legítimas vão para beneficiários habituais
            beneficiary_id = random.choice(
                usual_beneficiaries[customer_id]
            )
            beneficiary_new = 0
        else:
            # 10% podem envolver um beneficiário novo
            beneficiary_id = f"NEW_B{transaction_counter:06d}"
            beneficiary_new = 1

                # Escolher o dispositivo utilizado na transacção
        if random.random() < 0.95:
            # 95% das transacções legítimas usam um dispositivo habitual
            device_id = random.choice(
                usual_devices[customer_id]
            )
            device_new = 0
        else:
            # 5% podem ser realizadas através de um dispositivo novo
            device_id = f"NEW_D{transaction_counter:06d}"
            device_new = 1
                # Gerar possíveis alterações legítimas no contexto de acesso
        ip_anomaly = 1 if random.random() < 0.03 else 0
        location_anomaly = 1 if random.random() < 0.03 else 0

                # Adicionar a transacção à lista
        transactions.append({
            "transaction_id": transaction_id,
            "customer_id": customer_id,
            "amount": amount,
            "timestamp": timestamp,
            "beneficiary_id": beneficiary_id,
            "beneficiary_new": beneficiary_new,
            "device_id": device_id,
            "device_new": device_new,
            "ip_anomaly": ip_anomaly,
            "location_anomaly": location_anomaly,
            "fraud_scenario": "legitimate",
            "fraud_difficulty": "none",
            "fraud_label": 0
        })
# Converter a lista de transacções numa tabela
transactions_df = pd.DataFrame(transactions)

# Calcular o número de transacções fraudulentas a gerar
num_fraud_transactions = round(
    len(transactions_df) * FRAUD_RATIO
)

print(
    "\nNúmero de transacções fraudulentas a gerar:",
    num_fraud_transactions
)

# Lista onde serão armazenadas as transacções fraudulentas
fraud_transactions = []

# Tipos de cenários fraudulentos utilizados na simulação
fraud_scenarios = [
    "abnormal_amount",
    "new_beneficiary",
    "new_device",
    "anomalous_context",
    "anomalous_hour",
    "transfer_burst",
    "account_takeover"
]

# Gerar a estrutura inicial das transacções fraudulentas
for _ in range(num_fraud_transactions):

    # Escolher aleatoriamente um cliente
    customer = customers.sample(n=1).iloc[0]
    customer_id = customer["customer_id"]

    # Escolher aleatoriamente um cenário de fraude
    fraud_scenario = random.choice(fraud_scenarios)

    # Definir o nível de dificuldade da fraude
    fraud_difficulty = random.choice([
    "easy",
    "moderate",
    "hard"
    ])

    # Criar um identificador único para a transacção fraudulenta
    transaction_id = f"TX{transaction_counter:06d}"
    transaction_counter += 1

    # Escolher um dia dentro do período da simulação
    transaction_day = random.randint(0, SIMULATION_DAYS - 1)

    # Gerar inicialmente uma hora qualquer
    transaction_hour = random.randint(0, 23)
    minute = random.randint(0, 59)
    second = random.randint(0, 59)

    timestamp = (
        SIMULATION_START
        + timedelta(days=transaction_day)
        + timedelta(
            hours=transaction_hour,
            minutes=minute,
            seconds=second
        )
    )
        # Definir inicialmente valores semelhantes a uma transacção normal
    amount = np.random.normal(
        loc=customer["avg_amount"],
        scale=customer["avg_amount"] * 0.30
    )

    amount = max(50, amount)
    amount = round(amount, 2)

    # Utilizar inicialmente um beneficiário habitual
    beneficiary_id = random.choice(
        usual_beneficiaries[customer_id]
    )
    beneficiary_new = 0

    # Utilizar inicialmente um dispositivo habitual
    device_id = random.choice(
        usual_devices[customer_id]
    )
    device_new = 0

    # Inicialmente não existem anomalias de contexto
    ip_anomaly = 0
    location_anomaly = 0

        # Cenário 1: valor da transacção anormalmente elevado
    if fraud_scenario == "abnormal_amount":
        amount = customer["avg_amount"] * random.uniform(3.0, 7.0)
        amount = round(amount, 2)

            # Cenário 2: transferência para um beneficiário novo
    elif fraud_scenario == "new_beneficiary":
        beneficiary_id = f"FRAUD_B{transaction_counter:06d}"
        beneficiary_new = 1

            # Cenário 3: utilização de um dispositivo novo
    elif fraud_scenario == "new_device":
        device_id = f"FRAUD_D{transaction_counter:06d}"
        device_new = 1

            # Cenário 4: contexto de acesso anómalo
    elif fraud_scenario == "anomalous_context":
        ip_anomaly = 1
        location_anomaly = 1

            # Cenário 5: transacção realizada num horário anómalo
    elif fraud_scenario == "anomalous_hour":
        transaction_hour = random.choice([0, 1, 2, 3, 4, 5])

        timestamp = (
            SIMULATION_START
            + timedelta(days=transaction_day)
            + timedelta(
                hours=transaction_hour,
                minutes=minute,
                seconds=second
            )
        )

                # Cenário 6: várias transferências num curto intervalo de tempo
    elif fraud_scenario == "transfer_burst":
        beneficiary_id = f"FRAUD_B{transaction_counter:06d}"
        beneficiary_new = 1

        # Obter as transacções legítimas já existentes deste cliente
        customer_history = transactions_df[
            transactions_df["customer_id"] == customer_id
        ]

        # Escolher uma transacção anterior como referência
        reference_transaction = customer_history.sample(n=1).iloc[0]

        # Criar a fraude entre 1 e 5 minutos depois
        timestamp = (
            reference_transaction["timestamp"]
            + timedelta(minutes=random.randint(1, 5))
        )

            # Cenário 7: comprometimento da conta
    elif fraud_scenario == "account_takeover":
        beneficiary_id = f"FRAUD_B{transaction_counter:06d}"
        beneficiary_new = 1

        device_id = f"FRAUD_D{transaction_counter:06d}"
        device_new = 1

        ip_anomaly = 1
        location_anomaly = 1

        # Ajustar os sinais de acordo com a dificuldade da fraude
    if fraud_difficulty == "easy":
        # Fraudes fáceis apresentam vários sinais anómalos simultaneamente
        beneficiary_id = f"FRAUD_B{transaction_counter:06d}"
        beneficiary_new = 1

        device_id = f"FRAUD_D{transaction_counter:06d}"
        device_new = 1

        ip_anomaly = 1
        location_anomaly = 1

    elif fraud_difficulty == "moderate":
        # Fraudes moderadas apresentam apenas alguns sinais anómalos
        if random.random() < 0.50:
            device_id = f"FRAUD_D{transaction_counter:06d}"
            device_new = 1

        if random.random() < 0.50:
            ip_anomaly = 1

        if random.random() < 0.50:
            location_anomaly = 1
    elif fraud_difficulty == "hard":
        # Fraudes difíceis procuram imitar o comportamento normal do cliente
        device_id = random.choice(
            usual_devices[customer_id]
        )
        device_new = 0

        ip_anomaly = 0
        location_anomaly = 0

        # Na maioria dos casos utiliza um beneficiário habitual
        if random.random() < 0.80:
            beneficiary_id = random.choice(
                usual_beneficiaries[customer_id]
            )
            beneficiary_new = 0

            # Adicionar a transacção fraudulenta à lista
    fraud_transactions.append({
        "transaction_id": transaction_id,
        "customer_id": customer_id,
        "amount": amount,
        "timestamp": timestamp,
        "beneficiary_id": beneficiary_id,
        "beneficiary_new": beneficiary_new,
        "device_id": device_id,
        "device_new": device_new,
        "ip_anomaly": ip_anomaly,
        "location_anomaly": location_anomaly,
        "fraud_scenario": fraud_scenario,
        "fraud_difficulty": fraud_difficulty,
        "fraud_label": 1
    })

# Converter as transacções fraudulentas numa tabela
fraud_df = pd.DataFrame(fraud_transactions)

print("\nTotal de fraudes efectivamente geradas:", len(fraud_df))

print("\nPrimeiras 10 transacções fraudulentas:")
print(fraud_df.head(10))

# Juntar as transacções legítimas e fraudulentas
transactions_df = pd.concat(
    [transactions_df, fraud_df],
    ignore_index=True
)

# Ordenar novamente todas as transacções por data e hora
transactions_df = transactions_df.sort_values(
    by="timestamp"
).reset_index(drop=True)

# Guardar uma cópia das transacções antes da criação das características
# históricas utilizadas pelo modelo de Machine Learning
raw_transactions_df = transactions_df.copy()

print(
    "\nTotal de transacções após inclusão das fraudes:",
    len(transactions_df)
)

print("\nDistribuição das classes:")
print(transactions_df["fraud_label"].value_counts())

# Ordenar as transacções por data e hora
transactions_df = transactions_df.sort_values(
    by="timestamp"
).reset_index(drop=True)

# Preparar colunas para as características históricas
transactions_df["customer_avg_amount"] = 0.0
transactions_df["amount_ratio"] = 0.0
transactions_df["transactions_last_10m"] = 0
transactions_df["customer_tx_count_24h"] = 0
transactions_df["beneficiary_tx_count"] = 0
transactions_df["hour"] = transactions_df["timestamp"].dt.hour

# Calcular a média histórica das transacções anteriores de cada cliente
transactions_df["customer_avg_amount"] = (
    transactions_df
    .groupby("customer_id")["amount"]
    .transform(lambda x: x.shift(1).expanding().mean())
)

# Utilizar a média do perfil do cliente quando ainda não existe histórico
customer_initial_avg = customers.set_index("customer_id")["avg_amount"]

transactions_df["customer_avg_amount"] = (
    transactions_df["customer_avg_amount"].fillna(
        transactions_df["customer_id"].map(customer_initial_avg)
    )
)

# Calcular a relação entre o valor actual e a média histórica do cliente
transactions_df["amount_ratio"] = (
    transactions_df["amount"]
    / transactions_df["customer_avg_amount"]
)

# Calcular o número de transacções do cliente nos 10 minutos anteriores
for index, transaction in transactions_df.iterrows():
    customer_id = transaction["customer_id"]
    current_time = transaction["timestamp"]
    start_time = current_time - timedelta(minutes=10)

    previous_transactions = transactions_df[
        (transactions_df["customer_id"] == customer_id)
        & (transactions_df["timestamp"] < current_time)
        & (transactions_df["timestamp"] >= start_time)
    ]

    transactions_df.at[index, "transactions_last_10m"] = len(
        previous_transactions
    )

    

# Calcular o número de transacções do cliente nas 24 horas anteriores
for index, transaction in transactions_df.iterrows():
    customer_id = transaction["customer_id"]
    current_time = transaction["timestamp"]
    start_time = current_time - timedelta(hours=24)

    previous_transactions = transactions_df[
        (transactions_df["customer_id"] == customer_id)
        & (transactions_df["timestamp"] < current_time)
        & (transactions_df["timestamp"] >= start_time)
    ]

    transactions_df.at[index, "customer_tx_count_24h"] = len(
        previous_transactions
    )
# Calcular quantas vezes o cliente já transferiu para o beneficiário
for index, transaction in transactions_df.iterrows():
    customer_id = transaction["customer_id"]
    beneficiary_id = transaction["beneficiary_id"]
    current_time = transaction["timestamp"]

    previous_beneficiary_transactions = transactions_df[
        (transactions_df["customer_id"] == customer_id)
        & (transactions_df["beneficiary_id"] == beneficiary_id)
        & (transactions_df["timestamp"] < current_time)
    ]

    transactions_df.at[index, "beneficiary_tx_count"] = len(
        previous_beneficiary_transactions
    )

print("\nAmostra de fraudes com características calculadas:")

print(
    transactions_df[
        transactions_df["fraud_label"] == 1
    ][[
        "transaction_id",
        "customer_id",
        "amount",
        "customer_avg_amount",
        "amount_ratio",
        "beneficiary_new",
        "device_new",
        "ip_anomaly",
        "location_anomaly",
        "transactions_last_10m",
        "customer_tx_count_24h",
        "beneficiary_tx_count",
        "hour",
        "fraud_label"
    ]].head(10)
)

print("\nVerificação do cenário transfer_burst:")

transfer_burst_test = transactions_df[
    transactions_df["fraud_scenario"] == "transfer_burst"
][[
    "transaction_id",
    "customer_id",
    "timestamp",
    "amount",
    "transactions_last_10m",
    "fraud_label"
]]

print(transfer_burst_test)

print(
    "\nTotal de fraudes transfer_burst:",
    len(transfer_burst_test)
)

print(
    "Transfer_burst com operação nos 10 minutos anteriores:",
    (transfer_burst_test["transactions_last_10m"] >= 1).sum()
)

print("\nDistribuição dos cenários de fraude:")

print(
    transactions_df[
        transactions_df["fraud_label"] == 1
    ]["fraud_scenario"].value_counts()
)

print("\nDistribuição das fraudes por dificuldade:")

print(
    transactions_df[
        transactions_df["fraud_label"] == 1
    ]["fraud_difficulty"].value_counts()
)

print("\nMédia dos sinais de fraude por dificuldade:")

fraud_signal_comparison = (
    transactions_df[
        transactions_df["fraud_label"] == 1
    ]
    .groupby("fraud_difficulty")[
        [
            "beneficiary_new",
            "device_new",
            "ip_anomaly",
            "location_anomaly",
            "amount_ratio",
            "transactions_last_10m"
        ]
    ]
    .mean()
)

print(fraud_signal_comparison)

# Mostrar um resumo
print("\nTotal de transacções geradas:", len(transactions_df))
print("\nPrimeiras 10 transacções:")
print(transactions_df.head(10))

print("\nVerificação das características históricas:")
print(
    transactions_df[
        [
            "customer_id",
            "timestamp",
            "amount",
            "customer_avg_amount",
            "amount_ratio",
            "transactions_last_10m"
        ]
    ].head(20)
)
print("\nVerificação das características históricas:")
print(
    transactions_df[
        [
            "customer_id",
            "timestamp",
            "beneficiary_id",
            "amount",
            "customer_avg_amount",
            "amount_ratio",
            "transactions_last_10m",
            "customer_tx_count_24h",
            "beneficiary_tx_count"
        ]
    ].head(20)
)

print("\nVerificação de valores NaN:")
print(
    transactions_df[
        ["customer_avg_amount", "amount_ratio"]
    ].isna().sum()
)

print("\nTransacções com outra operação nos 10 minutos anteriores:")
print(
    transactions_df[
        transactions_df["transactions_last_10m"] > 0
    ][
        [
            "customer_id",
            "timestamp",
            "amount",
            "transactions_last_10m"
        ]
    ].head(10)
)
print("\nTransacções para beneficiários já utilizados anteriormente:")
print(
    transactions_df[
        transactions_df["beneficiary_tx_count"] > 0
    ][
        [
            "customer_id",
            "timestamp",
            "beneficiary_id",
            "beneficiary_new",
            "beneficiary_tx_count"
        ]
    ].head(10)
)

print(
    "\nTotal com beneficiário anteriormente utilizado:",
    (transactions_df["beneficiary_tx_count"] > 0).sum()
)

print(
    "\nTotal:",
    (transactions_df["transactions_last_10m"] > 0).sum()
)

# Mostrar os primeiros 10 clientes
print(customers.head(10))

print("\nBeneficiários do C0001:")
print(usual_beneficiaries["C0001"])

print("\nDispositivos do C0001:")
print(usual_devices["C0001"])

# Guardar os perfis dos clientes num ficheiro CSV
customers.to_csv(
    "data/raw/customers.csv",
    index=False
)

print("\nFicheiro customers.csv criado com sucesso.")

# Guardar as transacções brutas antes do Feature Engineering
raw_transactions_df.to_csv(
    "data/raw/transactions.csv",
    index=False
)

print("Ficheiro transactions.csv criado com sucesso.")

# Guardar as transacções com as características calculadas
transactions_df.to_csv(
    "data/processed/transactions_processed.csv",
    index=False
)

print("Ficheiro transactions_processed.csv criado com sucesso.")