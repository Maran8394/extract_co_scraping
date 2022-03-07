import csv


def excel_write(write_list, file_name):
    given_file_name = f"{file_name}.csv"
    try:
        with open(given_file_name, 'r+', newline='', encoding="ISO-8859-1", errors='ignore') as read_file:
            reader_writer = csv.reader((line.replace('\0', '') for line in read_file))
            if write_list not in reader_writer:
                with open(given_file_name, 'a+', newline='', encoding="ISO-8859-1",
                          errors='ignore') as f:
                    writer = csv.writer(f, delimiter=",")
                    writer.writerow(write_list)
                    f.close()
                print("Writed -->", write_list[0])
                return True
            else:
                print("Exist -->", write_list[0])
                return False
    except FileNotFoundError:
        f = open(given_file_name, 'w+', newline='', encoding="ISO-8859-1", errors='ignore')
        f.close()
        excel_write(write_list, file_name)
    except Exception as e:
        print(e)




