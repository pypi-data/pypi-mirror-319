# necessary packages
import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Install Werkzeug
try:
    import werkzeug
except ImportError:
    install('Werkzeug==2.3.8')

# import Flask
try:
    from flask import Flask, render_template, request, redirect, url_for, flash, session, send_from_directory, jsonify
except ImportError:
    install('Flask==2.2.2')
    from flask import Flask, render_template, request, redirect, url_for, flash, session, send_from_directory, jsonify

# import Flask-SocketIO
try:
    from flask_socketio import SocketIO
except ImportError:
    install('Flask-SocketIO==5.3.6')
    from flask_socketio import SocketIO

# import SentencePiece for transformers
try:
    import sentencepiece
except ImportError:
    install('sentencepiece==0.2.0')
    import sentencepiece

# import torch and transformers
try:
    import torch
    from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, pipeline, T5Tokenizer
    from transformers import T5ForConditionalGeneration, Seq2SeqTrainingArguments, Seq2SeqTrainer
except ImportError:
    install('torch==2.0.1')
    install('transformers==4.29.2')
    import torch
    from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, pipeline, T5Tokenizer
    from transformers import T5ForConditionalGeneration, Seq2SeqTrainingArguments, Seq2SeqTrainer

# import pandas and numpy
try:
    import pandas as pd
    import numpy as np
except ImportError:
    install('pandas==1.5.3')
    install('numpy==1.24.3')
    import pandas as pd
    import numpy as np

# import OpenAI
try:
    from openai import OpenAI
except ImportError:
    install('openai==1.18.0')
    from openai import OpenAI