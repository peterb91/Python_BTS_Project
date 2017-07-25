import logs


def write_to_txt(a):
    b = []
    logs.logger.info("Starting writting output to txt files")
    for i in range(len(a)):
        if a[i][0] != 0:
            b.append(a[i])

    # find unique MS names
    output_f_names = []
    for i in range(len(b)):
        if b[i][2] not in output_f_names:
            output_f_names.append(b[i][2])
            logs.logger.info(("unique MS names:", output_f_names))
    # print(output_f_names)
    # save data to separate txt files
    # path=r"C:\Users\U58224\Desktop\Python_project\output_data\\" #select path to save your output data
    for f_name in output_f_names:
        with open(f_name + ".txt", "w") as f:
            for i in range(len(b)):
                if b[i][2] == f_name:
                    if b[i][3] == "NCH":
                        f.write("%s %s %s %s" % (b[i][0], b[i][1], b[i][2], b[i][3]))
                        f.write("\n")
                    else:
                        f.write(" ".join(str(item) for item in b[i]))
                        f.write("\n")
    logs.logger.info("Finishing writting output to txt files\n")
