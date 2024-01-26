from llama_cpp.llama import Llama, LlamaGrammar

# Load the model.

# MODEL_PATH = phi-2.Q6_K.gguf"
# MODEL_PATH = phi-2.Q8_0.gguf" # 1 second smart bool
MODEL_PATH = "mistral-7b-instruct-v0.1.Q5_K_M.gguf" # 2 seconds smart bool
# MODEL_PATH = "mistral-7b-instruct-v0.2.Q5_K_M.gguf" # sensitive to spacing...
# MODEL_PATH = "mixtral-8x7b-instruct-v0.1.Q4_K_M.gguf" # 30 seconds smart bool

LLM = Llama(MODEL_PATH, embedding=True, verbose=False, n_gpu_layers=-1)


# Define useful grammars to constrain the output.

AFFIRMATIVE_NEGATIVE = LlamaGrammar.from_string(r'''
root ::= (([tT]"rue") | ([yY] "es")) | (([fF]"alse") | ([nN] "o"))
''', verbose=False)

ONE_SENTENCE_GRAMMAR = LlamaGrammar.from_string(r'''
root ::= " "? word (" " word)* "."
word ::= [0-9A-Za-z',()-]+
''', verbose=False)


# Truncate some text to the specified token length.
def truncate(text, llm=LLM, n_ctx=512):
    return llm.detokenize(llm.tokenize(text.encode())[-n_ctx+1:]).decode()


# Get the completion for a prompt. Return it and the stop reason.
#   "min_tokens" is the minimum number of tokens that there will be
#   room for in the response before "n_ctx" is exhausted.
def complete(prompt, max_tokens=-1, min_tokens=16, n_ctx=2**12, temperature=0.2, llm=LLM, grammar=None, **kwargs):
    prompt = truncate(prompt, n_ctx=n_ctx-min_tokens, llm=llm)
    response = llm(
        prompt,
        grammar=grammar,
        max_tokens=max_tokens,
        temperature=temperature,
        **kwargs
    )
    return response['choices'][0]['text'], response['choices'][0]['finish_reason']



if __name__ == "__main__":
    prompt = "User: How many states and territories does the US have?\nAssistant: "
    answer, stop_reason = complete(
        prompt,
        grammar=ONE_SENTENCE_GRAMMAR
    )
    print("\n" + prompt + answer)
    print()
