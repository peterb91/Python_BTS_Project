def WriteToTxt():
    A=[['DL','S0','MS776','INC',8],
        ['UL','S0','MS333','NCH'],
        [0],
        ['DL','S0','MS776','INC',2],
        ['UL','S0','MS222','DEC',1],
        ['UL','S0','MS222','DEC',2]]

    #create timestamp for all output data
    timestamp,B=0,[]
    for i in range(len(A)):
        timestamp+=0.5
        A[i]=([timestamp]+A[i])
        if A[i][1]!=0:
            B.append(A[i])
   # print(A)
   # print(B)

    # find unique MS names
    output_f_names = []
    for i in range(len(B)):
        if B[i][3] not in output_f_names:
            output_f_names.append(B[i][3])
   # print(output_f_names)

    # save data to separate txt files
    path=r"C:\Users\U58224\Desktop\Python_project\output_data\\" #select path to save your output data
    for f_name in output_f_names:
        with open(path + f_name + ".txt", "w") as f:
            for i in range(len(B)):
                if B[i][3] == f_name:
                    f.write(" ".join(str(item) for item in B[i][1:]))
                    f.write("\n")
    return
print(WriteToTxt())
