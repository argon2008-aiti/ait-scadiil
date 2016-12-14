import xlrd


def read_grade_sheet(file_path):
    # open the excel file to work on
    print file_path
    book = xlrd.open_workbook(file_path)

    sheet_name = "GRADE SHEET"
    # check if this has a valid sheet called "GRADE SHEET"
    if not sheet_name in book.sheet_names():
    # the file does not contain a grade sheet
        return 0

    # open the grade sheet for processing
    grade_sheet = book.sheet_by_name(sheet_name)

    # dictionary to store grade details in
    grade_dict = {}
    
    for row_num in range(2, grade_sheet.nrows):
        row = grade_sheet.row_values(row_num)
        # allow only valid IDs
        try:
            if len(row[1])<12:
                continue
        except TypeError:
            continue
        grade_dict[row_num] = [row[0], row[1], row[-2]]

    return grade_dict


def read_attendance_sheet(file_path):
    # open the excel file to work on
    print file_path
    book = xlrd.open_workbook(file_path)

    sheet_name = "ATTENDANCE"
    # check if this has a valid sheet called "ATTENDANCE"
    if not sheet_name in book.sheet_names():
    # the file does not contain a grade sheet
        print "problem with attendance 1"
        return 0

    # open the grade sheet for processing
    attendance_sheet = book.sheet_by_name(sheet_name)

    # dictionary to store grade details in
    attendance_dict = {}
    
    for row_num in range(1, attendance_sheet.nrows):
        row = attendance_sheet.row_values(row_num)
        # allow only valid IDs
        try:
            if len(row[1])<12:
                continue
        except TypeError:
            print "problem with a_sheet 2"
            continue
        attendance_dict[row_num] = [row[0], row[1]]

    return attendance_dict
