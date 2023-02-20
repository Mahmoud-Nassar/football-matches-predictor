import matplotlib.pyplot as plt


def create_graph(x_values, y_values, x_label, y_label, save_path, title):
    plt.clf()
    plt.plot(x_values, y_values, 'r--')
    plt.scatter(x_values, y_values, c='r')
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.savefig(save_path)
