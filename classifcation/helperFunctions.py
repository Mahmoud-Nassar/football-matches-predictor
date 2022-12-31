import matplotlib.pyplot as plt

csvProcessedDataReadPath = "dataSet\\"


def create_graph(x_values, y_values, x_label, y_label, save_path):
    # Create the plot
    plt.plot(x_values, y_values)
    # Add labels to the X and Y axes
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    # Save the plot as a picture in the specified location
    plt.savefig(save_path)
