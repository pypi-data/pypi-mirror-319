import subprocess
import sys
import os


from flask import Flask, render_template, request, url_for, flash, send_from_directory, jsonify
from transformers import T5Tokenizer
from transformers import T5ForConditionalGeneration
import pandas as pd
from openai import OpenAI


def web():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'b9e788f9874c3f59deaa781a1766e92833c4e2ebc6ed5c2d'
    app.config['UPLOAD_FOLDER'] = 'uploads'
    app.config['DOWNLOAD_FOLDER'] = os.path.join(app.static_folder, 'downloads')
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['DOWNLOAD_FOLDER'], exist_ok=True)

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

    # GPT or flant
    def process_data(df, gpt, api_key):
        if gpt:
            client = OpenAI(api_key=api_key)
            for index, row in df.iterrows():

                if index % 5 == 0:
                    flash(f'Already rated: {index}')

                scene = row['aihq_scene']
                a = row['a_reason']
                e = row['e_reaction']

                response_a = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant."},
                        {"role": "user", "content": f"{scene}\n{instruction_a} Written response: {a}"}
                    ],
                    temperature=0,
                    max_tokens=10)

                response_e = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant."},
                        {"role": "user", "content": f"{scene}\n{instruction_e} Behavioral response: {e}"}
                    ],
                    temperature=0,
                    max_tokens=10)

                df.at[index, 'gpt_rate_a'] = response_a.choices[0].message.content
                df.at[index, 'gpt_rate_e'] = response_e.choices[0].message.content

        else:
            model = T5ForConditionalGeneration.from_pretrained("/Users/lyuyizhou/Documents/NLP/website/flant5-large-finetuned")
            tokenizer = T5Tokenizer.from_pretrained("/Users/lyuyizhou/Documents/NLP/website/flant5-large-finetuned")

            for index, row in df.iterrows():

                if index % 5 == 0:
                    flash(f'Already rated: {index}')
                
                scene = row['aihq_scene']
                a = row['a_reason']
                e = row['e_reaction']

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

        processed_file = os.path.join(app.config['DOWNLOAD_FOLDER'], "processed_data.csv")
        df.to_csv(processed_file, index=False)
        return processed_file

    @app.route('/', methods=['GET', 'POST'])
    def upload_file():
        if request.method == 'POST':
            file = request.files['csv-file']
            model_choice = request.form.get('model-choice')
            api_key = request.form.get('api-key')
            gpt = model_choice == 'gpt'

            if gpt and not api_key:
                return jsonify({'success': False, 'message': 'Please provide an API key for GPT.'}), 400

            if file and file.filename.endswith('.csv'):
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
                file.save(filepath)
                df = pd.read_csv(filepath)

                try:
                    output_file = process_data(df, gpt, api_key)
                    return jsonify({
                        'success': True,
                        'message': 'File successfully processed. Download your file below.',
                        'downloadUrl': url_for('download_file', filename=os.path.basename(output_file))
                    })
                except Exception as e:
                    return jsonify({'success': False, 'message': f'An error occurred: {str(e)}'}), 500
            else:
                return jsonify({'success': False, 'message': 'Invalid file type, please upload a CSV file.'}), 400

        return render_template('session.html')

    @app.route('/downloads/<filename>')
    def download_file(filename):
        directory = app.config['DOWNLOAD_FOLDER']
        try:
            return send_from_directory(directory, filename, as_attachment=True)
        except FileNotFoundError:
            abort(404)

    
    print("Server is running. Please open http://127.0.0.1:5005 in your browser to access the application.")
    app.run(debug=True, port=5005)
