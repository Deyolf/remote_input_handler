def get(request,value):
    data = request.get_json()
    return data.get(value)