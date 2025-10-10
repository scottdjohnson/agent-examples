"""Tests for react_simple module."""
import pytest
from react_simple.app import process_react_query
from test_utils import llm_judge


def test_weather_query():
    """Test ReAct agent with weather query: What is the weather in Seattle?"""
    question = "What is the weather in Seattle?"
    
    result = process_react_query(question, max_iterations=5)
    
    criteria = """
    The result should show successful ReAct agent execution for a weather query:
    - 'answer' should contain information about Seattle's weather
    - 'completed' should be True (agent reached Final action)
    - 'iterations' should be a list with at least one iteration
    - The agent should have used the geocode and weather tools
    - The final answer should be relevant to Seattle's weather conditions
    """
    
    # Basic assertions
    assert result is not None, "Result should not be None"
    assert isinstance(result, dict), "Result should be a dictionary"
    assert 'answer' in result, "Result should have 'answer' key"
    assert 'iterations' in result, "Result should have 'iterations' key"
    assert 'completed' in result, "Result should have 'completed' key"
    
    # Validate structure
    assert isinstance(result['iterations'], list), "Iterations should be a list"
    assert len(result['iterations']) > 0, "Should have at least one iteration"
    assert isinstance(result['answer'], str), "Answer should be a string"
    
    # Check that tools were used
    tool_names = [iter_data['tool_name'] for iter_data in result['iterations'] if iter_data['tool_name']]
    assert 'geocode' in tool_names or 'weather' in tool_names, "Should use geocode or weather tool"
    
    # Use LLM judge for semantic validation
    assert llm_judge(result, criteria), f"Weather query validation failed. Result:\n{result}"


def test_time_query():
    """Test ReAct agent with time query: What time is it in NYC?"""
    question = "What time is it in NYC?"
    
    result = process_react_query(question, max_iterations=5)
    
    criteria = """
    The result should show successful ReAct agent execution for a time query:
    - 'answer' should contain time information for NYC
    - 'completed' should be True (agent reached Final action)
    - 'iterations' should be a list with at least one iteration
    - The agent should have used the time tool (possibly with timezone like America/New_York)
    - The final answer should be relevant to the current time in NYC
    """
    
    # Basic assertions
    assert result is not None, "Result should not be None"
    assert isinstance(result, dict), "Result should be a dictionary"
    assert 'answer' in result, "Result should have 'answer' key"
    assert 'iterations' in result, "Result should have 'iterations' key"
    assert 'completed' in result, "Result should have 'completed' key"
    
    # Validate structure
    assert isinstance(result['iterations'], list), "Iterations should be a list"
    assert len(result['iterations']) > 0, "Should have at least one iteration"
    assert isinstance(result['answer'], str), "Answer should be a string"
    
    # Check that time tool was used
    tool_names = [iter_data['tool_name'] for iter_data in result['iterations'] if iter_data['tool_name']]
    assert 'time' in tool_names, "Should use time tool"
    
    # Use LLM judge for semantic validation
    assert llm_judge(result, criteria), f"Time query validation failed. Result:\n{result}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

