from flask import Flask, flash

app = Flask(__name__)

@app.route('/api/home')

def hello():
    return 'hola mundo desde cero'

if __name__ == '__main__':
    app.run(host='0.0.0.0' , port=5000)