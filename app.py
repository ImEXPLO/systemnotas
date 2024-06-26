from flask import Flask, request, jsonify, render_template
import pandas as pd

app = Flask(__name__)

def clean_ra(ra_value):
    """Função para converter RAs possivelmente em notação científica para string limpa."""
    try:
        return str(int(float(ra_value)))
    except ValueError:
        return str(ra_value)

def format_number(value):
    """Função para formatar números com duas casas decimais."""
    try:
        return round(float(value), 2)
    except ValueError:
        return value

try:
    # Carregar a planilha e garantir que RA seja tratado como string
    df = pd.read_excel('database.xlsx', sheet_name='Planilha1', dtype=str)
    df['RA'] = df['RA'].apply(clean_ra).str.strip()  # Limpar e converter RAs
    print(df.head())  # Adicionado para verificar a leitura dos dados
except Exception as e:
    print(f"Erro ao ler o arquivo Excel: {e}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search')
def search():
    ra = request.args.get('ra')
    if ra:
        try:
            ra = clean_ra(ra).strip()
            result = df[df['RA'] == ra]
            if not result.empty:
                row = result.iloc[0].to_dict()
                print(row)  # Adicionado para verificar os dados da linha correspondente
                data = {
                    'success': True,
                    'name': row.get('Nome', ''),
                    'jogo_nota_1bim': format_number(row.get('Jogo Nota (1º Bim)', '')),
                    'jogo_peso_40': format_number(row.get('Jogo Peso 40%', '')),
                    'prova_nota_1bim': format_number(row.get('Prova Nota (1º Bim)', '')),
                    'prova_peso_60': format_number(row.get('Prova Peso 60%', '')),
                    'soma_1bim': format_number(row.get('Soma (1º Bim)', '')),
                    'nota_b1': format_number(row.get('Nota B1', '')),
                    'prova2_nota_2bim': format_number(row.get('Prova 2 Nota (2º Bim)', '')),
                    'prova2_peso_70': format_number(row.get('Prova 2 Peso 70%', '')),
                    'trabalhos_nota_2bim': format_number(row.get('Trabalhos Nota (2º Bim)', '')),
                    'trabalhos_peso_30': format_number(row.get('Trabalhos Peso 30%', '')),
                    'nota_b2': format_number(row.get('Nota B2', '')),
                    'soma_final': format_number(row.get('Soma Final', '')),
                    'media_final': format_number(row.get('Média Final', '')),
                    'nota_final': format_number(row.get('Nota Final', '')),
                    'atingiu_media': row.get('Atingiu Média', '')
                }
                return jsonify(data)
            else:
                return jsonify({'success': False, 'error': 'RA não encontrado'})
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)})
    else:
        return jsonify({'success': False, 'error': 'Parâmetro RA ausente'})

if __name__ == '__main__':
    app.run(debug=True)