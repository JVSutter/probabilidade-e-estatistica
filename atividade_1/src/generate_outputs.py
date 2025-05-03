from frequency_tables import generate_frequency_tables
from variables_graphs import plot_all_graphs
from relation_variables_graphs import plot_relation_variables

def generate_outputs() -> None:
    print('Construindo tabelas de frequências...')
    generate_frequency_tables()
    print('Plotando gráficos...')
    plot_all_graphs()
    plot_relation_variables()

if __name__ == '__main__':
    generate_outputs()