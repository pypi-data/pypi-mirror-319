import requests
from nieto_curcio_example.some_module import some_module

def make_request():
     print("Making request")
     r = requests.get('https://jsonplaceholder.typicode.com/todos/1')
     body = r.json()
     print('Request result')
     print(body)

def main() -> None:
    some_module()
    print("Hello from nieto-curcio-example!")
    make_request()

if __name__ == "__main__":
    print("aqui")
    main()