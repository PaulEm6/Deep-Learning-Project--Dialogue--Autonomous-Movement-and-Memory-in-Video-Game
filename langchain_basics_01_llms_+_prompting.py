# -*- coding: utf-8 -*-
"""LangChain Basics 01 - LLMs + Prompting.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1BkpMLfYEofhNK-PCKCSj9_SJqnUK40gR

# Langchain: The basics



<img src="https://dl.dropboxusercontent.com/s/b33t7ivjx6oture/YT-cover-vid%231-edited2.png" alt="LangChain Basics" width=600>
"""

!pip -q install openai langchain huggingface_hub

import os

os.environ['OPENAI_API_KEY'] = 'sk-'
os.environ['HUGGINGFACEHUB_API_TOKEN'] = ''

"""## Plain Conditional Generation

### First with OpenAI GPT3
"""

from langchain.llms import OpenAI

llm = OpenAI(model_name='text-davinci-003',
             temperature=0.9,
             max_tokens = 256)

text = "Why did the duck cross the road?"

print(llm(text))

"""### Now with T5-Flan-XL"""

from langchain.llms import HuggingFaceHub

llm_hf = HuggingFaceHub(
    repo_id="google/flan-t5-small",
    model_kwargs={"temperature":0.9 }
)

text = "Why did the chicken cross the road?"

print(llm_hf(text))



"""## Prompt Templates"""

from langchain import PromptTemplate


restaurant_template = """
I want you to act as a naming consultant for new restaurants.

Return a list of restaurant names. Each name should be short, catchy and easy to remember. It shoud relate to the type of restaurant you are naming.

What are some good names for a restaurant that is {restaurant_desription}?
"""

prompt = PromptTemplate(
    input_variables=["restaurant_desription"],
    template=restaurant_template,
)

# An example prompt with one input variable
prompt_template = PromptTemplate(input_variables=["restaurant_desription"], template=restaurant_template)

description = "a Greek place that serves fresh lamb souvlakis and other Greek food "
description_02 = "a burger place that is themed with baseball memorabilia"
description_03 = "a cafe that has live hard rock music and memorabilia"

## to see what the prompt will be like
prompt_template.format(restaurant_desription=description)

## querying the model with the prompt template
from langchain.chains import LLMChain


chain = LLMChain(llm=llm,
                 prompt=prompt_template)

# Run the chain only specifying the input variable.
print(chain.run(description_03))

"""## with Few Shot Learning"""

from langchain import PromptTemplate, FewShotPromptTemplate

# First, create the list of few shot examples.
examples = [
    {"word": "happy", "antonym": "sad"},
    {"word": "tall", "antonym": "short"},
]

# Next, we specify the template to format the examples we have provided.
# We use the `PromptTemplate` class for this.
example_formatter_template = """
Word: {word}
Antonym: {antonym}\n
"""
example_prompt = PromptTemplate(
    input_variables=["word", "antonym"],
    template=example_formatter_template,
)

# Finally, we create the `FewShotPromptTemplate` object.
few_shot_prompt = FewShotPromptTemplate(
    # These are the examples we want to insert into the prompt.
    examples=examples,
    # This is how we want to format the examples when we insert them into the prompt.
    example_prompt=example_prompt,
    # The prefix is some text that goes before the examples in the prompt.
    # Usually, this consists of intructions.
    prefix="Give the antonym of every input",
    # The suffix is some text that goes after the examples in the prompt.
    # Usually, this is where the user input will go
    suffix="Word: {input}\nAntonym:",
    # The input variables are the variables that the overall prompt expects.
    input_variables=["input"],
    # The example_separator is the string we will use to join the prefix, examples, and suffix together with.
    example_separator="\n",
)

# We can now generate a prompt using the `format` method.
print(few_shot_prompt.format(input="big"))

from langchain.chains import LLMChain

chain = LLMChain(llm=llm, prompt=few_shot_prompt)

# Run the chain only specifying the input variable.
print(chain.run("big"))

