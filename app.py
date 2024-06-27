from flask import Flask, request, render_template
import pandas as pd

app = Flask(__name__)

# Carregar o banco de dados
df = pd.read_excel('database.xlsx')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result', methods=['POST'])
def result():
    ra = request.form['ra']
    student = df[df['RA'] == ra]
    
    if not student.empty:
        nome = student.iloc[0]['Nome']
        jogo_nota = student.iloc[0]['Nota 1º Bim Jogo Nota']
        jogo_peso = student.iloc[0]['Nota 1º Bim Jogo Peso 40%']
        prova_nota = student.iloc[0]['Nota 1º Bim Prova Nota']
        prova_peso = student.iloc[0]['Nota 1º Bim Prova Peso 60%']
        nota_b1 = student.iloc[0]['Nota B1']
        prova2_nota = student.iloc[0]['Nota 2º Bim Prova 2 Nota']
        prova2_peso = student.iloc[0]['Nota 2º Bim Prova 2 Peso 70%']
        trabalhos_nota = student.iloc[0]['Nota 2º Bim Trabalhos Nota']
        trabalhos_peso = student.iloc[0]['Nota 2º Bim Trabalhos Peso 30%']
        nota_b2 = student.iloc[0]['Nota B2']
        soma_final = student.iloc[0]['Soma Final']
        media_final = student.iloc[0]['Media Final']
        nota_final = student.iloc[0]['Nota Final']
        atingiu_media = student.iloc[0]['Atingiu Media']

        return render_template('result.html', 
                               ra=ra, 
                               nome=nome, 
                               jogo_nota=jogo_nota, 
                               jogo_peso=jogo_peso,
                               prova_nota=prova_nota,
                               prova_peso=prova_peso,
                               nota_b1=nota_b1,
                               prova2_nota=prova2_nota,
                               prova2_peso=prova2_peso,
                               trabalhos_nota=trabalhos_nota,
                               trabalhos_peso=trabalhos_peso,
                               nota_b2=nota_b2,
                               soma_final=soma_final,
                               media_final=media_final,
                               nota_final=nota_final,
                               atingiu_media=atingiu_media)
    else:
        return render_template('index.html', error='RA não encontrado')

if __name__ == '__main__':
    app.run(debug=True)
