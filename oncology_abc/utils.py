from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def get_page_num_list(research, curr_page):
    paginator = Paginator(research, 10)
    page = curr_page
    try:
        research_paginator = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        research_paginator = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        research_paginator = paginator.page(paginator.num_pages)

    curr_page_num = research_paginator.number
    start_page_num = max(1, curr_page_num - 5)
    end_page_num = min(paginator.num_pages + 1, curr_page_num + 5)
    page_num_list = list(range(start_page_num, end_page_num))

    if len(page_num_list) < 10:
        if start_page_num == 1:
            end_page_num = min(paginator.num_pages + 1,
                               end_page_num + (10 - len(page_num_list)))
        if end_page_num - 1 == paginator.num_pages:
            start_page_num = max(1,
                                 start_page_num - (10 - len(page_num_list)))
        page_num_list = list(range(start_page_num, end_page_num))

    return research_paginator, page_num_list

def get_page_num_list_patient(assignment, curr_page):
    paginator = Paginator(assignment, 10)
    page = curr_page
    try:
        assignment_paginator = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        assignment_paginator = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        assignment_paginator = paginator.page(paginator.num_pages)

    curr_page_num = assignment_paginator.number
    start_page_num = max(1, curr_page_num - 5)
    end_page_num = min(paginator.num_pages + 1, curr_page_num + 5)
    page_num_list = list(range(start_page_num, end_page_num))

    if len(page_num_list) < 10:
        if start_page_num == 1:
            end_page_num = min(paginator.num_pages + 1,
                               end_page_num + (10 - len(page_num_list)))
        if end_page_num - 1 == paginator.num_pages:
            start_page_num = max(1,
                                 start_page_num - (10 - len(page_num_list)))
        page_num_list = list(range(start_page_num, end_page_num))

    return assignment_paginator, page_num_list