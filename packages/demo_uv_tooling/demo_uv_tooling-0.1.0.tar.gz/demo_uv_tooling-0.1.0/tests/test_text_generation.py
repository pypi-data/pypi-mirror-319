from src.text_generation import generate_text


def test_generate_text():
    # Arrange
    prompt_0 = "Explain quantum computing in simple terms:"
    prompt_1 = "What is the meaning of life?"
    prompt_2 = "What is the best programming language?"

    # Act
    response_0 = generate_text(prompt=prompt_0)
    response_1 = generate_text(prompt=prompt_1)
    response_2 = generate_text(prompt=prompt_2)

    assert response_0 is not None
    assert response_0 != ""
    assert response_1 is not None
    assert response_1 != ""
    assert response_2 is not None
    assert response_2 != ""
