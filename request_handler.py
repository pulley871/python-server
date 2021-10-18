import json
from http.server import BaseHTTPRequestHandler, HTTPServer 
from animals import get_all_animals, get_single_animal, create_animal, delete_animal, update_animal, get_animals_by_location, get_animals_by_status
from employees import get_all_employees, get_single_employee, post_employee, delete_employee, update_employee, get_employees_by_location
from locations import get_all_locations, get_single_location, post_location, delete_location, update_location
from customers import get_all_customers, get_single_customer, post_customer, delete_customer, update_customer, get_customer_by_email
# /Users/joshpulley/.pyenv/shims/autopep8

# Here's a class. It inherits from another class.
# For now, think of a class as a container for functions that
# work together for a common purpose. In this case, that
# common purpose is to respond to HTTP requests from a client.


class HandleRequests(BaseHTTPRequestHandler):
    # This is a Docstring it should be at the beginning of all classes and functions
    # It gives a description of the class or function
    """Controls the functionality of any GET, PUT, POST, DELETE requests to the server
    """
    def parse_url(self, path):
        path_params = path.split("/")
        resource = path_params[1]

        # Check if there is a query string parameter
        if "?" in resource:
            # GIVEN: /customers?email=jenna@solis.com

            param = resource.split("?")[1]  # email=jenna@solis.com
            resource = resource.split("?")[0]  # 'customers'
            pair = param.split("=")  # [ 'email', 'jenna@solis.com' ]
            key = pair[0]  # 'email'
            value = pair[1]  # 'jenna@solis.com'

            return ( resource, key, value )

        # No query string parameter
        else:
            id = None

            try:
                id = int(path_params[2])
            except IndexError:
                pass  # No route parameter exists: /animals
            except ValueError:
                pass  # Request had trailing slash: /animals/

            return (resource, id)

    # Here's a class function
    def _set_headers(self, status):
        # Notice this Docstring also includes information about the arguments passed to the function
        """Sets the status code, Content-Type and Access-Control-Allow-Origin
        headers on the response

        Args:
            status (number): the status code to return to the front end
        """
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    # Another method! This supports requests with the OPTIONS verb.
    def do_OPTIONS(self):
        """Sets the options headers
        """
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods',
                         'GET, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers',
                         'X-Requested-With, Content-Type, Accept')
        self.end_headers()

    # Here's a method on the class that overrides the parent's method.
    # It handles any GET request.
    def do_GET(self):
        self._set_headers(200)
        response = {}  # Default response
        parsed = self.parse_url(self.path)
        # Parse the URL and capture the tuple that is returned
        
        if len(parsed) == 2:
            (resource, id) = self.parse_url(self.path)
            if resource == "animals":
                if id is not None:
                    response = f"{get_single_animal(id)}"

                else:
                    response = f"{get_all_animals()}"
            elif resource == "employees":
                if id is not None:
                    response = f"{get_single_employee(id)}" 
                else:
                    response = f"{get_all_employees()}"
            elif resource == "locations":
                if id is not None:
                    response = f"{get_single_location(id)}"
                else:
                    response = f"{get_all_locations()}"
            elif resource == "customers":
                if id is not None:
                    response = f"{get_single_customer(id)}"
                else:
                    response = f"{get_all_customers()}"
            
        elif len(parsed) == 3:
            ( resource, key, value ) = parsed

            # Is the resource `customers` and was there a
            # query parameter that specified the customer
            # email as a filtering value?
            if resource == "customers":
                if key == "email":
                    response = get_customer_by_email(value)
            elif resource == "animals":
                if key == "location_id":
                    response = get_animals_by_location(value)
                elif key == "status":
                    response = get_animals_by_status(value)
            elif resource == "locations":
                if key == "location_id":
                    pass
            elif resource == "employees":
                if key == "location_id":
                    response = get_employees_by_location(value)
        self.wfile.write(response.encode())


    # Here's a method on the class that overrides the parent's method.
    # It handles any POST request.
    def do_POST(self):
        self._set_headers(201)
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)

        # Convert JSON string to a Python dictionary
        post_body = json.loads(post_body)

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        # Initialize new animal
        new_item = None
        # Add a new animal to the list. Don't worry about
        # the orange squiggle, you'll define the create_animal
        # function next.
        if resource == "animals":
            new_item = create_animal(post_body)
            
        elif resource == "locations":
            new_item = post_location(post_body)
        elif resource == "employees":
            new_item = post_employee(post_body)
        elif resource == "customers":
            new_item = post_customer(post_body)
        self.wfile.write(f"{new_item}".encode())
        # Encode the new animal and send in response
        

    # Here's a method on the class that overrides the parent's method.
    # It handles any PUT request.

    def do_PUT(self):
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)

        # Parse the URL
        (resource, id) = self.parse_url(self.path)
        success = False
        # Delete a single animal from the list
        if resource == "animals":
            success = update_animal(id, post_body)
        elif resource == "locations":
            update_location(id, post_body)
        elif resource == "employees":
            update_employee(id, post_body)
        elif resource == "customers":
            update_customer(id, post_body)
        # Encode the new animal and send in response
        if success:
            self._set_headers(204)
        else:
            self._set_headers(404)
        self.wfile.write("".encode())


    def do_DELETE(self):
    # Set a 204 response code
        self._set_headers(204)

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        # Delete a single animal from the list
        if resource == "animals":
            delete_animal(id)
        elif resource == "employees":
            delete_employee(id)
        elif resource == "locations":
            delete_location(id)
        elif resource == "customers":
            delete_customer(id)
        # Encode the new animal and send in response
        self.wfile.write("".encode())

# This function is not inside the class. It is the starting
# point of this application.
def main():
    """Starts the server on port 8088 using the HandleRequests class
    """
    host = ''
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()


if __name__ == "__main__":
    main()
