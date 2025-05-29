from .models import Assignment

def generate_search_query(request):
    register_number = request.GET.get('register_number', '')
    register_number = None if register_number.strip() == '' else register_number
    name = request.GET.get('name', '')
    name = None if name.strip() == '' else name

    # Create Query
    query = Assignment.objects.filter(is_deleted=False)\
                              .values('research__id', 'research__research_name', 'research__research_explanation', 'id', 'name', 'status', 'no', 'register_number', 'sex', 'age')
    if register_number is not None:
        query = query.filter(register_number__icontains=register_number)
    if name is not None:
        query = query.filter(name__icontains=name)


    sort_q = request.GET.get('sort', '-register_number')
    sort_q = 'register_number' if sort_q == '' else sort_q
    query = query.order_by(sort_q)

    query_dict = {
        'sort': sort_q,
        'register_number': register_number
    }

    return query, query_dict


def create_assignment_field_change_summary(value):
    if isinstance(value, list):
        text = '['
        for v in value:
            text += str(v['show']) if 'show' in v else str(v)
            text += ', '
        text = text[:-2] + ']'
    else:
        text = str(value)
    return text


def compare_assignment_fields(prev_json, curr_json):
    comparing_field = ['status']

    text_summary = {}
    for field_name in comparing_field:
        if field_name in prev_json and field_name in curr_json:
            if prev_json[field_name] != curr_json[field_name]:
                curr_summary = create_assignment_field_change_summary(
                    curr_json[field_name])
                text_summary[field_name] = 'edited_status : ' + curr_summary
        elif field_name not in prev_json and field_name in curr_json:
            curr_summary = create_assignment_field_change_summary(
                curr_json[field_name])
            text_summary[field_name] = 'added_status : ' + curr_summary
        else:
            prev_summary = create_assignment_field_change_summary(
                prev_json[field_name])
            text_summary[field_name] = prev_summary + ' -> None'

    return text_summary
