"""
Parse a CSV file from SFPD:
https://data.sfgov.org/Public-Safety/SFPD-Reported-Incidents-2003-to-Present/dyj4-n68b

Then, creates a new CSV file with an additional column for the Zillow neighborhood.

Things to note:
    - homicide data was intentionally left out by SFPD
    - X is the longitude, Y is the latitude
"""
import sys
import csv


class SfpdIncident(object):
    def __init__(self):
        pass

    @classmethod
    def parse_row(cls, row):
        incident = SfpdIncident()
        incident.incident_number = row[0]
        incident.category = row[1]
        incident.description = row[2]
        # The day of the week isn't necessary since we have date and time.
        #incident.day_of_week = row[3]
        # If we want to, we could parse the DateTime from date and time
        incident.date = row[4]
        incident.time = row[5]
        incident.pd_district = row[6]
        incident.resolution = row[7]
        # We don't need the text description of location since we have lat/lon.
        #incident.location = row[8]
        incident.longitude = float(row[9])
        incident.latitude = float(row[10])

        incident.neighborhood = None # this is populated later
        return incident

    def __repr__(self):
        return "<SFPD Incident {0}>".format(self.incident_number)


def parse_sfpd_incidents_csv(filename):
    incidents = []
    with open(filename, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        reader.next() # skip the header
        for row in reader:
            incidents.append(SfpdIncident.parse_row(row))
    return incidents

def write_sfpd_incidents_csv_with_neighborhoods(filename, incidents):
    with open(filename, 'wb') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(['Incident Number',
                         'Category',
                         'Description',
                         'Date',
                         'Time',
                         'PD District',
                         'Resolution',
                         'Longitude',
                         'Latitude',
                         'Neighborhood'])
        for incident in incidents:
            writer.writerow([incident.incident_number,
                             incident.category,
                             incident.description,
                             incident.date,
                             incident.time,
                             incident.pd_district,
                             incident.resolution,
                             incident.longitude,
                             incident.latitude,
                             incident.neighborhood])
    return True


if __name__ == "__main__":
    import neighborhood

    filename = sys.argv[1]

    incidents = parse_sfpd_incidents_csv(filename)

    for incident in incidents:
        n = neighborhood.get_neighborhood(incident.longitude, incident.latitude)
        incident.neighborhood = n

    output_filename = sys.argv[2]
    write_sfpd_incidents_csv_with_neighborhoods(output_filename, incidents)
