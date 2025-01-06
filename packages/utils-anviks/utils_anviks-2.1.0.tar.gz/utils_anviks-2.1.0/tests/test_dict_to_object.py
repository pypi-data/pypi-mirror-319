from src import dict_to_object


def test_dict_to_object():

    data = {
        "name": "John",
        "age": 30,
        "city": "New York"
    }

    obj = dict_to_object(data)

    assert obj.name == "John"
    assert obj.age == 30
    assert obj.city == "New York"
