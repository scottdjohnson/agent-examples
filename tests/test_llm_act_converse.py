"""Tests for llm_act_converse module."""
import pytest
import os
from llm_act_converse.app import process_conversation_turn
from test_utils import llm_judge


def test_process_conversation_turn(tmp_path):
    """Test two conversational turns to verify context is maintained."""
    messages = []
    
    # First turn: Create a function
    user_input_1 = "Write a function that adds two numbers"
    result_1 = process_conversation_turn(user_input_1, messages, scripts_dir=str(tmp_path))
    
    # Validate first turn
    criteria_1 = """
    The result should indicate successful code generation:
    - 'code' should contain a function definition related to adding numbers
    - 'filename' should be a valid .py file
    - 'llm_response' should be a non-empty string
    """
    
    assert result_1['code'] is not None, "First turn: Code should be generated"
    assert result_1['filename'] is not None, "First turn: File should be created"
    assert os.path.exists(result_1['filename']), f"First turn: File should exist"
    assert len(messages) == 3, "First turn: Should have 3 messages in history"
    assert llm_judge(result_1, criteria_1), f"First turn validation failed. Result:\n{result_1}"
    
    # Second turn: Modify the request (tests if conversation context is maintained)
    user_input_2 = "Now modify it to multiply two numbers instead and show me the result of 5 times 3"
    result_2 = process_conversation_turn(user_input_2, messages, scripts_dir=str(tmp_path))
    
    # Validate second turn
    criteria_2 = """
    The result should show the conversation context was maintained:
    - 'code' should contain a function that multiplies (not adds) two numbers
    - Either 'output' should contain the result of 5*3 (15) or code should execute successfully
    - 'filename' should be a valid .py file (different from the first)
    - The code should demonstrate understanding that we're modifying from addition to multiplication
    """
    
    assert result_2['code'] is not None, "Second turn: Code should be generated"
    assert result_2['filename'] is not None, "Second turn: File should be created"
    assert result_2['filename'] != result_1['filename'], "Second turn: Should create a new file"
    assert os.path.exists(result_2['filename']), f"Second turn: File should exist"
    assert len(messages) == 6, "Second turn: Should have 6 messages in history (3 per turn)"
    
    # Validate conversation history structure
    assert messages[0]['role'] == 'user', "Message 0 should be user"
    assert messages[1]['role'] == 'code_generation', "Message 1 should be code_generation"
    assert messages[2]['role'] == 'assistant', "Message 2 should be assistant"
    assert messages[3]['role'] == 'user', "Message 3 should be user"
    assert messages[4]['role'] == 'code_generation', "Message 4 should be code_generation"
    assert messages[5]['role'] == 'assistant', "Message 5 should be assistant"
    
    assert llm_judge(result_2, criteria_2), f"Second turn validation failed. Result:\n{result_2}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

