from frequency_tables import generate_frequency_tables
from variables_graphs import plot_all_graphs
from variable_relationships import plot_variable_relationships
from summary_statistics import get_summary_statistics

def generate_outputs() -> None:
    print('Construindo tabelas de frequências...')
    generate_frequency_tables()
    print('Plotando gráficos...')
    plot_all_graphs()
    print('Gerando gráficos de relação entre variáveis...')
    plot_variable_relationships()
    print("Gerando as medidas de resumo das variáveis...")
    get_summary_statistics()
    print('Outputs gerados com sucesso!')

if __name__ == '__main__':
    generate_outputs()