from frequency_tables import generate_frequency_tables
from variables_graphs import plot_all_graphs

def generate_outputs() -> None:
    print('Construindo tabelas de frequências...')
    generate_frequency_tables()
    print('Plotando gráficos...')
    plot_all_graphs()

if __name__ == '__main__':
    generate_outputs()