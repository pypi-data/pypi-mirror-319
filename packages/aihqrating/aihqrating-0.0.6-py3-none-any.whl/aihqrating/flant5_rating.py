import subprocess
import sys
import os

# run the package installation script
subprocess.check_call([sys.executable, "install_packages.py"])


from transformers import T5Tokenizer, T5ForConditionalGeneration
import pandas as pd

# instruction messages
instruction_a = "Read the following written responses people give regarding why they thought the person in the scene \
    before acted toward them the way they did. Your task is to rate the hostility of the attributed intent. \
        A rating of 1 would be given if someone perceived the situation as an accident. \
            A rating of 5 would be given if someone thought the person in the scene did this on purpose and wanted to harm them. \
                A rating of 3 might be given if the person thought the person in the scene did this on purpose to some degree, \
                    but did not intend to harm them. Please output a single numeric number from 1 to 5, \
                        do not include anything other than the number in the output."

instruction_e = "Read the following behavioral responses people give toward the social situation above. \
    Your task is to rate the presence of aggression in the behavioral response. \
        A rating of 1 is given for a passive response or one in which the participant says that she/he would do nothing. \
            A rating of 5 would be given for physical retaliation. \
                Other examples of ratings include: 2 (the participant reports that he /she would ask why the other \
                    person acted toward them in that way), 3(the participant would tell the other person not to act that way again), \
                        and 4 (the participant would yell at the other person). Please output a single numeric number from 1 to 5, \
                            do not include anything other than the number in the output."

df = pd.read_csv("/Users/lyuyizhou/Documents/NLP/1_data/testingData.csv")

model = T5ForConditionalGeneration.from_pretrained("/Users/lyuyizhou/Documents/NLP/website/flant5-large-finetuned")
tokenizer = T5Tokenizer.from_pretrained("/Users/lyuyizhou/Documents/NLP/website/flant5-large-finetuned")

for index, row in df.iterrows():

    if index % 100 == 0:
        print(f'Already rated: {index}')
    
    scene = row['aihq_scene']
    a = row['a']
    e = row['e']

    message_a = f"{scene} \n{instruction_a} \nResponses:{a}"
    inputs_a = tokenizer(message_a, return_tensors="pt")
    output_a = model.generate(**inputs_a, do_sample=False, max_new_tokens=10)
    result_a = tokenizer.batch_decode(output_a, skip_special_tokens=True)

    message_e = f"{scene} \n{instruction_e} \nResponses:{e}"
    inputs_e = tokenizer(message_e, return_tensors="pt")
    output_e = model.generate(**inputs_e, do_sample=False, max_new_tokens=10)
    result_e = tokenizer.batch_decode(output_e, skip_special_tokens=True)

    df.at[index, 'flant5_rate_a'] = result_a[0]
    df.at[index, 'flant5_rate_e'] = result_e[0]

df.to_csv("/Users/lyuyizhou/Documents/NLP/3_results/flant5_testingData.csv", index=False)
