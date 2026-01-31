"""Tests for llm_act_converse module."""
import pytest
import os
from llm_act_converse.app import process_conversation_turn
from test_utils import llm_judge


def test_process_conversation_turn(tmp_path):
    """Test two conversational turns to verify context is maintained.
    
    Note: Due to LLM variability, this test may occasionally fail if the LLM
    doesn't generate code or generates incorrect code. Run the test again if this happens.
    """
    max_attempts = 3
    
    for attempt in range(max_attempts):
        messages = []
        
        # First turn: Create a function
        user_input_1 = "Write a function that adds two numbers"
        result_1 = process_conversation_turn(user_input_1, messages, scripts_dir=str(tmp_path))
        
        # Validate first turn basic structure
        assert result_1 is not None, "First turn: Result should not be None"
        assert 'code' in result_1, "First turn: Result should have 'code' key"
        assert 'filename' in result_1, "First turn: Result should have 'filename' key"
        
        # Check if first turn succeeded
        if result_1['code'] is None:
            if attempt < max_attempts - 1:
                print(f"Attempt {attempt + 1}: First turn failed to generate code, retrying...")
                continue
            else:
                pytest.fail(f"First turn failed to generate code after {max_attempts} attempts")
        
        assert result_1['filename'] is not None, "First turn: File should be created"
        assert os.path.exists(result_1['filename']), f"First turn: File should exist"
        assert len(messages) == 4, "First turn: Should have 4 messages in history"
        
        criteria_1 = """
        The result should indicate successful code generation:
        - 'code' should contain a function definition related to adding numbers
        - 'filename' should be a valid .py file
        - 'llm_response' should be a non-empty string
        """
        
        if not llm_judge(result_1, criteria_1):
            if attempt < max_attempts - 1:
                print(f"Attempt {attempt + 1}: First turn failed validation, retrying...")
                continue
            else:
                pytest.fail(f"First turn validation failed after {max_attempts} attempts. Result:\n{result_1}")
        
        # Second turn: Modify the request (tests if conversation context is maintained)
        user_input_2 = "Now modify it to multiply two numbers instead and show me the result of 5 times 3"
        result_2 = process_conversation_turn(user_input_2, messages, scripts_dir=str(tmp_path))
        
        # Validate second turn basic structure
        assert result_2 is not None, "Second turn: Result should not be None"
        assert 'code' in result_2, "Second turn: Result should have 'code' key"
        assert 'filename' in result_2, "Second turn: Result should have 'filename' key"
        
        # Check if second turn succeeded
        if result_2['code'] is None:
            if attempt < max_attempts - 1:
                print(f"Attempt {attempt + 1}: Second turn failed to generate code, retrying...")
                continue
            else:
                pytest.fail(f"Second turn failed to generate code after {max_attempts} attempts")
        
        assert result_2['filename'] is not None, "Second turn: File should be created"
        assert result_2['filename'] != result_1['filename'], "Second turn: Should create a new file"
        assert os.path.exists(result_2['filename']), f"Second turn: File should exist"
        assert len(messages) == 7, "Second turn: Should have 7 messages in history (4 + 3)"
        
        # Validate conversation history structure
        assert messages[0]['role'] == 'system', "Message should be system"
        assert messages[1]['role'] == 'user', "Message should be user"
        assert messages[2]['role'] == 'code_generation', "Message should be code_generation"
        assert messages[3]['role'] == 'assistant', "Message should be assistant"
        assert messages[4]['role'] == 'user', "Message should be user"
        assert messages[5]['role'] == 'code_generation', "Message 4 should be code_generation"
        assert messages[6]['role'] == 'assistant', "Message should be assistant"
        
        criteria_2 = """
        The result should show the conversation context was maintained:
        - 'code' should contain a function that multiplies (not adds) two numbers
        - Either 'output' should contain the result of 5*3 (15) or code should execute successfully
        - 'filename' should be a valid .py file (different from the first)
        - The code should demonstrate understanding that we're modifying from addition to multiplication
        """
        
        if llm_judge(result_2, criteria_2):
            # Test passed
            return
        elif attempt < max_attempts - 1:
            print(f"Attempt {attempt + 1}: Second turn failed validation, retrying...")
            continue
        else:
            pytest.fail(f"Second turn validation failed after {max_attempts} attempts. Result:\n{result_2}")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

