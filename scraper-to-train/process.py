import csv

if __name__ == "__main__":

    processed_data = []
    with open("./scraped.csv", newline='', encoding='utf-8', errors='ignore') as file:
        reader = csv.reader(file, delimiter=',')
        for row in reader: 
            processed_row = []
            for i,item in enumerate(row):
                if row[5] == -1 or row[4] == "Just a moment...Enable JavaScript and cookies to continue":
                    break 
                else:
                    processed_row.append(item.replace("\n"," "))
            processed_data.append(processed_row)

    with open("./processed_scraped.csv",'a', newline='', encoding='utf-8', errors='ignore') as file:
        csvwriter = csv.writer(file)
        csvwriter.writerows(processed_data)