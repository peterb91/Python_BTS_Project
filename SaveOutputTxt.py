def writeToTxt(A):
    B = []
    for i in range(len(A)):
        if A[i][0] != 0:
            B.append(A[i])

    # find unique MS names
    output_f_names = []
    for i in range(len(B)):
        if B[i][2] not in output_f_names:
            output_f_names.append(B[i][2])
   # print(output_f_names)

    # save data to separate txt files
   # path=r"C:\Users\U58224\Desktop\Python_project\output_data\\" #select path to save your output data
    for f_name in output_f_names:
        with open(f_name + ".txt", "w") as f:
            for i in range(len(B)):
                if B[i][2] == f_name:
                    if B[i][3] == "NCH":
                        f.write("%s %s %s %s" %(B[i][0],B[i][1],B[i][2],B[i][3]))
                        f.write("\n")
                    else:
                        f.write(" ".join(str(item) for item in B[i]))
                        f.write("\n")
