import algorithm
import json


if __name__ == '__main__':

    data = json.load(open('data.json','r'))
    distances = data['distances']
    requests = data['requests']
    vehicles = data['vehicles']

    # Iterating over all the items in vehicles and initializing the availability for each one to TRUE
    for vehicle in vehicles:
        vehicle['available'] = True

    # Creating an object of algorithm class
    zipexist = algorithm.Graph()

    # Iterating over all the elements in distances variable and adding vertices/nodes/points it to graph
    for distance in distances:
        # adding zipcodes depending on whether they exist or not in object
        if not distance['zipcode1'] in zipexist.get_vertices():
            zipexist.add_vertex(distance['zipcode1'])

        if not distance['zipcode2'] in zipexist.get_vertices():
            zipexist.add_vertex(distance['zipcode2'])

        zipexist.add_edge(distance['zipcode1'], distance['zipcode2'], distance['distance'])


    # requesting for a vehicle by giving the zipcode -passing vehicle type, and zipcode
    def get_vehicle(vehicle_type, zipcode):

        available_vehicles = [v for v in vehicles if v['type'] == vehicle_type and v['available']]

        # If there are available vehicles
        if len(available_vehicles) > 0:
            zipexist.reset_vertices()  # vertex's distance = infinityvi; vextex.visited = False; vertex.previous = None will be done in reset_vertices() method
            place = zipexist.get_vertex(zipcode)  # Returns vert_dict
            algorithm.algorithm(zipexist, place)  # passing the graph object and place into algorithm method in

            # Calculating and storing the list of distances for all the available vehicles done by adding vertex and getting distance
            for av in available_vehicles:
                av['distance'] = zipexist.get_vertex(av['zipcode']).get_distance()

            # sorted list based on distances
            available_vehicles = sorted(available_vehicles, key=lambda k: k['distance'])

        return available_vehicles


    # Iterating within requests
    for requestedvehicle in requests:
        # calling 'get_vehicle' and ordering as FIFO
        emergencyvehicle = get_vehicle(requestedvehicle['vehicle_type'], requestedvehicle['zipcode'])

        if len(emergencyvehicle) > 0:  # If the number of available vehicles is at least 1
            vehicles[vehicles.index(emergencyvehicle[0])]['available'] = False  # availability change from false to true
            requestedvehicle['vehicle_id'] = emergencyvehicle[0]['id']  # store the vehicle id in requestedvehicle variable as emergencyvehicle[0]'s ID
            requestedvehicle['distance'] = emergencyvehicle[0]['distance']  # store distance of requestedvehicle variable from emergencyvehicle[0]'s distance

            [print(k, '--->', requestedvehicle[k]) for k in requestedvehicle]  # Printing key value pairs in each of the requests
            print('--------------------------------------')
    with open('output','w') as out:
        json.dump(vehicles, out, ensure_ascii=False) # Writing into a new file the result of the data