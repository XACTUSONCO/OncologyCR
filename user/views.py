import collections, re, io, xlsxwriter, math
from datetime import date, datetime, timedelta
from urllib.parse import quote

from django.core.exceptions import SuspiciousOperation
from django.utils import timezone

from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.models import User, Group, update_last_login
from django.contrib.auth.decorators import login_required
from django.db.models import Case, When, Value, IntegerField
from django.views.decorators.csrf import csrf_exempt

from administration.models import Commute
from oncology_abc import settings
from .models import Contact, Agreement, Location, Team
from research.models import DownloadLog

@csrf_exempt
def login_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/')

    if request.method == 'GET':
        #current_time_string = datetime.now().strftime('%Y-%m-%d %H-%M-%S') # 현재 시간 (naive)
        #aware_time = request.session.get_expiry_date()
        #expiration_time_string = aware_time.astimezone(pytz.timezone('Asia/Seoul')).replace(tzinfo=None).strftime('%Y-%m-%d %H-%M-%S') # 세션 만료 시간 (aware)

        #current_time = datetime.strptime(current_time_string, '%Y-%m-%d %H-%M-%S')
        #expiration_time = datetime.strptime(expiration_time_string, '%Y-%m-%d %H-%M-%S')
        #session_expired = True if current_time >= expiration_time else False

        session_key = request.COOKIES.get("sessionid") # Get the session key from the cookies
        #session = Session.objects.filter(session_key=session_key).first()

        #if session and session.expire_date < datetime.now():
        #    display_popup = True  # Session expired, display the pop-up
        #else:
        #    display_popup = False

        return render(
            request, 'pages/user/login.html', {'session': session_key, 'now': datetime.now}
        )

    user_id = request.POST.get('x_oncotrack_id')
    user_pw = request.POST.get('x_oncotrack_pw')
    user = authenticate(request, username=user_id, password=user_pw)
    if user is not None:
        keep_me = True if request.POST.get('keep_me', None) == 'on' \
            else False
        if keep_me: # Keep me signed in 7 days 체크한 경우
            request.session.set_expiry(60 * 60 * 24 * 7)  # seconds
        login(request, user)
        update_last_login(None, user)
        next_url = request.POST.get('next', None)

        agreement = Agreement.objects.get_or_create(user=user)[0]
        one_year_ago = timezone.now() - timedelta(days=365)

        today = date.today()
        commute = Commute.objects.filter(date=today, user=user)
        if not commute.exists():
            Commute.objects.create(date=today, start_work=timezone.now(), user=user)

        if agreement.term_agreement_date is not None and one_year_ago <= agreement.term_agreement_date and \
                agreement.security_agreement_date is not None and one_year_ago <= agreement.security_agreement_date: # 개인정보, 비밀보안 동의하였으며, 각각 동의일 >= 1년 전
            if user_id == 'uro':
                return HttpResponseRedirect('/dataroom/data/?cancer=urological')
            elif user_id == 'nobelg@yuhs.ac':
                return HttpResponseRedirect('/dataroom/data/?cancer=phase1')
            elif next_url is None or next_url.strip() == '':
                return HttpResponseRedirect('/')
            else:
                return HttpResponseRedirect(next_url)
        elif agreement.term_agreement_date is None or one_year_ago > agreement.term_agreement_date: # 개인정보 동의하지 않았거나, 동의일 < 1년전
            return HttpResponseRedirect('/user/term')
        elif agreement.security_agreement_date is None or one_year_ago > agreement.security_agreement_date: # 비밀보안 동의하지 않았거나, 동의일 < 1년전
            return HttpResponseRedirect('/user/security')
    else:
        return render(
            request, 'pages/user/login.html', {
                'error': '로그인에 실패하였습니다.'
            }
        )


def logout_view(request):
    today = date.today()
    commute = Commute.objects.filter(date=today, user=request.user)
    if commute.exists():
        commute.update(end_work=timezone.now())
    else:
        Commute.objects.create(date=today, end_work=timezone.now(), user=request.user)
    logout(request)
    return HttpResponseRedirect(settings.LOGIN_URL)


def register(request):
    if request.method == 'GET':
        return render(
            request, 'pages/user/register.html'
        )

    errors = collections.defaultdict(list)
    username = request.POST.get('username', None)
    job_title = request.POST.get('job_title', None)
    fullname = request.POST.get('fullname', None)
    password = request.POST.get('password', None)
    password_again = request.POST.get('password_again', None)
    term_agree = request.POST.get('term-agree', None)
    email = request.POST.get('email', None)

    if username is None or username.strip() == '':
        errors['username'].append("필수 정보입니다.")
    elif ' ' in username:
        errors['username'].append("공백을 포함할 수 없습니다.")
    elif User.objects.filter(username=username).exists():
        errors['username'].append("이미 사용 중인 아이디입니다.")

    if fullname is None or fullname.strip() == '':
        errors['fullname'].append("필수 정보입니다.")

    if password is None or password == '':
        errors['password'].append("필수 정보입니다.")
    elif len(password) < 8:
        errors['password'].append("비밀번호는 최소 8자 이상이어야 합니다.")
    elif re.search('[0-9]+', password) is None:
        errors['password'].append("비밀번호는 최소 1개 이상의 숫자가 포함되어야 합니다.")
    elif re.search('[a-zA-Z]+', password) is None:
        errors['password'].append("비밀번호는 최소 1개 이상의 영문이 포함되어야 합니다.")
    elif re.search('[`~!@#$%^&*(),<.>/?]+', password) is None:
        errors['password'].append("비밀번호는 최소 1개 이상의 특수문자가 포함되어야 합니다.")
    elif password != password_again:
        errors['password'].append("비밀번호가 일치하지 않습니다.")

    if password_again is None or password_again == '':
        errors['password_again'].append("필수 정보입니다.")

    group = Group.objects.filter(name=job_title)
    if job_title is None:
        errors['job_title'].append("필수 정보입니다.")

    if term_agree is None:
        errors['term_agree'].append("사용자 동의를 체크해주시기 바랍니다.")

    if errors:
        error_msg = {k: '<br>'.join(v) for k, v in errors.items()}
        return render(
            request, 'pages/user/register.html',
            {'username': username,
             'email': email,
             'job_title': job_title,
             'fullname': fullname,
             'password': password,
             'password_again': password_again,
             'errors': error_msg}
        )

    user = User.objects.create_user(username=username,
                                    password=password,
                                    first_name=fullname,
                                    email=email)

    # There should be only one group!
    group = group[0]
    group.user_set.add(user)

    new_contact = Contact.objects.create(user_id=user.id,
                                        name=fullname,
                                        email=email)
    new_contact.save()

    user.save()
    login(request, user)
    return HttpResponseRedirect('/user/term')

@login_required()
def term(request):
    if request.method == 'GET':
        return render(
            request, 'pages/user/term.html'
        )

    agreement = Agreement.objects.get_or_create(user=request.user)[0]
    agreement.set_term_agreement_date(agreement)

    one_year_ago = timezone.now() - timedelta(days=365)

    if agreement.security_agreement_date is not None and one_year_ago <= agreement.security_agreement_date:
        return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/user/security')


def security(request):
    if request.method == 'GET':
        return render(
            request, 'pages/user/security.html'
        )
    agreement = Agreement.objects.get_or_create(user=request.user)[0]
    agreement.set_security_agreement_date(agreement)
    return HttpResponseRedirect('/')

@login_required()
def edit_profile(request):

    if request.method == 'GET':
        return render(
            request, 'pages/user/edit.html'
        )

    errors = collections.defaultdict(list)
    user = request.user
    #fullname = request.POST.get('fullname', None)
    job_title = request.POST.get('job_title', None)

    change_password = request.POST.get('change_password', None)
    change_password = True if change_password == 'on' else False
    new_password = request.POST.get('new_password', None)
    new_password_re = request.POST.get('new_password_re', None)

    group = Group.objects.filter(name=job_title)
    if change_password and \
            (len(new_password) == 0 or len(new_password_re) == 0):
        errors['password'].append("- 필수 정보입니다.")
    elif len(new_password) < 8:
        errors['password'].append("비밀번호는 최소 8자 이상이어야 합니다.")
    elif re.search('[0-9]+', new_password) is None:
        errors['password'].append("비밀번호는 최소 1개 이상의 숫자가 포함되어야 합니다.")
    elif re.search('[a-zA-Z]+', new_password) is None:
        errors['password'].append("비밀번호는 최소 1개 이상의 영문이 포함되어야 합니다.")
    elif re.search('[`~!@#$%^&*(),<.>/?]+', new_password) is None:
        errors['password'].append("비밀번호는 최소 1개 이상의 특수문자가 포함되어야 합니다.")

    if change_password and \
            new_password != new_password_re:
        errors['password'].append("- 패스워드가 일치하지 않습니다.")

    if errors:
        error_msg = {k: '<br>'.join(v) for k, v in errors.items()}
        return render(
            request, 'pages/user/edit.html',
            {'job_title': job_title,
             #'fullname': fullname,
             'errors': error_msg}
        )

    #user.first_name = fullname
    user.groups.set(group)

    if change_password:
        user.set_password(new_password)
    user.save()

    return HttpResponseRedirect('/user/')

@login_required()
def profile_overview(request):
    return render(
        request, 'pages/user/overview.html'
    )


@login_required()
def profile_edit_info(request):
    if request.method == 'GET':
        return render(
            request, 'pages/user/edit_info.html',
            {'groups': Group.objects.all(),
             'locations': Location.objects.all(),
             'teams': Team.objects.all})
    elif request.method == 'POST':
        user_id = request.POST.get('user_id')
        email = request.POST.get('email') or ""
        name = request.POST.get('name') or None
        eng_name = request.POST.get('eng_name') or None
        phone = request.POST.get('phone') or None
        work_phone = request.POST.get('work_phone') or None
        groups = request.POST.getlist('groups') or None
        team = request.POST.get('team') or None
        location = request.POST.get('location') or None

        updated_user = User.objects.get(id=user_id)
        updated_user.email = email
        updated_user.save()
        if groups is not None:
            updated_user.groups.clear()
            for group in groups:
                new_group = Group.objects.get(name=group)
                new_group.user_set.add(updated_user)
        Contact.objects.get_or_create(user=updated_user)
        Contact.objects.filter(user_id=user_id).update(name=name, eng_name=eng_name, phone=phone, work_phone=work_phone,
                                                       team=Team.objects.get(name=team) if team is not None else None,
                                                       location=Location.objects.get(
                                                           name=location) if location is not None else None),
        return render(
            request, 'pages/user/edit_info.html',
            {'user': updated_user, 'groups': Group.objects.all(),
             'locations': Location.objects.all(), 'teams': Team.objects.all})
    else:
        raise SuspiciousOperation("Invalid request")

@login_required()
def view_profile(request):
    return render(
        request, 'pages/user/detail.html'
    )


@login_required()
def user_list(request):
    contacts = Contact.objects.filter(onco_A=True)\
        .select_related('team', 'location')\
        .annotate(group_order=Case(
                    When(user__groups__name="nurse", then=1),
                    When(user__groups__name="technician", then=2),
                    When(user__groups__name="medical records", then=3),
                    default=4,
                    output_field=IntegerField()
        )) \
        .order_by('team', 'group_order', 'career')

    # 표시용 필드 추가
    for c in contacts:
        if not c.team or c.team.name == "etc":
            if c.name == "타기관":
                c.display_team = ""  # 빈 값 → 테이블 필터에서 제외됨
            else:
                group_name = c.user.groups.first().name if c.user and c.user.groups.exists() else ""
                mapping = {
                    "medical records": "의무기록사",
                    "technician": "임상병리사",
                }
                c.display_team = mapping.get(group_name, "연구행정")
        else:
            c.display_team = c.team.name

    return render(request, 'pages/user/user_list.html', {'contact': contacts,
                                                         'teams': Team.objects.all(),
                                                         'locations': Location.objects.all()})

@login_required()
def download_contact(request):
    contact_download = DownloadLog(downloader=request.user, content='연락처')
    contact_download.save()

    return response

@login_required()
def edit_contact(request, id):
    contact = get_object_or_404(Contact, pk=id)
    edited_contact, errors = Contact.contact_form_validation(request)

    if errors:
        return JsonResponse({'code': 'error', 'error': errors})

    contact.team = edited_contact.team
    contact.name = edited_contact.name
    contact.eng_name = edited_contact.eng_name
    contact.phone = edited_contact.phone
    contact.work_phone = edited_contact.work_phone
    contact.email = edited_contact.email
    #contact.career = edited_contact.career
    #contact.career_end = edited_contact.career_end
    contact.location = edited_contact.location
    contact.save()

    return JsonResponse({'code': 'success'})
