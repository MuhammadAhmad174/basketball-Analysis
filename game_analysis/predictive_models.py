"""
Predictive Models

Machine learning models for basketball game predictions.
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, roc_auc_score
from sklearn.preprocessing import StandardScaler
import pickle
import os
from typing import Dict, Tuple, List


class PredictiveModels:
    """Builds and evaluates predictive models for basketball analysis."""
    
    def __init__(self, df: pd.DataFrame):
        """
        Initialize predictive models.
        
        Args:
            df: DataFrame with engineered features
        """
        self.df = df
        self.models = {}
        self.scalers = {}
        self.feature_importance = {}
        
    def prepare_possession_prediction_data(self) -> Tuple[pd.DataFrame, pd.Series]:
        """
        Prepare data for possession prediction.
        
        Returns:
            Tuple of (features DataFrame, target Series)
        """
        print("\n=== Preparing Possession Prediction Data ===")
        
        # Select features
        feature_cols = [
            'speed_speed_kmh',
            'distance_to_basket',
            'distance_per_frame',
            'teammates_count',
            'speed_vs_team_avg',
            'acceleration',
            'team_has_possession'
        ]
        
        # Filter to available columns
        available_features = [col for col in feature_cols if col in self.df.columns]
        
        # Prepare data
        X = self.df[available_features].copy()
        y = self.df['has_possession'].copy()
        
        # Remove rows with missing values
        mask = ~(X.isnull().any(axis=1) | y.isnull())
        X = X[mask]
        y = y[mask]
        
        print(f"Features: {len(available_features)}")
        print(f"Samples: {len(X)}")
        print(f"Positive class ratio: {y.mean():.3f}")
        
        return X, y
    
    def train_possession_predictor(
        self,
        test_size: float = 0.2,
        random_state: int = 42
    ) -> Dict[str, any]:
        """
        Train model to predict ball possession.
        
        Args:
            test_size: Proportion of data for testing
            random_state: Random seed
            
        Returns:
            Dictionary with model performance metrics
        """
        print("\n=== Training Possession Predictor ===")
        
        # Prepare data
        X, y = self.prepare_possession_prediction_data()
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state, stratify=y
        )
        
        # Scale features
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        self.scalers['possession'] = scaler
        
        # Train Random Forest
        print("\nTraining Random Forest...")
        rf_model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=random_state,
            n_jobs=-1
        )
        rf_model.fit(X_train_scaled, y_train)
        
        # Predictions
        y_pred = rf_model.predict(X_test_scaled)
        y_pred_proba = rf_model.predict_proba(X_test_scaled)[:, 1]
        
        # Evaluate
        accuracy = accuracy_score(y_test, y_pred)
        
        try:
            auc = roc_auc_score(y_test, y_pred_proba)
        except:
            auc = None
        
        print(f"\nAccuracy: {accuracy:.4f}")
        if auc:
            print(f"AUC-ROC: {auc:.4f}")
        
        print("\nClassification Report:")
        print(classification_report(y_test, y_pred))
        
        # Feature importance
        feature_importance = pd.DataFrame({
            'feature': X.columns,
            'importance': rf_model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        print("\nTop 5 Important Features:")
        print(feature_importance.head())
        
        self.models['possession_rf'] = rf_model
        self.feature_importance['possession'] = feature_importance
        
        return {
            'model': rf_model,
            'accuracy': accuracy,
            'auc': auc,
            'feature_importance': feature_importance,
            'confusion_matrix': confusion_matrix(y_test, y_pred),
            'test_size': len(X_test)
        }
    
    def prepare_pass_prediction_data(self, lookahead_frames: int = 30) -> Tuple[pd.DataFrame, pd.Series]:
        """
        Prepare data for pass prediction (will a pass occur in next N frames).
        
        Args:
            lookahead_frames: Number of frames to look ahead
            
        Returns:
            Tuple of (features DataFrame, target Series)
        """
        print(f"\n=== Preparing Pass Prediction Data (lookahead={lookahead_frames}) ===")
        
        # Create target: will pass occur in next N frames?
        self.df['pass_in_next_frames'] = self.df['is_pass_frame'].rolling(
            window=lookahead_frames, min_periods=1
        ).max().shift(-lookahead_frames).fillna(False)
        
        # Select features
        feature_cols = [
            'speed_speed_kmh',
            'distance_to_basket',
            'has_possession',
            'teammates_count',
            'possession_duration',
            'team_has_possession'
        ]
        
        available_features = [col for col in feature_cols if col in self.df.columns]
        
        X = self.df[available_features].copy()
        y = self.df['pass_in_next_frames'].copy()
        
        # Remove rows with missing values
        mask = ~(X.isnull().any(axis=1) | y.isnull())
        X = X[mask]
        y = y[mask]
        
        # Ensure y is boolean/binary
        y = y.astype(bool).astype(int)
        
        # Remove any remaining invalid values
        valid_mask = (y == 0) | (y == 1)
        X = X[valid_mask]
        y = y[valid_mask]
        
        print(f"Features: {len(available_features)}")
        print(f"Samples: {len(X)}")
        print(f"Positive class ratio: {y.mean():.3f}")
        
        return X, y
    
    def train_pass_predictor(
        self,
        lookahead_frames: int = 30,
        test_size: float = 0.2,
        random_state: int = 42
    ) -> Dict[str, any]:
        """
        Train model to predict upcoming passes.
        
        Args:
            lookahead_frames: Number of frames to look ahead
            test_size: Proportion of data for testing
            random_state: Random seed
            
        Returns:
            Dictionary with model performance metrics
        """
        print("\n=== Training Pass Predictor ===")
        
        # Prepare data
        X, y = self.prepare_pass_prediction_data(lookahead_frames)
        
        if y.sum() < 10:
            print("Warning: Too few pass events for reliable prediction")
            return {'error': 'Insufficient pass events'}
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state, stratify=y
        )
        
        # Scale features
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        self.scalers['pass'] = scaler
        
        # Train Gradient Boosting
        print("\nTraining Gradient Boosting...")
        gb_model = GradientBoostingClassifier(
            n_estimators=100,
            max_depth=5,
            random_state=random_state
        )
        gb_model.fit(X_train_scaled, y_train)
        
        # Predictions
        y_pred = gb_model.predict(X_test_scaled)
        y_pred_proba = gb_model.predict_proba(X_test_scaled)[:, 1]
        
        # Evaluate
        accuracy = accuracy_score(y_test, y_pred)
        
        try:
            auc = roc_auc_score(y_test, y_pred_proba)
        except:
            auc = None
        
        print(f"\nAccuracy: {accuracy:.4f}")
        if auc:
            print(f"AUC-ROC: {auc:.4f}")
        
        print("\nClassification Report:")
        print(classification_report(y_test, y_pred))
        
        # Feature importance
        feature_importance = pd.DataFrame({
            'feature': X.columns,
            'importance': gb_model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        print("\nTop 5 Important Features:")
        print(feature_importance.head())
        
        self.models['pass_gb'] = gb_model
        self.feature_importance['pass'] = feature_importance
        
        return {
            'model': gb_model,
            'accuracy': accuracy,
            'auc': auc,
            'feature_importance': feature_importance,
            'confusion_matrix': confusion_matrix(y_test, y_pred),
            'test_size': len(X_test)
        }
    
    def predict_player_performance_category(self) -> pd.DataFrame:
        """
        Classify players into performance categories.
        
        Returns:
            DataFrame with player performance categories
        """
        print("\n=== Player Performance Classification ===")
        
        # Aggregate player stats
        player_stats = self.df.groupby('player_id').agg({
            'speed_speed_kmh': 'mean',
            'distance_cumulative_distance_meters': 'max',
            'has_possession': 'sum',
            'frame_number': 'count'
        }).round(2)
        
        player_stats.columns = ['avg_speed', 'total_distance', 'possession_count', 'frames']
        
        # Create performance score
        player_stats['performance_score'] = (
            player_stats['avg_speed'] * 0.3 +
            player_stats['total_distance'] * 0.4 +
            player_stats['possession_count'] * 0.3
        )
        
        # Classify into categories
        player_stats['performance_category'] = pd.qcut(
            player_stats['performance_score'],
            q=3,
            labels=['Low', 'Medium', 'High']
        )
        
        print(player_stats.sort_values('performance_score', ascending=False))
        
        return player_stats
    
    def save_models(self, output_dir: str = 'game_analysis/models'):
        """
        Save trained models to disk.
        
        Args:
            output_dir: Directory to save models
        """
        os.makedirs(output_dir, exist_ok=True)
        
        for model_name, model in self.models.items():
            filepath = os.path.join(output_dir, f'{model_name}.pkl')
            with open(filepath, 'wb') as f:
                pickle.dump(model, f)
            print(f"Saved {model_name} to {filepath}")
        
        # Save scalers
        for scaler_name, scaler in self.scalers.items():
            filepath = os.path.join(output_dir, f'scaler_{scaler_name}.pkl')
            with open(filepath, 'wb') as f:
                pickle.dump(scaler, f)
            print(f"Saved scaler_{scaler_name} to {filepath}")
    
    def load_models(self, output_dir: str = 'game_analysis/models'):
        """
        Load trained models from disk.
        
        Args:
            output_dir: Directory containing saved models
        """
        for filename in os.listdir(output_dir):
            if filename.endswith('.pkl'):
                filepath = os.path.join(output_dir, filename)
                with open(filepath, 'rb') as f:
                    obj = pickle.load(f)
                
                if filename.startswith('scaler_'):
                    scaler_name = filename.replace('scaler_', '').replace('.pkl', '')
                    self.scalers[scaler_name] = obj
                else:
                    model_name = filename.replace('.pkl', '')
                    self.models[model_name] = obj
                
                print(f"Loaded {filename}")
