from latex_generator_hw import table_generator, image_generator, document_generator

with open("table.tex", "w") as f:
    success, table_tex = table_generator(
        [
            ["Name", "Age", "City"],
            ["Kate", "20", "Moscow"],
            ["Bill", "22", "Kaliningrad"],
            ["Sam", "38", "Saint-Petersburg"],
        ]
    )
    if success:
        success, document = document_generator(table_tex)
        if success:
            f.write(document)
        else:
            print(document)
    else:
        print(table_tex)

with open("image.tex", "w") as f:
    success, image_tex = image_generator("resources/cat.png", 0.5)
    if success:
        success, document = document_generator(image_tex)
        if success:
            f.write(document)
        else:
            print(document)
    else:
        print(image_tex)


with open("table_and_image.tex", "w") as f:
    print("invoked")
    success, table_tex = table_generator(
        [
            ["Name", "Age", "City"],
            ["Kate", "20", "Moscow"],
            ["Bill", "22", "Kaliningrad"],
            ["Sam", "38", "Saint-Petersburg"],
        ]
    )
    if not success:
        print(table_tex)
        exit(1)
    success, image_tex = image_generator("resources/cat.png", 0.5)
    if not success:
        print(image_tex)
        exit(1)
    success, document = document_generator(table_tex, image_tex)
    if not success:
        print(document)
        exit(1)
    f.write(document)

