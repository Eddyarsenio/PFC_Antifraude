import pandas as pd
import joblib

from sklearn.model_selection import (
    train_test_split,
    StratifiedKFold,
    cross_validate,
    cross_val_predict
)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    confusion_matrix,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score
)


DATA_PATH = "data/processed/transactions_processed.csv"

FEATURES = [
    "amount",
    "beneficiary_new",
    "device_new",
    "ip_anomaly",
    "location_anomaly",
    "transactions_last_10m",
    "customer_avg_amount",
    "amount_ratio",
    "customer_tx_count_24h",
    "beneficiary_tx_count",
    "hour"
]

TARGET = "fraud_label"


df = pd.read_csv(DATA_PATH)

X = df[FEATURES]
y = df[TARGET]

fraud_difficulty = df["fraud_difficulty"]

print("Dimensão do dataset completo:")
print(df.shape)

print("\nDimensão das features X:")
print(X.shape)

print("\nDimensão da variável alvo y:")
print(y.shape)

print("\nDistribuição da variável alvo:")
print(y.value_counts())

print("\nDistribuição percentual:")
print(
    (y.value_counts(normalize=True) * 100).round(2)
)

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

difficulty_test = fraud_difficulty.loc[X_test.index]

print("\n--- Divisão treino/teste ---")

print("X_train:", X_train.shape)
print("X_test:", X_test.shape)

print("\nClasses no treino:")
print(y_train.value_counts())

print("\nClasses no teste:")
print(y_test.value_counts())

logistic_model = Pipeline([
    (
        "scaler",
        StandardScaler()
    ),
    (
        "model",
        LogisticRegression(
            class_weight="balanced",
            random_state=42,
            max_iter=1000
        )
    )
])

logistic_model.fit(
    X_train,
    y_train
)

print("\nLogistic Regression treinada com sucesso.")

y_pred_logistic = logistic_model.predict(X_test)

y_prob_logistic = logistic_model.predict_proba(
    X_test
)[:, 1]

print("\n--- Previsões da Logistic Regression ---")

print("Transacções avaliadas:", len(y_pred_logistic))

print("\nClassificações previstas pelo modelo:")
print(
    pd.Series(y_pred_logistic)
    .value_counts()
    .sort_index()
)

print("\nClassificações reais no conjunto de teste:")
print(
    y_test.value_counts()
    .sort_index()
)

conf_matrix_logistic = confusion_matrix(
    y_test,
    y_pred_logistic
)

print("\n--- Matriz de Confusão ---")
print(conf_matrix_logistic)

precision_logistic = precision_score(
    y_test,
    y_pred_logistic
)

recall_logistic = recall_score(
    y_test,
    y_pred_logistic
)

f1_logistic = f1_score(
    y_test,
    y_pred_logistic
)

roc_auc_logistic = roc_auc_score(
    y_test,
    y_prob_logistic
)

print("\n--- Métricas da Logistic Regression ---")
print(f"Precision: {precision_logistic:.4f}")
print(f"Recall: {recall_logistic:.4f}")
print(f"F1-Score: {f1_logistic:.4f}")
print(f"ROC-AUC: {roc_auc_logistic:.4f}")

random_forest_model = RandomForestClassifier(
    n_estimators=300,
    class_weight="balanced",
    random_state=42
)

random_forest_model.fit(
    X_train,
    y_train
)

print("\nRandom Forest treinada com sucesso.")

y_pred_rf = random_forest_model.predict(
    X_test
)

y_prob_rf = random_forest_model.predict_proba(
    X_test
)[:, 1]

conf_matrix_rf = confusion_matrix(
    y_test,
    y_pred_rf
)

print("\n--- Matriz de Confusão - Random Forest ---")
print(conf_matrix_rf)

precision_rf = precision_score(
    y_test,
    y_pred_rf
)

recall_rf = recall_score(
    y_test,
    y_pred_rf
)

f1_rf = f1_score(
    y_test,
    y_pred_rf
)

roc_auc_rf = roc_auc_score(
    y_test,
    y_prob_rf
)

print("\n--- Métricas do Random Forest ---")
print(f"Precision: {precision_rf:.4f}")
print(f"Recall: {recall_rf:.4f}")
print(f"F1-Score: {f1_rf:.4f}")
print(f"ROC-AUC: {roc_auc_rf:.4f}")

difficulty_analysis = pd.DataFrame({
    "fraud_label": y_test,
    "fraud_difficulty": difficulty_test,
    "logistic_prediction": pd.Series(
        y_pred_logistic,
        index=y_test.index
    ),
    "random_forest_prediction": pd.Series(
        y_pred_rf,
        index=y_test.index
    )
})

fraud_test = difficulty_analysis[
    difficulty_analysis["fraud_label"] == 1
]

difficulty_results = (
    fraud_test
    .groupby("fraud_difficulty")
    .agg(
        total_frauds=("fraud_label", "count"),
        detected_logistic=("logistic_prediction", "sum"),
        detected_random_forest=(
            "random_forest_prediction",
            "sum"
        )
    )
)

difficulty_results["recall_logistic"] = (
    difficulty_results["detected_logistic"]
    / difficulty_results["total_frauds"]
)

difficulty_results["recall_random_forest"] = (
    difficulty_results["detected_random_forest"]
    / difficulty_results["total_frauds"]
)

print("\n--- Detecção de Fraudes por Dificuldade ---")
print(difficulty_results)

cv = StratifiedKFold(
    n_splits=5,
    shuffle=True,
    random_state=42
)

scoring = [
    "precision",
    "recall",
    "f1",
    "roc_auc"
]

cv_logistic = cross_validate(
    logistic_model,
    X_train,
    y_train,
    cv=cv,
    scoring=scoring
)

cv_random_forest = cross_validate(
    random_forest_model,
    X_train,
    y_train,
    cv=cv,
    scoring=scoring
)

print("\n--- Cross-Validation: Logistic Regression ---")
print(
    f"Precision média: "
    f"{cv_logistic['test_precision'].mean():.4f}"
)
print(
    f"Recall médio: "
    f"{cv_logistic['test_recall'].mean():.4f}"
)
print(
    f"F1-Score médio: "
    f"{cv_logistic['test_f1'].mean():.4f}"
)
print(
    f"ROC-AUC médio: "
    f"{cv_logistic['test_roc_auc'].mean():.4f}"
)

print("\nDesvio-padrão - Logistic Regression:")
print(
    f"Precision: "
    f"{cv_logistic['test_precision'].std():.4f}"
)
print(
    f"Recall: "
    f"{cv_logistic['test_recall'].std():.4f}"
)
print(
    f"F1-Score: "
    f"{cv_logistic['test_f1'].std():.4f}"
)
print(
    f"ROC-AUC: "
    f"{cv_logistic['test_roc_auc'].std():.4f}"
)

print("\n--- Cross-Validation: Random Forest ---")
print(
    f"Precision média: "
    f"{cv_random_forest['test_precision'].mean():.4f}"
)
print(
    f"Recall médio: "
    f"{cv_random_forest['test_recall'].mean():.4f}"
)
print(
    f"F1-Score médio: "
    f"{cv_random_forest['test_f1'].mean():.4f}"
)
print(
    f"ROC-AUC médio: "
    f"{cv_random_forest['test_roc_auc'].mean():.4f}"
)

print("\nDesvio-padrão - Random Forest:")
print(
    f"Precision: "
    f"{cv_random_forest['test_precision'].std():.4f}"
)
print(
    f"Recall: "
    f"{cv_random_forest['test_recall'].std():.4f}"
)
print(
    f"F1-Score: "
    f"{cv_random_forest['test_f1'].std():.4f}"
)
print(
    f"ROC-AUC: "
    f"{cv_random_forest['test_roc_auc'].std():.4f}"
)

rf_oof_probabilities = cross_val_predict(
    random_forest_model,
    X_train,
    y_train,
    cv=cv,
    method="predict_proba"
)[:, 1]

thresholds = [
    0.30,
    0.35,
    0.40,
    0.45,
    0.50,
    0.55,
    0.60
]

print("\n--- Análise de Threshold - Random Forest ---")

for threshold in thresholds:

    predictions = (
        rf_oof_probabilities >= threshold
    ).astype(int)

    precision = precision_score(
        y_train,
        predictions
    )

    recall = recall_score(
        y_train,
        predictions
    )

    f1 = f1_score(
        y_train,
        predictions
    )

    print(
        f"Threshold {threshold:.2f} | "
        f"Precision: {precision:.4f} | "
        f"Recall: {recall:.4f} | "
        f"F1: {f1:.4f}"
    )


SELECTED_THRESHOLD = 0.50

print("\n--- Verificação do Threshold 0.50 ---")

print(
    "Probabilidades exactamente iguais a 0.50:",
    (y_prob_rf == 0.50).sum()
)

print(
    "Diferenças entre predict() e threshold manual:",
    (y_pred_rf != (y_prob_rf >= 0.50).astype(int)).sum()
)

y_pred_rf_adjusted = (
    y_prob_rf > SELECTED_THRESHOLD
).astype(int)

conf_matrix_rf_adjusted = confusion_matrix(
    y_test,
    y_pred_rf_adjusted
)

precision_rf_adjusted = precision_score(
    y_test,
    y_pred_rf_adjusted
)

recall_rf_adjusted = recall_score(
    y_test,
    y_pred_rf_adjusted
)

f1_rf_adjusted = f1_score(
    y_test,
    y_pred_rf_adjusted
)

print(
    "\n--- Random Forest Final - Threshold 0.50 ---"
)

print("Matriz de Confusão:")
print(conf_matrix_rf_adjusted)

print(
    f"Precision: {precision_rf_adjusted:.4f}"
)

print(
    f"Recall: {recall_rf_adjusted:.4f}"
)

print(
    f"F1-Score: {f1_rf_adjusted:.4f}"
)

print(
    f"ROC-AUC: {roc_auc_rf:.4f}"
)






feature_importance = pd.DataFrame({
    "feature": FEATURES,
    "importance": random_forest_model.feature_importances_
})

feature_importance = feature_importance.sort_values(
    by="importance",
    ascending=False
)

print("\n--- Importância das Features - Random Forest ---")
print(
    feature_importance.to_string(
        index=False
    )
)

print(
    "\nSoma das importâncias:",
    feature_importance["importance"].sum()
)

MODEL_PATH = "ml/models/random_forest_model.joblib"

joblib.dump(
    random_forest_model,
    MODEL_PATH
)

print(
    f"\nModelo Random Forest guardado em: {MODEL_PATH}"
)