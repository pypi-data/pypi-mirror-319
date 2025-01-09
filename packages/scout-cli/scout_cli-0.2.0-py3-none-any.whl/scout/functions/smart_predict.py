import os
from pathlib import Path
import pickle
from datetime import datetime
from typing import List, Dict, Tuple
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import json

class SmartPredictor:
    def __init__(self):
        self.model_file = Path.home() / ".scout_model"
        self.history_file = Path.home() / ".scout_history"
        self.vectorizer = TfidfVectorizer(analyzer='char', ngram_range=(2, 4))
        self.classifier = MultinomialNB()
        self.history: List[Dict] = []
        self.load_history()
        self.train_if_needed()

    def load_history(self):
        """Load navigation history"""
        if self.history_file.exists():
            try:
                with open(self.history_file, 'r') as f:
                    self.history = json.load(f)
            except:
                self.history = []

    def save_history(self):
        """Save navigation history"""
        with open(self.history_file, 'w') as f:
            json.dump(self.history[-1000:], f)  # Keep last 1000 entries

    def add_to_history(self, path: str, time_of_day: int, success: bool = True):
        """Add a navigation event to history"""
        entry = {
            'path': path,
            'time': time_of_day,
            'weekday': datetime.now().weekday(),
            'success': success,
            'timestamp': datetime.now().isoformat()
        }
        self.history.append(entry)
        self.save_history()

    def train_if_needed(self):
        """Train the model if enough data is available"""
        if len(self.history) < 5:  # Need at least 5 entries to train
            return False

        # Prepare training data
        X_text = [h['path'] for h in self.history if h['success']]
        if not X_text:
            return False

        # Add time-based features
        times = np.array([h['time'] for h in self.history if h['success']])
        weekdays = np.array([h['weekday'] for h in self.history if h['success']])

        # Transform text features
        X_tfidf = self.vectorizer.fit_transform(X_text)
        
        # Create labels (just use 1 for all successful navigations)
        y = np.ones(len(X_text))

        # Train the model
        self.classifier.fit(X_tfidf, y)
        return True

    def predict_directories(self, partial_path: str, current_time: int, 
                          available_dirs: List[str]) -> List[Tuple[str, float]]:
        """Predict most likely directories based on partial path and time"""
        if not available_dirs or len(self.history) < 5:
            return []

        try:
            # Transform available directories
            X_pred = self.vectorizer.transform(available_dirs)
            
            # Get probabilities
            probs = self.classifier.predict_proba(X_pred)[:, 1]

            # Time-based boost
            time_boosts = []
            current_weekday = datetime.now().weekday()
            
            for dir_path in available_dirs:
                # Find relevant history entries
                relevant = [h for h in self.history 
                          if h['success'] and h['path'] == dir_path]
                
                if relevant:
                    # Time similarity boost
                    time_diffs = [abs(h['time'] - current_time) for h in relevant]
                    time_boost = 1 + (0.5 * (1 - min(time_diffs) / 12))
                    
                    # Weekday boost
                    weekday_matches = [h for h in relevant 
                                     if h['weekday'] == current_weekday]
                    weekday_boost = 1 + (0.3 * (len(weekday_matches) / len(relevant)))
                    
                    time_boosts.append(time_boost * weekday_boost)
                else:
                    time_boosts.append(1.0)

            # Combine probabilities with time boosts
            final_scores = probs * np.array(time_boosts)
            
            # Sort and return results
            results = list(zip(available_dirs, final_scores))
            results.sort(key=lambda x: x[1], reverse=True)
            
            return results
        except Exception:
            return []  # Fallback to no predictions if something goes wrong 