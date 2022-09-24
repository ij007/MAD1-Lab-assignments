import csv
from jinja2 import Template
import sys
import matplotlib.pyplot as plt

temp1 = '''
<!DOCTYPE html>
<html>
<head><title>Student Data</title></head>
<body>
<h1>Student Details</h1>
<table border="Solid">
<tr>
<th>Student ID</th>
<th>Course ID</th>
<th>Marks</th>
</tr>
{% for row in rows %}
<tr>
<td>{{row[0]}}</td>
<td>{{row[1]}}</td>
<td>{{row[2]}}</td>
</tr>
{% endfor %}
<td colspan="2">Marks</td>
<td>{{mark}}</td>
</table>
</body>
</html>
'''

temp2 = '''
<!DOCTYPE html>
<html>
<head><title>Course Data</title></head>
<body>
<h1>Course Details</h1>
<table border="Solid">
<tr>
<th>Average Marks</th>
<th>Maximum Marks</th>
</tr>
<tr>
<td>{{avg}}</td>
<td>{{max}}</td>
</tr>
</table>
<img src="histogram.png" alt="Histogram">
</body>
</html>
'''

error = '''
<!DOCTYPE html>
<html>
<head><title>Soething went wrong</title></head>
<body>
<h1>Wrong Inputs</h1>
<p>Something went wrong.</p>
</body>
</html>
'''
def studentDetails(p2):
    att=[]
    sum=0
    with open('data.csv', newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['Student id'] == p2:
                sum=sum+int(row[' Marks'])
                att.append([row['Student id'],row[' Course id'],row[' Marks']])

    if sum!=0:
        with open('output.html', 'w') as f:
            f.write(Template(temp1).render(rows=att, mark=sum))

    else:
        with open('error.html', 'w') as f:
            f.write(error)

def courseDetails(p2):
    sum=0
    num=0
    max=0
    marks = {}
    with open('data.csv', newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if int(row[' Course id']) == int(p2):
                sum=sum+int(row[' Marks'])
                num=num+1
                try:
                    marks[int(row[' Marks'])]+=1
                except KeyError:
                    marks[int(row[' Marks'])] = 1
                if int(row[' Marks'])>max:
                    max=int(row[' Marks'])

    if num!=0:
        plt.hist(marks.keys(), weights=marks.values())
        plt.xlabel('Marks')
        plt.ylabel('Frequency')
        plt.savefig('histogram.png')
        avg=sum/num
        with open('output.html', 'w') as f:
            f.write(Template(temp2).render(avg=avg, max=max))
    
    else:
        with open('error.html', 'w') as f:
            f.write(error)

if __name__ == "__main__":
    p1 = sys.argv[1]
    p2 = sys.argv[2]
    if p1 == '-s':
        studentDetails(p2)
    elif p1 == '-c':
        courseDetails(p2)
    else:
        with open('error.html', 'w') as f:
            f.write(error)