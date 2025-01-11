import torch
from tokenizers import Tokenizer
from tokenizers.models import Model
from torch.fx.experimental.symbolic_shapes import lru_cache
from transformers import AutoModelForCausalLM
from transformers import AutoTokenizer


@lru_cache(maxsize=1)
def setup_model_and_tokenizer() -> tuple[Model, Tokenizer]:
    # Initialize tokenizer and model
    tokenizer = AutoTokenizer.from_pretrained(
        pretrained_model_name_or_path="microsoft/Phi-3-mini-4k-instruct",
    )
    model = AutoModelForCausalLM.from_pretrained(
        pretrained_model_name_or_path="microsoft/Phi-3-mini-4k-instruct",
        device_map="auto",
        torch_dtype=torch.float16,
    )
    return model, tokenizer

def generate_text(
    *,
    prompt: str,
    max_length: int = 50,
) -> str:
    model: Model
    tokenizer: Tokenizer
    model, tokenizer = setup_model_and_tokenizer()

    # Tokenize input
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

    # Generate response
    outputs = model.generate(
        **inputs,
        max_length=max_length,
        temperature=0.7,
        do_sample=True,
        pad_token_id=tokenizer.pad_token_id,
    )

    # Decode and return response
    response: str = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return response


def main() -> None:
    prompt: str = "Explain quantum computing in simple terms:"
    response: str = generate_text(prompt=prompt)
    print(response)


if __name__ == '__main__':
    main()
