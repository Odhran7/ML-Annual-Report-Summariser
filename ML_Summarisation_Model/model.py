# Importing prerequisites to run model

from transformers import PegasusForConditionalGeneration, PegasusTokenizer

# Create tokenizer and the model

tokenizer = PegasusTokenizer.from_pretrained("google/pegasus-xsum")

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