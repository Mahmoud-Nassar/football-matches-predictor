import matplotlib.pyplot as plt


def createGraph(xValues, yValues, xLabel, yLabel, savePath, title):
    plt.clf()
    plt.plot(xValues, yValues, 'r--')
    plt.scatter(xValues, yValues, c='r')
    plt.xlabel(xLabel)
    plt.ylabel(yLabel)
    plt.title(title)
    plt.savefig(savePath)


def createMultipleFunctionGraph(xValues, linesArray, linesHeadLines,
                                linesNames, xLabel, yLabel, savePath, title):
    """
    :param xValues:
    :param linesArray: array of plot lines,
    every cell in this array contains the Y values of different line in the figure
    :param linesNames: the names of lines,
    in the same order that there were supplied in the line array
    :param xLabel:
    :param yLabel:
    :param savePath:
    :param title:
    :return:
    """
    fig, ax = plt.subplots(figsize=(8, 6))

    for i, line in enumerate(linesArray):
        ax.plot(xValues, line, label=linesNames[i])

    ax.set_title(title)
    ax.set_xlabel(xLabel)
    ax.set_ylabel(yLabel)

    # ax.legend()
    ax.legend(bbox_to_anchor=(1.125, 1.125), loc='upper right',
              title=linesHeadLines, fontsize="small")

    plt.savefig(savePath)
