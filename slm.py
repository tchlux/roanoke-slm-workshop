
# The following is a dependency for loading the model files and generating output.
# 
#   python3 -m pip install --user llama-cpp-python
# 

# Import the library for loading ".gguf" model files and specifying grammars (constrained outputs).
from llama_cpp.llama import Llama, LlamaGrammar

# Models downloaded with LMStudio will be in a path such as:
#    ~/.cache/lm-studio/models/...

# Set the path to the model.
MODEL_PATH = "mistral-7b-instruct-v0.1.Q5_K_M.gguf" # 2 seconds smart bool
# MODEL_PATH = "phi-2.Q6_K.gguf" # 2 seconds smart bool

# Load the model.
LLM = Llama(MODEL_PATH, embedding=True, verbose=False)

# ------------------------------------------------------------------------------------
# Define useful grammars to constrain the output.

# Grammar for stricly "yes" / "no" outputs.
YES_NO = LlamaGrammar.from_string(r'''
root ::= (([nN] "o") | ([yY] "es"))
''', verbose=False)

# Grammar for a single sentence.
ONE_SENTENCE_GRAMMAR = LlamaGrammar.from_string(r'''
root ::= " "? word (" " word)* "."
word ::= [0-9A-Za-z',()-]+
''', verbose=False)

# Grammar for valid JSON-parseable output (doesn't handle premature stops).
JSON_ARRAY_GRAMMAR = LlamaGrammar.from_string(r'''# For generating JSON arrays
root ::= "[" ws ( value ("," ws value)* )? "]"
ws ::= ([ \t\n] ws)?
number ::= ("-"? ([0-9] | [1-9] [0-9]*)) ("." [0-9]+)? ([eE] [-+]? [0-9]+)? ws
string ::= "\"" ( [^"\\]  # anything that's not a quote or backslash, OR ...
   | "\\" (["\\/bfnrt] | "u" [0-9a-fA-F] [0-9a-fA-F] [0-9a-fA-F] [0-9a-fA-F]) # escapes
  )* "\"" ws
array  ::= "[" ws (value ("," ws value)* )? "]" ws
object ::= "{" ws (string ":" ws value ("," ws string ":" ws value)* )? "}" ws
value ::= object | array | string | number | ("true" | "false" | "null") ws
''', verbose=False)

# ------------------------------------------------------------------------------------


# Truncate some text to the specified token length.
def truncate(text, llm=LLM, n_ctx=512):
    return llm.detokenize(llm.tokenize(text.encode())[-n_ctx+1:]).decode()


# Get the completion for a prompt. Return it and the stop reason.
#   "min_tokens" is the minimum number of tokens that there will be
#   room for in the response before "n_ctx" is exhausted.
def complete(prompt, max_tokens=-1, min_tokens=16, n_ctx=2**12, temperature=0.2, llm=LLM, grammar=None, stream=False, **kwargs):
    prompt = truncate(prompt, n_ctx=n_ctx-min_tokens, llm=llm)
    response = llm(
        prompt,
        grammar=grammar,
        max_tokens=max_tokens,
        temperature=temperature,
        stream=stream,
        **kwargs
    )
    # Return a generator of [(text, reason) ...] if streaming is wanted.
    if (stream):
        generator = ((token['choices'][0]['text'], token['choices'][0]['finish_reason']) for token in response)
        return generator
    # Otherwise just return the response.
    else:
        return response['choices'][0]['text'], response['choices'][0]['finish_reason']


if __name__ == "__main__":
    # 
    # Ideas for language model uses:
    # - generate data for class demonstrations
    # - summarize lecture transcriptions
    # - anything creative
    # - traveling, tour guides, iteneraries
    # 

    # python3 slm.py 

    # Demo one.
    prompt = "User: How many states and territories does the US have?\nAssistant: "
    print(prompt, end="")
    answer, reason = complete(
        prompt,
        grammar=ONE_SENTENCE_GRAMMAR,
    )
    print(answer)
    print()
    # 
    # User: How many states and territories does the US have?
    # Assistant: 50 states and 5 territories.
    # 

    # Demo two.
    prompt = "User: Provide a list of tourist destinations in San Francisco in JSON format.\nAssistant: "
    print(prompt, end="")
    for (token, stop_reason) in complete(
        prompt,
        grammar=JSON_ARRAY_GRAMMAR,
        stream=True,
    ):
        print(token, end="", flush=True)
    print()
    # 
    # User: Provide a list of tourist destinations in San Francisco in JSON format.
    # Assistant: ["Alcatraz Island", "Golden Gate Bridge", "Lombard Street", "Cable Car Museum", "Chinatown", "Coit Tower", "Fisherman's Wharf", "Palace of Fine Arts", "Exploratorium"]
    # 

    # HACK: Silence any shutdown errors that might occur.
    import os
    devnull = open(os.devnull, "w")
    os.dup2(devnull.fileno(), 2)

