import matplotlib.pyplot as plt

csvProcessedDataReadPath = "dataSet\\"


def create_graph(x_values, y_values, x_label, y_label, save_path):
    plt.clf()
    plt.plot(x_values, y_values, 'r--')
    plt.scatter(x_values, y_values, c='r')
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.savefig(save_path)
