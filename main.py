from flask import Flask
from flask_restful import Resource, Api
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

app = Flask(__name__)
api = Api(app)

class Trabalho(Resource):

    def get(self, rank):

        url = 'https://raw.githubusercontent.com/vfxsoares/api_avaliacao2/main/Forbes%20Worlds%20Billionaires.csv'
        df = pd.read_csv(url)
        # Filtrar os dados
        df_filtrado = df[df['Rank'] <= rank]

        df_groupby = df_filtrado.groupby('Gender')['Age'].mean()

        # Persistir o csv
        df_groupby.to_csv('idade_media.csv')
        # Persistir o json
        df_groupby.to_json('idade_media.json')

        # Gráfico
        df_plot = sns.barplot(data=df_filtrado, x="Industry", y="Net Worth", hue='Gender', estimator=sum, ci=None)
        _ = df_plot.set_xticklabels(df_plot.get_xticklabels(), rotation=90)
        fig = df_plot.get_figure()
        plt.tight_layout()
        sns.set(font_scale=1)
        fig.savefig('grafico.png')

        return df_filtrado.to_json()


api.add_resource(Trabalho,  '/<float:rank>')


if __name__ == '__main__':
    app.run(debug=True)  # run our Flask app