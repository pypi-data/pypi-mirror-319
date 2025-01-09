import os
from pathlib import Path
import pickle
from datetime import datetime
from typing import List, Dict, Tuple, Optional
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.cluster import KMeans
import json
from collections import Counter

class SmartPredictor:
    def __init__(self):
        self.model_file = Path.home() / ".scout_model"
        self.history_file = Path.home() / ".scout_history"
        self.patterns_file = Path.home() / ".scout_patterns"
        self.vectorizer = TfidfVectorizer(analyzer='char', ngram_range=(2, 4))
        self.classifier = MultinomialNB()
        self.pattern_classifier = KMeans(n_clusters=5)
        self.history: List[Dict] = []
        self.patterns: Dict = {
            'common_paths': [],
            'time_patterns': {},
            'frequent_jumps': {},
            'project_roots': set(),
            'suggestions': {}
        }
        self.load_history()
        self.load_patterns()
        self.train_if_needed()

    def load_history(self):
        """Load navigation history"""
        if self.history_file.exists():
            try:
                with open(self.history_file, 'r') as f:
                    self.history = json.load(f)
            except:
                self.history = []

    def load_patterns(self):
        """Load learned navigation patterns"""
        if self.patterns_file.exists():
            try:
                with open(self.patterns_file, 'r') as f:
                    data = json.load(f)
                    self.patterns['common_paths'] = data.get('common_paths', [])
                    self.patterns['time_patterns'] = data.get('time_patterns', {})
                    self.patterns['frequent_jumps'] = data.get('frequent_jumps', {})
                    self.patterns['project_roots'] = set(data.get('project_roots', []))
                    self.patterns['suggestions'] = data.get('suggestions', {})
            except:
                pass

    def save_patterns(self):
        """Save learned navigation patterns"""
        data = {
            'common_paths': self.patterns['common_paths'],
            'time_patterns': self.patterns['time_patterns'],
            'frequent_jumps': self.patterns['frequent_jumps'],
            'project_roots': list(self.patterns['project_roots']),
            'suggestions': self.patterns['suggestions']
        }
        with open(self.patterns_file, 'w') as f:
            json.dump(data, f)

    def detect_project_root(self, path: str) -> Optional[str]:
        """Detect if a path is likely a project root"""
        path = Path(path)
        project_indicators = [
            '.git', '.svn', 'package.json', 'setup.py', 'requirements.txt',
            'Cargo.toml', 'pom.xml', 'build.gradle', '.project', '.idea'
        ]
        
        for indicator in project_indicators:
            if (path / indicator).exists():
                return str(path)
        return None

    def analyze_path_patterns(self):
        """Analyze path patterns to generate helpful suggestions"""
        if not self.history:
            return

        # Analyze common parent directories
        parent_dirs = [str(Path(h['path']).parent) for h in self.history if h['success']]
        common_parents = Counter(parent_dirs).most_common(5)
        
        # Analyze common project roots
        for path in set(h['path'] for h in self.history if h['success']):
            root = self.detect_project_root(path)
            if root:
                self.patterns['project_roots'].add(root)

        # Analyze time-based patterns
        hour_paths = {}
        for h in self.history:
            if h['success']:
                hour = h['time']
                if hour not in hour_paths:
                    hour_paths[hour] = []
                hour_paths[hour].append(h['path'])

        # Generate suggestions based on patterns
        for hour, paths in hour_paths.items():
            if len(paths) >= 3:
                common = Counter(paths).most_common(1)[0][0]
                self.patterns['time_patterns'][str(hour)] = common

        # Analyze frequent jumps (A → B patterns)
        jumps = {}
        for i in range(1, len(self.history)):
            if self.history[i-1]['success'] and self.history[i]['success']:
                from_path = self.history[i-1]['path']
                to_path = self.history[i]['path']
                if from_path != to_path:
                    if from_path not in jumps:
                        jumps[from_path] = []
                    jumps[from_path].append(to_path)

        # Store frequent jumps
        for from_path, to_paths in jumps.items():
            if len(to_paths) >= 2:
                common_jump = Counter(to_paths).most_common(1)[0][0]
                self.patterns['frequent_jumps'][from_path] = common_jump

        # Generate helpful suggestions
        self.patterns['suggestions'] = {
            'project_roots': list(self.patterns['project_roots']),
            'common_parents': [p[0] for p in common_parents],
            'time_patterns': self.patterns['time_patterns'],
            'frequent_jumps': self.patterns['frequent_jumps']
        }

        self.save_patterns()

    def get_contextual_suggestions(self, current_path: str, current_time: int) -> Dict:
        """Get contextual suggestions based on current state"""
        suggestions = {
            'next_likely': None,
            'time_based': None,
            'project_root': None,
            'helpful_tips': []
        }

        # Check if we're in a project
        root = self.detect_project_root(current_path)
        if root:
            suggestions['project_root'] = root
            suggestions['helpful_tips'].append(f"You're in a project at {root}")

        # Check frequent next jumps
        if current_path in self.patterns['frequent_jumps']:
            suggestions['next_likely'] = self.patterns['frequent_jumps'][current_path]
            suggestions['helpful_tips'].append(f"You often go to {self.patterns['frequent_jumps'][current_path]} from here")

        # Check time-based patterns
        hour_str = str(current_time)
        if hour_str in self.patterns['time_patterns']:
            suggestions['time_based'] = self.patterns['time_patterns'][hour_str]
            suggestions['helpful_tips'].append(f"At this time, you often use {self.patterns['time_patterns'][hour_str]}")

        return suggestions

    def save_history(self):
        """Save navigation history"""
        with open(self.history_file, 'w') as f:
            json.dump(self.history[-1000:], f)  # Keep last 1000 entries
        self.analyze_path_patterns()

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
            # Get contextual suggestions
            current_dir = os.getcwd()
            context = self.get_contextual_suggestions(current_dir, current_time)
            
            # Transform available directories
            X_pred = self.vectorizer.transform(available_dirs)
            
            # Get probabilities
            probs = self.classifier.predict_proba(X_pred)[:, 1]

            # Time-based boost
            time_boosts = []
            current_weekday = datetime.now().weekday()
            
            for dir_path in available_dirs:
                boost = 1.0
                
                # Boost project roots
                if dir_path in self.patterns['project_roots']:
                    boost *= 1.3
                
                # Boost contextual suggestions
                if context['next_likely'] == dir_path:
                    boost *= 1.4
                if context['time_based'] == dir_path:
                    boost *= 1.2
                
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
                    
                    boost *= time_boost * weekday_boost
                
                time_boosts.append(boost)

            # Combine probabilities with boosts
            final_scores = probs * np.array(time_boosts)
            
            # Sort and return results with context
            results = list(zip(available_dirs, final_scores))
            results.sort(key=lambda x: x[1], reverse=True)
            
            return results
        except Exception:
            return []  # Fallback to no predictions if something goes wrong 