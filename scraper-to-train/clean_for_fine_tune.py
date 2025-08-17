import csv

if __name__ == "__main__":

    processed_data = []
    with open("./processed_scraped.csv", newline='', encoding='utf-8', errors='ignore') as file:
        reader = csv.reader(file, delimiter=',')
        for row in reader: 
            processed_row = []
            for i,item in enumerate(row):
                if row[5] == -1 or row[4] == "Just a moment...Enable JavaScript and cookies to continue":
                    break 
                elif i == 0:
                    processed_row.append(item.replace("\n"," "))
                elif i == 1 or i == 4:
                    processed_row[0] += item
                elif i == 5:
                    processed_row.append(item.replace("\n"," "))
            processed_data.append(processed_row)

    with open("./cleaned.csv",'a', newline='', encoding='utf-8', errors='ignore') as file:
        csvwriter = csv.writer(file)
        csvwriter.writerows(processed_data)