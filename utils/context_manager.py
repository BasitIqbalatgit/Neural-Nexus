from typing import List
import logging
from config import MAX_CONTEXT_LENGTH

logger = logging.getLogger(__name__)

class ConversationManager:
    def __init__(self):
        self.context = []
        self.max_context_length = MAX_CONTEXT_LENGTH
        
    def add_to_context(self, user_input: str, bot_response: str):
        try:
            self.context.append({"role": "user", "content": user_input})
            self.context.append({"role": "assistant", "content": bot_response})
            
            if len(self.context) > self.max_context_length * 2:
                self.context = self.context[-self.max_context_length * 2:]
        except Exception as e:
            logger.error(f"Error adding to context: {str(e)}")
            
    def get_context(self) -> List[dict]:
        return self.context
        
    def clear_context(self):
        self.context = []
