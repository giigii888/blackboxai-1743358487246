from typing import List, Dict
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from database import SessionLocal, get_db
import models
import logging

# Initialize NLTK resources
nltk.download('punkt')
nltk.download('stopwords')

class ChatbotTrainer:
    def __init__(self, bot_id: int):
        self.bot_id = bot_id
        self.vectorizer = TfidfVectorizer(
            stop_words=stopwords.words('english'),
            ngram_range=(1, 2),
            max_features=5000
        )
        self.trained_data = None
        self.personality_profile = {}

    def preprocess_text(self, text: str) -> str:
        """Clean and normalize text for training"""
        text = text.lower()
        text = re.sub(r'[^\w\s]', '', text)
        tokens = word_tokenize(text)
        return ' '.join(tokens)

    def load_training_data(self, db):
        """Load all scripts assigned to this bot from database"""
        scripts = db.query(models.Script).filter(models.Script.bot_id == self.bot_id).all()
        if not scripts:
            raise ValueError("No training data found for this bot")
        
        self.raw_texts = [script.content for script in scripts]
        self.processed_texts = [self.preprocess_text(text) for text in self.raw_texts]
        
        # Analyze personality traits from text
        self._analyze_personality()

    def _analyze_personality(self):
        """Extract personality traits from training texts"""
        word_counts = {}
        for text in self.processed_texts:
            for word in text.split():
                word_counts[word] = word_counts.get(word, 0) + 1
        
        # Simple personality metrics
        self.personality_profile = {
            'word_variety': len(word_counts),
            'avg_sentence_length': sum(len(t.split()) for t in self.processed_texts) / len(self.processed_texts),
            'common_words': sorted(word_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        }

    def train(self, db):
        """Train the model on loaded scripts"""
        self.load_training_data(db)
        self.trained_data = self.vectorizer.fit_transform(self.processed_texts)
        logging.info(f"Bot {self.bot_id} trained on {len(self.processed_texts)} documents")
        return self.personality_profile

    def generate_response(self, query: str, threshold: float = 0.3) -> str:
        """Generate response based on trained knowledge"""
        if self.trained_data is None:
            raise ValueError("Model not trained yet")
        
        processed_query = self.preprocess_text(query)
        query_vec = self.vectorizer.transform([processed_query])
        
        similarities = cosine_similarity(query_vec, self.trained_data)
        max_sim_idx = np.argmax(similarities)
        max_sim = similarities[0, max_sim_idx]
        
        if max_sim < threshold:
            return "I'm not sure how to respond to that. Could you rephrase?"
        
        # Return the most similar training text
        return self.raw_texts[max_sim_idx]

def train_bot(bot_id: int, db: SessionLocal):
    """Train a specific bot and save personality profile"""
    trainer = ChatbotTrainer(bot_id)
    personality = trainer.train(db)
    
    # Update bot's personality profile in database
    bot = db.query(models.Bot).filter(models.Bot.id == bot_id).first()
    if bot:
        bot.personality = str(personality)
        db.commit()
    
    return personality