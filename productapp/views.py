from django.shortcuts import render, HttpResponse
import requests
import base64

global selected_operator
from django.core.paginator import Paginator

# Create your views here.

# def product(request):
#     data = requests.get("https://fakestoreapi.com/products")
#     if data.status_code == 200:
#         decodeData = data.json()
#         print(decodeData,type(decodeData))

#     for product in decodeData:
#         print(type(product))
#         print(product['rating']['rate'])

#     return HttpResponse("<h1>Hello</h1>")


def product(request):
    data = requests.get("https://fakestoreapi.com/products")
    if data.status_code == 200:
        decodeData = data.json()
        return render(request, template_name='product.html', context={'decodeData': decodeData})
    else:
        return render(request, template_name='error.html', context={'error_message': 'Failed to fetch data from the API'})
    

def carts(request):
    data = requests.get("https://fakestoreapi.com/carts")
    if data.status_code == 200:
        decodeData = data.json()
        # print(decodeData[0].keys())
        # for i in decodeData[0].keys():
        #     print(i,type(i))
        print(decodeData[0]['__v'])
        return render(request, template_name='carts.html', context={'decodeData': decodeData})
    else:
        return render(request, template_name='error.html', context={'error_message': 'Failed to fetch data from the API'})
    


def users(request):
    data = requests.get("https://fakestoreapi.com/users")
    if data.status_code == 200:
        decodeData = data.json()
        return render(request, template_name='users.html', context={'decodeData': decodeData})
    else:
        return render(request, template_name='error,.html', context={'error_message': 'Failed to fetch data from the API'})

#APIintegration
def tour(request,op="", page="", duration="", group_size=""):
    url = "https://oauth.api.sandbox.b2b.tourradar.com/oauth2/token"
    client_id = "p5ybo3nr8o8nh47da7k7k46src"
    client_key = "zhy3g50dg02ce4q37iirbgu2y72zs1mkc0heqsw5t7sd4ohiu6z"
    credentials = f"{client_id}:{client_key}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()
    payload = {
        "grant_type": "client_credentials",
        "scope": "com.tourradar.tours/read"
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": f"Basic {encoded_credentials}"
    }

    response = requests.post(url, headers=headers, data=payload)
    response_data = response.json()

    acc_token = response_data['access_token']

    if op and page and duration and group_size:
        url_api = "https://api.sandbox.b2b.tourradar.com/v1/tours/search?operator={}&page={}&duration={}&group_size{}".format(op, page, duration, group_size)
        print("url=>", url_api)
    elif op:
        url_api = "https://api.sandbox.b2b.tourradar.com/v1/tours/search?operator={}".format(op)
        print("url=>", url_api)
    elif page:
        url_api = "https://api.sandbox.b2b.tourradar.com/v1/tours/search?page={}".format(page)
        print("url=>", url_api)
    elif duration:
        url_api = "https://api.sandbox.b2b.tourradar.com/v1/tours/search?duration={}".format(duration)
        print("url=>", url_api)
    elif group_size:
        url_api = "https://api.sandbox.b2b.tourradar.com/v1/tours/search?group_size={}".format(group_size)
        print("url=>", url_api)
    else:
        url_api = "https://api.sandbox.b2b.tourradar.com/v1/tours/search"
        print("url=>", url_api)


    headers_api = {
        "Authorization": f"Bearer {acc_token}"
    }

    response_api = requests.get(url_api, headers=headers_api)

    global decodedata

    decodedata = response_api.json()

    # print(response_data)

    # print(decodeData)

    # print(decodeData['items'][0]['tour_name'])

    # operators = set()
    # unique_tours = []
    # for item in decodeData:
    #     operator_name = item['operator']['name']
    #     if operator_name not in operators:
    #         operators.add(operator_name)
    #         unique_tours.append(item)


    # paginator = Paginator(decodedata['items'],20)  # Show 10 tours per page
    # page_number = request.GET.get('page', 1)
    # page_obj = paginator.get_page(page_number)

    # return render(request, 'tour.html', {'page_obj': page_obj})

    current_page = int(page) if page else 1
    return render(request, 'tour.html', context={"key": decodedata['items'], "current_page": current_page})

def operator_filter(request):
    selected_operator = request.POST.get('operator', '')
    print('selected_operator : ', selected_operator)
    return tour(request, selected_operator)

def days(request):
    search_tour_length = request.GET.get('search_tour_length', '')
    # filtered_tours = [tour for tour in decodedata['items'] if str(tour.get('tour_length_days', '')) == search_tour_length]

    print('search_tour_length : ', search_tour_length)

    return tour(request, duration=search_tour_length)

def group_size(request):
    search_group_size = request.GET.get('search_group_size')

    print(search_group_size)

    return tour(request, group_size=search_group_size)

def page(request, page_number):
    selected_operator = 0
    print('selected page_number : ', page_number)
    return tour(request, selected_operator, page_number)


