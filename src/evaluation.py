"""
Model Evaluation Module
========================
This module handles model performance evaluation with metrics and visualizations.
"""

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report
import os


class ModelEvaluator:
    """Comprehensive model evaluation and visualization."""
    
    def __init__(self, class_names=None):
        if class_names is not None and hasattr(class_names, 'tolist'):
            self.class_names = class_names.tolist()
        else:
            self.class_names = class_names
        self.evaluation_results = {}
    
    def evaluate_model(self, model, X_test, y_test, model_name='Model'):
        """Evaluate a single model and calculate all metrics."""
        y_pred = model.predict(X_test)
        
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred, average='weighted', zero_division=0)
        recall = recall_score(y_test, y_pred, average='weighted', zero_division=0)
        f1 = f1_score(y_test, y_pred, average='weighted', zero_division=0)
        cm = confusion_matrix(y_test, y_pred)
        
        results = {
            'model_name': model_name,
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1_score': f1,
            'confusion_matrix': cm,
            'y_true': y_test,
            'y_pred': y_pred
        }
        
        self.evaluation_results[model_name] = results
        return results
    
    def evaluate_multiple_models(self, models_dict, X_test, y_test):
        """Evaluate multiple models and compare performance."""
        print("\n" + "="*60)
        print("EVALUATING MODELS ON TEST SET")
        print("="*60 + "\n")
        
        comparison_data = []
        
        for model_name, model in models_dict.items():
            print(f"Evaluating {model_name}...")
            results = self.evaluate_model(model, X_test, y_test, model_name)
            
            comparison_data.append({
                'Model': model_name,
                'Accuracy': results['accuracy'],
                'Precision': results['precision'],
                'Recall': results['recall'],
                'F1-Score': results['f1_score']
            })
            
            print(f"  ✓ Accuracy: {results['accuracy']:.4f}")
            print(f"  ✓ Precision: {results['precision']:.4f}")
            print(f"  ✓ Recall: {results['recall']:.4f}")
            print(f"  ✓ F1-Score: {results['f1_score']:.4f}\n")
        
        comparison_df = pd.DataFrame(comparison_data).sort_values(by='Accuracy', ascending=False)
        
        print("="*60)
        print("MODEL COMPARISON")
        print("="*60)
        print(comparison_df.to_string(index=False))
        print()
        
        return comparison_df
    
    def plot_confusion_matrix(self, model_name, save_path=None, figsize=(10, 8)):
        """Plot confusion matrix for a specific model."""
        if model_name not in self.evaluation_results:
            print(f"⚠ No evaluation results found for {model_name}")
            return
        
        cm = self.evaluation_results[model_name]['confusion_matrix']
        
        plt.figure(figsize=figsize)
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                    xticklabels=self.class_names if self.class_names else 'auto',
                    yticklabels=self.class_names if self.class_names else 'auto',
                    cbar_kws={'label': 'Count'})
        
        plt.title(f'Confusion Matrix - {model_name}', fontsize=16, fontweight='bold')
        plt.ylabel('True Label', fontsize=12)
        plt.xlabel('Predicted Label', fontsize=12)
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"✓ Confusion matrix saved to {save_path}")
        
        plt.close()  # Close the figure to free memory
    
    def plot_metrics_comparison(self, save_path=None, figsize=(12, 6)):
        """Plot bar chart comparing metrics across all models."""
        if not self.evaluation_results:
            print("⚠ No evaluation results available")
            return
        
        models, accuracies, precisions, recalls, f1_scores = [], [], [], [], []
        
        for model_name, results in self.evaluation_results.items():
            models.append(model_name)
            accuracies.append(results['accuracy'])
            precisions.append(results['precision'])
            recalls.append(results['recall'])
            f1_scores.append(results['f1_score'])
        
        x = np.arange(len(models))
        width = 0.2
        
        fig, ax = plt.subplots(figsize=figsize)
        ax.bar(x - 1.5*width, accuracies, width, label='Accuracy', color='#3498db')
        ax.bar(x - 0.5*width, precisions, width, label='Precision', color='#2ecc71')
        ax.bar(x + 0.5*width, recalls, width, label='Recall', color='#f39c12')
        ax.bar(x + 1.5*width, f1_scores, width, label='F1-Score', color='#e74c3c')
        
        ax.set_xlabel('Models', fontsize=12, fontweight='bold')
        ax.set_ylabel('Score', fontsize=12, fontweight='bold')
        ax.set_title('Model Performance Comparison', fontsize=16, fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels(models, rotation=15, ha='right')
        ax.legend()
        ax.set_ylim([0, 1.1])
        ax.grid(axis='y', alpha=0.3)
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"✓ Metrics comparison saved to {save_path}")
        
        plt.close()  # Close the figure to free memory
    
    def generate_classification_report(self, model_name):
        """Generate detailed classification report for a model."""
        if model_name not in self.evaluation_results:
            print(f"⚠ No evaluation results found for {model_name}")
            return None
        
        results = self.evaluation_results[model_name]
        report = classification_report(results['y_true'], results['y_pred'],
                                       target_names=self.class_names, zero_division=0)
        
        print(f"\n{'='*60}")
        print(f"CLASSIFICATION REPORT - {model_name}")
        print('='*60)
        print(report)
        
        return report
