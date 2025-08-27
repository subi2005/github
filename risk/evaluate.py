"""
from sklearn.metrics import confusion_matrix, classification_report
import pandas as pd

def assign_label(score):
    if score < 20:
        return "Very Low"
    elif score < 40:
        return "Low"
    elif score < 60:
        return "Medium"
    elif score < 85:
        return "High"
    else:
        return "Very High"

def evaluate_classifier(y_true_scores, y_pred_scores):
    y_true_labels = y_true_scores.apply(assign_label)
    y_pred_labels = pd.Series(y_pred_scores).apply(assign_label)

    labels = ["Very Low", "Low", "Medium", "High", "Very High"]
    cm = confusion_matrix(y_true_labels, y_pred_labels, labels=labels)
    report = classification_report(y_true_labels, y_pred_labels, target_names=labels)

    print("Confusion Matrix:\n", cm)
    print("\nClassification Report:\n", report)
"""
"""
from sklearn.metrics import confusion_matrix, classification_report
import pandas as pd

def assign_label(score: float) -> str:
    if score < 20: return "Very Low"
    if score < 40: return "Low"
    if score < 60: return "Medium"
    if score < 85: return "High"
    return "Very High"

def evaluate_30d_scores(y_true_scores, y_pred_scores):
    y_true_labels = y_true_scores.apply(assign_label)
    y_pred_labels = pd.Series(y_pred_scores).apply(assign_label)
    labels = ["Very Low", "Low", "Medium", "High", "Very High"]
    cm = confusion_matrix(y_true_labels, y_pred_labels, labels=labels)
    report = classification_report(y_true_labels, y_pred_labels, target_names=labels)
    return cm, report
"""


from sklearn.metrics import confusion_matrix, classification_report
from risk.model import assign_label

def evaluate_risk(y_true, y_pred):
    y_true_labels = y_true.apply(assign_label)
    y_pred_labels = y_pred.apply(assign_label)

    labels = ["Very Low Risk", "Low Risk", "Moderate Risk", "High Risk", "Very High Risk"]
    cm = confusion_matrix(y_true_labels, y_pred_labels, labels=labels)
    print("Confusion Matrix:\n", cm)
    print("\nClassification Report:\n")
    print(classification_report(y_true_labels, y_pred_labels, target_names=labels))

