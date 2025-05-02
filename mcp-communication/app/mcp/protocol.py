from pydantic import BaseModel
from typing import Any, Dict

class MCPMessage(BaseModel):
    message_type: str
    payload: Dict[str, Any]

class MCPProtocol:
    @staticmethod
    def encode_message(message_type: str, payload: Dict[str, Any]) -> bytes:
        message = MCPMessage(message_type=message_type, payload=payload)
        return message.json().encode('utf-8')

    @staticmethod
    def decode_message(data: bytes) -> MCPMessage:
        return MCPMessage.parse_raw(data)

    @staticmethod
    def process_message(message: MCPMessage) -> Dict[str, Any]:
        # Implement the logic to process the message based on its type
        if message.message_type == "greeting":
            return {"response": "Hello! How can I assist you today?"}
        elif message.message_type == "query":
            # Handle query logic here
            return {"response": f"You asked about: {message.payload.get('query')}"}
        else:
            return {"response": "Unknown message type."}