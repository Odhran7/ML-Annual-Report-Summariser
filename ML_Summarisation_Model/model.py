
'''# Importing prerequisites to run model

from transformers import PegasusForConditionalGeneration, PegasusTokenizer

# Create tokenizer and the model

tokenizer = PegasusTokenizer.from_pretrained("human-centered-summarization/financial-summarization-pegasus")

# Loading the model

model = PegasusForConditionalGeneration.from_pretrained("google/pegasus-xsum")

# Performing abstractive summarisation using the model

test_text = """
TechnipFMC plc, a public limited company incorporated and organized under the laws of England and Wales, with registered\n
number 09909709, and with registered office at Hadrian House, Wincomblee Road, Newcastle Upon Tyne, NE6 3PL, United
Kingdom (\“TechnipFMC,\” the \“Company,\” \“we,\” or \“our”\) is a global leader in the energy industry, delivering projects, products,
technologies, and services. With our proprietary technologies and production systems, integrated expertise, and comprehensive
solutions, we are transforming our customers’ project economics. We have operational headquarters in Houston, Texas, United
States, and in 2021 we principally operated across two business segments: Subsea and Surface Technologies.
We are uniquely positioned to deliver greater efficiency across project lifecycles, from concept to project delivery and beyond.
Through innovative technologies and improved efficiencies, our offering unlocks new possibilities for our customers in developing
their energy resources and in their positioning to meet the energy transition challenge.
Enhancing our performance and competitiveness is a key component of our strategy, which is achieved through technology and
innovation differentiation, seamless execution, and reliance on simplification to drive costs down. We are targeting profitable and
sustainable growth by seizing market growth opportunities and expanding our range of services. We are managing our assets
efficiently to ensure we are well-prepared to drive and benefit from the opportunities in many of the markets we serve.
Each of our more than 20,000 employees is driven by a steady commitment to clients and a culture of project execution, purposeful
innovation, challenging industry conventions, and rethinking how the best results are achieved. This leads to fresh thinking,
streamlined decisions, and smarter results, enabling us to achieve our vision of enhancing the performance of the world’s energy
industry
"""

# Creating the tokens -> a number representation of our text

tokens = tokenizer(test_text, truncation = True, padding = "longest", return_tensors = "pt")

# Summarise the data in tokens 

summary = model.generate(**tokens)

# We need to decode the tokens

print(tokenizer.decode(summary[0]))
'''

from transformers import PegasusTokenizer, PegasusForConditionalGeneration, TFPegasusForConditionalGeneration

# Let's load the model and the tokenizer 
model_name = "human-centered-summarization/financial-summarization-pegasus"
tokenizer = PegasusTokenizer.from_pretrained(model_name)
model = PegasusForConditionalGeneration.from_pretrained(model_name) # If you want to use the Tensorflow model 
                                                                    # just replace with TFPegasusForConditionalGeneration


# Some text to summarize here
text_to_summarize = "National Commercial Bank (NCB), Saudi Arabia’s largest lender by assets, agreed to buy rival Samba Financial Group for $15 billion in the biggest banking takeover this year.NCB will pay 28.45 riyals ($7.58) for each Samba share, according to a statement on Sunday, valuing it at about 55.7 billion riyals. NCB will offer 0.739 new shares for each Samba share, at the lower end of the 0.736-0.787 ratio the banks set when they signed an initial framework agreement in June.The offer is a 3.5% premium to Samba’s Oct. 8 closing price of 27.50 riyals and about 24% higher than the level the shares traded at before the talks were made public. Bloomberg News first reported the merger discussions.The new bank will have total assets of more than $220 billion, creating the Gulf region’s third-largest lender. The entity’s $46 billion market capitalization nearly matches that of Qatar National Bank QPSC, which is still the Middle East’s biggest lender with about $268 billion of assets."

# Tokenize our text
# If you want to run the code in Tensorflow, please remember to return the particular tensors as simply as using return_tensors = 'tf'
input_ids = tokenizer(text_to_summarize, return_tensors="pt").input_ids

# Generate the output (Here, we use beam search but you can also use any other strategy you like)
output = model.generate(
    input_ids, 
    max_length=32, 
    num_beams=5, 
    early_stopping=True
)

# Finally, we can print the generated summary
print(tokenizer.decode(output[0], skip_special_tokens=True))
# Generated Output: Saudi bank to pay a 3.5% premium to Samba share price. Gulf region’s third-largest lender will have total assets of $220 billion