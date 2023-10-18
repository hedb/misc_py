import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

import csv

# Initialize lists for storing data
hours = []
metrics = []
notes = []

# Open the CSV file and read the data
with open('glucose_sample.csv', 'r') as f:
    reader = csv.reader(f)
    next(reader)  # Skip the header row
    for row in reader:
        hour = row[0]
        metric = int(row[1]) if row[1] else -1
        note = row[2]

        # If the metric is not empty, add it to the list
        if metric != -1:
            hours.append(hour)
            metrics.append(metric)
        # If the note is not empty, add it to the list
        elif note:
            notes.append(note)


# Plot the metric data as a line graph
plt.plot(hours, metrics)
plt.ylim(50,150)
#tilting the x axis labels
plt.xticks(rotation=45)

fig = plt.figure()
fig.canvas.manager.window.attributes('-fullscreen', True)


# Add a callout line for each note
for note in notes:
    plt.axvline(x=note, color='red', linestyle='--')

# Add a title and axis labels
plt.title('Metric Graph with Notes')
plt.xlabel('Hour')
plt.ylabel('Metric')



# Show the plot
plt.show()