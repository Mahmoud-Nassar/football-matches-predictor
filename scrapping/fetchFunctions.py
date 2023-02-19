def cleanLinks():
    # open the input file
    with open('scrapping\\input.txt', 'r') as f:
        # read all lines and strip any leading/trailing whitespaces
        lines = [line.strip() for line in f.readlines()]

    # create an empty list to hold the links
    links = []

    # iterate over each line in the lines list
    for line in lines:
        # split the line into words
        words = line.split()

        # iterate over each word in the words list
        for word in words:
            # check if the word starts with http:// or https://
            if word.startswith('http://') or word.startswith('https://'):
                # if yes, add the word to the links list
                links.append(word)
                break

    allLinks = ""
    for link in links:
        allLinks += "\"" + link + "\"" + ","
    allLinks = allLinks[:-1]

    with open("scrapping\\output.txt", "w") as op:
        op.write(allLinks)
