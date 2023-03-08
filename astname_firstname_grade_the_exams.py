import pandas as pd
import re

answer_key = "B,A,D,D,C,B,D,A,C,C,D,B,A,B,A,C,B,D,A,C,A,A,B,D,D".split(',')

#đọc file và tìm các dòng lỗi
def read_file(filename):
    list_line_error = []
    try:
        with open("./Data Files/{}".format(filename), "r") as fileRead:
            print("Successfully opened {}".format(filename))
            print("**** ANALYZING ****")
            #lặp từng dòng để kiểm tra
            for index, line in enumerate(fileRead):
                answers = line.split(',')
                student_code = answers[0]
                if len(answers) != 26:
                    print("Invalid line of data: does not contain exactly 26 values:")
                    print(line)
                    list_line_error.append(index)
                elif not re.search('^N\\d{8}$', student_code):
                    print("Invalid line of data: N# is invalid")
                    print(line)
                    print(student_code)
                    list_line_error.append(index)
    except:
        #In ra thông báo khi tên file không đúng
        print("File cannot be found.")
    #Trả lại số index các dòng lỗi
    return list_line_error

#tạo converters để đổi các đáp án ra điểm
def get_converters():
    converters = {}
    for index, answer in enumerate(answer_key):
        def check_score(value, a=answer):
            print(a)
            if value == a:
                return 4
            elif value == "":
                return 0
            return -1

        converters[index + 1] = check_score
    return converters

#Dùng pandas xử lý file
def read_file_pandas():
    filename = input("Enter a class to grade (i.e. class1 for class1.txt): ")
    list_line_error = read_file(filename)
    # read file lọc ra các dòng lỗi
    df = pd.read_csv("./Data Files/{}".format(filename), header=None,
                     engine='python', usecols=range(26), skiprows=list_line_error, converters=get_converters())
    print("Successfully opened {}".format(filename))
    # đặt cột id làm index
    df.set_index(0, inplace=True)
    #Thêm cột total bằng tổng tất cả các điểm cuả một dòng
    df['Total'] = df.sum(axis=1)
    #Nếu không có dòng lỗi thi in ra thông báo
    if len(list_line_error) == 0:
        print("No errors found!")
    print("**** REPORT ****")
    print("Total valid lines of data: {}".format(df.shape[0]))
    print("Total invalid lines of data: {}".format(len(list_line_error)))
    print("Mean (average) score: {}".format(df.Total.mean()))
    print("Highest score: {}".format(df.Total.max()))
    print("Lowest score: {}".format(df.Total.min()))
    print("Range of scores: {}".format(df.Total.max() - df.Total.min()))
    print("Median score: {}".format(df.Total.median()))
    #Tạo tên file mới
    filename_export = "{}_grades.txt".format(filename.split('.')[0])
    #Export kết quả ra file
    df.Total.to_csv("./Data Files/Expected Output/{}".format(filename_export), header=False)
    print(df.Total)

read_file_pandas()
