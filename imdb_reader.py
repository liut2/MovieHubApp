import csv

def read_file():
    #read newer.csv
    file = open("newer.csv")
    dict = {}
    for row in csv.reader(file):
        movie_id = row[0]
        dict[movie_id] = row

    file.close()
    #read imdb.csv
    i = 0
    max_img = 0
    max_des = 0
    max_title = 0
    file = open("imdb.csv")
    write_fn = open("movie_obj.csv", "wb")
    output = csv.writer(write_fn, delimiter=',')
    for row in csv.reader(file):
        if i == 0:
            i = i + 1
            continue
        if row[0] in dict:
            old_row = dict[row[0]]
            old_row[1] = row[1].lower()
            max_title = max(max_title, len(row[1]))
            old_row.append(row[3])
            max_img = max(max_img, len(row[3]))
            old_row.append(row[4])
            max_des = max(max_des, len(row[4]))
            old_row.append(row[6])
            old_row.append(row[7])
            output.writerow(old_row)
    file.close()
    write_fn.close()
    print "max img is %s\n" % max_img
    print "max des is %s\n" % max_des
    print "max title is %s\n" % max_title


def display(dict):
    i = 0
    for key, value in dict.iteritems():
        print key
        print value[1]
        i = i + 1
        if i == 10:
            break





if __name__ == "__main__":
    read_file()
    
